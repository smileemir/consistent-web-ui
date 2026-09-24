// Tidewell: shared behaviour for every page
(function () {
  "use strict";

  var root = document.documentElement;
  var STORAGE_KEY = "tidewell-theme";

  function applyTheme(theme) {
    if (theme === "dark" || theme === "light") root.setAttribute("data-theme", theme);
    else root.removeAttribute("data-theme");
  }

  var saved = null;
  try { saved = localStorage.getItem(STORAGE_KEY); } catch (e) { /* storage blocked */ }
  if (!saved && window.matchMedia("(prefers-color-scheme: dark)").matches) saved = "dark";
  applyTheme(saved);

  var toggle = document.getElementById("theme-toggle");
  if (toggle) {
    var isDark = root.getAttribute("data-theme") === "dark";
    toggle.setAttribute("aria-pressed", String(isDark));
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      applyTheme(next);
      toggle.setAttribute("aria-pressed", String(next === "dark"));
      try { localStorage.setItem(STORAGE_KEY, next); } catch (e) { /* storage blocked */ }
    });
  }

  var toastTimer = null;
  window.showToast = function (message) {
    var toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = message;
    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.hidden = true; }, 5000);
  };
})();
