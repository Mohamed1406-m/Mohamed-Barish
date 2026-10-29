const csrf = document.querySelector('meta[name=csrf]').content;
const post = (u, b) => fetch(u, {method: 'POST', headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf}, body: JSON.stringify(b || {})});
// Chat
const log = document.getElementById('log'), q = document.getElementById('q'), hist = [];
const add = (t, c) => { const d = document.createElement('div'); d.className = 'b ' + c; d.textContent = t; log.append(d); log.scrollTop = log.scrollHeight; return d; };
document.getElementById('f').onsubmit = async e => {
  e.preventDefault(); const t = q.value.trim(); if (!t) return; q.value = '';
  add(t, 'me'); hist.push({role: 'user', content: t}); const w = add('Typing…', 'bot');
  try { const r = await post('/api/chat', {messages: hist}); const j = await r.json(); if (!r.ok) throw 0;
    w.textContent = j.reply; hist.push({role: 'assistant', content: j.reply});
  } catch { w.textContent = 'The chatbot is unavailable right now. Email mdbarish1502@gmail.com instead.'; }
};
// Voice call
const btn = document.getElementById('callBtn'), st = document.getElementById('callState'); let room;
btn.onclick = async () => {
  if (room) { room.disconnect(); return; }
  try {
    st.textContent = 'Dialing…';
    const {url, token} = await (await post('/api/call-token')).json();
    room = new LivekitClient.Room();
    room.on(LivekitClient.RoomEvent.TrackSubscribed, tr => { if (tr.kind === 'audio') { document.body.append(tr.attach()); st.textContent = 'AI joined. Say hello.'; } });
    room.on(LivekitClient.RoomEvent.ActiveSpeakersChanged, sp => { if (sp.some(p => !p.isLocal)) st.textContent = 'AI is speaking…'; });
    room.on(LivekitClient.RoomEvent.Disconnected, () => { room = null; btn.textContent = 'Call my AI'; btn.classList.remove('live'); st.textContent = 'Call ended.'; });
    room.on(LivekitClient.RoomEvent.AudioPlaybackStatusChanged, () => { if (!room.canPlaybackAudio) st.textContent = 'Tap anywhere on the page to turn on sound.'; });
    await room.connect(url, token); await room.startAudio(); await room.localParticipant.setMicrophoneEnabled(true);
    document.body.addEventListener('click', () => room && room.startAudio(), {once: true});
    btn.textContent = 'End call'; btn.classList.add('live'); st.textContent = 'Connected. Say hello and ask about my projects.';
  } catch { room = null; st.textContent = 'Could not start the call. Allow the microphone, or try the chat below.'; }
};
