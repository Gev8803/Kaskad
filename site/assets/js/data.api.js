/* ============================================================================
 * KASKAD GROUP — LIVE CONTENT LOADER
 * Fetches /api/content/ from the CMS backend and overwrites the global
 * window.DATA / window.I18N objects with live, editable content.
 *
 * Progressive enhancement: if the API is unreachable (e.g. the page is opened
 * directly over file://, or served without the backend), the statically loaded
 * data.*.js / i18n.js bundles remain in place and the site works unchanged.
 *
 * Must be loaded AFTER the data.*.js + i18n.js fallbacks and BEFORE app.js.
 * ==========================================================================*/
(function () {
  "use strict";

  // Use the same origin in production so HTTPS pages fetch the API securely.
  // For local files or a separate local dev server, use the Django backend on
  // port 8000 instead.
  // Override for other hosts, e.g.
  //   <script>window.KASKAD_API_BASE="https://cms.example.com/api"</script>
  var BACKEND_PORT = "8000";
  var backendHost = location.hostname || "127.0.0.1";
  var servedByBackend =
    location.protocol !== "file:" &&
    (!location.port || location.port === "80" || location.port === "443" || location.port === BACKEND_PORT);
  var DEFAULT_BASE = location.protocol !== "file:" && servedByBackend
    ? "/api"
    : "http://" + backendHost + ":" + BACKEND_PORT + "/api";
  var API_BASE = (window.KASKAD_API_BASE || DEFAULT_BASE).replace(/\/+$/, "");

  window.KASKAD = window.KASKAD || {};
  window.KASKAD.apiBase = API_BASE;
  window.KASKAD.live = false;

  function applyContent(data) {
    if (!data || typeof data !== "object") return;
    window.DATA = window.DATA || {};
    if (data.company) window.DATA.company = data.company;
    if (data.construction) window.DATA.construction = data.construction;
    if (data.switchgear) window.DATA.switchgear = data.switchgear;
    if (data.meters) window.DATA.meters = data.meters;
    if (data.news) window.DATA.news = data.news;
    if (data.galleries) window.DATA.galleries = data.galleries;
    if (data.i18n && data.i18n.hy && data.i18n.ru && data.i18n.en) {
      window.I18N = data.i18n;
    }
    window.KASKAD.live = true;
  }

  /* Returns a Promise<boolean> — true if live content was loaded.
     Always attempts the API (even over file://); if it is unreachable we keep
     the bundled fallback data so the site still works offline. */
  window.KASKAD.load = function () {
    if (typeof fetch !== "function") {
      return Promise.resolve(false); // very old browser: keep bundled fallback
    }
    return fetch(API_BASE + "/content/", { headers: { Accept: "application/json" }, cache: "no-store" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (d) { applyContent(d); return true; })
      .catch(function () { return false; }); // silent fallback
  };

  /* POST the contact form; resolves true on success. */
  window.KASKAD.sendContact = function (payload) {
    if (typeof fetch !== "function") {
      return Promise.resolve(false);
    }
    return fetch(API_BASE + "/contact/", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload),
    })
      .then(function (r) { return r.ok; })
      .catch(function () { return false; });
  };
})();
