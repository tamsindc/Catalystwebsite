# fishpond.ai homepage

A single-page, interactive homepage for fishpond.ai: search step-by-step AI workflows, follow them with apps you already use, and save the ones you like.

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
- `cat`: one of 19 topics (12 work, 7 life)
- `lvl`, `mins`, `tools`, `when`: difficulty, setup time, what you need, when it runs
- `steps`: 3 to 6 steps, each with a heading, instructions and an optional copy-paste prompt (`[brackets]` are filled in by the user)
- `example`, `tips`: a sample result and practical tips
- `auto`: a machine-readable blueprint (a trigger plus actions) so fishpond can later run the recipe automatically. The page shows it as "Coming soon".
