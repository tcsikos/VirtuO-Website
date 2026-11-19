<script>
(function () {
  var box = document.getElementById('lp'), btn = document.getElementById('lp-btn');
  if (!box || !btn) return;
  var links = box.querySelectorAll('.lp-list a');
  function isOpen() { return box.classList.contains('open'); }
  function set(o) { box.classList.toggle('open', o); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); }
  btn.addEventListener('click', function () { set(!isOpen()); });
  document.addEventListener('click', function (e) { if (!box.contains(e.target)) set(false); });
  box.addEventListener('focusout', function (e) { if (e.relatedTarget && !box.contains(e.relatedTarget)) set(false); });
  box.addEventListener('keydown', function (e) {
    var k = e.key, i = Array.prototype.indexOf.call(links, document.activeElement);
    if (k === 'Escape' && isOpen()) { set(false); btn.focus(); e.preventDefault(); }
    else if (k === 'ArrowDown') { e.preventDefault(); set(true); links[(i + 1) % links.length].focus(); }
    else if (k === 'ArrowUp' && isOpen()) { e.preventDefault(); links[(i < 0 ? 0 : i + links.length - 1) % links.length].focus(); }
  });
  Array.prototype.forEach.call(links, function (a) {
    a.addEventListener('click', function () {
      try { localStorage.setItem('virtuo-lang-choice', a.getAttribute('data-lang')); } catch (e) {}
    });
  });
})();
</script>
