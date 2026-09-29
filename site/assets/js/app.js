/* ============================================================================
 * KASKAD GROUP — FRONT-END ENGINE
 * Pure vanilla JS. No build step, no fetch (works over file://).
 * Responsibilities: i18n, header/footer injection, dynamic catalog rendering,
 * language switcher, mobile nav, scroll-reveal, counters, filtering, search,
 * comparison table, contact form.
 * ==========================================================================*/
(function () {
  "use strict";

  var LANGS = ["hy", "ru", "en"];
  var STORE_KEY = "kaskad_lang";
  var lang = localStorage.getItem(STORE_KEY);
  if (LANGS.indexOf(lang) === -1) lang = "hy";

  /* ---- helpers --------------------------------------------------------- */
  function t(key) {
    var d = window.I18N[lang];
    return (d && d[key] != null) ? d[key] : (window.I18N.en[key] != null ? window.I18N.en[key] : key);
  }
  function pick(obj) {
    if (obj == null) return "";
    if (typeof obj === "string") return obj;
    return obj[lang] != null ? obj[lang] : (obj.ru != null ? obj.ru : (obj.en != null ? obj.en : ""));
  }
  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === "class") e.className = attrs[k];
      else e.setAttribute(k, attrs[k]);
    }
    if (html != null) e.innerHTML = html;
    return e;
  }
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* ---- SVG icon set ---------------------------------------------------- */
  var ICONS = {
    bolt: '<path d="M13 2 4 14h6l-1 8 9-12h-6z"/>',
    factory: '<path d="M3 21V9l6 4V9l6 4V4h6v17z"/>',
    blueprint: '<path d="M3 4h18v16H3z"/><path d="M3 9h18M9 4v16"/>',
    network: '<circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M6 8v3a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V8M12 16v-2"/>',
    gauge: '<path d="M12 13 16 9"/><path d="M4 20a8 8 0 1 1 16 0z"/>',
    test: '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/>',
    cycle: '<path d="M4 12a8 8 0 0 1 14-5m2-2v5h-5"/><path d="M20 12a8 8 0 0 1-14 5m-2 2v-5h5"/>',
    medal: '<circle cx="12" cy="9" r="5"/><path d="M9 13l-2 8 5-3 5 3-2-8"/>',
    globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    team: '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 6a3 3 0 0 1 0 6M21 20a6 6 0 0 0-5-5.9"/>',
    shield: '<path d="M12 3l8 3v5c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6z"/>',
    wifi: '<path d="M5 12a10 10 0 0 1 14 0M8 15a6 6 0 0 1 8 0"/><circle cx="12" cy="18" r="1.4"/>',
    code: '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    bulb: '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 1 4 10l-1 3H9l-1-3A6 6 0 0 1 12 3z"/>',
    leaf: '<path d="M4 20C4 10 12 4 20 4c0 10-8 16-16 16z"/><path d="M4 20c4-6 8-8 12-9"/>',
    box: '<path d="M12 3 3 7.5v9L12 21l9-4.5v-9z"/><path d="M3 7.5 12 12l9-4.5M12 12v9"/>',
    phone: '<path d="M4 4h4l2 5-3 2a12 12 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 2 6a2 2 0 0 1 2-2z"/>',
    pin: '<path d="M12 22s7-6 7-12a7 7 0 0 0-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    mail: '<path d="M3 6h18v12H3z"/><path d="m3 7 9 6 9-6"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>'
  };
  function icon(name, cls) {
    return '<svg class="icon ' + (cls || "") + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (ICONS[name] || ICONS.box) + '</svg>';
  }
  /* Decorative image placeholder (self-contained; used when no real image set) */
  function media(label, variant) {
    var v = variant || "a";
    return '<div class="media media--' + v + '" role="img" aria-label="' + String(label).replace(/"/g, "") + '">' +
      icon("box", "media__icon") + '<span class="media__label">' + label + '</span></div>';
  }
  /* Real image inside the same .media box (aspect-ratio + overflow preserved),
     falling back to the styled placeholder when no URL is available. */
  function mediaImg(url, label, variant, objectFit) {
    if (!url) return media(label, variant);
    var v = variant || "a";
    var safe = String(label == null ? "" : label).replace(/"/g, "");
    return '<div class="media media--' + v + (objectFit === "contain" ? " media--contain" : "") + '" role="img" aria-label="' + safe + '">' +
      '<img src="' + url + '" alt="' + safe + '" loading="lazy" ' +
      'style="position:absolute;inset:0;width:100%;height:100%;object-fit:' + (objectFit || "cover") + ';object-position:center;z-index:2" />' +
      '</div>';
  }

  /* ==================================================================== */
  /*  HEADER + FOOTER                                                      */
  /* ==================================================================== */
  var NAV = [
    ["home", "index.html"], ["construction", "construction.html"], ["switchgear", "switchgear.html"],
    ["meters", "meters.html"], ["projects", "projects.html"], ["products", "products.html"],
    ["about", "about.html"], ["contact", "contact.html"]
  ];

  function buildHeader() {
    var host = $("#site-header");
    if (!host) return;
    var page = document.body.getAttribute("data-page") || "home";
    var links = NAV.map(function (n) {
      var active = n[0] === page ? " active" : "";
      return '<a class="nav__link' + active + '" href="' + n[1] + '" data-i18n="nav.' + n[0] + '"></a>';
    }).join("");
    var langBtns = LANGS.map(function (l) {
      return '<button class="lang__opt' + (l === lang ? " active" : "") + '" data-lang="' + l + '">' + l.toUpperCase() + '</button>';
    }).join("");

    host.innerHTML =
      '<div class="topbar"><div class="wrap topbar__in">' +
        '<a class="topbar__item" href="tel:' + window.DATA.company.contact.phoneLink + '">' + icon("phone") + '<span>' + window.DATA.company.contact.phone + '</span></a>' +
        '<span class="topbar__item topbar__addr">' + icon("pin") + '<span data-render="topAddr"></span></span>' +
      '</div></div>' +
      '<div class="wrap header__in">' +
        '<a class="brand" href="index.html" aria-label="KASKAD Holding">' +
          '<img class="brand__logo" src="assets/img/logo-light.png" alt="KASKAD Holding" width="362" height="96" />' +
        '</a>' +
        '<nav class="nav" id="primaryNav">' + links + '</nav>' +
        '<div class="header__tools">' +
          '<div class="lang" role="group" aria-label="Language">' + langBtns + '</div>' +
          '<button class="burger" id="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>' +
        '</div>' +
      '</div>';
  }

  function buildFooter() {
    var host = $("#site-footer");
    if (!host) return;
    var c = window.DATA.company.contact;
    function col(titleKey, items) {
      return '<div class="foot__col"><h4 data-i18n="' + titleKey + '"></h4><ul>' +
        items.map(function (i) { return '<li><a href="' + i[1] + '" data-i18n="' + i[0] + '"></a></li>'; }).join("") + '</ul></div>';
    }
    host.innerHTML =
      '<div class="wrap foot__grid">' +
        '<div class="foot__col foot__brand">' +
          '<a class="brand brand--foot" href="index.html" aria-label="KASKAD Holding">' +
          '<img class="brand__logo" src="assets/img/logo-light.png" alt="KASKAD Holding" width="362" height="96" /></a>' +
          '<p class="foot__about" data-i18n="footer.about"></p>' +
        '</div>' +
        col("footer.divisions", [["nav.construction","construction.html"],["nav.switchgear","switchgear.html"],["nav.meters","meters.html"],["nav.products","products.html"]]) +
        col("footer.company", [["nav.about","about.html"],["nav.projects","projects.html"],["nav.contact","contact.html"]]) +
        '<div class="foot__col"><h4 data-i18n="footer.contact"></h4><ul class="foot__contact">' +
          '<li>' + icon("pin") + '<span data-render="footAddr"></span></li>' +
          '<li>' + icon("phone") + '<a href="tel:' + c.phoneLink + '">' + c.phone + '</a></li>' +
          '<li>' + icon("mail") + '<a href="mailto:' + c.email + '">' + c.email + '</a></li>' +
        '</ul></div>' +
      '</div>' +
      '<div class="wrap foot__bar"><span>© <span id="year"></span> <span data-i18n="brand.name"></span> <span data-i18n="brand.suffix"></span>. <span data-i18n="footer.rights"></span></span></div>';
  }

  /* ==================================================================== */
  /*  I18N APPLICATION                                                     */
  /* ==================================================================== */
  function applyI18n(root) {
    $all("[data-i18n]", root).forEach(function (e) { e.textContent = t(e.getAttribute("data-i18n")); });
    $all("[data-i18n-html]", root).forEach(function (e) { e.innerHTML = t(e.getAttribute("data-i18n-html")); });
    $all("[data-i18n-ph]", root).forEach(function (e) { e.setAttribute("placeholder", t(e.getAttribute("data-i18n-ph"))); });
    document.documentElement.setAttribute("lang", lang);
    document.documentElement.setAttribute("dir", t("meta.dir"));
    var y = $("#year"); if (y) y.textContent = new Date().getFullYear();
  }

  /* ==================================================================== */
  /*  RENDERERS (populate [data-render] containers if present)            */
  /* ==================================================================== */
  function fill(name, htmlOrFn) {
    $all('[data-render="' + name + '"]').forEach(function (host) {
      host.innerHTML = typeof htmlOrFn === "function" ? htmlOrFn(host) : htmlOrFn;
    });
  }

  function renderChrome() {
    fill("topAddr", pick(window.DATA.company.contact.address));
    fill("footAddr", pick(window.DATA.company.contact.address));
    var contact = window.DATA.company.contact;
    var phone = $("#cPhone");
    if (phone) {
      phone.textContent = contact.phone;
      phone.href = "tel:" + contact.phoneLink;
    }
    var email = $("#cMail");
    if (email) {
      email.textContent = contact.email;
      email.href = "mailto:" + contact.email;
    }
  }

  /* Divisions (home) */
  function renderDivisions() {
    var items = [
      ["construction", "construction.html", "blueprint"],
      ["switchgear", "switchgear.html", "factory"],
      ["meters", "meters.html", "gauge"]
    ];
    fill("divisions", items.map(function (d, i) {
      return '<a class="divcard reveal" style="--d:' + (i * 90) + 'ms" href="' + d[1] + '">' +
        '<span class="divcard__ico">' + icon(d[2]) + '</span>' +
        '<h3 data-i18n="home.div.' + d[0] + '.title"></h3>' +
        '<p data-i18n="home.div.' + d[0] + '.text"></p>' +
        '<span class="divcard__more">' + t("cta.more") + ' ' + icon("arrow") + '</span></a>';
    }).join(""));
  }

  /* Construction services */
  function renderServices() {
    fill("services", window.DATA.construction.services.map(function (s, i) {
      var pts = (s.points || []).map(function (p) { return "<li>" + pick(p) + "</li>"; }).join("");
      return '<article class="service reveal" style="--d:' + (i * 60) + 'ms">' +
        '<span class="service__ico">' + icon(s.icon) + '</span>' +
        '<h3>' + pick(s.name) + '</h3><p>' + pick(s.summary) + '</p>' +
        (pts ? '<ul class="ticks">' + pts + '</ul>' : '') + '</article>';
    }).join(""));
  }

  /* Project cards */
  function projectCard(p, i) {
    return '<article class="projcard reveal" data-cat="' + p.category + '" style="--d:' + (i * 60) + 'ms">' +
      '<div class="projcard__media">' + mediaImg(p.image, pick(p.name), "b") + '<span class="projcard__spec">' + p.spec + '</span></div>' +
      '<div class="projcard__body"><span class="tag">' + pick(p.location) + ' · ' + p.year + '</span>' +
      '<h3>' + pick(p.name) + '</h3><p>' + pick(p.description) + '</p>' +
      '<span class="projcard__client">' + t("label.client") + ': ' + pick(p.client) + '</span></div></article>';
  }
  function renderProjects(limit) {
    var list = window.DATA.construction.projects.slice(0, limit || 999);
    fill("projects", list.map(projectCard).join(""));
  }

  /* Project filter (projects page) */
  function renderProjectFilters() {
    fill("projectFilters", window.DATA.construction.projectCategories.map(function (c, i) {
      return '<button class="chip' + (i === 0 ? " active" : "") + '" data-filter="' + c.id + '">' + pick(c.name) + '</button>';
    }).join(""));
  }

  /* Switchgear category cards */
  function switchgearCard(c, i) {
    var meta = [c.voltage, c.current ? pick(c.current) : null].filter(Boolean).join(" · ");
    return '<article class="prodcard reveal" style="--d:' + (i * 55) + 'ms">' +
      '<div class="prodcard__media">' + mediaImg(c.image, c.name.en || pick(c.name), "c") + '</div>' +
      '<div class="prodcard__body">' + (meta ? '<span class="tag">' + meta + '</span>' : '') +
      '<h3>' + pick(c.name) + '</h3><p>' + pick(c.summary) + '</p>' + '</div></article>';
  }
  function renderSwitchgear(limit) {
    var list = window.DATA.switchgear.categories.slice(0, limit || 999);
    fill("switchgear", list.map(switchgearCard).join(""));
  }

  /* A "rich" module carries a full product detail (KD-2 family): its own spec
     table and/or description. Thin legacy items only have {code,name}. */
  function isRichModule(it) {
    return !!(it && ((it.specs && it.specs.length && it.specs[0] && it.specs[0].param) ||
      pick(it.description) || pick(it.purpose)));
  }

  /* Clickable module card that opens the detail modal */
  function switchgearModuleCard(it) {
    var sub = pick(it.name) || pick(it.purpose);
    return '<button type="button" class="modcard reveal" data-module="' + encodeURIComponent(it.code) + '">' +
      '<div class="modcard__media">' + mediaImg(it.image, it.code, "c") + '</div>' +
      '<div class="modcard__body"><b class="modcard__code">' + it.code + '</b>' +
      (sub ? '<span class="modcard__name">' + sub + '</span>' : '') + '</div>' +
      '<span class="modcard__go">' + pick({ hy: "Մանրամասն", ru: "Подробнее", en: "Details" }) +
      icon("arrow", "modcard__arrow") + '</span></button>';
  }

  /* Switchgear detailed spec accordions (+ rich KD-2 module grid) */
  function renderSwitchgearSpecs() {
    fill("switchgearSpecs", window.DATA.switchgear.categories.map(function (c) {
      var specs = (c.specs || []).map(function (s) {
        return '<tr><th>' + pick(s.label) + '</th><td>' + pick(s.value) + '</td></tr>';
      }).join("");
      var rich = (c.items || []).some(isRichModule);
      var items;
      if (rich) {
        items = '<div class="modgrid">' + (c.items || []).map(switchgearModuleCard).join("") + '</div>';
      } else {
        var hasItemImg = (c.items || []).some(function (it) { return it.image; });
        var lis = (c.items || []).map(function (it) {
          if (hasItemImg) {
            return '<li class="module"><div class="module__media">' + mediaImg(it.image, it.code, "c") +
              '</div><div class="module__cap"><b>' + it.code + '</b> — ' + pick(it.name) + '</div></li>';
          }
          return '<li><b>' + it.code + '</b> — ' + pick(it.name) + '</li>';
        }).join("");
        items = lis ? '<ul class="modules' + (hasItemImg ? ' modules--cards' : '') + '">' + lis + '</ul>' : '';
      }
      return '<details class="acc reveal"' + (rich ? ' open' : '') + '><summary><span>' + pick(c.name) + '</span>' +
        (c.voltage ? '<em>' + c.voltage + '</em>' : '') + '</summary>' +
        '<div class="acc__body"><p>' + pick(c.description) + '</p>' +
        (specs ? '<table class="spectable">' + specs + '</table>' : '') + items + '</div></details>';
    }).join(""));
  }

  /* ---- Module detail modal -------------------------------------------- */
  function findModule(code) {
    var cats = (window.DATA.switchgear && window.DATA.switchgear.categories) || [];
    for (var i = 0; i < cats.length; i++) {
      var its = cats[i].items || [];
      for (var j = 0; j < its.length; j++) if (its[j].code === code) return its[j];
    }
    return null;
  }

  function moduleDetailHTML(it) {
    var L = {
      equip: pick({ hy: "Ստանդարտ սարքավորում", ru: "Стандартное оборудование", en: "Standard equipment" }),
      opt: pick({ hy: "Ընտրանքներ", ru: "Опции", en: "Options" }),
      vac: pick({ hy: "Վակուումային անջատիչի ընտրանքներ", ru: "Опции вакуумного выключателя", en: "Vacuum-breaker options" }),
      specs: pick({ hy: "Տեխնիկական բնութագրեր", ru: "Технические характеристики", en: "Technical characteristics" }),
      desc: pick({ hy: "Նկարագրություն", ru: "Описание", en: "Description" }),
      purpose: pick({ hy: "Նշանակություն", ru: "Назначение", en: "Purpose" }),
      fuse: pick({ hy: "Ապահովիչների ընտրության աղյուսակ", ru: "Таблица выбора предохранителей", en: "Fuse selection table" }),
      pdf: pick({ hy: "Ներբեռնել հրահանգը (PDF)", ru: "Скачать инструкцию (PDF)", en: "Download instructions (PDF)" })
    };
    var imgs = [];
    if (it.image) imgs.push(it.image);
    (it.gallery || []).forEach(function (g) { if (imgs.indexOf(g) < 0) imgs.push(g); });
    var gallery = imgs.length
      ? '<div class="kmodal__gallery"><div class="kmodal__main">' + mediaImg(imgs[0], it.code, "c") + '</div>' +
        (imgs.length > 1 ? '<div class="kmodal__thumbs">' + imgs.map(function (u, i) {
          return '<button type="button" class="kthumb' + (i === 0 ? ' is-active' : '') + '" data-full="' + u +
            '"><img src="' + u + '" alt="' + it.code + '" loading="lazy"></button>';
        }).join("") + '</div>' : '') + '</div>'
      : '';

    var specTable = "";
    if (it.specs && it.specs.length && it.specs[0] && it.specs[0].param) {
      var cols = it.specCols || [];
      var head = '<tr><th></th><th></th>' + cols.map(function (c) { return '<th>' + c + '</th>'; }).join("") + '</tr>';
      var body = it.specs.map(function (r) {
        if (r.group) return '<tr class="specrow--group"><th colspan="' + (2 + cols.length) + '">' + pick(r.param) + '</th></tr>';
        var vals = [];
        for (var k = 0; k < cols.length; k++) vals.push('<td>' + (r.values[k] || '—') + '</td>');
        return '<tr><th>' + pick(r.param) + '</th><td class="specunit">' + (r.unit || '') + '</td>' + vals.join("") + '</tr>';
      }).join("");
      specTable = '<div class="tablewrap"><table class="spectable spectable--mod"><thead>' + head +
        '</thead><tbody>' + body + '</tbody></table></div>';
    }
    var notes = pick(it.notes);
    var notesHTML = notes ? '<p class="kmodal__notes">' + notes.replace(/\n/g, '<br>') + '</p>' : '';

    function bl(title, arr) {
      if (!arr || !arr.length) return "";
      return '<div class="kmodal__block"><h4>' + title + '</h4><ul class="kmodal__list">' +
        arr.map(function (x) { return '<li>' + pick(x) + '</li>'; }).join("") + '</ul></div>';
    }
    var fuseHTML = "";
    if (it.fuse && it.fuse.cols) {
      var f = it.fuse;
      var fh = '<tr><th>' + pick(f.head) + '</th>' + f.cols.map(function (c) { return '<th>' + c + '</th>'; }).join("") + '</tr>';
      var fb = f.rows.map(function (row) {
        return '<tr>' + row.map(function (cell, ci) {
          return ci === 0 ? '<th>' + cell + '</th>' : '<td>' + (cell || '') + '</td>';
        }).join("") + '</tr>';
      }).join("");
      fuseHTML = '<div class="kmodal__block"><h4>' + L.fuse + '</h4><div class="tablewrap">' +
        '<table class="spectable spectable--fuse"><thead>' + fh + '</thead><tbody>' + fb + '</tbody></table></div></div>';
    }
    var pdfBtn = it.pdf ? '<a class="btn btn--hot kmodal__pdf" href="' + it.pdf + '" target="_blank" rel="noopener">' +
      icon("box") + '<span>' + L.pdf + '</span></a>' : '';

    return '<div class="kmodal__headrow"><div><span class="kmodal__code">' + it.code + '</span>' +
      (pick(it.name) ? '<h3 class="kmodal__title">' + pick(it.name) + '</h3>' : '') + '</div></div>' +
      '<div class="kmodal__grid"><div class="kmodal__left">' + gallery +
      (pdfBtn ? '<div class="kmodal__actions">' + pdfBtn + '</div>' : '') + '</div>' +
      '<div class="kmodal__right">' +
      (pick(it.description) ? '<div class="kmodal__block"><h4>' + L.desc + '</h4><p>' + pick(it.description) + '</p></div>' : '') +
      (pick(it.purpose) ? '<div class="kmodal__block"><h4>' + L.purpose + '</h4><p>' + pick(it.purpose) + '</p></div>' : '') +
      '</div></div>' +
      (specTable ? '<div class="kmodal__block"><h4>' + L.specs + '</h4>' + specTable + notesHTML + '</div>' : '') +
      '<div class="kmodal__cols">' + bl(L.equip, it.equipment) + bl(L.opt, it.options) + bl(L.vac, it.vacuum) + '</div>' +
      fuseHTML;
  }

  var openModuleCode = null;
  function ensureModal() {
    var m = $("#kmodal");
    if (m) return m;
    m = el("div", { id: "kmodal", "class": "kmodal", "aria-hidden": "true" });
    m.innerHTML = '<div class="kmodal__backdrop" data-close></div>' +
      '<div class="kmodal__dialog" role="dialog" aria-modal="true">' +
      '<button type="button" class="kmodal__x" data-close aria-label="Close">&times;</button>' +
      '<div class="kmodal__content"></div></div>';
    document.body.appendChild(m);
    return m;
  }
  function openModule(code) {
    var it = findModule(code);
    if (!it) return;
    var m = ensureModal();
    $(".kmodal__content", m).innerHTML = moduleDetailHTML(it);
    var dlg = $(".kmodal__dialog", m); if (dlg) dlg.scrollTop = 0;
    m.classList.add("open");
    m.setAttribute("aria-hidden", "false");
    document.body.classList.add("kmodal-open");
    openModuleCode = code;
    if ("history" in window && window.history.replaceState) {
      window.history.replaceState(null, "", "#module=" + encodeURIComponent(code));
    }
  }
  function closeModule() {
    var m = $("#kmodal");
    if (!m) return;
    m.classList.remove("open");
    m.setAttribute("aria-hidden", "true");
    document.body.classList.remove("kmodal-open");
    openModuleCode = null;
    if (location.hash.indexOf("#module=") === 0 && window.history.replaceState) {
      window.history.replaceState(null, "", location.pathname + location.search);
    }
  }
  /* Open a module from a #module=CODE deep link (shareable product links). */
  function openModuleFromHash() {
    var mm = /^#module=(.+)$/.exec(location.hash || "");
    if (mm) openModule(decodeURIComponent(mm[1]));
  }
  function wireModal() {
    document.addEventListener("click", function (e) {
      if (!e.target.closest) return;
      var opener = e.target.closest("[data-module]");
      if (opener) { e.preventDefault(); openModule(decodeURIComponent(opener.getAttribute("data-module"))); return; }
      if (e.target.closest("[data-close]")) { closeModule(); return; }
      var th = e.target.closest(".kthumb");
      if (th) {
        var full = th.getAttribute("data-full");
        var main = $("#kmodal .kmodal__main");
        if (main) main.innerHTML = mediaImg(full, "", "c");
        $all("#kmodal .kthumb").forEach(function (x) { x.classList.remove("is-active"); });
        th.classList.add("is-active");
      }
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeModule(); });
  }

  /* Manufacturing process steps */
  function renderProcess() {
    var steps = [
      { n: "01", t: { hy: "Նախագծում", ru: "Проектирование", en: "Engineering" } },
      { n: "02", t: { hy: "Մետաղամշակում", ru: "Металлообработка", en: "Metalwork" } },
      { n: "03", t: { hy: "Հավաքում", ru: "Сборка", en: "Assembly" } },
      { n: "04", t: { hy: "Փորձարկում և սերտիֆիկացում", ru: "Испытания и сертификация", en: "Testing & certification" } }
    ];
    fill("process", '<p class="lead">' + pick(window.DATA.switchgear.manufacturing) + '</p>' +
      '<ol class="steps">' + steps.map(function (s, i) {
        return '<li class="reveal" style="--d:' + (i * 70) + 'ms"><span class="steps__n">' + s.n + '</span><span>' + pick(s.t) + '</span></li>';
      }).join("") + '</ol>');
  }

  /* A meter feature is either a plain {hy,ru,en} object (bundled fallback) or a
     {text:{hy,ru,en}, image} object (live from the API). Normalise to one shape. */
  function featureParts(f) {
    if (f && f.text) return { text: f.text, image: f.image || null };
    return { text: f, image: null };
  }

  /* Meter cards */
  function meterCard(m, i) {
    var chips = m.interfaces.slice(0, 4).map(function (x) { return '<span class="mini">' + x + '</span>'; }).join("");
    var feats = (m.features || []).map(featureParts);
    var hasFeatImg = feats.some(function (f) { return f.image; });
    var featBlock = hasFeatImg
      ? '<ul class="modules modules--cards modules--feat">' + feats.map(function (f) {
          return '<li class="module"><div class="module__media">' + mediaImg(f.image, pick(f.text), "d") + '</div>' +
            '<div class="module__cap">' + pick(f.text) + '</div></li>';
        }).join("") + '</ul>'
      : '';
    return '<article class="prodcard reveal" data-cat="' + m.category + '" style="--d:' + (i * 55) + 'ms">' +
      '<div class="prodcard__media">' + mediaImg(m.image, m.name, "d", "contain") + '</div>' +
      '<div class="prodcard__body"><span class="tag">' + pick(m.form) + ' · ' + t("label.accuracy") + ' ' + m.accuracy + '</span>' +
      '<h3>' + m.name + '</h3><p>' + pick(m.tagline) + '</p>' +
      '<div class="minis">' + chips + '</div>' + featBlock + '</div></article>';
  }
  function renderMeters(limit) {
    var list = window.DATA.meters.products.slice(0, limit || 999);
    fill("meters", list.map(meterCard).join(""));
  }

  /* Meter technology tiles */
  function renderMeterTech() {
    fill("meterTech", window.DATA.meters.technology.map(function (x, i) {
      return '<article class="feature reveal" style="--d:' + (i * 60) + 'ms"><span class="feature__ico">' + icon(x.icon) + '</span>' +
        '<h3>' + pick(x.title) + '</h3><p>' + pick(x.text) + '</p></article>';
    }).join(""));
  }

  /* Meter docs list */
  function renderMeterDocs() {
    fill("meterDocs", '<ul class="doclist">' + window.DATA.meters.docTypes.map(function (d) {
      return '<li><a href="#" onclick="return false">' + icon("box") + '<span>' + pick(d) + '</span><em>PDF</em></a></li>';
    }).join("") + '</ul>');
  }

  /* Meter comparison table */
  function renderMeterCompare() {
    var rows = window.DATA.meters.products.map(function (m) {
      return '<tr><td><b>' + m.name + '</b></td><td>' + pick(m.form) + '</td><td>' + m.accuracy + '</td><td>' + m.current + '</td><td>' + m.interfaces.join(", ") + '</td></tr>';
    }).join("");
    fill("meterCompare", '<div class="tablewrap"><table class="spectable spectable--wide"><thead><tr>' +
      '<th data-i18n="mt.compare.model"></th><th data-i18n="mt.compare.type"></th><th data-i18n="mt.compare.accuracy"></th>' +
      '<th data-i18n="mt.compare.current"></th><th data-i18n="mt.compare.interfaces"></th></tr></thead><tbody>' + rows + '</tbody></table></div>');
  }

  /* Stats (animated) */
  function renderStats() {
    fill("stats", window.DATA.company.stats.map(function (s) {
      return '<div class="stat reveal"><span class="stat__num" data-count="' + s.value + '">0</span><span class="stat__suf">' + s.suffix + '</span>' +
        '<span class="stat__lbl">' + pick(s.label) + '</span></div>';
    }).join(""));
  }

  /* Advantages */
  function renderAdvantages() {
    fill("advantages", window.DATA.company.advantages.map(function (a, i) {
      return '<article class="feature reveal" style="--d:' + (i * 55) + 'ms"><span class="feature__ico">' + icon(a.icon) + '</span>' +
        '<h3>' + pick(a.title) + '</h3><p>' + pick(a.text) + '</p></article>';
    }).join(""));
  }

  /* Values */
  function renderValues() {
    fill("values", window.DATA.company.values.map(function (a, i) {
      return '<article class="feature reveal" style="--d:' + (i * 55) + 'ms"><span class="feature__ico">' + icon(a.icon) + '</span>' +
        '<h3>' + pick(a.title) + '</h3><p>' + pick(a.text) + '</p></article>';
    }).join(""));
  }

  /* History timeline */
  function renderHistory() {
    fill("history", '<ol class="timeline">' + window.DATA.company.history.map(function (h, i) {
      return '<li class="reveal" style="--d:' + (i * 70) + 'ms"><span class="timeline__yr">' + h.year + '</span><p>' + pick(h.text) + '</p></li>';
    }).join("") + '</ol>');
  }

  /* Certificates gallery */
  function renderCerts() {
    fill("certs", window.DATA.switchgear.certificates.map(function (c) {
      return '<figure class="cert reveal">' + mediaImg(c.image, pick(c.title), "e") + '<figcaption>' + pick(c.title) + '</figcaption></figure>';
    }).join(""));
  }

  /* Partners */
  function renderPartners() {
    fill("partners", window.DATA.company.partners.map(function (p) {
      return '<span class="plogo reveal">' + p.name + '</span>';
    }).join(""));
  }

  /* Clients */
  function renderClients() {
    fill("clients", window.DATA.company.clients.map(function (c) {
      return '<span class="plogo reveal">' + pick(c.name) + '</span>';
    }).join(""));
  }

  /* Gallery (generic decorative) */
  function renderGallery(name, labels, variant, section) {
    var db = (window.DATA && window.DATA.galleries && section) ? window.DATA.galleries[section] : null;
    if (db && db.length) {
      fill(name, db.map(function (g) {
        var cap = pick(g.caption) || g.alt || "";
        return '<figure class="gal reveal">' + mediaImg(g.image, cap, variant || "b") + '</figure>';
      }).join(""));
      return;
    }
    fill(name, labels.map(function (l) {
      return '<figure class="gal reveal">' + media(pick(l), variant || "b") + '</figure>';
    }).join(""));
  }

  /* News (from switchgear + construction context) */
  function renderNews() {
    var fallback = [
      { date: "2020-04-01", title: { hy: "Կալուգայի մարզի ղեկավարն այցելեց «Կասկադ» հոլդինգի օբյեկտներ", ru: "Глава Калужской области посетил объекты холдинга «Каскад»", en: "The head of Kaluga Region visited Kaskad Holding facilities" } },
      { date: "2019-12-05", title: { hy: "Միջազգային ֆորում «Էլեկտրական ցանցեր»՝ KD-2 լուծումների ներկայացում", ru: "Международный форум «Электрические сети»: решения на базе KD-2", en: "International forum “Electric Grids”: KD-2-based solutions presented" } },
      { date: "2019-05-01", title: { hy: "«Ախթանակ» 220 կՎ ենթակայանի վերակառուցման ավարտ Հայաստանում", ru: "Завершена реконструкция ПС «Ахтанак» 220 кВ в Армении", en: "Reconstruction of the Akhtanak 220 kV substation completed in Armenia" } }
    ];
    var news = (window.DATA && window.DATA.news && window.DATA.news.length) ? window.DATA.news : fallback;
    fill("news", news.map(function (n, i) {
      var d = new Date(n.date);
      return '<article class="news reveal" style="--d:' + (i * 60) + 'ms">' +
        '<time datetime="' + n.date + '"><b>' + ("0" + d.getDate()).slice(-2) + '</b>' + d.toLocaleDateString(lang, { month: "short", year: "numeric" }) + '</time>' +
        '<h3>' + pick(n.title) + '</h3><a class="news__more" href="#" onclick="return false">' + t("cta.more") + ' ' + icon("arrow") + '</a></article>';
    }).join(""));
  }

  /* Unified products (products.html) */
  function renderAllProducts() {
    var host = $('[data-render="allProducts"]');
    if (!host) return;
    var items = [];
    window.DATA.switchgear.categories.forEach(function (c) {
      items.push({ kind: "switchgear", name: pick(c.name), en: c.name.en, sub: pick(c.summary),
        meta: [c.voltage, c.current ? pick(c.current) : ""].filter(Boolean).join(" · "), variant: "c", image: c.image });
    });
    window.DATA.meters.products.forEach(function (m) {
      items.push({ kind: "meters", name: m.name, en: m.name, sub: pick(m.tagline),
        meta: pick(m.form) + " · " + t("label.accuracy") + " " + m.accuracy, variant: "d", image: m.image });
    });
    host._items = items;
    paintProducts(host, items);
  }
  function paintProducts(host, items) {
    if (!items.length) { host.innerHTML = '<p class="empty">' + t("products.empty") + '</p>'; return; }
    host.innerHTML = items.map(function (p, i) {
      return '<article class="prodcard reveal" data-kind="' + p.kind + '" data-search="' + (p.name + " " + p.en + " " + p.sub).toLowerCase() + '" style="--d:' + (i * 40) + 'ms">' +
        '<div class="prodcard__media">' + mediaImg(p.image, p.en || p.name, p.variant) + '</div>' +
        '<div class="prodcard__body">' + (p.meta ? '<span class="tag">' + p.meta + '</span>' : '') +
        '<h3>' + p.name + '</h3><p>' + p.sub + '</p></div></article>';
    }).join("");
    revealScan();
  }

  /* ==================================================================== */
  /*  INTERACTIONS                                                         */
  /* ==================================================================== */
  function wireLang() {
    document.addEventListener("click", function (e) {
      var b = e.target.closest ? e.target.closest(".lang__opt") : null;
      if (!b) return;
      var next = b.getAttribute("data-lang");
      if (next === lang) return;
      lang = next;
      localStorage.setItem(STORE_KEY, lang);
      renderPage();
    });
  }

  function wireBurger() {
    // Delegated: the header (and thus #burger) is rebuilt on each language switch.
    document.addEventListener("click", function (e) {
      var burger = e.target.closest ? e.target.closest("#burger") : null;
      if (burger) {
        var open = document.body.classList.toggle("nav-open");
        burger.setAttribute("aria-expanded", open ? "true" : "false");
        return;
      }
      if (e.target.closest && e.target.closest(".nav__link")) {
        document.body.classList.remove("nav-open");
        var b = $("#burger"); if (b) b.setAttribute("aria-expanded", "false");
      }
    });
  }

  function wireFilters() {
    document.addEventListener("click", function (e) {
      var chip = e.target.closest ? e.target.closest(".chip") : null;
      if (!chip) return;
      var group = chip.parentElement;
      $all(".chip", group).forEach(function (c) { c.classList.remove("active"); });
      chip.classList.add("active");
      var f = chip.getAttribute("data-filter");
      var scope = group.getAttribute("data-scope");
      if (scope === "products") {
        $all('[data-render="allProducts"] .prodcard').forEach(function (card) {
          card.style.display = (f === "all" || card.getAttribute("data-kind") === f) ? "" : "none";
        });
      } else {
        $all(".projcard").forEach(function (card) {
          card.style.display = (f === "all" || card.getAttribute("data-cat") === f) ? "" : "none";
        });
      }
    });
  }

  function wireSearch() {
    var input = $("#productSearch");
    if (!input) return;
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      $all('[data-render="allProducts"] .prodcard').forEach(function (card) {
        var hit = !q || card.getAttribute("data-search").indexOf(q) !== -1;
        card.style.display = hit ? "" : "none";
      });
    });
  }

  function wireForm() {
    var form = $("#contactForm");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $("#formMsg");
      var payload = {
        name: (form.name && form.name.value || "").trim(),
        email: (form.email && form.email.value || "").trim(),
        phone: (form.phone && form.phone.value || "").trim(),
        subject: (form.subject && form.subject.value || "").trim(),
        message: (form.message && form.message.value || "").trim()
      };
      function done() {
        if (msg) { msg.textContent = t("contact.form.success"); msg.classList.add("show"); }
        form.reset();
      }
      // Send to the CMS backend when available; fall back to the demo message.
      if (window.KASKAD && typeof window.KASKAD.sendContact === "function") {
        window.KASKAD.sendContact(payload).then(done, done);
      } else {
        done();
      }
    });
  }

  function wireScrollTop() {
    var btn = $("#toTop");
    if (!btn) return;
    window.addEventListener("scroll", function () {
      btn.classList.toggle("show", window.scrollY > 500);
    });
    btn.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }

  /* Scroll reveal + counters via IntersectionObserver */
  var io;
  function revealScan() {
    if (!("IntersectionObserver" in window)) { $all(".reveal").forEach(function (r) { r.classList.add("in"); }); return; }
    if (!io) {
      io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add("in"); if (en.target.hasAttribute("data-count")) countUp(en.target); io.unobserve(en.target); }
        });
      }, { threshold: 0.14 });
    }
    $all(".reveal:not(.in), [data-count]").forEach(function (r) { io.observe(r); });
  }
  function countUp(node) {
    var target = parseInt(node.getAttribute("data-count"), 10) || 0, start = null, dur = 1400;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      node.textContent = Math.floor((0.5 - Math.cos(Math.PI * p) / 2) * target);
      if (p < 1) requestAnimationFrame(step); else node.textContent = target;
    }
    requestAnimationFrame(step);
  }

  /* ==================================================================== */
  /*  PAGE RENDER                                                          */
  /* ==================================================================== */
  function renderPage() {
    buildHeader();
    buildFooter();
    renderChrome();
    // dynamic sections (each no-ops if its container is absent on the page)
    renderDivisions();
    renderServices();
    if ($('[data-render="projects"]')) {
      var lim = $('[data-render="projects"]').getAttribute("data-limit");
      renderProjects(lim ? parseInt(lim, 10) : null);
    }
    renderProjectFilters();
    if ($('[data-render="switchgear"]')) {
      var sl = $('[data-render="switchgear"]').getAttribute("data-limit");
      renderSwitchgear(sl ? parseInt(sl, 10) : null);
    }
    renderSwitchgearSpecs();
    renderProcess();
    if ($('[data-render="meters"]')) {
      var ml = $('[data-render="meters"]').getAttribute("data-limit");
      renderMeters(ml ? parseInt(ml, 10) : null);
    }
    renderMeterTech();
    renderMeterDocs();
    renderMeterCompare();
    renderStats();
    renderAdvantages();
    renderValues();
    renderHistory();
    renderCerts();
    renderPartners();
    renderClients();
    renderNews();
    renderAllProducts();
    // galleries
    renderGallery("galleryConstr", [
      { hy:"Ենթակայան 220 կՎ", ru:"Подстанция 220 кВ", en:"220 kV substation" },
      { hy:"Մալուխային գծեր", ru:"Кабельные линии", en:"Cable lines" },
      { hy:"ՌՊԱ վահանակներ", ru:"Панели РЗА", en:"RPA panels" },
      { hy:"Օդային գծեր", ru:"Воздушные линии", en:"Overhead lines" },
      { hy:"Հողանցում", ru:"Заземление", en:"Earthing" },
      { hy:"Փորձարկումներ", ru:"Испытания", en:"Testing" }
    ], "b", "construction");
    renderGallery("gallerySwitch", [
      { hy:"KD-2 մոդուլ", ru:"Модуль KD-2", en:"KD-2 module" },
      { hy:"KDW ԿՌՈՒ", ru:"КРУ KDW", en:"KDW switchgear" },
      { hy:"КСО-КТИС", ru:"КСО-КТИС", en:"KSO-KTiS" },
      { hy:"KD-3 SF6", ru:"KD-3 элегаз", en:"KD-3 SF6" },
      { hy:"ԲԿՏԵ", ru:"БКТП", en:"BKTP" },
      { hy:"Արտադրական հատված", ru:"Производство", en:"Production floor" }
    ], "c", "switchgear");
    renderGallery("galleryMeters", [
      { hy:"МИРТЕК-12", ru:"МИРТЕК-12", en:"MIRTEK-12" },
      { hy:"МИРТЕК-32", ru:"МИРТЕК-32", en:"MIRTEK-32" },
      { hy:"МИРТЕК-135", ru:"МИРТЕК-135", en:"MIRTEK-135" },
      { hy:"Կապի մոդուլ", ru:"Модуль связи", en:"Comm module" }
    ], "d", "meters");

    applyI18n(document);
    revealScan();
    // one-time wiring
    if (!document.body._wired) {
      wireLang(); wireBurger(); wireFilters(); wireSearch(); wireForm(); wireScrollTop(); wireModal();
      window.addEventListener("hashchange", openModuleFromHash);
      document.body._wired = true;
      openModuleFromHash();  // honour a #module=CODE deep link on first load
    }
    // keep an open module modal in sync with the current language
    if (openModuleCode) {
      var openIt = findModule(openModuleCode);
      var host = $("#kmodal .kmodal__content");
      if (openIt && host) host.innerHTML = moduleDetailHTML(openIt);
      else closeModule();
    }
  }

  /* Boot: load live content from the CMS first (if available), then render.
     On any failure we still render with the bundled fallback data. */
  function boot() {
    var loader = (window.KASKAD && typeof window.KASKAD.load === "function")
      ? window.KASKAD.load()
      : Promise.resolve(false);
    loader.then(renderPage, renderPage);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
