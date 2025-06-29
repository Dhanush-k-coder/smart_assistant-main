# 🧠 Smart Research Assistant

Smart Research Assistant is an AI-powered tool that enables users to intelligently interact with research documents (PDF/TXT). It offers document summarization, question answering, logic-based challenges, and intelligent evaluation — all grounded directly in the document content.


🎥 **Watch Demo Video:** [Click to watch on Google Drive](https://drive.google.com/file/d/1DlIA-g_D_VU46VqPh509Zy1FA8jCbPzx/view?usp=sharing)

🔗 **Live Demo:** [https://smartassistant-charan.streamlit.app/](https://smartassistant-charan.streamlit.app/)  
📦 **Tech Stack:** Python · Streamlit · Hugging Face Transformers · OpenRouter API · PDF/Text Parsing

---

## ✨ Features

| Feature               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| 📄 Upload Docs        | Upload any PDF or TXT file to analyze its content                          |
| 📝 Auto Summary       | Generate concise summaries (≤150 words) using Transformer-based models     |
| 💬 Ask Anything       | Ask any question grounded in the document, with justification               |
| 🧠 Challenge Me        | Auto-generate 3 logic/comprehension questions + evaluate user answers       |
| ☁️ Local + Cloud Mode | Toggle between free local models and powerful cloud APIs via OpenRouter     |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/smart-research-assistant.git
cd smart-research-assistant
2. Set Up Virtual Environment
bash
Copy
Edit
python -m venv smart_env
source smart_env/bin/activate  # Windows: smart_env\Scripts\activate
3. Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
4. Run the App Locally
bash
Copy
Edit
streamlit run app.py
🔐 API Key Configuration
To enable cloud-based responses using OpenRouter:

python
Copy
Edit
api_key = "your_openrouter_api_key"
For better security, use .env files or Streamlit secrets in production.

📁 Project Structure
bash
Copy
Edit
smart-research-assistant/
│
├── app.py                        # Main Streamlit app
├── modules/
│   ├── file_handler.py          # Extracts text from uploaded documents
│   ├── summarizer.py            # Summarizes extracted text
│   ├── qa_module.py             # Local Q&A processing
│   ├── question_gen.py          # Generates logic questions
│   └── evaluator.py             # Evaluates user answers
├── assets/                      # Optional: icons or media
├── requirements.txt             # Dependency list
└── README.md
🚧 Future Enhancements
🔊 Whisper Integration (Audio → Text → Q&A)

🧵 Context memory across sessions

🎓 Difficulty-scaled challenge questions

📊 Interactive document analytics dashboard

🙌 Credits
Built by Charan Yedida with ❤️ using:

Streamlit

Hugging Face Transformers

OpenRouter AI

