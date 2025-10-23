// Import Firebase modules (ensure these imports are at the top or loaded properly)
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-app.js";
import { 
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendPasswordResetEmail
} from "https://www.gstatic.com/firebasejs/12.2.1/firebase-auth.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.2.1/firebase-analytics.js";

// Firebase config and initialization
const firebaseConfig = {
  apiKey: "AIzaSyC_h17EoE_Dzfwq1eJx1x5fMuZWdC_Iw6c",
  authDomain: "login-page-f939f.firebaseapp.com",
  projectId: "login-page-f939f",
  storageBucket: "login-page-f939f.appspot.com",
  messagingSenderId: "355086410029",
  appId: "1:355086410029:web:377bcfc39eb0dafc08b3a4",
  measurementId: "G-P0K1V57T9T"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const analytics = getAnalytics(app);

// Hide dashboard initially
document.getElementById('app-container').style.display = 'none';
// Login form submit handler
document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const email = document.getElementById("login-username").value.trim().toLowerCase();
  const password = document.getElementById("login-password").value;
  signInWithEmailAndPassword(auth, email, password)
    .then(() => {
      document.getElementById('login-container').style.display = 'none';
      document.getElementById('app-container').style.display = 'block';
      document.getElementById('login-error').textContent = '';
    })
    .catch((error) => {
      document.getElementById('login-error').textContent = error.message;
    });
});

// Forgot password link click handler
document.querySelector('.forgot-link').addEventListener('click', function(event) {
  event.preventDefault();
  const email = document.getElementById("login-username").value.trim().toLowerCase();
  if (email) {
    sendPasswordResetEmail(auth, email)
      .then(() => {
        document.getElementById('login-error').textContent = "Password reset email sent! Check your inbox.";
      })
      .catch((error) => {
        document.getElementById('login-error').textContent = error.message;
      });
  } else {
    document.getElementById('login-error').textContent = "Enter your email address to reset password.";
  }
});

// Charts
new Chart(document.getElementById('weeklyActivityChart').getContext('2d'), {
  type: 'line',
  data: {
    labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    datasets: [{
      label: 'Workouts',
      data: [2,1,3,2,1,4,3],
      fill: false,
      borderColor: '#2563eb',
      backgroundColor: '#2563eb',
      tension: 0.3,
      pointBorderColor: '#2563eb',
      pointBackgroundColor: '#fff',
      pointRadius: 5,
    }]
  },
  options: {
    responsive: true,
    plugins: {legend: {display: false}},
    scales: {
      y: {
        beginAtZero: true,
        suggestedMax: 4,
        ticks: {stepSize: 1}
      }
    }
  }
});
new Chart(document.getElementById('caloriesBurnedChart').getContext('2d'), {
  type: 'bar',
  data: {
    labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
    datasets: [{
      label: 'Calories',
      data: [350,290,420,380,260,450,340],
      backgroundColor: '#6c97fd',
      hoverBackgroundColor: '#2563eb',
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {display: false},
      tooltip: {
        callbacks: {
          label: ctx => "Calories: " + ctx.parsed.y
        }
      }
    },
    scales: {y: {beginAtZero: true, suggestedMax: 600}}
  }
});

// Section Switching with Animation
const menuItems = document.querySelectorAll('#sidebar-menu li');
const sections = document.querySelectorAll('.dashboard-area > section');
function switchSection(activeSection) {
  sections.forEach(s => {
    if (s === activeSection) {
      s.style.display = "block";
      s.classList.remove("fade-out");
      s.style.animation = "fadeIn 0.8s";
    } else {
      s.classList.add("fade-out");
      setTimeout(() => {
        s.style.display = "none";
        s.classList.remove("fade-out");
      }, 500);
    }
  });
}
menuItems.forEach(item => {
  item.addEventListener('click', () => {
    menuItems.forEach(i => i.classList.remove('active'));
    item.classList.add('active');
    const sec = item.getAttribute('data-section');
    const secMap = {
      "dashboard":"dashboard-section",
      "ai-chat":"ai-chat-section",
      "workouts":"workouts-section",
      "speech":"speech-section",
      "history":"history-section"
    };
    const activeSection = document.getElementById(secMap[sec] || sec + "-section");
    if (activeSection) switchSection(activeSection);
  });
});
sections.forEach(s => s.style.display = "none");
document.getElementById("dashboard-section").style.display = "block";

// Logout
document.getElementById('logout-btn').onclick = () => {
  auth.signOut().then(() => {
    document.getElementById('app-container').style.display = 'none';
    document.getElementById('login-container').style.display = 'block';
    location.reload();
  });
};

// Dashboard stat animation
function animateStat(element, endValue, duration=900) {
  const startValue = parseInt(element.textContent.replace(/[^\d]/g, '')) || 0;
  let startTime = null;
  function step(ts) {
    if (!startTime) startTime = ts;
    const progress = Math.min((ts - startTime) / duration, 1);
    element.textContent = Math.floor(startValue + (endValue - startValue) * progress);
    if (progress < 1) requestAnimationFrame(step);
    else element.textContent = endValue;
  }
  requestAnimationFrame(step);
}
document.getElementById('start-workout').addEventListener('click', () => {
  const workouts = Math.floor(Math.random() * 5) + 12;
  const calories = Math.floor(Math.random() * 500) + 2000;
  const timeH = (Math.floor(Math.random() * 4) + 6) + Math.floor(Math.random() * 10) / 10;
  const progress = Math.floor(Math.random() * 30) + 60;
  animateStat(document.getElementById('workouts-count'), workouts);
  animateStat(document.getElementById('calories-count'), calories);
  document.getElementById('total-time').textContent = timeH.toFixed(1) + "h";
  document.getElementById('goal-progress').textContent = progress + "%";
});

// AI Chat Section (Backend-powered)
const chatList = document.getElementById('chatList');
function submitChat() {
  const input = document.getElementById('chatInput').value.trim();
  if(input === "") return;
  // Display user message
  const userRow = document.createElement('div');
  userRow.className = 'ai-chat-row user';
  const userBubble = document.createElement('div');
  userBubble.className = 'ai-chat-bubble';
  userBubble.textContent = input;
  userRow.appendChild(userBubble);
  chatList.appendChild(userRow);
  chatList.scrollTop = chatList.scrollHeight;
  document.getElementById('chatInput').value = '';

  // Fetch AI reply from backend API
  fetch('http://localhost:5000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: input })
  })
  .then(response => response.json())
  .then(data => {
    const aiRow = document.createElement('div');
    aiRow.className = 'ai-chat-row assistant';
    const aiBubble = document.createElement('div');
    aiBubble.className = 'ai-chat-bubble';
    aiBubble.textContent = data.reply;
    aiRow.appendChild(aiBubble);
    chatList.appendChild(aiRow);
    chatList.scrollTop = chatList.scrollHeight;
  })
  .catch(err => {
    console.error("Error fetching AI response:", err);
    const aiRow = document.createElement('div');
    aiRow.className = 'ai-chat-row assistant';
    const aiBubble = document.createElement('div');
    aiBubble.className = 'ai-chat-bubble';
    aiBubble.textContent = "Sorry, there was an error processing your request.";
    aiRow.appendChild(aiBubble);
    chatList.appendChild(aiRow);
    chatList.scrollTop = chatList.scrollHeight;
  });
}
document.getElementById('chatForm').onsubmit = e => { e.preventDefault(); submitChat(); }
document.getElementById('sendBtn').onclick = e => { e.preventDefault(); submitChat(); };

// Workouts filter
const grid = document.getElementById('workoutGrid');
const filterBtns = document.querySelectorAll('.workout-filter-btn');
filterBtns.forEach(btn => {
  btn.onclick = () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const type = btn.getAttribute('data-filter');
    Array.from(grid.children).forEach(card => {
      card.style.display = (type === "all" || card.getAttribute('data-type') === type) ? "" : "none";
    });
  }
});

// Speech recognition and TTS integration

let recording = false;
let mediaRecorder;
let audioChunks = [];
const startStopMic = document.getElementById('startStopMic');
const transcriptBox = document.getElementById('transcriptBox');

startStopMic.onclick = async () => {
  if (!recording) {
    // Start recording
    recording = true;
    startStopMic.classList.add('stopping');
    startStopMic.innerHTML = '<i class="fas fa-microphone-slash"></i> Stop Recording';
    transcriptBox.textContent = '';

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
      audioChunks = [];

      mediaRecorder.ondataavailable = e => {
        audioChunks.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

        // Upload audio blob to backend (/api/speech/transcribe)
        const formData = new FormData();
        formData.append('audio', audioBlob, 'speech.wav');

        try {
          const response = await fetch('/api/speech/transcribe', {
            method: 'POST',
            body: formData
          });
          const result = await response.json();
          if (result.ok) {
            transcriptBox.textContent = result.text;

            // Optional: Call TTS API to play the transcript aloud
            await playTTS(result.text);
          } else {
            transcriptBox.textContent = "Could not transcribe audio.";
          }
        } catch (error) {
          console.error("Error sending audio for transcription:", error);
          transcriptBox.textContent = "Error during transcription.";
        }
      };
    } catch (err) {
      console.error("Could not start audio recorder:", err);
      transcriptBox.textContent = "Cannot access microphone.";
      recording = false;
      startStopMic.classList.remove('stopping');
      startStopMic.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
    }

  } else {
    // Stop recording
    recording = false;
    startStopMic.classList.remove('stopping');
    startStopMic.innerHTML = '<i class="fas fa-microphone"></i> Start Recording';
    if (mediaRecorder) {
      mediaRecorder.stop();
    }
  }
};

async function playTTS(text) {
  try {
    const response = await fetch('/api/speech/tts', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ text })
    });
    const data = await response.json();
    if (data.ok && data.audio_base64) {
      const audio = new Audio("data:audio/mp3;base64," + data.audio_base64);
      audio.play();
    }
  } catch (error) {
    console.error("Error fetching TTS:", error);
  }
}