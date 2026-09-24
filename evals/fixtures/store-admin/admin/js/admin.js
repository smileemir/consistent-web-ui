// Kestrel Supply admin: page behaviour
(function () {
  "use strict";

  var toast = document.getElementById("toast");
  var toastTimer = null;

  function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.hidden = true; }, 5000);
  }

  // Products: sort, search and status filter
  var table = document.getElementById("products");
  if (table) {
    var body = table.tBodies[0];

    table.querySelectorAll("button.sort").forEach(function (button) {
      button.addEventListener("click", function () {
        var th = button.closest("th");
        var index = Array.prototype.indexOf.call(th.parentNode.children, th);
        var direction = th.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        table.querySelectorAll("th[aria-sort]").forEach(function (h) { h.removeAttribute("aria-sort"); });
        th.setAttribute("aria-sort", direction);
        var rows = Array.prototype.slice.call(body.rows);
        rows.sort(function (a, b) {
          var x = parseFloat(a.cells[index].dataset.value);
          var y = parseFloat(b.cells[index].dataset.value);
          return direction === "ascending" ? x - y : y - x;
        });
        rows.forEach(function (row) { body.appendChild(row); });
      });
    });

    var search = document.getElementById("product-search");
    var status = document.getElementById("status-filter");

    function applyFilters() {
      var query = search.value.trim().toLowerCase();
      var wanted = status.value;
      Array.prototype.forEach.call(body.rows, function (row) {
        var statusOk = wanted ? row.dataset.status === wanted : row.dataset.status !== "Archived";
        var textOk = !query || row.dataset.search.indexOf(query) !== -1;
        row.hidden = !(statusOk && textOk);
      });
    }

    search.addEventListener("input", applyFilters);
    status.addEventListener("change", applyFilters);
    applyFilters();
  }

  // Settings: save, rebuild search index, reset to defaults
  var form = document.getElementById("settings-form");
  if (form) {
    var saveState = document.getElementById("save-state");

    form.addEventListener("input", function () { saveState.textContent = "Unsaved changes"; });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = {};
      new FormData(form).forEach(function (value, key) { data[key] = value; });
      form.querySelectorAll('input[type="checkbox"]').forEach(function (box) { data[box.name] = box.checked; });
      saveState.textContent = "Saving…";
      fetch("/api/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      }).then(function (response) {
        if (!response.ok) throw new Error(String(response.status));
        saveState.textContent = "All changes saved";
        showToast("Changes saved");
      }).catch(function () {
        saveState.textContent = "Not saved";
        showToast("Couldn't save your changes. Check your connection and try again.");
      });
    });

    document.getElementById("rebuild-index").addEventListener("click", function () {
      fetch("/api/search/rebuild", { method: "POST" }).then(function (response) {
        if (!response.ok) throw new Error(String(response.status));
        showToast("Search index rebuild started.");
      }).catch(function () {
        showToast("Couldn't start the rebuild. Try again in a moment.");
      });
    });

    var dialog = document.getElementById("reset-dialog");
    document.getElementById("reset-defaults").addEventListener("click", function () {
      dialog.returnValue = "";
      dialog.showModal();
    });
    dialog.addEventListener("close", function () {
      if (dialog.returnValue !== "reset") return;
      fetch("/api/settings/reset", { method: "POST" }).then(function (response) {
        if (!response.ok) throw new Error(String(response.status));
        showToast("Settings reset to defaults. Reload to see them.");
      }).catch(function () {
        showToast("Couldn't reset the settings. Try again in a moment.");
      });
    });
  }
})();
