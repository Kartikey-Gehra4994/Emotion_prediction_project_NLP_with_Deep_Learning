from fastapi import FastAPI
import re
import string
from pydantic import BaseModel, field
from keras.models import load_model
import pickle
from contextlib import asynccontextmanager

app = FastAPI()

@app.get('/')
def greet():
    return {"message": "Hello, World!"}

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

    text: str = field(
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