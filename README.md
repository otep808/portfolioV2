# Otep Codes – portfolio (pv2)

Plain HTML5, CSS3 and vanilla JavaScript. No Bootstrap, no frameworks. Every page works without JavaScript; `javascript/main.js` only upgrades it.

## Structure
- `index.html, journeys.html, projects.html, skills.html, learn.html, about.html, contact.html`
- `css/styles.css` – design tokens, light/dark themes, layout
- `javascript/main.js` – theme, menu, Follow the Packet, journey stepper, tips, filters, contact form
- `data/*.json` – all editable content (packet steps, journeys, tips, work, projects, certs, tools)
- `tools/build.py` – regenerates the HTML pages from `data/`
- `images/`, `files/` (PDFs, résumé, demo reel), `fonts/` (unused: fonts load from Google Fonts)

## Editing content
1. Edit a file in `data/` (for example add a tip to `tips.json`).
2. Run `python tools/build.py`.
3. Open `index.html` to check it.

Note: build.py rewrites the HTML pages. If you edit the HTML by hand, do not run it afterwards.

## Deploy on GitHub Pages
Push the folder to a repository, then Settings → Pages → deploy from the main branch (root).

## Monthly upkeep
Add one journey or tip, update the project list, and re-test on a phone.
