import os
import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model import get_bert_prediction_tools, device

app = FastAPI(title="Financial Sentiment Analyzer API")

# Setup CORS agar frontend dari port mana pun bisa mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BERT_WEIGHTS_PATH = os.path.join(BASE_DIR, 'saved_weights.pt')

LABEL_MAP = {
    0: "Bearish",
    1: "Bullish",
    2: "Neutral"
}

# Request schema menggunakan Pydantic
class SentimentRequest(BaseModel):
    text: str

# Memuat model saat startup
tokenizer, bert_model = None, None
print("Memuat model BERT (ini akan memakan waktu beberapa detik)...")
try:
    tokenizer, bert_model = get_bert_prediction_tools(BERT_WEIGHTS_PATH)
    print("Model BERT berhasil dimuat!")
except Exception as e:
    print(f"Gagal memuat BERT (Pastikan file saved_weights.pt sudah ditaruh di folder backend): {e}")


@app.post('/predict')
async def predict(payload: SentimentRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Teks masukan tidak boleh kosong")
    
    if not bert_model or not tokenizer:
        raise HTTPException(status_code=500, detail="Model BERT belum berhasil dimuat di server.")

    try:
        # Tokenisasi dengan max_length = 50 sesuai setelan training Colab Anda
        inputs = tokenizer(
            [payload.text],
            max_length=50,
            padding='max_length',
            truncation=True,
            return_tensors="pt"
        )
        
        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)
        
        with torch.no_grad():
            outputs = bert_model(input_ids, attention_mask)
            prediction = torch.argmax(outputs, dim=1).item()
            
        return {
            'label': prediction,
            'sentiment': LABEL_MAP.get(prediction, "Unknown")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses prediksi: {str(e)}")


if __name__ == '__main__':
    # Berjalan di port 8000 (port default FastAPI)
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)