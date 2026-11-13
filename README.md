# fishpond homepage

A single-page, interactive homepage for fishpond: search step-by-step AI workflows, follow them with apps you already use, and save the ones you like.

## Files

- `index.html`: the whole page (styles and script inline). Open it in a browser or serve the folder.
- `data/recipes/*.json`: the workflow guides ("recipes"), written by fishpond. Edit these.
- `data/workflows.js`: generated from the recipes for the page. Don't edit by hand.
- `scripts/build_recipes.py`: checks the recipes and regenerates `data/workflows.js`.

After adding or editing recipes, run:

```bash
python3 scripts/build_recipes.py
```

It reports how many recipes each topic has, and warns about missing fields, duplicates, or wording that doesn't belong (for example developer jargon).

## Recipe format

Each recipe is a fishpond-native guide that works with everyday tools (an AI assistant such as ChatGPT, Claude or Gemini, plus apps like Gmail, Sheets or Calendar):

- `t`, `d`: title and one-line outcome
- `cat`: one of the topics listed in `scripts/build_recipes.py`
- `job` (optional): the job the guide is for, such as "Bookkeeper". Job guides are based on task lists from the O*NET database (U.S. Department of Labor, Employment and Training Administration, CC BY 4.0) and always count as work guides. They appear under "Find guides for your job".
- `lvl`, `mins`, `tools`, `when`: difficulty, setup time, what you need, when it runs
- `steps`: 3 to 6 steps, each with a heading, instructions and an optional copy-paste prompt (`[brackets]` are filled in by the user)
- `example`, `tips`: a sample result and practical tips
- `auto`: a machine-readable blueprint (a trigger plus actions) so fishpond can later run the recipe automatically. The page shows it as "Coming soon".

## Run it here and the set-up kit

Each guide opens with **Run it right here**: a short form built from the prompt's `[placeholders]`, plus an optional photo or text file. fishpond does the task and streams back a formatted result. People can copy it, save it as a document, try another version, or ask for a change. This uses the Claude app's `sample` ability (with images) when the page is published as a Claude artifact. Opened anywhere else, the page says so and points to the prompt instead. A real launch needs its own AI back end here.

The **set-up kit** gives ready-made pieces:
- **Your own AI assistant**: instructions to paste into a custom GPT, a Claude Project or a Gemini Gem (every guide)
- **Calendar reminder**: a repeating event with the steps inside, for Google Calendar or Outlook (guides that run on a schedule). A `.ics` file is also offered outside the Claude app.
- **Ready-made spreadsheet**: AI-designed columns and example rows, saved as CSV (guides that use Sheets or Excel)
- **Email filter**: a Gmail search and filter steps plus Outlook rule steps (email-sorting guides). A Gmail filter file is also offered outside the Claude app.
- **Save this guide**: a printable page

## Guide pages, sign-ups and deploying

- `python3 scripts/build_pages.py` writes one page per guide to `guides/`, plus `guides/index.html`, `sitemap.xml` and `robots.txt`. Run it after `build_recipes.py`. Set `FISHPOND_URL` to the live address (default `https://thefishpond.online`).
- Sign-up buttons save to a Supabase table. Run `supabase/schema.sql` once, then put the project URL and its publishable (anon) key in `config.js`. Until then, the forms say nothing was saved.
- `vercel.json` turns on clean URLs (`/creators`, `/guides/<id>`). `.vercelignore` keeps the brand files, scripts and drafts off the live site.
- `docs/creator-invite-email.md` holds the founding-creator invite and follow-up.
