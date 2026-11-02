/* ═══════════════════════════════════════════════════
   ЮвелирКар — основной JavaScript
   ═══════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. Шапка: скрывается при прокрутке вниз ── */
  const header = document.getElementById('site-header');
  let lastScrollY = window.scrollY;

  window.addEventListener('scroll', () => {
    const currentScrollY = window.scrollY;
    if (currentScrollY > lastScrollY && currentScrollY > 80) {
      header.classList.add('hidden');
    } else {
      header.classList.remove('hidden');
    }
    lastScrollY = currentScrollY;
  }, { passive: true });


  /* ── 2. Мобильное меню ── */
  const navToggle = document.getElementById('nav-toggle');
  const mobileMenu = document.getElementById('nav-mobile-menu');

  navToggle?.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });

  // Закрыть меню при клике на ссылку
  mobileMenu?.querySelectorAll('.nav-mobile-link').forEach(link => {
    link.addEventListener('click', () => mobileMenu.classList.remove('open'));
  });


  /* ── 3. Подсветка активного пункта меню ── */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        navLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
        });
      }
    });
  }, { rootMargin: '-30% 0px -60% 0px' });

  sections.forEach(s => observer.observe(s));


  /* ── 4. Модальное окно ── */
  const overlay  = document.getElementById('modal-overlay');
  const modal    = document.getElementById('modal');
  const fabBtn   = document.getElementById('fab-btn');
  const closeBtn = document.getElementById('modal-close');

  const screenChoose  = document.getElementById('modal-screen-choose');
  const screenContact = document.getElementById('modal-screen-contact');
  const screenForm    = document.getElementById('modal-screen-form');

  const btnContact    = document.getElementById('btn-contact');
  const btnForm       = document.getElementById('btn-form');
  const btnBackContact = document.getElementById('btn-back-contact');
  const btnBackForm   = document.getElementById('btn-back-form');

  function openModal(screen = 'choose') {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    showScreen(screen);
  }

  function closeModal() {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  function showScreen(name) {
    screenChoose.classList.add('hidden');
    screenContact.classList.add('hidden');
    screenForm.classList.add('hidden');
    if (name === 'choose') screenChoose.classList.remove('hidden');
    if (name === 'contact') screenContact.classList.remove('hidden');
    if (name === 'form') screenForm.classList.remove('hidden');
  }

  // Открыть по FAB
  fabBtn?.addEventListener('click', () => openModal('choose'));

  // Открыть по кнопкам с классом fab-trigger
  document.querySelectorAll('.fab-trigger').forEach(btn => {
    btn.addEventListener('click', () => openModal('choose'));
  });

  // Закрыть
  closeBtn?.addEventListener('click', closeModal);
  overlay?.addEventListener('click', e => { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

  // Переходы между экранами
  btnContact?.addEventListener('click', () => showScreen('contact'));
  btnForm?.addEventListener('click', () => showScreen('form'));
  btnBackContact?.addEventListener('click', () => showScreen('choose'));
  btnBackForm?.addEventListener('click', () => {
    showScreen('choose');
    resetForm();
  });


  /* ── 5. Форма заявки ── */
  const form       = document.getElementById('app-form');
  const submitBtn  = document.getElementById('form-submit-btn');
  const statusDiv  = document.getElementById('form-status');

  const phoneInput = document.getElementById('f-phone');
  const makeInput  = document.getElementById('f-make');
  const modelInput = document.getElementById('f-model');

  function setError(input, errorId, msg) {
    const el = document.getElementById(errorId);
    if (el) el.textContent = msg;
    if (msg) input.classList.add('invalid');
    else input.classList.remove('invalid');
  }

  function validatePhone(val) {
    const cleaned = val.replace(/[\s\-\(\)\+]/g, '');
    return /^\d{10,15}$/.test(cleaned);
  }

  function validateRequired(val) {
    return val.trim().length > 0;
  }

  function resetForm() {
    form?.reset();
    statusDiv.textContent = '';
    statusDiv.className = 'form-status';
    submitBtn.disabled = false;
    [phoneInput, makeInput, modelInput].forEach(inp => inp?.classList.remove('invalid'));
    ['error-phone', 'error-make', 'error-model'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.textContent = '';
    });
  }

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Валидация
    let valid = true;

    if (!validatePhone(phoneInput.value)) {
      setError(phoneInput, 'error-phone', 'Введите корректный номер телефона');
      valid = false;
    } else {
      setError(phoneInput, 'error-phone', '');
    }

    if (!validateRequired(makeInput.value)) {
      setError(makeInput, 'error-make', 'Укажите марку автомобиля');
      valid = false;
    } else {
      setError(makeInput, 'error-make', '');
    }

    if (!validateRequired(modelInput.value)) {
      setError(modelInput, 'error-model', 'Укажите модель автомобиля');
      valid = false;
    } else {
      setError(modelInput, 'error-model', '');
    }

    if (!valid) return;

    // Отправка
    submitBtn.disabled = true;
    submitBtn.textContent = 'Отправляем...';
    statusDiv.textContent = '';
    statusDiv.className = 'form-status';

    const data = {
      name:      document.getElementById('f-name').value.trim(),
      phone:     phoneInput.value.trim(),
      car_make:  makeInput.value.trim(),
      car_model: modelInput.value.trim(),
      service:   document.getElementById('f-service').value,
    };

    try {
      const resp = await fetch('/api/application', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const result = await resp.json();

      if (resp.ok && result.ok) {
        statusDiv.textContent = result.message || 'Заявка отправлена! Мы перезвоним вам в ближайшее время.';
        statusDiv.className = 'form-status success';
        form.reset();
        submitBtn.textContent = 'Отправить заявку';
        // Кнопку не разблокируем — предотвращаем повторную отправку
      } else {
        statusDiv.textContent = result.detail || 'Произошла ошибка. Пожалуйста, позвоните нам.';
        statusDiv.className = 'form-status error';
        submitBtn.disabled = false;
        submitBtn.textContent = 'Попробовать снова';
      }
    } catch (err) {
      statusDiv.textContent = 'Нет соединения с сервером. Пожалуйста, позвоните нам.';
      statusDiv.className = 'form-status error';
      submitBtn.disabled = false;
      submitBtn.textContent = 'Попробовать снова';
    }
  });


  /* ── 6. Плавный скролл для якорных ссылок ── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href').slice(1);
      const target = document.getElementById(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
