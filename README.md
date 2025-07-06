# 🕸️ AI Web Scraper - DevOps Edition

This project is a fully Dockerized, Jenkins-integrated, and Kubernetes-ready **AI-powered web scraper** built with `Streamlit`, `Selenium`, `BeautifulSoup`, and `Ollama`. It extracts web data and presents it with a sleek UI, designed for scalability and CI/CD in modern DevOps environments.

---

## 🔧 Features

- 🧠 AI integration via Ollama for intelligent content summarization
- 🌐 Web scraping using `Selenium` & `BeautifulSoup`
- 🚀 Deployed with:
  - **Docker**
  - **Jenkins CI/CD pipeline**
  - **Kubernetes (via Kind)**
- 💡 Simple Streamlit frontend
- 📦 Environment managed via `.env` and `requirements.txt`

---

## 🗂️ Project Structure

```bash
ai-webscraper-devops/
│
├── app/
│   ├── main.py              # Streamlit app
│   ├── scraper.py           # Selenium & BS logic
│   └── ai_helper.py         # Ollama/GPT functions
│
├── Dockerfile               # Docker config
├── .env                     # Environment variables
├── jenkins/
│   └── Jenkinsfile          # Jenkins Pipeline
├── k8s-deployment.yaml      # Kubernetes manifest
├── README.md
└── requirements.txt
