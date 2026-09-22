(() => {
  const dialog = document.querySelector('.lightbox');
  if (!dialog) return;
  const buttons = [...document.querySelectorAll('.article .photo__open')];
  let current = -1;
  let trigger = null;
  const image = dialog.querySelector('img');
  const caption = dialog.querySelector('figcaption');
  function show(index) {
    current = (index + buttons.length) % buttons.length;
    const photo = buttons[current].closest('figure');
    const source = photo.querySelector('img');
    image.src = source.src;
    image.alt = source.alt;
    caption.textContent = photo.querySelector('figcaption')?.textContent || '';
  }
  function close() {
    dialog.hidden = true;
    document.body.classList.remove('dialog-open');
    image.removeAttribute('src');
    trigger?.focus();
  }
  buttons.forEach((button, i) => button.addEventListener('click', () => {
    trigger = button;
    show(i);
    dialog.hidden = false;
    document.body.classList.add('dialog-open');
    dialog.querySelector('[data-close]').focus();
  }));
  dialog.querySelector('[data-close]').addEventListener('click', close);
  dialog.querySelector('[data-prev]').addEventListener('click', () => show(current - 1));
  dialog.querySelector('[data-next]').addEventListener('click', () => show(current + 1));
  dialog.addEventListener('click', event => { if (event.target === dialog) close(); });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); close(); }
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(current - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(current + 1); }
    if (event.key === 'Tab') {
      const controls = [...dialog.querySelectorAll('button')];
      const next = controls.indexOf(document.activeElement) + (event.shiftKey ? -1 : 1);
      if (next < 0 || next >= controls.length) { event.preventDefault(); controls[(next + controls.length) % controls.length].focus(); }
    }
  });
})();
