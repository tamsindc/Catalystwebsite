#!/usr/bin/env python3
"""Build the fishpond workflow library from n8n's public template gallery.

Usage: python3 scripts/build_workflows.py [--per-source 60] [--max 650]
Writes data/workflows.js. Every entry links back to its original template and credits its author.
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import time
import urllib.parse
import urllib.request

API = "https://api.n8n.io/api/templates/search"
TEMPLATE_URL = "https://n8n.io/workflows/{id}"

N8N_CATEGORIES = [
    "AI", "AI Chatbot", "AI Summarization", "AI RAG", "Multimodal AI", "Content Creation",
    "Document Ops", "Engineering", "Finance", "HR", "IT Ops", "Lead Generation", "Lead Nurturing",
    "Market Research", "Marketing", "Personal Productivity", "Product", "Project Management",
    "Sales", "SecOps", "Social Media", "Support", "Ticket Management", "Invoice Processing", "CRM",
]

# n8n is mostly work automation, so everyday-life topics are searched for directly.
LIFE_SEARCHES = [
    "recipe", "meal plan", "grocery", "travel", "trip itinerary", "flight", "fitness", "workout",
    "health", "personal finance", "budget", "expense", "habit", "journal", "language learning",
    "study", "flashcards", "job search", "resume", "news digest", "podcast", "youtube summary",
    "book", "calendar", "reminder", "telegram assistant", "personal assistant", "weather",
    "family", "home", "shopping", "price tracker", "real estate", "learning",
]
WORK_SEARCHES = [
    "email", "inbox", "meeting", "transcript", "invoice", "contract", "linkedin", "seo",
    "blog", "newsletter", "customer support", "whatsapp", "slack", "notion", "pdf", "spreadsheet",
    "lead", "cold email", "competitor", "interview", "recruiting", "onboarding", "report",
    "voice", "image generation", "video", "translation", "social media", "crm", "faq",
]

UTILITY = {
    "Sticky Note", "Code", "Edit Fields (Set)", "If", "Merge", "Switch", "Filter", "Wait",
    "No Operation, do nothing", "Split Out", "Aggregate", "Loop Over Items (Split in Batches)",
    "Split In Batches", "Item Lists", "Execute Workflow", "Execute Workflow Trigger",
    "When Executed by Another Workflow", "Respond to Webhook", "Sort", "Limit", "Date & Time",
    "Remove Duplicates", "Summarize", "Execution Data", "Stop and Error", "Function", "Function Item",
    "Set", "Manual Trigger", "When clicking ‘Execute workflow’", "Structured Output Parser",
    "Auto-fixing Output Parser", "Crypto", "Compare Datasets", "Markdown", "HTML", "XML",
    "Extract from File", "Convert to File", "Rename Keys", "Default Data Loader",
    "Recursive Character Text Splitter", "Character Text Splitter", "Token Splitter",
    "Window Buffer Memory", "Simple Memory", "Calculator", "Think Tool", "Wikipedia",
    "Execute Command", "Error Trigger", "n8n", "Information Extractor", "Basic LLM Chain",
}

# Ordered: first match wins. (label, side, keywords)
LIFE_TOPICS = [
    ("Food & Home", "life", r"\brecipes?\b|\bmeals?\b|grocer|\bcook|kitchen|\bdiet\b|nutrition|calorie|home ?assistant|household|\bplants?\b|garden|\bpets?\b|restaurant|\bfood\b"),
    ("Travel", "life", r"\btravel|\btrips?\b|itinerar|\bflights?\b|\bhotels?\b|airbnb|vacation|holiday|\btours?\b|tourism"),
    ("Health & Fitness", "life", r"fitness|workout|\bgym\b|\bhealth|\bsleep\b|wellness|medical|symptom|meditat|mental health|strava|\bdoctor|nutrition"),
    ("Money", "life", r"personal financ|\bbudget|\bexpenses?\b|spending|\bstocks?\b|crypto|bitcoin|trading|portfolio|\btax(es)?\b|receipts?\b|price (track|drop|alert)|\binvest"),
    ("Learning", "life", r"\blearn(ing)?\b|\bstud(y|ying)\b|flashcard|\bquiz|\btutor|\bstudents?\b|\bcourses?\b|language learning|vocab|homework|book summar|\bteach"),
    ("Careers", "life", r"job search|job hunt|\bresumes?\b|\bcv\b|cover letter|job (post|listing|board|application|alert)|\bcareer"),
    ("Personal Assistant", "life", r"personal (ai )?assistant|\bjournal|\bhabits?\b|\bdiary|\breminders?\b|\bto-?do|daily (brief|digest)|morning (brief|report)|\bweather|\bfamily|second brain"),
]
WORK_TOPICS = [
    ("Sales & Leads", "work", r"\bleads?\b|\bsales\b|\bcrm\b|hubspot|pipedrive|salesforce|prospect|outreach|cold email|apollo|enrich"),
    ("HR & Hiring", "work", r"recruit|hiring|candidates?\b|\binterviews?\b|\bonboard|employee|\bhr\b|applicant"),
    ("Email & Inbox", "work", r"\be-?mails?\b|\binbox|gmail|outlook|newsletter|mailchimp"),
    ("Meetings & Calendar", "work", r"\bmeetings?\b|calendar|transcri|\bzoom\b|google meet|fireflies|\bschedul|call recording"),
    ("Customer Support", "work", r"\bsupport\b|\btickets?\b|helpdesk|zendesk|\bfaq|customer service|chat ?bot|whatsapp|intercom"),
    ("Marketing & Social", "work", r"social media|linkedin|twitter|\bx\b posts?|instagram|tiktok|facebook|\bseo\b|marketing|\bads\b|campaign|\bbrand"),
    ("Video, Image & Voice", "work", r"\bvideos?\b|\bimages?\b|\bphotos?\b|youtube|\bvoice|\baudio|podcast|speech|thumbnail|avatar|dall-?e|midjourney|elevenlabs"),
    ("Content & Writing", "work", r"\bblog|\barticles?\b|\bcontent\b|\bwrit(e|ing)\b|\bcopy|\bposts?\b|\bstor(y|ies)\b|\bscripts?\b|wordpress"),
    ("Research & News", "work", r"research|\bnews\b|competitor|\bmarket\b|scrap|crawl|\bmonitor|\btrends?\b|\brss\b|reddit"),
    ("Documents & Data", "work", r"\bpdfs?\b|document|invoice|contract|\bocr\b|spreadsheet|\bsheets?\b|\breports?\b|\bdata\b|database|\brag\b|knowledge|notion|\bdrive\b"),
    ("Dev & IT", "work", r"github|\bcode\b|devops|security|incident|\bservers?\b|\bapi\b|\bbugs?\b|\bjira\b|deploy|\blogs?\b|\balerts?\b"),
]
# Tutorials about n8n itself and model plumbing are for builders, not everyday users.
BUILDER = re.compile(r"\bn8n\b|sub-?workflow|\bollama\b|\bllms?\b|\bjson\b|webhook|authenticat|proxmox|\bmcp\b|vector (store|db)|qdrant|pinecone|embedding|\bpattern\b", re.I)
FALLBACK = ("Productivity", "work")

HEAD_HOW = re.compile(r"^(how (it|this|the workflow) works|what (it|this workflow) does|workflow (steps|overview)|steps|the workflow)\b", re.I)
HEAD_SETUP = re.compile(r"^(how to set ?up|set ?up( steps| guide| instructions)?|setup|getting started|requirements|prerequisites|how to use)\b", re.I)
HEAD_ANY = re.compile(r"^(#{1,6}\s|[A-Z][\w '’/&-]{2,40}:?$)")
SKIP_PARA = re.compile(r"^(quick overview|overview|description|who('s| is) (it|this) for|what problem|about|summary|introduction)\W*$", re.I)


def fetch(params, retries=3):
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "fishpond-library-builder/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)


def clean_line(s):
    s = html.unescape(s)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"`{1,3}", "", s)
    s = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", s)
    s = re.sub(r"^#{1,6}\s*", "", s)
    s = re.sub(r"^\s*(?:[-*•▪►✅✔️👉🔹🔸]|\d+[.)]|step \d+:?)\s*", "", s, flags=re.I)
    s = re.sub(r"\*\*|__", "", s)
    return re.sub(r"\s+", " ", s).strip(" -–—:")


def clip(s, n):
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0].rstrip(",;:.-")
    return cut + "…"


def sections(desc):
    lines = [l.rstrip() for l in (desc or "").replace("\r", "").split("\n")]
    out, cur = [("", [])], None
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue
        text = clean_line(stripped)
        if not text:
            continue
        is_head = stripped.startswith("#") or (len(text) <= 45 and not text.endswith(".") and HEAD_ANY.match(text) and len(text.split()) <= 7)
        if is_head:
            out.append((text.rstrip(":"), []))
        elif not stripped.endswith(":"):
            out[-1][1].append(text)
    return out


def summarise(desc, name):
    secs = sections(desc)
    for head, body in secs:
        if HEAD_HOW.match(head) or HEAD_SETUP.match(head):
            continue
        for para in body:
            if len(para) >= 70 and not SKIP_PARA.match(para) and not para.lower().startswith(("http", "note", "⚠")):
                return clip(para, 230)
    return clip(name, 230)


def pick(desc, head_re, limit=5):
    for head, body in sections(desc):
        if head_re.match(head):
            items = [clip(b, 150) for b in body if len(b) > 12 and not b.lower().startswith("http")]
            if items:
                return items[:limit]
    return []


def topic_for(name, context):
    # Life topics trust only the title; work topics may fall back to tools and description.
    for label, side, rx in LIFE_TOPICS + WORK_TOPICS:
        if re.search(rx, name, re.I):
            if label == "Careers" and re.search(r"\bhr\b|candidate|screen|hiring|recruit|applicant|evaluat", name, re.I):
                return "HR & Hiring", "work"
            return (label, side) if side == "work" or not BUILDER.search(name) else ("Dev & IT", "work")
    if BUILDER.search(name):
        return "Dev & IT", "work"
    for label, side, rx in WORK_TOPICS:
        if re.search(rx, context, re.I):
            return label, side
    return FALLBACK


def normalise(w):
    nodes = [n.get("displayName", "") for n in w.get("nodes", [])]
    tools = []
    for n in nodes:
        n = re.sub(r"\s+(Trigger|Tool)$", "", n)
        if n and n not in UTILITY and n not in tools:
            tools.append(n)
    meaningful = [n for n in nodes if n not in UTILITY]
    size = len(meaningful)
    level = "Beginner" if size <= 5 else "Intermediate" if size <= 10 else "Advanced"
    desc = w.get("description") or ""
    name = re.sub(r"^[^\w(]+", "", clean_line(w["name"])).strip()
    topic, side = topic_for(name, " ".join(tools) + " " + desc[:400])
    user = w.get("user") or {}
    return {
        "id": w["id"],
        "t": name,
        "d": summarise(desc, name),
        "how": pick(desc, HEAD_HOW),
        "setup": pick(desc, HEAD_SETUP, 4),
        "tools": tools[:6],
        "cat": topic,
        "side": side,
        "lvl": level,
        "views": w.get("totalViews") or 0,
        "by": user.get("name") or user.get("username") or "n8n community",
        "v": bool(user.get("verified")),
        "date": (w.get("createdAt") or "")[:10],
        "url": TEMPLATE_URL.format(id=w["id"]),
    }


def collect(params, want, seen, bag, tag):
    page, got = 1, 0
    while got < want:
        rows = min(100, want - got)
        data = fetch({**params, "rows": rows, "page": page, "sort": "views:desc"})
        items = data.get("workflows") or []
        if not items:
            break
        for w in items:
            if (w.get("price") or 0) > 0 or w.get("purchaseUrl"):
                continue
            got += 1
            if w["id"] in seen:
                continue
            seen.add(w["id"])
            bag.append(w)
        if len(items) < rows:
            break
        page += 1
        time.sleep(0.25)
    print(f"  {tag:<28} +{got:>3}  total {len(bag)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-source", type=int, default=60)
    ap.add_argument("--per-search", type=int, default=20)
    ap.add_argument("--max", type=int, default=700)
    ap.add_argument("--floor", type=int, default=30)
    ap.add_argument("--out", default="data/workflows.js")
    ap.add_argument("--cache", help="JSON file of raw templates; reused if present, written if not")
    a = ap.parse_args()

    if a.cache and os.path.exists(a.cache):
        raw = json.load(open(a.cache, encoding="utf-8"))
        print(f"Loaded {len(raw)} cached templates from {a.cache}")
    else:
        seen, raw = set(), []
        print("Categories")
        for c in N8N_CATEGORIES:
            collect({"category": c}, a.per_source, seen, raw, c)
        print("Life searches")
        for q in LIFE_SEARCHES:
            collect({"search": q, "category": "AI"}, a.per_search, seen, raw, q)
        print("Work searches")
        for q in WORK_SEARCHES:
            collect({"search": q, "category": "AI"}, a.per_search, seen, raw, q)
        if a.cache:
            json.dump(raw, open(a.cache, "w", encoding="utf-8"))
    bag = [normalise(w) for w in raw]

    # Keep the most-viewed overall, but guarantee every topic keeps its best entries.
    by_topic = {}
    for w in sorted(bag, key=lambda x: -x["views"]):
        by_topic.setdefault(w["cat"], []).append(w)
    keep = {w["id"] for ws in by_topic.values() for w in ws[:a.floor]}
    for w in sorted(bag, key=lambda x: -x["views"]):
        if len(keep) >= a.max:
            break
        keep.add(w["id"])
    items = sorted((w for w in bag if w["id"] in keep), key=lambda x: -x["views"])

    meta = {
        "source": "n8n.io community workflow templates",
        "sourceUrl": "https://n8n.io/workflows/",
        "built": dt.date.today().isoformat(),
        "count": len(items),
    }
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("// Generated by scripts/build_workflows.py. Do not edit by hand.\n")
        f.write("window.FISHPOND = ")
        json.dump({"meta": meta, "items": items}, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    counts = {}
    for w in items:
        counts[w["cat"]] = counts.get(w["cat"], 0) + 1
    print(f"\nWrote {len(items)} workflows to {a.out}")
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {v:>4}  {k}")


if __name__ == "__main__":
    main()
