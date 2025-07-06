# 🕸️ AI Web Scraper - DevOps Edition

This project is a fully Dockerized, Jenkins-integrated, and Kubernetes-ready **AI-powered web scraper** built with `Streamlit`, `Selenium`, `BeautifulSoup`, and `Ollama`. It extracts web data and presents it with a sleek UI, designed for scalability and CI/CD in modern DevOps environments.

## 🔧 Features

* 🧠 AI integration via Ollama for intelligent content summarization
* 🌐 Web scraping using `Selenium` & `BeautifulSoup`
* 🚀 Deployed with:
   * **Docker**
   * **Jenkins CI/CD pipeline**
   * **Kubernetes (via Kind)**
* 💡 Simple Streamlit frontend
* 📦 Environment managed via `.env` and `requirements.txt`

## 🗂️ Project Structure

```
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
```

## ⚙️ DevOps Stack

| Tool | Purpose |
|------|---------|
| Docker | Containerization |
| Jenkins | CI/CD Pipeline |
| Kind | Local Kubernetes Cluster |
| Kubectl | Managing K8s resources |

## 🚀 Run Locally

### 1. Docker

```bash
docker build -t ai-webscraper .
docker run -p 8501:8501 --env-file .env ai-webscraper
```

Then open: http://localhost:8501

### 2. Jenkins CI/CD

Use the Jenkinsfile for a declarative pipeline

Ensure Jenkins container is run with Docker socket:

```bash
docker run -d \
  --name jenkins-devops \
  -u root \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts-jdk11
```

### 3. Kubernetes Deployment (Kind)

```bash
kind create cluster --name ai-webscraper-cluster
docker build -t ai-webscraper .
kind load docker-image ai-webscraper --name ai-webscraper-cluster
kubectl apply -f k8s-deployment.yaml
```

## 🌐 Access

```bash
kubectl get svc
# Note NodePort, e.g. 32752

curl http://localhost:<NodePort>
```

Or port-forward:

```bash
kubectl port-forward svc/ai-webscraper-service 8501:8501
```

Then visit: http://localhost:8501

## 🧠 Author

**Sankalp Raj**  
DevOps Enthusiast | AI Builder  
📧 sankalpraj59@gmail.com  
🔗 GitHub

## 🏁 Future Work

* Terraform deployment
* AWS EKS hosting
* GitHub Actions CI/CD
* Autoscaling with HPA

## ⭐️ Show your support

If you found this helpful, leave a ⭐️ on the repo!
