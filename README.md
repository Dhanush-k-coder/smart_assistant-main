# 🧠 Smart Research Assistant

Smart Research Assistant is an AI-powered tool that enables users to intelligently interact with research documents (PDF/TXT). It offers document summarization, question answering, logic-based challenges, and intelligent evaluation — all grounded directly in the document content.


🎥 **Watch Demo Video:** [Click to watch on Google Drive]()

🔗 **Live Demo:** [https://dhanush-k-coder-smart-assistant-main-app-t6uvbl.streamlit.app/](https://dhanush-k-coder-smart-assistant-main-app-t6uvbl.streamlit.app/)  


📦 **Tech Stack:** Python · Streamlit · Hugging Face Transformers · OpenRouter API · PDF/Text Parsing

# 🧠 Smart Research Assistant

A powerful, AI-driven tool to extract, summarize, question, and evaluate content from documents—built with Streamlit, Hugging Face, and OpenRouter.

---

## 🚀 Quick Start Guide

### 📥 1. Clone the Repo

```bash
git clone https://github.com/yourusername/smart-research-assistant.git
cd smart-research-assistant
```

### 🧪 2. Set Up Your Environment

Create and activate a virtual environment:

```bash
python -m venv smart_env
source smart_env/bin/activate       # On Windows: smart_env\Scripts\activate
```

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### ▶️ 4. Launch the App

```bash
streamlit run app.py
```

---

## 🔐 API Key Setup (for Cloud Responses)

To use OpenRouter for cloud-based AI responses, set your API key like this:

```python
api_key = "your_openrouter_api_key"
```

**🔒 Pro tip:** Use a `.env` file or [Streamlit's secret manager](https://docs.streamlit.io/streamlit-cloud/secrets-management) in production to avoid hardcoding sensitive info.

---

## 🗂️ Folder Overview

```
smart-research-assistant/
│
├── app.py               # The main Streamlit app
├── modules/             # Modular logic for each feature
│   ├── file_handler.py
│   ├── summarizer.py
│   ├── qa_module.py
│   ├── question_gen.py
│   └── evaluator.py
├── assets/              # Optional media/icons
├── requirements.txt     # All Python dependencies
└── README.md
```

---

## 🛠️ Roadmap & Upcoming Features

* 🎤 Audio support with Whisper (speech → text → answers)
* 🧠 Session memory for smarter follow-ups
* 🎯 Skill-based question scaling
* 📊 Visual dashboards for document analysis

---

## 🙏 Credits

Created with ❤️ by **Charan Yedida**
Powered by:

* [Streamlit](https://streamlit.io/)
* [Hugging Face Transformers](https://huggingface.co/)
* [OpenRouter AI](https://openrouter.ai/)

---

