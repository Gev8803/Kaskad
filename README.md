# Kaskad Group — Unified Trilingual Corporate Website

Merges three source businesses into one brand, in **Armenian / Russian / English**:

- **Construction & Engineering** — from kaskad-energo.ru (also the design reference)
- **Switchgear Manufacturing** — from kaskad-ts.ru
- **Electricity Meters** — from mirtekgroup.com (meters only)

## Run it
No build step. Open **`site/index.html`** in a browser (works over `file://`).
Switch language with the **HY / RU / EN** control in the header.
Optional local server: `cd site && python -m http.server 8080`.

## Structure
```
site/
  index.html construction.html switchgear.html meters.html
  projects.html products.html about.html contact.html
  assets/
    css/styles.css              # design system (navy + electric blue, kaskad-energo identity)
    js/
      i18n.js                   # UI/page copy — hy/ru/en
      data.common.js            # company, stats, advantages, partners, clients, values, history
      data.construction.js      # services + projects
      data.switchgear.js        # 7 categories / ~37 products + specs + certs
      data.meters.js            # single/three-phase + HV meters + comparison
      app.js                    # engine: i18n, header/footer, renderers, filters, search, forms
    img/                        # drop real images here (paths already referenced in data.*.js)
docs/
  PROJECT-SPEC.md               # full dossier: analysis → schema → roadmap (10 sections)
```

## Editing content

**Recommended — via the admin CMS (no code):** a Django backend + admin panel
now powers the site. Manage all text, products, projects, images, news,
categories, publish state and contact messages at **`/admin/`**. See
**`BACKEND-README.md`** for setup, login and the full workflow. In short:

```
cd backend
py -m pip install -r requirements.txt
copy .env.example .env        # then edit values
py manage.py migrate
py manage.py seed_content      # loads existing content into the database
py manage.py create_admin
py manage.py runserver         # site: http://127.0.0.1:8000/  ·  admin: /admin/
```

The frontend loads live content from the API (`/api/content/`) and falls back to
the bundled files below if the backend is offline, so `site/index.html` still
works over `file://`.

**Fallback / offline editing (advanced):**
- **Text/labels:** `site/assets/js/i18n.js`
- **Products / projects / company data:** the `site/assets/js/data.*.js` files (each field is `{hy, ru, en}`)
- **Colours / type / spacing:** CSS custom properties at the top of `site/assets/css/styles.css`

See `docs/PROJECT-SPEC.md` for the specification, design system, DB schema and
roadmap, and `BACKEND-README.md` for the backend/CMS documentation.
