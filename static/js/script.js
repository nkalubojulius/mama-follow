// MamaFollow Interactive JavaScript Client Logic
document.addEventListener('DOMContentLoaded', () => {
  // Initialize Tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map((el) => new bootstrap.Tooltip(el));

  // Initialize Water Tracker
  initWaterTracker();

  // Initialize Kegel Trainer if on exercise page
  if (document.getElementById('kegel-ring')) {
    initKegelTrainer();
  }

  // Initialize MamaFollow AI Chatbot
  initChatbot();

  // Initialize Real-Time Meal Alarm & Notification Engine
  initMealAlarmEngine();

  // Real-time Week Selector slider in Tracker page
  const weekSlider = document.getElementById('weekRangeSlider');
  if (weekSlider) {
    weekSlider.addEventListener('input', (e) => {
      document.getElementById('sliderWeekDisplay').textContent = e.target.value;
    });
    weekSlider.addEventListener('change', (e) => {
      window.location.href = `/tracker?week=${e.target.value}`;
    });
  }
});

/* --- Water Tracker Logic --- */
function initWaterTracker() {
  const glasses = document.querySelectorAll('.water-glass-btn');
  if (!glasses.length) return;

  const todayKey = 'mamacare_water_' + new Date().toISOString().slice(0, 10);
  let drankCount = parseInt(localStorage.getItem(todayKey) || '0', 10);

  function updateWaterUI() {
    glasses.forEach((btn, idx) => {
      if (idx < drankCount) {
        btn.classList.add('drank');
        btn.innerHTML = '💧';
      } else {
        btn.classList.remove('drank');
        btn.innerHTML = '🥛';
      }
    });
    const totalMl = drankCount * 250;
    const progressEl = document.getElementById('waterProgressText');
    if (progressEl) {
      progressEl.textContent = `${drankCount} / 8 Glasses (${totalMl} ml / 2000 ml)`;
    }
  }

  glasses.forEach((btn, idx) => {
    btn.addEventListener('click', () => {
      if (idx === drankCount - 1) {
        drankCount = Math.max(0, drankCount - 1);
      } else {
        drankCount = idx + 1;
      }
      localStorage.setItem(todayKey, drankCount);
      updateWaterUI();
    });
  });

  const resetBtn = document.getElementById('resetWaterBtn');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      drankCount = 0;
      localStorage.setItem(todayKey, drankCount);
      updateWaterUI();
    });
  }

  updateWaterUI();
}

/* --- Kegel Pelvic Floor Trainer Logic --- */
function initKegelTrainer() {
  const ring = document.getElementById('kegel-ring');
  const timerText = document.getElementById('kegel-timer-text');
  const actionLabel = document.getElementById('kegel-action-label');
  const repCountText = document.getElementById('kegel-rep-count');
  const startBtn = document.getElementById('kegelStartBtn');
  const stopBtn = document.getElementById('kegelStopBtn');

  let interval = null;
  let isRunning = false;
  let state = 'squeeze'; // 'squeeze' or 'relax'
  let secondsLeft = 5;
  let repsCompleted = 0;
  const targetReps = 10;

  function playTone(freq = 440, duration = 0.15) {
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.1, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + duration);
    } catch (e) {
      // AudioContext not allowed or unsupported
    }
  }

  function tick() {
    secondsLeft--;
    if (timerText) timerText.textContent = secondsLeft;

    if (secondsLeft <= 0) {
      if (state === 'squeeze') {
        state = 'relax';
        secondsLeft = 5;
        ring.className = 'kegel-ring relax';
        actionLabel.textContent = 'RELAX & BREATHE';
        actionLabel.style.color = '#2ed573';
        playTone(330, 0.2);
      } else {
        repsCompleted++;
        if (repCountText) repCountText.textContent = `${repsCompleted} / ${targetReps}`;
        if (repsCompleted >= targetReps) {
          stopTrainer();
          actionLabel.textContent = '🎉 SET COMPLETED!';
          actionLabel.style.color = '#ff6b8b';
          playTone(587, 0.4);
          return;
        }
        state = 'squeeze';
        secondsLeft = 5;
        ring.className = 'kegel-ring contract';
        actionLabel.textContent = 'SQUEEZE & LIFT';
        actionLabel.style.color = '#ff4757';
        playTone(523, 0.2);
      }
      if (timerText) timerText.textContent = secondsLeft;
    }
  }

  function startTrainer() {
    if (isRunning) return;
    isRunning = true;
    repsCompleted = 0;
    state = 'squeeze';
    secondsLeft = 5;
    if (timerText) timerText.textContent = secondsLeft;
    if (repCountText) repCountText.textContent = `0 / ${targetReps}`;
    ring.className = 'kegel-ring contract';
    actionLabel.textContent = 'SQUEEZE & LIFT';
    actionLabel.style.color = '#ff4757';
    startBtn.classList.add('d-none');
    stopBtn.classList.remove('d-none');
    playTone(523, 0.2);
    interval = setInterval(tick, 1000);
  }

  function stopTrainer() {
    isRunning = false;
    clearInterval(interval);
    ring.className = 'kegel-ring';
    if (actionLabel) {
      actionLabel.textContent = 'READY TO START';
      actionLabel.style.color = '#718096';
    }
    if (timerText) timerText.textContent = '5';
    startBtn.classList.remove('d-none');
    stopBtn.classList.add('d-none');
  }

  if (startBtn) startBtn.addEventListener('click', startTrainer);
  if (stopBtn) stopBtn.addEventListener('click', stopTrainer);
}

/* --- MamaFollow AI Chatbot Logic --- */
function initChatbot() {
  const toggleBtn = document.getElementById('chatbot-toggle-btn');
  const chatWindow = document.getElementById('chatbot-window');
  const closeBtn = document.getElementById('chatbot-close-btn');
  const clearBtn = document.getElementById('chatbot-clear-btn');
  const form = document.getElementById('chatbot-form');
  const input = document.getElementById('chatbot-input');
  const messagesContainer = document.getElementById('chatbot-messages');
  const typingIndicator = document.getElementById('chatbot-typing');
  const iconAi = document.querySelector('.chatbot-icon-ai');
  const iconClose = document.querySelector('.chatbot-icon-close');

  if (!toggleBtn || !chatWindow) return;

  const STORAGE_KEY = 'mamacare_client_chat';

  function scrollToBottom() {
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }

  function formatMessageText(text) {
    if (!text) return '';
    let escaped = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    
    // Bold: **text**
    escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Italic: *text*
    escaped = escaped.replace(/\*(.*?)\*/g, '<em>$1</em>');
    // Line breaks
    escaped = escaped.replace(/\n/g, '<br>');
    return escaped;
  }

  function appendMessage(role, text, isEmergency = false, links = []) {
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-message ${role === 'user' ? 'user-message' : 'bot-message'}`;

    let linksHtml = '';
    if (links && links.length > 0) {
      linksHtml = '<div class="mt-2 d-flex flex-wrap gap-1">';
      links.forEach(l => {
        linksHtml += `<a href="${l.url}" class="chat-link-btn"><i class="fa-solid fa-arrow-up-right-from-square"></i> ${l.title}</a>`;
      });
      linksHtml += '</div>';
    }

    if (role === 'user') {
      msgDiv.innerHTML = `
        <div class="message-content">
          <p class="mb-0">${formatMessageText(text)}</p>
          <span class="message-time">${timeStr}</span>
        </div>
      `;
    } else {
      const emergencyClass = isEmergency ? 'emergency-bot-bubble' : '';
      msgDiv.innerHTML = `
        <div class="message-avatar">
          <i class="fa-solid fa-baby"></i>
        </div>
        <div class="message-content ${emergencyClass}">
          <p class="mb-0">${formatMessageText(text)}</p>
          ${linksHtml}
          <span class="message-time">${timeStr}</span>
        </div>
      `;
    }

    messagesContainer.appendChild(msgDiv);
    scrollToBottom();
  }

  function saveChatToStorage(role, text, isEmergency = false, links = []) {
    try {
      const history = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '[]');
      history.push({ role, text, isEmergency, links, time: new Date().toISOString() });
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(history.slice(-15)));
    } catch (e) {
      console.warn('Session storage write error:', e);
    }
  }

  function loadChatHistory() {
    try {
      const history = JSON.parse(sessionStorage.getItem(STORAGE_KEY) || '[]');
      if (history.length > 0) {
        history.forEach(item => {
          appendMessage(item.role, item.text, item.isEmergency, item.links);
        });
      }
    } catch (e) {
      console.warn('Session storage read error:', e);
    }
  }

  function toggleChat(forceOpen = null) {
    const isClosed = chatWindow.classList.contains('d-none');
    const shouldOpen = forceOpen !== null ? forceOpen : isClosed;

    if (shouldOpen) {
      chatWindow.classList.remove('d-none');
      if (iconAi) iconAi.classList.add('d-none');
      if (iconClose) iconClose.classList.remove('d-none');
      if (input) input.focus();
      scrollToBottom();
    } else {
      chatWindow.classList.add('d-none');
      if (iconAi) iconAi.classList.remove('d-none');
      if (iconClose) iconClose.classList.add('d-none');
    }
  }

  toggleBtn.addEventListener('click', () => toggleChat());
  if (closeBtn) closeBtn.addEventListener('click', () => toggleChat(false));

  if (clearBtn) {
    clearBtn.addEventListener('click', async () => {
      try {
        await fetch('/api/chat/clear', { method: 'POST' });
        sessionStorage.removeItem(STORAGE_KEY);
        // Reset container to initial welcome message
        messagesContainer.innerHTML = `
          <div class="chat-message bot-message">
            <div class="message-avatar">
              <i class="fa-solid fa-baby"></i>
            </div>
            <div class="message-content">
              <p class="mb-0">Hello! 👋 Welcome to <strong>MamaFollow</strong>. I can provide general pregnancy-related information and educational guidance. Please remember that I cannot provide a medical diagnosis or replace advice from a qualified healthcare professional. How can I help you today?</p>
              <span class="message-time">Just now</span>
            </div>
          </div>
          <div id="chatbot-quick-prompts" class="chatbot-quick-prompts my-2">
            <span class="prompt-chip" data-prompt="What should I eat in Trimester 1?">🥗 Trimester 1 Diet</span>
            <span class="prompt-chip" data-prompt="Tell me about fetal development at Week 20">🥑 Week 20 Growth</span>
            <span class="prompt-chip" data-prompt="Is walking safe during pregnancy?">🧘‍♀️ Safe Exercises</span>
            <span class="prompt-chip" data-prompt="How to relieve morning sickness?">🍋 Morning Sickness</span>
            <span class="prompt-chip" data-prompt="What are red-flag emergency symptoms?">🚨 Red-Flag Signs</span>
            <span class="prompt-chip" data-prompt="How do I do Kegel exercises?">💪 Kegel Guide</span>
          </div>
        `;
        bindPromptChips();
      } catch (e) {
        console.error('Failed to clear chat:', e);
      }
    });
  }

  async function handleSendMessage(messageText) {
    const text = messageText.trim();
    if (!text) return;

    if (input) input.value = '';
    appendMessage('user', text);
    saveChatToStorage('user', text);

    if (typingIndicator) typingIndicator.classList.remove('d-none');
    scrollToBottom();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();

      if (typingIndicator) typingIndicator.classList.add('d-none');

      if (response.ok && data.success) {
        appendMessage('bot', data.reply, data.emergency, data.links);
        saveChatToStorage('bot', data.reply, data.emergency, data.links);
      } else {
        const errorReply = "I apologize, I am temporarily having trouble connecting. Please try asking again in a moment. 🌸";
        appendMessage('bot', errorReply);
      }
    } catch (err) {
      if (typingIndicator) typingIndicator.classList.add('d-none');
      const networkError = "Connection interrupted. Please verify your internet connection and try again. 🌸";
      appendMessage('bot', networkError);
    }
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (input) handleSendMessage(input.value);
    });
  }

  function bindPromptChips() {
    document.querySelectorAll('.prompt-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        const prompt = e.currentTarget.getAttribute('data-prompt');
        if (prompt) {
          handleSendMessage(prompt);
        }
      });
    });
  }

  // Bind initial quick prompts and load history
  bindPromptChips();
  loadChatHistory();
}

/* =========================================================
   REAL-TIME MEAL ALARM & NOTIFICATION ENGINE
   ========================================================= */

function playMealAlarmChime() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const notes = [523.25, 659.25, 783.99]; // C5, E5, G5 cheerful chime
    notes.forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const startTime = ctx.currentTime + (idx * 0.14);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, startTime);
      gain.gain.setValueAtTime(0.12, startTime);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.35);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(startTime);
      osc.stop(startTime + 0.35);
    });
  } catch (e) {
    console.log('Audio chime not permitted by browser policy yet.');
  }
}

function showMealToast(reminder) {
  const toast = document.getElementById('meal-alarm-toast');
  const badge = document.getElementById('meal-alarm-badge');
  const title = document.getElementById('meal-alarm-title');
  const notes = document.getElementById('meal-alarm-notes');
  const time = document.getElementById('meal-alarm-time');
  const dismissBtn = document.getElementById('meal-alarm-dismiss-btn');
  const snoozeBtn = document.getElementById('meal-alarm-snooze-btn');
  const closeBtn = document.getElementById('meal-alarm-x-btn');

  if (!toast) return;

  if (badge) badge.textContent = reminder.meal_type || 'Meal Time';
  if (title) title.textContent = `Time for ${reminder.meal_name || 'your meal'}! 🍽️`;
  if (notes) notes.textContent = reminder.notes || 'Remember to eat slowly, chew well, and stay hydrated.';
  if (time) time.textContent = reminder.reminder_time || 'Now';

  toast.classList.remove('d-none');
  playMealAlarmChime();

  function hideToast() {
    toast.classList.add('d-none');
  }

  if (dismissBtn) dismissBtn.onclick = hideToast;
  if (closeBtn) closeBtn.onclick = hideToast;
  if (snoozeBtn) {
    snoozeBtn.onclick = () => {
      hideToast();
      setTimeout(() => {
        showMealToast(reminder);
      }, 10 * 60 * 1000); // 10 min snooze
    };
  }
}

function initMealAlarmEngine() {
  let alertedMinutes = new Set();

  async function checkAlarms() {
    try {
      const res = await fetch('/api/reminders');
      if (!res.ok) return;
      const data = await res.json();
      if (!data.success || !data.reminders) return;

      const now = new Date();
      const currentHours = String(now.getHours()).padStart(2, '0');
      const currentMinutes = String(now.getMinutes()).padStart(2, '0');
      const currentTimeStr = `${currentHours}:${currentMinutes}`;
      const todayDateStr = now.toISOString().slice(0, 10);
      const alertKey = `${todayDateStr}_${currentTimeStr}`;

      if (alertedMinutes.has(alertKey)) return;

      data.reminders.forEach(r => {
        const reminderTime = String(r.reminder_time).slice(0, 5);
        if (reminderTime === currentTimeStr) {
          alertedMinutes.add(alertKey);
          showMealToast(r);

          // Native Browser notification
          if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(`MamaFollow: Time for ${r.meal_name}!`, {
              body: `${r.meal_type} scheduled at ${r.reminder_time}. ${r.notes || ''}`,
              icon: '/static/images/logo.png'
            });
          }
        }
      });
    } catch (e) {
      // Background poll silently ignore
    }
  }

  // Initial check and background interval every 15 seconds
  checkAlarms();
  setInterval(checkAlarms, 15000);
}


