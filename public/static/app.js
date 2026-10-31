const csrf = document.querySelector('meta[name=csrf]').content;
const post = (u, b) => fetch(u, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf }, body: JSON.stringify(b || {}) });

// ── Mobile nav ────────────────────────────────────────────────────────────
document.getElementById('burger').onclick = () => document.getElementById('navMobile').classList.toggle('open');
document.querySelectorAll('.nav-mobile a').forEach(a => a.addEventListener('click', () => document.getElementById('navMobile').classList.remove('open')));

// ── Scroll reveal ─────────────────────────────────────────────────────────
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
}, { threshold: 0.1 });
document.querySelectorAll('.card').forEach((el, i) => {
  el.style.transitionDelay = (i % 3) * 80 + 'ms';
  observer.observe(el);
});

// ── Nav scroll style ──────────────────────────────────────────────────────
window.addEventListener('scroll', () => {
  document.getElementById('nav').style.background = window.scrollY > 40 ? 'rgba(10,22,40,.98)' : 'rgba(10,22,40,.92)';
});

// ── Chat ──────────────────────────────────────────────────────────────────
const log = document.getElementById('log'), q = document.getElementById('q'), hist = [];
const add = (t, c) => {
  const d = document.createElement('div'); d.className = 'b ' + c; d.textContent = t;
  log.append(d); log.scrollTop = log.scrollHeight; return d;
};
// Minimal, escape-first markdown: **bold**, "- " bullets, paragraphs, bare links/emails
const md = t => {
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const inline = s => esc(s)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(https?:\/\/[^\s<)]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>')
    .replace(/([\w.+-]+@[\w-]+\.[\w.]+\w)/g, '<a href="mailto:$1">$1</a>');
  return t.trim().split(/\n{2,}/).map(block => {
    const lines = block.split('\n');
    if (lines.every(l => /^\s*[-*•]\s+/.test(l)))
      return '<ul>' + lines.map(l => '<li>' + inline(l.replace(/^\s*[-*•]\s+/, '')) + '</li>').join('') + '</ul>';
    return '<p>' + lines.map(inline).join('<br>') + '</p>';
  }).join('');
};
document.getElementById('f').onsubmit = async e => {
  e.preventDefault(); const t = q.value.trim(); if (!t) return; q.value = '';
  add(t, 'me'); hist.push({ role: 'user', content: t }); const w = add('Typing…', 'bot typing');
  try {
    const r = await post('/api/chat', { messages: hist }); const j = await r.json(); if (!r.ok) throw 0;
    w.innerHTML = md(j.reply); hist.push({ role: 'assistant', content: j.reply });
  } catch { w.textContent = 'Chatbot unavailable. Email mdbarish1502@gmail.com instead.'; }
  w.classList.remove('typing'); log.scrollTop = log.scrollHeight;
};
document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', () => { q.value = chip.textContent; document.getElementById('f').requestSubmit(); });
});

// ── Voice call ────────────────────────────────────────────────────────────
const btn = document.getElementById('callBtn');
const st = document.getElementById('callState');
const transcriptBox = document.getElementById('transcriptBox');
const transcriptLog = document.getElementById('transcriptLog');
let room;

function addTranscript(text, who) {
  transcriptBox.hidden = false;
  const line = document.createElement('div');
  line.className = 'tr-line ' + who;
  line.textContent = (who === 'ai' ? '🤖 ' : '🎤 ') + text;
  transcriptLog.append(line);
  transcriptBox.scrollTop = transcriptBox.scrollHeight;
}

btn.onclick = async () => {
  if (room) { room.disconnect(); return; }
  try {
    st.textContent = 'Dialing…';
    const { url, token } = await (await post('/api/call-token')).json();
    room = new LivekitClient.Room();
    room.on(LivekitClient.RoomEvent.TrackSubscribed, (tr) => {
      if (tr.kind === 'audio') {
        const el = tr.attach(); el.autoplay = true; el.muted = false; el.volume = 1; document.body.append(el);
        st.textContent = 'AI joined. Say hello.';
        el.play().catch(() => {
          st.textContent = 'Tap anywhere to turn on sound.';
          document.body.addEventListener('click', () => { el.play(); room && room.startAudio(); }, { once: true });
        });
      }
      if (tr.kind === 'data') {
        tr.on('message', data => {
          try { const msg = JSON.parse(new TextDecoder().decode(data)); if (msg.text) addTranscript(msg.text, 'ai'); } catch {}
        });
      }
    });
    room.on(LivekitClient.RoomEvent.ActiveSpeakersChanged, sp => { if (sp.some(p => !p.isLocal)) st.textContent = 'AI is speaking…'; });
    room.on(LivekitClient.RoomEvent.TranscriptionReceived, (segments, participant) => {
      segments.forEach(seg => { if (seg.final) addTranscript(seg.text, participant?.isLocal ? 'me' : 'ai'); });
    });
    room.on(LivekitClient.RoomEvent.Disconnected, () => {
      room = null;
      btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81 19.79 19.79 0 01.01 1.18 2 2 0 012 0h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg> Call my AI';
      btn.classList.remove('live'); st.textContent = 'Call ended.';
    });
    room.on(LivekitClient.RoomEvent.AudioPlaybackStatusChanged, () => { if (!room.canPlaybackAudio) st.textContent = 'Tap anywhere to turn on sound.'; });
    await room.connect(url, token); await room.startAudio();
    await room.localParticipant.setMicrophoneEnabled(true, { echoCancellation: true, noiseSuppression: true, autoGainControl: true });
    document.body.addEventListener('click', () => room && room.startAudio(), { once: true });
    btn.textContent = '⏹ End call'; btn.classList.add('live');
    st.textContent = 'Connected. Say hello and ask about my projects.';
  } catch {
    room = null; st.textContent = 'Could not start the call. Allow microphone, or try the chat below.';
  }
};
