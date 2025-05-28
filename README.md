# Vision\_to\_LLM

A Streamlit app that turns an uploaded image into a short, funny audio story using Groq’s TTS (with gTTS fallback).

---

## 📁 Project Structure

```bash
.
├── app.py            # Main Streamlit application
├── .env              # Environment variables (not committed)
├── requirements.txt  # Python dependencies
├── Test_Folder       # Sample images for testing
│   └── sample.jpg    # Example image
└── README.md         # Project documentation
```

---

## 🚀 Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/ForwardDT/Vision_to_LLM_Comedy.git
   cd Vision_to_LLM_Comedy
   ```

2. **Create & activate** a virtual environment

   ```bash
   python -m venv .venv
   # macOS/Linux
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate.bat
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   * Create a `.env` file in the project root with:

     ```env
     GROQ_API_KEY=your_groq_api_key_here
     ```

5. **Run the app**

   ```bash
   streamlit run app.py
   ```

   * Open your browser to [http://localhost:8501](http://localhost:8501)

---

## 🧪 Testing

1. Place a sample image in `Test_Folder/sample.jpg`.
2. Upload it via the Streamlit uploader.
3. The app will:

   * Caption the image
   * Generate a short comedic story (max 60 words)
   * Produce audio via Groq or gTTS fallback
   * Play the audio in-browser

---

## ⚙️ Configuration

* **Change TTS voice/model** by editing the `text2speech_bytes()` function in `app.py`.
* **Suppress warnings** via `warnings.filterwarnings('ignore')` at startup.

---

Happy coding!
