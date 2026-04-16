const toggle = document.querySelector('.site-nav__toggle');
const menu = document.querySelector('.site-nav__list');
const i18n = window.SiteI18n;

function t(key, params) {
  return i18n && typeof i18n.t === 'function' ? i18n.t(key, params) : key;
}

if (i18n && typeof i18n.previewLocale === 'function') {
  const previewLocale = i18n.previewLocale();
  if (previewLocale) {
    document.documentElement.setAttribute('lang', previewLocale);
  }
}

if (toggle && menu) {
  toggle.addEventListener('click', () => {
    const isOpen = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
    toggle.textContent = isOpen ? t('nav.close') : t('nav.menu');
  });

  document.addEventListener('click', (event) => {
    if (!toggle.contains(event.target) && !menu.contains(event.target)) {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = t('nav.menu');
    }
  });

  menu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = t('nav.menu');
    });
  });
}

(function initScrollReveal() {
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.card, .sidebar-widget, .article-tpl__around, .article-tpl__practical, .article-tpl__gaps').forEach((el) => {
      el.classList.add('scroll-reveal--visible');
    });
    return;
  }

  const targets = document.querySelectorAll('.card, .sidebar-widget, .article-tpl__around, .article-tpl__practical, .article-tpl__gaps');
  if (!targets.length) return;

  targets.forEach((el) => el.classList.add('scroll-reveal'));

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('scroll-reveal--visible');
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px',
    }
  );

  targets.forEach((el) => observer.observe(el));
})();

(function initLightbox() {
  const galleryImages = document.querySelectorAll('.article-gallery figure img');
  if (!galleryImages.length) return;

  const overlay = document.createElement('div');
  overlay.className = 'lightbox';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', t('overlay.image.aria'));
  overlay.setAttribute('hidden', '');
  overlay.innerHTML = `
    <button class="lightbox__close" aria-label="${t('overlay.close')}">&times;</button>
    <figure class="lightbox__figure">
      <img class="lightbox__img" src="" alt="">
      <figcaption class="lightbox__caption"></figcaption>
    </figure>
  `;

  document.body.appendChild(overlay);

  const lightboxImg = overlay.querySelector('.lightbox__img');
  const lightboxCaption = overlay.querySelector('.lightbox__caption');
  const closeBtn = overlay.querySelector('.lightbox__close');
  let previousFocus = null;

  function open(img) {
    previousFocus = document.activeElement;
    lightboxImg.src = img.src;
    lightboxImg.alt = img.alt;
    lightboxCaption.textContent = img.closest('figure')?.querySelector('figcaption')?.textContent ?? '';
    overlay.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function close() {
    overlay.setAttribute('hidden', '');
    document.body.style.overflow = '';
    lightboxImg.src = '';
    if (previousFocus) previousFocus.focus();
  }

  galleryImages.forEach((img) => {
    img.setAttribute('tabindex', '0');
    img.setAttribute('role', 'button');
    img.setAttribute('aria-haspopup', 'dialog');
    img.addEventListener('click', () => open(img));
    img.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        open(img);
      }
    });
  });

  closeBtn.addEventListener('click', close);

  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) close();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !overlay.hasAttribute('hidden')) close();
  });

  overlay.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab') return;
    const focusable = overlay.querySelectorAll('button, [href], input, [tabindex]:not([tabindex="-1"])');
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
})();
