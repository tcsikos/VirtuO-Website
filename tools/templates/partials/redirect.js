<script>
/* Csak a gyökér (angol) oldalakon: első látogatáskor a böngésző nyelvére irányít. */
(function () {
  try {
    var OK = { en: 1, hu: 1, de: 1, fr: 1, es: 1, nb: 1, sv: 1, pl: 1, fi: 1, cs: 1 };
    var t = null, c = null;
    try { c = localStorage.getItem('virtuo-lang-choice'); } catch (e) {}
    if (c && OK[c]) { t = c; }
    else {
      var l = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
      for (var i = 0; i < l.length; i++) {
        var p = String(l[i] || '').toLowerCase().split('-')[0];
        if (p === 'no' || p === 'nn') p = 'nb';
        if (OK[p]) { t = p; break; }
      }
    }
    if (t && t !== 'en') {
      var f = location.pathname.replace(/^.*\//, '');
      if (f && f.indexOf('.') < 0) f += '.html';
      location.replace('/' + t + '/' + f + location.search + location.hash);
    }
  } catch (e) {}
})();
</script>
