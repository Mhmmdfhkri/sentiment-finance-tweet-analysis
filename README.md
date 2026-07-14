# Finance Sentiment Analyzer

Model ini dirancang untuk mendeteksi sentimen dari cuitan (*tweets*) atau berita keuangan. Untuk mengetahui pasar sedang bagus (**Bullish**), lesu (**Bearish**), atau biasa-biasa saja (**Neutral**).



https://github.com/user-attachments/assets/5464b4c1-2cd9-4a29-951f-c47abf7f761a



## 📁 Struktur Folder Proyek

```text
finance-sentiment-app/
│
├── backend/
│   ├── app.py                  # Server API
│   ├── model.py                # Arsitektur model BERT_Arch & utilitasnya
│   ├── saved_weights.pt        # File bobot BERT (Local only - gitignored)
│
├── frontend/
│   ├── index.html              # Interface aplikasi web
│   └── app.js                  
│
├── .gitignore                 
├── requirements.txt           
└── README.md
```

## Tech yang Digunakan
| Bagian | Teknologi |
| :--- | :--- |
| **Frontend** | HTML5, Tailwind CSS (via CDN), Vanilla JavaScript |
| **Backend API** | FastAPI |
| **Deep Learning** | PyTorch, Transformers, BERT |
| **Data Processing** | Pandas, NumPy |

## Implementasi
*   **Deep Learning (BERT):** Menggunakan arsitektur **BERT (`bert-base-uncased`)** dari Google sebagai tulang punggung (*backbone*) model, yang dikustomisasi dengan tambahan *dense layers* dan *dropout* untuk menangkap konteks semantik yang kompleks pada tweet keuangan.
*   **Imbalance Dataset (Class Weights):** Mengintegrasikan penghitungan bobot kelas otomatis (`compute_class_weight` dari Scikit-Learn) ke dalam fungsi loss *Negative Log-Likelihood* (`nn.NLLLoss`) milik PyTorch untuk mengatasi distribusi data sentimen yang tidak seimbang (*imbalanced dataset*).
*   **Pipeline Data:**
    *   **Hugging Face** untuk pemuatan dataset langsung via URL `hf://` dan tokenisasi cepat menggunakan `BertTokenizerFast` / `AutoTokenizer`.
    *   **PyTorch DataLoader** untuk *batching* (ukuran batch: 32) dan melakukan *shuffling* data latih secara acak menggunakan `RandomSampler`.
*   **Optimasi & GPU Accelerated:** Pengecekan otomatis perangkat keras GPU (CUDA), penanganan *exploding gradients* menggunakan teknik *Gradient Clipping* (`clip_grad_norm_`).
*   **Evaluasi:** Menyediakan laporan metrik klasifikasi (*Precision, Recall, F1-Score, dan Accuracy*) untuk mengukur performa nyata model pada data uji (*test set*).
*   **Model Serialization:** Menyimpan bobot model terbaik secara otomatis selama proses training (dalam format file `.pt` menggunakan *PyTorch*) 



---

          
