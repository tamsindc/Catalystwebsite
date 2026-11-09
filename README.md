# fishpond.ai homepage

A single-page, interactive homepage for fishpond.ai: search real AI workflows, learn how each works, and install them.

## Files

- `index.html`: the whole page (styles and script inline). Open it in a browser or serve the folder.
- `data/workflows.js`: the workflow library (700 real AI workflows). Generated, do not edit by hand.
- `scripts/build_workflows.py`: rebuilds the library.

## The workflow library

Workflows come from the free [n8n community template library](https://n8n.io/workflows/). The build script:

1. Pulls the most-viewed free templates from each n8n AI category, plus targeted searches for everyday-life topics (meals, travel, money, health, learning, careers) and common work tasks.
2. De-duplicates them, sorts each into a fishpond topic (work or life), and rates difficulty by how many apps it uses.
3. Keeps a short summary, the "how it works" and setup steps where the author wrote them, the apps involved, and a credit and link to the original template.

Refresh it (needs network access to `api.n8n.io`):

```bash
python3 scripts/build_workflows.py                 # defaults: 700 workflows, at least 30 per topic
python3 scripts/build_workflows.py --max 1000      # bigger library
python3 scripts/build_workflows.py --cache raw.json  # save raw data once, then re-run offline
```

Only short summaries are stored; every card links to the full template and credits its author.
