/**
 * Resolve the Flask API base URL for local and deployed frontends.
 *
 * Priority:
 *   1. ?api= / ?api_base= / ?API_BASE_URL= query param
 *   2. <meta name="api-base-url" content="..."> (non-empty)
 *   3. window.__API_BASE_URL__ or a pre-set window.API_BASE_URL
 *   4. localStorage key API_BASE_URL
 *   5. Smart default:
 *        - localhost/127.0.0.1 on port 3000 (static file server) → http://localhost:5000
 *        - otherwise → "" (same origin; Flask serves UI + API on Railway/Render)
 *
 * Split deploy (Vercel UI + separate API): open
 *   https://YOUR-VERCEL-URL/?api=https://YOUR-API-HOST
 */
(function resolveApiBaseUrl() {
  function normalize(url) {
    if (url == null || typeof url !== "string") return null;
    var trimmed = url.trim().replace(/\/+$/, "");
    // Empty string is a valid same-origin choice — only treat whitespace-only as missing.
    if (url.trim() === "") return null;
    return trimmed;
  }

  function smartDefault() {
    var host = window.location.hostname;
    var port = window.location.port;
    var isLocal = host === "localhost" || host === "127.0.0.1";
    if (isLocal && (port === "3000" || port === "5500" || port === "8080")) {
      return "http://localhost:5000";
    }
    // Flask single-deploy (any host, or localhost:5000) → same origin
    return "";
  }

  var params = new URLSearchParams(window.location.search);
  var fromQuery = normalize(
    params.get("api") || params.get("api_base") || params.get("API_BASE_URL")
  );

  var meta = document.querySelector('meta[name="api-base-url"]');
  var fromMeta = normalize(meta && meta.getAttribute("content"));

  var fromInject = null;
  if (typeof window.__API_BASE_URL__ === "string") {
    fromInject = normalize(window.__API_BASE_URL__);
  } else if (typeof window.API_BASE_URL === "string" && window.API_BASE_URL.trim() !== "") {
    fromInject = normalize(window.API_BASE_URL);
  }

  var fromStorage = null;
  try {
    fromStorage = normalize(window.localStorage.getItem("API_BASE_URL"));
  } catch (e) {
    /* private mode / blocked storage */
  }

  var resolved =
    fromQuery != null
      ? fromQuery
      : fromMeta != null
        ? fromMeta
        : fromInject != null
          ? fromInject
          : fromStorage != null
            ? fromStorage
            : smartDefault();

  window.API_BASE_URL = resolved;

  if (fromQuery != null) {
    try {
      window.localStorage.setItem("API_BASE_URL", fromQuery);
    } catch (e) {
      /* ignore */
    }
  }
})();
