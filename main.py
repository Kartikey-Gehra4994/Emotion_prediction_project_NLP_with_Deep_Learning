from keras.preprocessing.sequence import pad_sequences
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import re
import string
import numpy as np
from pydantic import BaseModel, Field
from keras.models import load_model
import pickle
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

model_path = "Artifacts/BIGRU_model.keras"

tokenizer_path = "Artifacts/tokenizer.pkl"

max_sequence_length = 66

emotion_labels = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

emotional_emojis = {
    'sadness': '😢',
    'joy': '😊',
    'love': '❤️',
    'anger': '😠',
    'fear': '😨',
    'surprise': '😲'
}

exclude = string.punctuation

def preprocess_text(text: str)-> str:

    print(f"Original text: {text}")

    text = text.lower()

    # Remove punctuation from the text
    text = text.translate(str.maketrans('', '', exclude))

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    print(f"Preprocessed text: {text}")

    return text

        
class TextInput(BaseModel):

    text: str = Field(
        ..., min_length=1, 
        max_length=1000, 
        description="Input text for emotion prediction model", 
        example="I am feeling very happy today!",
        )

class PredictionResponse(BaseModel):

    text: str
    predicted_emotion: str
    confidence: float
    all_probabilities: dict[str, float]

class HealthResponse(BaseModel):

    status: str
    model_loaded: bool

# Model Loading and Lifespan Management

dl_model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading the model and tokenizer...")
    dl_model['model'] = load_model(model_path)

    with open(tokenizer_path, 'rb') as f:
        dl_model['tokenizer'] = pickle.load(f)

    print("Model and tokenizer loaded successfully.")

    yield # Pass control to the application

    dl_model.clear() # Clear the model and tokenizer from memory when the application shuts down

# Api Endpoints
app = FastAPI(
    title="Emotion Detection API",
    description="An API for detecting emotions from text using a BiGRU model.",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Server ui at homepage("/")
@app.get("/", include_in_schema=False)
def serve_ui():
    return FileResponse("static/index.html")

# Health Check Endpoint
@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="Service is running", model_loaded=bool(dl_model.get('model', False)))

@app.post("/predict", response_model=PredictionResponse)
def predict_emotion(text_input: TextInput):

    # Load the model and tokenizer from the global dictionary
    BIGRU_model = dl_model.get('model')
    tokenizer = dl_model.get('tokenizer')

    if BIGRU_model is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Model or tokenizer not loaded.")

    # Preprocess the input text
    preprocessed_text = preprocess_text(text_input.text)

    # Tokenize and pad the input text
    tokenized_text = tokenizer.texts_to_sequences([preprocessed_text])
    padded_sequences = pad_sequences(tokenized_text, maxlen=max_sequence_length, padding='post', truncating='post')

    # Make predictions
    predictions = BIGRU_model.predict(padded_sequences)[0]

    top_emotion_index = int(np.argmax(predictions))
    all_probabilities = {
        emotion_labels: float(prob) for emotion_labels, prob in zip(emotion_labels, predictions)
    }

    return PredictionResponse(
        text=text_input.text,
        predicted_emotion=emotion_labels[top_emotion_index],
        confidence=float(predictions[top_emotion_index]),
        all_probabilities=all_probabilities
    )
    