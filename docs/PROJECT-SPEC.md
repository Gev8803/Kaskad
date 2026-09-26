# KASKAD GROUP — Unified Corporate Website
## Specification, Design & Implementation Dossier

A single trilingual (HY / RU / EN) corporate website that merges three source
businesses into one brand — **Kaskad Group** — headquartered at
**Bagratunyats 54/3, Yerevan, Armenia · +374 77 241 212**.

The visual identity follows **kaskad-energo.ru** (deep-navy base, electric-blue
accent, white ALL-CAPS display headings, the tagline *“Energy of Transformations”*).

---

## 1. Website Analysis

| # | Source | Business | Platform / Tech | What we take |
|---|--------|----------|-----------------|--------------|
| 1 | kaskad-energo.ru | **Construction & engineering** | Tilda; dark-navy + blue + white, ALL-CAPS bold, vertical section scroll, icon service tiles, project cards with blue corner accents | Full content → Construction division + **overall design language** |
| 2 | kaskad-ts.ru | **Switchgear manufacturing** | Legacy Yii/Bootstrap (~2013), fixed-width; brand blue `#0075bf` + orange `#ec4c0d`, Cuprum font, product carousel | Full product catalogue + specs → Switchgear division |
| 3 | mirtekgroup.com | **Electricity meters** (МИРТЕК) | Drupal; utilitarian white; numbered product grid | **Electricity meters ONLY** → Meter division |

### 1.1 kaskad-energo.ru (design reference + construction)
- **Hero:** dark full-width, white wordmark, tagline **“ЭНЕРГИЯ ПРЕОБРАЗОВАНИЙ”**.
- **Nav:** О компании · Услуги · Проекты (/clients) · Контакты.
- **6 services:** electrical installation; power-equipment manufacturing (50+ types / 750 mods, ABB·Legrand·Schneider·Hager); design & construction; SCADA/metering (АСУ ТП); commissioning (4 stages); electrical testing (mobile LVI HVT lab).
- **7 flagship projects:** Zatonskaya CHP (Ufa, 440 MW), Akhtanak 220 kV & Purak 35/6 kV & Armenian NPP & Echmiadzin TS & Yerevan “Circus” DP (Armenia), SEZ Tomsk 110/35/10 kV.
- **~25 clients** (Electric Networks of Armenia, Rosatom, Inter RAO, Moscow Metro, Rosseti, Gazprom…).
- **Stats:** 20 years · 100+ projects · 5 plants · 30+ regions.

### 1.2 kaskad-ts.ru (switchgear)
- **7 categories / ~37 products:** KD-2 (16 modular cells, 6–24 kV, ≤1250 A); KDW withdrawable KRU (6–20 kV, 630–3150 A, full spec table); KSO/KTiS chambers (≤10 kV); KD-3 SF6 (RV53, KD3-A/A+/P/D/C/K); BKTP-20/0.4; mechanical drives (DA/DP); components (RV44, VA-2, EM20, BB/TEL, RP-600).
- **Tech:** GOST 15150-69 / 1516.1 / 14254; IEC 62271-200; ISO 9001; DEBA (Belgium) technology; Kaluga plant.
- **Certificates:** ISO, GAZPROMCERT, conformity declarations (KDW, KD-3, KSO-KTiS, KD2).

### 1.3 mirtekgroup.com — meters only (everything else ignored)
- **Single-phase** МИРТЕК-12-РУ (D17 80 A, SP17 100 A, W9) — class 1/1, multi-tariff, load relay.
- **Three-phase** МИРТЕК-32-РУ (D37, W32 up to 0.2S direct+transformer, SP31 transformer) — 57.7/220/230 V.
- **High-voltage** МИРТЕК-135-РУ (6/10 kV, Rogowski-coil sensors, GLONASS/GPS).
- **Tech:** AMR/AMI (GSM, NB-IoT, RF, RS-485, Ethernet), DLMS/COSEM & СПОДЭС, anti-tamper, verification up to 16 yr, life up to 48 yr.

---

## 2. Content Extraction Strategy

- **Structured, source-of-truth data files** (not scraped HTML) — each item modelled once as a trilingual object `{ hy, ru, en }`, `ru` authoritative (original language), `hy`/`en` professionally translated.
- **Switchgear** extracted verbatim from the saved source pages (authoritative spec tables preserved: voltages, currents, IP, dimensions, service life).
- **Construction** extracted from crawl: services → `points[]`, projects → structured records (location, client, year, capacity, category).
- **Meters** filtered to electricity only; each model → specs + interfaces + features.
- **Images:** source assets are hot-link-unsafe (expired HTTPS / CDN tokens), so the build ships **self-contained styled media placeholders** carrying the real product code/label; `data.*.js` already stores the intended `image:` paths — drop real files at those paths to replace placeholders with `<img>`.

### Content Map (what comes from where)

| Site page / block | Source | Destination |
|---|---|---|
| Design system, hero, tagline, stats, advantages, services, projects, clients | kaskad-energo.ru | Home, **Construction**, About |
| Switchgear catalogue, spec tables, manufacturing, certificates | kaskad-ts.ru | **Switchgear**, Products, About (certs) |
| Electricity-meter models, specs, comparison, docs, technology | mirtekgroup.com | **Meters**, Products |
| Company address/phone (new) | brief | global header/footer/contact |

---

## 3. Information Architecture & Sitemap

```
Home (index.html)
├── Construction        (construction.html)   ← services · projects · gallery · clients · tech info
├── Switchgear          (switchgear.html)     ← catalogue · spec accordions · process · gallery
├── Meters              (meters.html)         ← catalogue · technology · comparison · docs · gallery
├── Projects            (projects.html)       ← all projects · category filter
├── Products            (products.html)       ← switchgear + meters · search + filter
├── About               (about.html)          ← history · mission · vision · values · certs · partners
└── Contact             (contact.html)        ← address · phone · form · Google Map
```
Language variants share one URL; language is a client-side state (`?lang=` mirrored via `hreflang`). Every page carries `canonical` + 3× `hreflang` + `x-default`.

---

## 4. Wireframes (ASCII)

**Home**
```
┌ topbar: phone · address ─────────────────────────────┐
├ header: [logo] KASKAD GROUP … nav … [HY|RU|EN] [≡] ──┤
│ HERO  kicker / "ENERGY OF TRANSFORMATIONS" / sub / [CTA][CTA] + grid motif
│ INTRO (centered): kicker · title · paragraph
│ DIVISIONS (dark): 3 cards → Construction / Switchgear / Meters
│ FEATURED PROJECTS (tint): 3 cards + "All projects"
│ FEATURED PRODUCTS: 3 switchgear + 3 meters + "All products"
│ ADVANTAGES (tint): 6 tiles
│ STATS (dark): 20+ / 100+ / 5 / 30+   (count-up)
│ PARTNERS: logo chips
│ NEWS (tint): 3 cards
│ CONTACT CTA (dark)
└ footer: brand · divisions · company · contact
```
**Division / catalogue pages:** page-hero + breadcrumbs → catalogue grid → spec accordions / comparison table → process/tech → gallery.
**Products:** hero → search box → [All | Switchgear | Meters] chips → responsive card grid.
**Contact:** two-column (info list ｜ form) → full-width map.

---

## 5. UI/UX Design System

- **Palette:** navy `#05101f/#08192b/#0b1a2b` · accent blue `#0f8ce8` · cyan `#38bdf8` · warm CTA orange `#f97316` · paper `#fff/#f4f7fb` · ink text `#10151b`.
- **Type:** headings **Montserrat 800/900 UPPERCASE** with **Noto Sans Armenian** fallback (covers HY glyphs); body **Inter** + Noto Sans Armenian. All three scripts (Latin/Cyrillic/Armenian) render from one stack.
- **Tokens:** CSS custom properties for color, radius, shadow, spacing, easing (`:root` in `styles.css`).
- **Motion:** IntersectionObserver scroll-reveal with per-item stagger (`--d`), animated stat counters, hover lifts; all disabled under `prefers-reduced-motion`.
- **Responsive:** fluid `clamp()` type/spacing; grids collapse 4→2→1; nav becomes a slide-down drawer < 1080 px.
- **Accessibility:** semantic landmarks, `aria-expanded` burger, `lang`/`dir` synced to selection, focus-visible states, color-contrast-safe on dark sections.

---

## 6. Component Hierarchy

```
App (app.js IIFE)
├── Header  (topbar, brand, Nav, LanguageSwitcher, Burger)
├── Footer  (brand, link columns, contact)
├── Primitives:  Button · Kicker · SectionHead · Tag · Media(placeholder) · Icon(SVG set)
├── Cards:  DivisionCard · ServiceCard · ProjectCard · ProductCard · MeterCard · FeatureTile · StatTile · NewsCard · CertCard
├── Data views:  SpecTable · SpecAccordion · ComparisonTable · Timeline · ProcessSteps · DocList · LogoWall · Gallery
└── Controls:  FilterChips · SearchBox · ContactForm · ScrollTop
```
Rendering is data-driven: HTML declares `data-render="<name>"` slots; `app.js` fills them from `window.DATA`. Text uses `data-i18n` / `data-i18n-ph` resolved from `window.I18N`.

---

## 7. Database Schema (future CMS/back-end)

Static site ships JSON-shaped JS today; this maps 1:1 to a relational schema when a CMS is added.

```sql
-- translatable string bundles
locale            (code PK)                                   -- 'hy','ru','en'
translation       (id PK, key, locale FK, value)              -- UI + free text

division          (id PK, slug, sort)                         -- construction|switchgear|meters
division_i18n     (division_id FK, locale FK, name, summary)

service           (id PK, division_id FK, icon, sort)
service_i18n      (service_id FK, locale FK, name, summary)
service_point     (id PK, service_id FK, sort)
service_point_i18n(service_point_id FK, locale FK, text)

product_category  (id PK, division_id FK, slug, image, voltage, current)
category_i18n     (category_id FK, locale FK, name, summary, description)
product           (id PK, category_id FK, code, image, kind)  -- module|meter|component
product_i18n      (product_id FK, locale FK, name, tagline)
product_spec      (id PK, product_id FK, sort, value)         -- value may be scalar or i18n
product_spec_i18n (spec_id FK, locale FK, label, value)
product_iface     (product_id FK, name)                       -- meter interfaces
product_feature   (id PK, product_id FK); feature_i18n(...)

project           (id PK, slug, image, country, year, category, spec, client_id FK)
project_i18n      (project_id FK, locale FK, name, location, description, client)

client            (id PK, logo); client_i18n(client_id, locale, name)
partner           (id PK, name, logo)
certificate       (id PK, image); certificate_i18n(...)
stat              (id PK, value, suffix, sort); stat_i18n(...)
company_value/advantage/history_milestone (+_i18n)
news             (id PK, slug, published_at, image); news_i18n(...)
contact_message  (id PK, name, email, phone, subject, message, created_at)  -- form intake
```
Indexes on every `*_i18n(entity_id, locale)`; FKs cascade; `slug` unique per table.

---

## 8. Translation Strategy (HY / RU / EN)

- **Two layers:** (a) UI chrome/page copy in `i18n.js` keyed strings; (b) domain content in `data.*.js` as inline `{hy,ru,en}` objects.
- **Fallback chain:** `selected → ru → en → key` (never blank).
- **Default language: HY** (Armenian HQ); persisted in `localStorage` and reflected in `<html lang>`/`dir`.
- **Switcher** is present in the header on every page; switching re-renders in place without reload.
- **RU is source of record** (original marketing/spec language); HY & EN are professional translations kept structurally parallel (same keys) — verified: **0 missing keys across 91 UI strings × 3 languages**.
- **SEO:** `hreflang` alternates + `x-default`; for full crawler indexing of each language, the same data can be pre-rendered to `/{hy,ru,en}/…` at build time (roadmap Phase 2).

---

## 9. SEO & Quality

- Unique `<title>` + meta description per page; canonical + hreflang; Open Graph; `Organization` JSON-LD on home.
- Semantic HTML5 (`header/main/section/article/footer/nav/time`), descriptive `alt`/`aria-label`, single `<h1>` per page.
- Performance: font `preconnect` + `display=swap`, lazy map iframe, zero framework/runtime deps, CSS+JS ~1 file each.

---

## 10. Implementation Roadmap

| Phase | Scope | Status |
|---|---|---|
| **0 — Discovery** | Crawl 3 sites, extract content, define IA & design language | ✅ done |
| **1 — Static build (this deliverable)** | Design system, trilingual engine, 8 pages, data-driven catalogues, forms, map, verification | ✅ done |
| **2 — Content & media** | Replace placeholder media with real photos/renders at `data.*.js` image paths; add remaining ~30 switchgear module detail pages & meter datasheet PDFs | ▢ |
| **3 — SEO hardening** | Static per-language pre-render (`/hy /ru /en`), `sitemap.xml`, `robots.txt`, structured data for products/breadcrumbs | ▢ |
| **4 — Back-end** | Implement schema (§7) in a CMS (Strapi/Directus) or DB; wire contact form to email/CRM + spam protection | ▢ |
| **5 — QA & launch** | Cross-browser/device QA, Lighthouse ≥90, WCAG AA audit, analytics, domain + TLS | ▢ |

---

## How to run
Pure static — **no build step**. Open `site/index.html` in any browser
(works over `file://`; no server needed). Use the **HY / RU / EN** switch in the
header. To serve locally: `cd site && python -m http.server 8080`.
