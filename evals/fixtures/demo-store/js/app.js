// Theme toggle (sets the attribute on <body>)
document.getElementById('theme-toggle')?.addEventListener('click', function () {
  var b = document.body;
  b.setAttribute('data-theme', b.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
});

// Sale countdown
(function () {
  var el = document.getElementById('countdown');
  if (!el) return;
  var seconds = 2 * 60 * 60;
  setInterval(function () {
    seconds = seconds > 0 ? seconds - 1 : 2 * 60 * 60;
    var h = String(Math.floor(seconds / 3600)).padStart(2, '0');
    var m = String(Math.floor(seconds % 3600 / 60)).padStart(2, '0');
    var s = String(seconds % 60).padStart(2, '0');
    el.textContent = h + ':' + m + ':' + s;
  }, 1000);
})();

// Cart: the server adds the item, then the cart page reloads
function addToCart(sku) {
  window.location.href = '/cart.html?add=' + sku;
}

function openModal() { document.getElementById('backdrop').style.display = 'block'; document.getElementById('terms').style.display = 'block'; }
function closeModal() { document.getElementById('backdrop').style.display = 'none'; document.getElementById('terms').style.display = 'none'; }
