// theme.js - mode toggles
(function() {
  var html = document.documentElement;

  // theme mode (light/dark)
  var themeMode = localStorage.getItem('theme-mode') || 'light';
  html.setAttribute('data-theme-mode', themeMode);

  // density mode (compact/comfortable)
  var density = localStorage.getItem('density') || 'compact';
  if (density === 'comfortable') html.setAttribute('data-density', 'comfortable');

  // width mode (narrow/wide) - default wide
  var width = localStorage.getItem('width') || 'wide';
  if (width === 'wide') html.setAttribute('data-width', 'wide');

  // justify mode (on/off) - default on
  var justify = localStorage.getItem('justify') || 'on';
  if (justify === 'off') html.setAttribute('data-justify', 'off');

  window.toggleThemeMode = function() {
    var current = html.getAttribute('data-theme-mode');
    var next = (current === 'dark') ? 'light' : 'dark';
    html.setAttribute('data-theme-mode', next);
    localStorage.setItem('theme-mode', next);
    updateButtons();
  };

  window.toggleDensity = function() {
    var current = html.getAttribute('data-density');
    if (current === 'comfortable') {
      html.removeAttribute('data-density');
      localStorage.setItem('density', 'compact');
    } else {
      html.setAttribute('data-density', 'comfortable');
      localStorage.setItem('density', 'comfortable');
    }
    updateButtons();
  };

  window.toggleWidth = function() {
    var current = html.getAttribute('data-width');
    if (current === 'wide') {
      html.removeAttribute('data-width');
      localStorage.setItem('width', 'narrow');
    } else {
      html.setAttribute('data-width', 'wide');
      localStorage.setItem('width', 'wide');
    }
    updateButtons();
  };

  window.toggleJustify = function() {
    var current = html.getAttribute('data-justify');
    if (current === 'off') {
      html.removeAttribute('data-justify');
      localStorage.setItem('justify', 'on');
    } else {
      html.setAttribute('data-justify', 'off');
      localStorage.setItem('justify', 'off');
    }
    updateButtons();
  };

  function updateButtons() {
    var themeBtn = document.querySelector('.toggle-theme');
    var densityBtn = document.querySelector('.toggle-density');
    var widthBtn = document.querySelector('.toggle-width');
    var justifyBtn = document.querySelector('.toggle-justify');
    var collapseBtn = document.querySelector('.toggle-collapse');

    var isDark = html.getAttribute('data-theme-mode') === 'dark';
    var isComfy = html.getAttribute('data-density') === 'comfortable';
    var isWide = html.getAttribute('data-width') === 'wide';
    var isJustify = html.getAttribute('data-justify') !== 'off';

    if (themeBtn) {
      themeBtn.innerHTML = isDark ? '&#xf0594;' : '&#xf05a8;';
      themeBtn.title = isDark ? 'dark|toggle for light' : 'light|toggle for dark';
      if (isDark) themeBtn.classList.add('non-default');
      else themeBtn.classList.remove('non-default');
    }
    if (densityBtn) {
      densityBtn.innerHTML = isComfy ? '&#xf084d;' : '&#xf084f;';
      densityBtn.title = isComfy ? 'comfortable|toggle for compact' : 'compact|toggle for comfortable';
      if (isComfy) densityBtn.classList.add('non-default');
      else densityBtn.classList.remove('non-default');
    }
    if (widthBtn) {
      widthBtn.innerHTML = isWide ? '&#xf084e;' : '&#xf084c;';
      widthBtn.title = isWide ? 'wide|toggle for narrow' : 'narrow|toggle for wide';
      if (!isWide) widthBtn.classList.add('non-default');
      else widthBtn.classList.remove('non-default');
    }
    if (justifyBtn) {
      justifyBtn.innerHTML = isJustify ? '&#xf039;' : '&#xf036;';
      justifyBtn.title = isJustify ? 'justified|toggle for natural' : 'natural|toggle for justified';
      if (!isJustify) justifyBtn.classList.add('non-default');
      else justifyBtn.classList.remove('non-default');
    }
    if (collapseBtn) {
      collapseBtn.innerHTML = '&#xf151;';
      collapseBtn.title = 'expand|toggle sections';
    }
  }

  // collapse/expand all sections on any page (only in main content, not sidebar)
  window.toggleAllSections = function() {
    var headings = document.querySelectorAll('section h1, section h2, section h3, section h4, section h5, section h6, .content h1, .content h2, .content h3, .content h4, .content h5, .content h6');
    if (!headings.length) return;
    var collapsed = document.querySelectorAll('section .collapsed, .content .collapsed');
    var expand = collapsed.length > 0;
    var collapseBtn = document.querySelector('.toggle-collapse');
    headings.forEach(function(h) {
      var next = h.nextElementSibling;
      while (next && !next.matches('h1,h2,h3,h4,h5,h6')) {
        if (expand) next.classList.remove('collapsed');
        else next.classList.add('collapsed');
        next = next.nextElementSibling;
      }
    });
    // Update button icon
    if (collapseBtn) {
      if (expand) {
        collapseBtn.innerHTML = '&#xf151;';
        collapseBtn.title = 'expand|toggle sections';
      } else {
        collapseBtn.innerHTML = '&#xf150;';
        collapseBtn.title = 'collapse|toggle sections';
      }
    }
  };

  window.toggleSection = function(el) {
    var next = el.nextElementSibling;
    while (next && !next.matches('h1,h2,h3,h4,h5,h6')) {
      next.classList.toggle('collapsed');
      next = next.nextElementSibling;
    }
  };

  // make headings clickable on all pages
  document.addEventListener('DOMContentLoaded', function() {
    var headings = document.querySelectorAll('section h1, section h2, section h3, section h4, section h5, section h6, .content h1, .content h2, .content h3, .content h4, .content h5, .content h6');
    headings.forEach(function(h) {
      h.style.cursor = 'pointer';
      h.addEventListener('click', function(e) {
        if (!e.target.classList.contains('top-link')) toggleSection(this);
      });
    });
  });

  document.addEventListener('DOMContentLoaded', updateButtons);
})();
