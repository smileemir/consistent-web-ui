// Tidewell: settings page behaviour
function toggleDigest(el) {
  el.classList.toggle("on");
  document.getElementById("weekly-digest").value = el.classList.contains("on") ? "true" : "false";
}

function flashSaved(text) {
  var toast = document.getElementById("settings-toast");
  toast.textContent = text;
  toast.style.display = "block";
  setTimeout(function () { toast.style.display = "none"; }, 2500);
}

function copyKey() {
  var key = document.getElementById("api-key").value;
  navigator.clipboard.writeText(key).then(function () { flashSaved("Copied!"); });
}

function regenerateKey() {
  fetch("/api/api-key/regenerate", { method: "POST" })
    .then(function (response) { return response.json(); })
    .then(function (data) {
      document.getElementById("api-key").value = data.key;
      flashSaved("New key created");
    });
}

function deleteWorkspace() {
  fetch("/api/workspace", { method: "DELETE" }).then(function () {
    flashSaved("Workspace deleted");
  });
}

document.getElementById("settings-form").addEventListener("submit", function (event) {
  event.preventDefault();
  var payload = {
    workspaceName: document.getElementById("workspace-name").value,
    timezone: document.getElementById("timezone").value,
    dataRetentionDays: Number(document.getElementById("retention").value),
    weeklyDigest: document.getElementById("weekly-digest").value === "true",
    require2fa: document.getElementById("require-2fa").checked
  };
  fetch("/api/settings", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  }).then(function (response) {
    if (!response.ok) throw new Error(String(response.status));
    flashSaved("Saved!");
  }).catch(function () {
    flashSaved("Error");
  });
});
