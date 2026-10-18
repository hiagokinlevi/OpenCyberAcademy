(() => {
  document.getElementById('theme-toggle')?.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('open-cyber-academy-theme', next); } catch (_) { /* Private mode. */ }
    window.dispatchEvent(new Event('oca-theme-change'));
  });
  const revealAnswer = () => {
    if (/^#(?:answer-ex\d{3,4}|w\d+-answer-\d{2})$/.test(location.hash)) {
      const target = document.querySelector(location.hash);
      target?.closest('details')?.setAttribute('open', '');
    }
  };
  addEventListener('hashchange', revealAnswer);
  revealAnswer();

  const shareButton = document.getElementById('share-lesson');
  shareButton?.addEventListener('click', async () => {
    const url = shareButton.dataset.url;
    try {
      if (navigator.share) {
        await navigator.share({ title: shareButton.dataset.title, url });
        return;
      }
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(url);
      document.getElementById('share-status').textContent = shareButton.dataset.copied;
    } catch (error) {
      if (error.name !== 'AbortError') document.getElementById('share-status').textContent = shareButton.dataset.copyHint;
    }
  });

  // Record only signed-in study activity. Anonymous reading never reaches D1.
  const lesson = location.pathname.match(/^\/courses\/([a-z0-9-]+)\/([a-z0-9-]+)\/(lessons|chapters)\/([a-z]{2})\/(\d+)\/?$/);
  if (lesson) {
    const payload = { level: lesson[1], area: lesson[2], language: lesson[4], chapter: Number(lesson[5]) };
    const unitKind = lesson[3] === 'chapters' ? 'chapter' : 'lesson';
    const panel = document.querySelector('.progress-sidebar');
    const panelStatus = document.getElementById('progress-status');
    const signIn = document.getElementById('progress-signin');
    const dashboard = document.getElementById('progress-dashboard');
    const markButton = document.getElementById('mark-lesson-complete');
    const ui = lesson[4] === 'pt'
      ? { count: (n, total) => `${n} de ${total} aulas publicadas concluídas.`, unavailable: 'O progresso está indisponível agora.', marked: 'Aula concluída.', saved: 'Escolha salva na sua conta.', signIn: 'Entre para salvar sua escolha.', failed: 'Não foi possível salvar a escolha.', noChoice: 'Ainda não há questão revisada com cinco alternativas para este exercício. Consulte o enunciado e a resposta comentada.', choiceFailed: 'Não foi possível carregar as alternativas agora.', correct: 'Correto.', incorrect: 'Incorreto.', right: 'Resposta correta' }
      : lesson[4] === 'es'
      ? { count: (n, total) => `${n} de ${total} lecciones publicadas completadas.`, unavailable: 'El progreso no está disponible ahora.', marked: 'Lección completada.', saved: 'Elección guardada en tu cuenta.', signIn: 'Inicia sesión para guardar tu elección.', failed: 'No se pudo guardar la elección.', noChoice: 'Todavía no hay una pregunta revisada con cinco opciones para este ejercicio. Lee el enunciado y la respuesta desarrollada.', choiceFailed: 'No se pudieron cargar las opciones.', correct: 'Correcto.', incorrect: 'Incorrecto.', right: 'Respuesta correcta' }
      : { count: (n, total) => `${n} of ${total} published lessons completed.`, unavailable: 'Progress is unavailable right now.', marked: 'Lesson completed.', saved: 'Choice saved to your account.', signIn: 'Sign in to save your choice.', failed: 'Could not save the choice.', noChoice: 'A reviewed five-choice question is not available for this exercise yet. Read the prompt and worked answer.', choiceFailed: 'Could not load the choices now.', correct: 'Correct.', incorrect: 'Incorrect.', right: 'Correct answer' };
    const practiceCards = [...document.querySelectorAll('.exercise-attempt')];
    if (practiceCards.length) {
      const url = `/api/practice/${payload.level}/${payload.area}/${lesson[3]}/${payload.language}/${payload.chapter}`;
      fetch(url, { cache: 'no-store' }).then(async response => {
        if (!response.ok) {
          for (const card of practiceCards) {
            card.dataset.mode = 'written';
            card.querySelector('.exercise-attempt-status').textContent = response.status === 404 ? '' : ui.choiceFailed;
          }
          return;
        }
        const bank = await response.json();
        const questions = new Map(bank.questions.map(question => [question.exercise_id, question]));
        for (const card of practiceCards) {
          const question = questions.get(card.dataset.exerciseId);
          const status = card.querySelector('.exercise-attempt-status');
          if (!question) { card.dataset.mode = 'written'; status.textContent = ''; continue; }
          const fieldset = document.createElement('fieldset'); fieldset.className = 'exercise-choices';
          const legend = document.createElement('legend'); legend.textContent = question.prompt; fieldset.append(legend);
          for (const option of question.options) {
            const label = document.createElement('label');
            const radio = document.createElement('input'); radio.type = 'radio'; radio.name = `choice-${question.exercise_id}`; radio.value = option.id;
            const text = document.createElement('span'); text.textContent = `${option.id.toUpperCase()}. ${option.text}`;
            label.append(radio, text); fieldset.append(label);
            radio.addEventListener('change', async () => {
              fieldset.disabled = true;
              const chosen = option.id === question.correct;
              const right = question.options.find(item => item.id === question.correct);
              const verdict = chosen ? `${ui.correct} ${question.explanation}` :
                `${ui.incorrect} ${ui.right}: ${right.id.toUpperCase()}. ${right.text}. ${question.explanation}`;
              status.textContent = verdict; status.dataset.correct = String(chosen); card.dataset.result = chosen ? 'correct' : 'incorrect';
              try {
                const response = await fetch('/student/progress/exercise', { method: 'POST', credentials: 'same-origin',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ ...payload, unit_kind: unitKind, exercise_id: question.exercise_id,
                    answer: option.id, status: chosen ? 'completed' : 'attempted' }),
                });
                status.textContent = `${verdict} ${response.ok ? ui.saved : [401, 403].includes(response.status) ? ui.signIn : ui.failed}`;
                if (response.ok) void loadProgress();
                if ([401, 403].includes(response.status) && signIn) signIn.hidden = false;
              } catch { status.textContent = `${verdict} ${ui.failed}`; }
            }, { once: true });
          }
          card.querySelector('.exercise-choice-options').replaceChildren(fieldset);
          status.textContent = '';
        }
      }).catch(() => {
        for (const card of practiceCards) card.querySelector('.exercise-attempt-status').textContent = ui.choiceFailed;
      });
    }
    const showGuest = () => { if (panelStatus) panelStatus.textContent = ''; if (signIn) signIn.hidden = false; };
    const loadProgress = async () => {
      if (!panel || !panelStatus) return;
      try {
        const [statsResponse, progressResponse] = await Promise.all([
          fetch('/student/stats', { credentials: 'same-origin', cache: 'no-store' }),
          fetch('/student/progress', { credentials: 'same-origin', cache: 'no-store' }),
        ]);
        if (!statsResponse.ok || !progressResponse.ok) throw new Error('Study record is unavailable');
        const [stats, progress] = await Promise.all([statsResponse.json(), progressResponse.json()]);
        const course = stats.courses.find(item => item.level === payload.level && item.area === payload.area && item.language === payload.language);
        const completed = Number(course?.lessons_completed || 0);
        const published = Number(panel.dataset.published || 0);
        document.getElementById('progress-completed').textContent = `${completed}/${published}`;
        document.getElementById('progress-exercises').textContent = String(course?.exercises_saved || 0);
        document.getElementById('progress-correct').textContent = `${course?.best_correct || 0}/${course?.best_possible || 0}`;
        document.getElementById('progress-metrics').hidden = false;
        panelStatus.textContent = ui.count(completed, published);
        if (dashboard) dashboard.hidden = false;
        const current = progress.lessons.find(item => item.level === payload.level && item.area === payload.area
          && item.language === payload.language && Number(item.chapter) === payload.chapter);
        if (markButton) markButton.hidden = current?.status === 'completed';
      } catch { panelStatus.textContent = ui.unavailable; }
    };
    markButton?.addEventListener('click', async () => {
      markButton.disabled = true;
      try {
        const response = await fetch('/student/progress/lesson', { method: 'POST', credentials: 'same-origin',
          headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...payload, status: 'completed' }) });
        if (!response.ok) throw new Error('Could not save progress');
        panelStatus.textContent = ui.marked;
        markButton.hidden = true;
        await loadProgress();
      } catch { panelStatus.textContent = ui.unavailable; }
      finally { markButton.disabled = false; }
    });
    const send = (kind, seconds = 0) => fetch('/student/activity', {
      method: 'POST', credentials: 'same-origin', keepalive: true,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...payload, kind, seconds }),
    }).catch(() => {});
    fetch('/auth/me', { credentials: 'same-origin', cache: 'no-store' }).then(response => {
      if (!response.ok) { showGuest(); return; }
      void loadProgress();
      void send('lesson_opened');
      const labels = lesson[4] === 'pt' ? ['Sua análise da aula', 'Salvar análise', 'Análise salva.']
        : lesson[4] === 'es' ? ['Tu análisis de la lección', 'Guardar análisis', 'Análisis guardado.']
        : ['Your lesson analysis', 'Save analysis', 'Analysis saved.'];
      const section = document.createElement('section'); section.className = 'student-analysis';
      const heading = document.createElement('h2'); heading.textContent = labels[0];
      const form = document.createElement('form');
      const textarea = document.createElement('textarea'); textarea.rows = 6; textarea.maxLength = 10_000;
      textarea.setAttribute('aria-label', labels[0]);
      const button = document.createElement('button'); button.type = 'submit'; button.textContent = labels[1];
      const status = document.createElement('p'); status.setAttribute('role', 'status');
      form.append(textarea, button, status); section.append(heading, form);
      document.querySelector('article.prose')?.after(section);
      const query = new URLSearchParams({ ...payload, chapter: String(payload.chapter) });
      fetch(`/student/analysis?${query}`, { credentials: 'same-origin', cache: 'no-store' }).then(async result => {
        if (result.ok) textarea.value = (await result.json()).analysis?.note || '';
      }).catch(() => {});
      form.addEventListener('submit', async event => {
        event.preventDefault(); button.disabled = true;
        try {
          const result = await fetch('/student/analysis', { method: 'POST', credentials: 'same-origin',
            headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...payload, note: textarea.value }) });
          status.textContent = result.ok ? labels[2] : '';
        } finally { button.disabled = false; }
      });
      let started = document.visibilityState === 'visible' ? Date.now() : 0;
      const flush = () => {
        if (!started) return;
        const seconds = Math.min(3600, Math.floor((Date.now() - started) / 1000));
        started = document.visibilityState === 'visible' ? Date.now() : 0;
        if (seconds > 0) void send('lesson_read', seconds);
      };
      document.addEventListener('visibilitychange', () => {
        flush();
        if (document.visibilityState === 'visible') started = Date.now();
      });
      window.addEventListener('pagehide', flush);
      window.setInterval(flush, 60_000);
    }).catch(showGuest);
  }
})();
