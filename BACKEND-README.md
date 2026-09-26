# Kaskad Group — Backend & Admin CMS

This document explains the backend and content-management panel added to the
existing Kaskad Group website. The **frontend design is unchanged** — the same
`site/` pages now pull their content live from a database you control through a
simple admin panel, instead of from hardcoded files.

---

## 1. What was built (technology)

| Layer | Technology |
|-------|-----------|
| Backend framework | **Django 5.1** (Python 3.11) |
| API | **Django REST Framework** — one JSON endpoint feeding the site |
| Admin / CMS | **Django Admin** (customised per content type) |
| Database | **SQLite** by default (swappable to PostgreSQL via `.env`) |
| Image processing | **Pillow** — automatic resize + compression on upload |
| Config | **python-dotenv** — secrets in a `.env` file, never in code |
| CORS | **django-cors-headers** |

Everything is inside the new **`backend/`** folder. The existing **`site/`**
frontend was touched only minimally (see §7).

```
Kaskad/
├── site/                       ← the existing frontend (design unchanged)
│   └── assets/js/
│       ├── data.*.js, i18n.js  ← now used only as an OFFLINE FALLBACK
│       ├── data.api.js         ← NEW: loads live content from the API
│       └── app.js              ← lightly edited (live load + real images)
└── backend/                    ← NEW backend + CMS
    ├── manage.py  .env  .env.example  requirements.txt
    ├── kaskad_cms/             ← settings, urls
    ├── content/                ← models, admin, API, seed command
    ├── media/                  ← uploaded images (auto-created)
    └── db.sqlite3              ← the database (auto-created)
```

---

## 2. First-time setup

You need Python 3.11+. From a terminal:

```bash
cd backend

# 1. (Optional) create/activate a virtual environment
#    py -m venv .venv && .venv\Scripts\activate

# 2. Install dependencies
py -m pip install -r requirements.txt

# 3. Create your .env from the template and edit the values
copy .env.example .env            # Windows   (cp .env.example .env on macOS/Linux)

# 4. Create the database tables
py manage.py migrate

# 5. Load all existing website content into the database (one time)
py manage.py seed_content

# 6. Create your admin login (reads ADMIN_* from .env)
py manage.py create_admin
#    …or interactively:  py manage.py createsuperuser
```

> On this machine, if the `py` launcher misbehaves, use the full path:
> `C:\Users\User\AppData\Local\Programs\Python\Python311\python.exe manage.py …`

### Run it

```bash
py manage.py runserver
```

Then open:

| URL | What |
|-----|------|
| http://127.0.0.1:8000/ | The website (identical design, now live-data-driven) |
| http://127.0.0.1:8000/admin/ | **The admin panel (CMS)** |
| http://127.0.0.1:8000/api/content/ | The JSON content feed (read-only) |

---

## 3. Admin panel & login

- **URL:** `/admin/`
- **Login:** the username/password from `ADMIN_USERNAME` / `ADMIN_PASSWORD` in
  your `.env` (defaults in `.env.example` are `admin` / `KaskadAdmin!2026` — 
  **change these**). Access is protected by Django's secure session
  authentication; all admin routes require login.

The admin is organised by section — **Company**, **Construction**,
**Switchgear**, **Meters**, **News**, **Galleries**, **Site text (UI strings)**
and **Contact messages**. For every content type you can:

- View, **search**, **filter** and page through all records
- **Add**, **edit**, **delete** records
- **Publish / unpublish** (the `is_published` tick — unticked = hidden draft)
- Reorder with the **sort** number (lower = earlier), editable right in the list
- Upload/replace/delete images with a **live thumbnail preview**
- Edit all three languages (**HY / RU / EN**) on one form

---

## 4. How images work

- Upload from your computer in the relevant record (e.g. a Project's *Cover*,
  or add rows to a Project's **gallery**). Formats: JPG / PNG / WebP.
- On save, images are **automatically optimised** with Pillow: downscaled to a
  max width of **1600px** and re-compressed (JPEG q82 / PNG optimise). Aspect
  ratio is preserved; images are never upscaled.
- Files are stored on disk under **`backend/media/`** (e.g.
  `media/projects/…`, `media/switchgear/…`, `media/meters/…`, `media/news/…`,
  `media/gallery/…`, `media/certs/…`).
- The API returns each image as a URL; the frontend then renders a real
  `<img>` in the **same card box** it used before. Where no image is uploaded,
  the original styled placeholder is shown — so the site never looks broken.
- **Cover image** = a record's main image field. **Multiple images** =
  the *Project gallery* and *Gallery images* (per section) inlines, each with
  alt text / captions.

---

## 5. Database structure (overview)

Purpose-built for this site. Trilingual text is stored as three columns
(`*_hy`, `*_ru`, `*_en`) and served as `{hy, ru, en}` objects.

- **Company / global:** `SiteSettings` (contact, address, map, manufacturing
  text), `Stat`, `Advantage`, `Value`, `Partner`, `Client`, `HistoryMilestone`
- **Construction:** `Service` → `ServicePoint`; `ProjectCategory`; `Project` →
  `ProjectImage`
- **Switchgear:** `SwitchgearCategory` → `SwitchgearItem`, `SwitchgearSpec`,
  `SwitchgearDoc`; `Certificate`
- **Meters:** `MeterCategory`; `Meter` → `MeterSpec`, `MeterFeature`;
  `MeterTechnology`; `MeterDocType`
- **Other:** `News`, `GalleryImage`, `UIString` (all editable labels/headings),
  `ContactMessage` (form submissions)

Most display models carry `sort` + `is_published`. All content is served through
one endpoint, **`GET /api/content/`**, shaped exactly like the site's original
`window.DATA` / `window.I18N` objects.

---

## 6. Contact form

The contact form now **POSTs to `/api/contact/`** and stores each submission as
a **Contact message** in the admin (with basic validation and rate-limiting).
Over `file://` (no server) it falls back to the original demo confirmation.

---

## 7. What changed on the frontend (and what didn't)

**Unchanged:** all HTML layouts, `styles.css`, the design system, the i18n copy,
page URLs, filters, search, language switching, and the legacy root-level draft
HTML files.

**Minimal edits (in `site/assets/js/`):**
- **`data.api.js`** (new) — fetches `/api/content/` and populates
  `window.DATA` / `window.I18N`. If the API is unreachable it silently keeps the
  bundled fallback data, so opening `site/index.html` directly still works.
- **`app.js`** — three small changes: (1) load live content before rendering;
  (2) render real `<img>` for records that have an uploaded image (placeholder
  otherwise); (3) source Home "News" and the gallery sections from live data.
- Each of the 8 pages got **one added `<script>` line** for `data.api.js`.

Components now driven by the CMS: divisions text, services, projects
(+filter), switchgear catalogue + spec accordions + items + docs, meters +
specs + features + comparison, stats, advantages, values, history, partners,
clients, certificates, manufacturing text, galleries, **news**, all UI
labels/headings, contact details, and the contact form.

---

## 8. Editing content — the everyday workflow

1. Go to `/admin/` and log in.
2. Pick a section (e.g. **Projects**), click a record or **Add**.
3. Fill in the HY / RU / EN fields, upload images, set **sort**, tick
   **is published**, **Save**.
4. Reload the website — the change is live immediately.

No code or database editing is ever required.

---

## 9. Re-seeding / resetting content

`seed_content` only runs on an empty database. To wipe **content** (never users
or contact messages) and reload it from the original source text:

```bash
py manage.py seed_content --force
```

---

## 10. Going to production (checklist)

- Set a strong `SECRET_KEY`, `DEBUG=False`, and real `ALLOWED_HOSTS` /
  `CSRF_TRUSTED_ORIGINS` in `.env`.
- Serve `site/` and `/media/` via nginx or a CDN; run Django behind a WSGI
  server (gunicorn/uwsgi/waitress). The dev `runserver` already serves them for
  convenience.
- Optionally switch `DATABASE` to PostgreSQL via the `DB_*` env vars.
- Back up `backend/db.sqlite3` (or your DB) and `backend/media/` regularly.
```
