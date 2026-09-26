# Emotion AI 😊

A modern **Emotion Detection Web Application** built using **FastAPI**, **TensorFlow/Keras**, and a **BiGRU deep learning model**.

The application analyzes text input and predicts one of six emotions with confidence scores and probability distribution visualization.

---

## Features

* Emotion classification from text
* BiGRU deep learning model
* FastAPI backend
* Interactive frontend with animations
* Confidence score and probability bars
* Health check API
* Responsive design
* Render deployment support

---

## Supported Emotions

| Emotion  | Emoji |
| -------- | ----- |
| Joy      | 😊    |
| Sadness  | 😢    |
| Love     | ❤️    |
| Anger    | 😠    |
| Fear     | 😨    |
| Surprise | 😲    |

---

## Tech Stack

### Backend

* FastAPI
* Python
* Pydantic
* Uvicorn

### Machine Learning

* TensorFlow
* Keras
* BiGRU
* NumPy

### Frontend

* HTML
* CSS
* JavaScript

### Deployment

* Render

---

## Project Structure

```text
Emotion-AI/
│
├── Artifacts/
│   ├── BIGRU_model.keras
│   └── tokenizer.pkl
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── main.py
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## API Endpoints

### Home Page

```http
GET /
```

Serves the frontend application.

### Health Check

```http
GET /health
```

Example Response:

```json
{
  "status": "Service is running",
  "model_loaded": true
}
```

### Emotion Prediction

```http
POST /predict
```

Request:

```json
{
  "text": "I am feeling very happy today!"
}
```

Response:

```json
{
  "predicted_emotion": "joy",
  "confidence": 0.94
}
```

---

## How It Works

```text
User Input
    ↓
Text Preprocessing
    ↓
Tokenizer
    ↓
Sequence Padding
    ↓
BiGRU Model
    ↓
Emotion Prediction
    ↓
Frontend Visualization
```

---

## Run Locally

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## Deployment (Render)

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Future Improvements

* Add prediction history
* Add dark/light theme
* Improve model performance
* Add Docker support
* Add user authentication

---

## Author

**Kartikey Gehra**

GitHub: https://github.com/Kartikey-Gehra4994

LinkedIn: https://www.linkedin.com/in/kartikey-gehra-11b259344/

---

⭐ If you found this project useful, consider giving it a star.
