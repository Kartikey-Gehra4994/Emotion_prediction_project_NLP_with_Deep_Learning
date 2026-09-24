const textInput = document.getElementById("textInput");
const counter = document.getElementById("counter");
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");
const errorMessage = document.getElementById("errorMessage");
const emptyState = document.getElementById("emptyState");
const predictionState = document.getElementById("predictionState");
const emotionIcon = document.getElementById("emotionIcon");
const emotionName = document.getElementById("emotionName");
const confidence = document.getElementById("confidence");
const confidenceFill = document.getElementById("confidenceFill");
const analyzedText = document.getElementById("analyzedText");
const probabilityList = document.getElementById("probabilityList");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");

const emojiMap = {
  sadness: "😢",
  joy: "😊",
  love: "❤️",
  anger: "😠",
  fear: "😨",
  surprise: "😲"
};

const prettyNames = {
  sadness: "Sadness",
  joy: "Joy",
  love: "Love",
  anger: "Anger",
  fear: "Fear",
  surprise: "Surprise"
};

function updateCounter() {
  counter.textContent = `${textInput.value.length} / 1000`;
}

function setLoading(loading) {
  analyzeBtn.classList.toggle("loading", loading);
  analyzeBtn.disabled = loading;
}

function showError(message) {
  errorMessage.textContent = message;
}

function clearError() {
  errorMessage.textContent = "";
}

function resetResult() {
  predictionState.hidden = true;
  emptyState.hidden = false;
  confidenceFill.style.width = "0%";
  probabilityList.innerHTML = "";
}

async function checkHealth() {
  try {
    const response = await fetch("/health", { cache: "no-store" });
    if (!response.ok) throw new Error();
    const data = await response.json();

    if (data.model_loaded) {
      statusDot.className = "status-dot online";
      statusText.textContent = "Model online";
    } else {
      statusDot.className = "status-dot";
      statusText.textContent = "Model loading";
    }
  } catch {
    statusDot.className = "status-dot offline";
    statusText.textContent = "API unavailable";
  }
}

function renderProbabilities(probabilities) {
  probabilityList.innerHTML = "";

  Object.entries(probabilities)
    .sort((a, b) => b[1] - a[1])
    .forEach(([emotion, value], index) => {
      const percentage = value * 100;

      const row = document.createElement("div");
      row.className = "probability-row";

      row.innerHTML = `
        <span class="probability-name">${prettyNames[emotion] || emotion}</span>
        <div class="probability-bar">
          <div class="probability-fill" data-width="${percentage}"></div>
        </div>
        <span class="probability-value">${percentage.toFixed(1)}%</span>
      `;

      probabilityList.appendChild(row);

      requestAnimationFrame(() => {
        setTimeout(() => {
          row.querySelector(".probability-fill").style.width = `${percentage}%`;
        }, 80 + index * 45);
      });
    });
}

async function analyzeEmotion() {
  const text = textInput.value.trim();

  if (!text) {
    showError("Enter some text before analyzing.");
    textInput.focus();
    return;
  }

  clearError();
  setLoading(true);

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Prediction failed.");
    }

    const emotion = data.predicted_emotion;
    const confidenceValue = data.confidence * 100;

    emptyState.hidden = true;
    predictionState.hidden = false;

    emotionIcon.textContent = emojiMap[emotion] || "✦";
    emotionName.textContent = prettyNames[emotion] || emotion;
    confidence.textContent = `${confidenceValue.toFixed(1)}%`;
    analyzedText.textContent = data.text;

    confidenceFill.style.width = "0%";
    requestAnimationFrame(() => {
      setTimeout(() => {
        confidenceFill.style.width = `${confidenceValue}%`;
      }, 80);
    });

    renderProbabilities(data.all_probabilities);

    document.getElementById("resultCard").scrollIntoView({
      behavior: "smooth",
      block: "nearest"
    });
  } catch (error) {
    showError(error.message || "Something went wrong. Please try again.");
  } finally {
    setLoading(false);
  }
}

textInput.addEventListener("input", () => {
  updateCounter();
  clearError();
});

textInput.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
    analyzeEmotion();
  }
});

analyzeBtn.addEventListener("click", analyzeEmotion);

clearBtn.addEventListener("click", () => {
  textInput.value = "";
  updateCounter();
  clearError();
  resetResult();
  textInput.focus();
});

document.querySelectorAll(".prompt-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    textInput.value = chip.dataset.text;
    updateCounter();
    clearError();
    textInput.focus();
  });
});

updateCounter();
checkHealth();
setInterval(checkHealth, 30000);