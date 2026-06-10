/**
 * Cookie consent management.
 *
 * Stores the user's choice in localStorage and loads Google Analytics only
 * after explicit consent. No analytics script is injected before the user
 * accepts the "audience measurement" category (CNIL-compliant).
 */
(function () {
  "use strict";

  var STORAGE_KEY = "miaouff_cookie_consent";
  var CONSENT_VERSION = 1;

  function readConsent() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
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
    // anonymize_ip keeps the audience measurement privacy-friendly.
    gtag("config", id, { anonymize_ip: true });
  }

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

    function applyAndClose(analyticsAllowed) {
      saveConsent(analyticsAllowed);
      hide(banner);
      hide(prefs);
      if (analyticsAllowed) loadAnalytics();
    }

    function handleAction(action) {
      switch (action) {
        case "accept":
          applyAndClose(true);
          break;
        case "refuse":
          applyAndClose(false);
          break;
        case "customize":
          hide(banner);
          show(prefs);
          break;
        case "save":
          applyAndClose(analyticsToggle && analyticsToggle.checked);
          break;
      }
    }

    document.querySelectorAll("[data-cookie-action]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        handleAction(btn.getAttribute("data-cookie-action"));
      });
    });

    // Footer entry point to reopen the banner at any time.
    var reopen = document.getElementById("open-cookie-settings");
    if (reopen) {
      reopen.addEventListener("click", function (e) {
        e.preventDefault();
        var current = readConsent();
        if (analyticsToggle) analyticsToggle.checked = !!(current && current.analytics);
        hide(prefs);
        show(banner);
      });
    }

    // Public hook so other scripts can reopen the settings if needed.
    window.MiaouffCookies = { open: function () { show(banner); } };

    var consent = readConsent();
    if (!consent) {
      show(banner);
    } else if (consent.analytics) {
      loadAnalytics();
    }
  });
})();
