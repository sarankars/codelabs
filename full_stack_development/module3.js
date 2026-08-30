(() => {
  const titles = JSON.parse(document.body.dataset.steps || '[]');
  const views = [...document.querySelectorAll('.view')];
  const nav = document.querySelector('#stepNav');
  const progressBar = document.querySelector('#progressBar');
  const progressText = document.querySelector('#progressText');
  const previous = document.querySelector('#previous');
  const next = document.querySelector('#next');
  const mobileTitle = document.querySelector('#mobileTitle');
  let current = 0;

  nav.innerHTML = titles.map((title, index) =>
    `<button class="step-link" type="button" data-go="${index}"><span class="step-num">${String(index + 1).padStart(2, '0')}</span><span>${title}</span></button>`
  ).join('');

  function fromHash() {
    const step = Number(location.hash.replace('#step-', ''));
    return step >= 1 && step <= views.length ? step - 1 : 0;
  }

  function render(push = true) {
    views.forEach((view, index) => view.classList.toggle('active', index === current));
    document.querySelectorAll('.step-link').forEach((button, index) => {
      button.classList.toggle('active', index === current);
      button.setAttribute('aria-current', index === current ? 'step' : 'false');
    });
    const percent = Math.round((current + 1) / views.length * 100);
    progressBar.style.width = `${percent}%`;
    progressText.textContent = `${percent}%`;
    previous.disabled = current === 0;
    next.disabled = current === views.length - 1;
    mobileTitle.textContent = titles[current];
    document.title = `${titles[current]} · Servlets and JSP Codelab`;
    if (push) history.pushState(null, '', `#step-${current + 1}`);
    window.scrollTo({ top: 0, behavior: 'auto' });
    document.querySelector('#sidebar').classList.remove('open');
  }

  function go(index) {
    if (index < 0 || index >= views.length) return;
    current = index;
    render();
  }

  nav.addEventListener('click', event => {
    const button = event.target.closest('[data-go]');
    if (button) go(Number(button.dataset.go));
  });
  previous.addEventListener('click', () => go(current - 1));
  next.addEventListener('click', () => go(current + 1));
  document.querySelector('#menuButton').addEventListener('click', event => {
    const open = document.querySelector('#sidebar').classList.toggle('open');
    event.currentTarget.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('click', event => {
    const option = event.target.closest('.option');
    if (option) {
      const quiz = option.closest('.quiz');
      const options = [...quiz.querySelectorAll('.option')];
      const answer = Number(quiz.dataset.answer);
      options.forEach((item, index) => {
        item.disabled = true;
        item.classList.toggle('correct', index === answer);
      });
      if (options.indexOf(option) !== answer) option.classList.add('wrong');
      quiz.querySelector('.feedback').classList.add('show');
    }
    const copy = event.target.closest('[data-copy]');
    if (copy) {
      const code = document.querySelector(copy.dataset.copy).innerText;
      navigator.clipboard.writeText(code).then(() => {
        const original = copy.textContent;
        copy.textContent = 'Copied';
        setTimeout(() => { copy.textContent = original; }, 1200);
      });
    }
  });
  addEventListener('popstate', () => { current = fromHash(); render(false); });
  current = fromHash();
  render(false);
})();
