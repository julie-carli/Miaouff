/**
 * Cookie consent management (single source of truth).
 *
 * Stores the user's choice in localStorage under one key and loads Google
 * Analytics only after explicit consent. The same API is reused by the cookie
 * policy page, so the banner and the policy page always stay in sync.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "miaouff_cookie_consent";
  var CONSENT_VERSION = 1;

  function readConsent() {
    try {
      var data = JSON.parse(window.localStorage.getItem(STORAGE_KEY));
      return data && data.version === CONSENT_VERSION ? data : null;
    } catch (e) {
      return null;
    }
  }

  function saveConsent(analyticsAllowed) {
    var data = {
      version: CONSENT_VERSION,
      analytics: !!analyticsAllowed,
      date: new Date().toISOString(),
    };
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      /* localStorage unavailable: consent simply won't be remembered */
    }
  }

  function loadAnalytics() {
    var id = window.GA_MEASUREMENT_ID;
    if (!id || window.__miaouffGaLoaded) return;
    window.__miaouffGaLoaded = true;

    var script = document.createElement("script");
    script.async = true;
    script.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag() {
      window.dataLayer.push(arguments);
    }
    window.gtag = gtag;
    gtag("js", new Date());
    gtag("config", id, { anonymize_ip: true });
  }

  function applyConsent(analyticsAllowed) {
    saveConsent(analyticsAllowed);
    if (analyticsAllowed) loadAnalytics();
  }

  // Public API, available synchronously and reused by the cookie policy page.
  window.MiaouffCookies = {
    getConsent: readConsent,
    setAnalytics: applyConsent,
    open: function () {
      var banner = document.getElementById("cookie-banner");
      if (banner) banner.hidden = false;
    },
  };

  function show(el) {
    if (el) el.hidden = false;
  }
  function hide(el) {
    if (el) el.hidden = true;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var banner = document.getElementById("cookie-banner");
    var prefs = document.getElementById("cookie-prefs");
    var analyticsToggle = document.getElementById("cookie-analytics-toggle");
    if (!banner) return;

    function close(analyticsAllowed) {
      applyConsent(analyticsAllowed);
      hide(banner);
      hide(prefs);
    }

    function handleAction(action) {
      if (action === "accept") close(true);
      else if (action === "refuse") close(false);
      else if (action === "save") close(analyticsToggle && analyticsToggle.checked);
      else if (action === "customize") {
        hide(banner);
        show(prefs);
      }
    }

    document.querySelectorAll("[data-cookie-action]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        handleAction(btn.getAttribute("data-cookie-action"));
      });
    });

    var consent = readConsent();
    if (!consent) {
      show(banner);
    } else if (consent.analytics) {
      loadAnalytics();
    }
  });
})();
