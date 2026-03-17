# 🤖 DevMind-AI

> A fully local AI-powered CI/CD pipeline that automatically reviews Pull Requests using Kubernetes, Terraform, and a locally hosted LLM — zero cloud cost, zero data leaving your machine.

![Status](https://img.shields.io/badge/Status-Complete-green)
![DevOps](https://img.shields.io/badge/Domain-DevOps%20%2B%20AI-blue)
![Stack](https://img.shields.io/badge/Stack-Kubernetes%20%7C%20Docker%20%7C%20Terraform%20%7C%20Ollama-green)
![CI](https://github.com/diksha-rawat/DevMind-AI/actions/workflows/pipeline.yml/badge.svg)

---

## 💡 What This Project Does

Most teams rely on expensive cloud AI APIs (like OpenAI) to automate code reviews.
This project builds the same thing — but **100% locally on your own machine**, with zero cloud cost and zero data leaving your network.

When a developer opens a Pull Request:

```
👨‍💻 Developer opens Pull Request
               ↓
⚙️  GitHub Actions triggers
               ↓
🐳  Docker builds the app
               ↓
☸️  Kubernetes deploys it
               ↓
🤖  Ollama + Mistral reviews the code diff
               ↓
💬  AI posts review comment on the PR
               ↓
👨‍💻  Developer gets feedback instantly
```

---

## 🛠 Tech Stack

| Tool | Purpose | Status |
|------|---------|--------|
| **Docker** | Containerise the application | ✅ Done |
| **Minikube** | Run Kubernetes locally on laptop | ✅ Done |
| **Ollama** | Run AI model locally | ✅ Done |
| **Mistral** | The AI model that reviews code | ✅ Done |
| **Terraform** | Provision Kubernetes resources as code | ✅ Done |
| **Flask** | Sample app deployed to Kubernetes | ✅ Done |
| **Python** | AI review agent code | ✅ Done |
| **GitHub Actions** | CI/CD pipeline automation | ✅ Done |

---

## ⚡ Quick Start

```bash
# 1. Start minikube
minikube start --cpus=2 --memory=4096 --driver=docker

# 2. Apply Terraform
cd terraform && terraform init && terraform apply

# 3. Build and deploy the app
eval $(minikube docker-env)
docker build -t devmind-ai-app:latest ./app
kubectl apply -f k8s/

# 4. Run the AI review agent
cd agent
pip install -r requirements.txt
export GITHUB_TOKEN=your_token
python review.py --repo yourname/DevMind-AI --pr 1 --dry-run
```

---

## 📁 Project Structure

```
DevMind-AI/
├── .github/
│   └── workflows/
│       └── pipeline.yml      # CI/CD pipeline
├── terraform/
│   ├── main.tf               # K8s namespaces + ConfigMap
│   └── variables.tf
├── k8s/
│   └── deployment.yaml       # Kubernetes manifests
├── agent/
│   ├── review.py             # AI code review agent
│   ├── requirements.txt
│   └── tests/
│       └── test_review.py    # Agent unit tests
├── app/
│   ├── main.py               # Sample Flask app
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

---

## 🧠 Key Concepts

**Kubernetes** — Container orchestration. Manages deploying, scaling and running containers across a cluster of machines.

**Terraform** — Infrastructure as Code. Write configuration files and Terraform creates your infrastructure automatically.

**Ollama** — Run open-source AI models locally on your own machine, without needing cloud AI APIs.

**Mistral** — An open-source AI language model that understands and reviews code. Runs via Ollama on a standard laptop.

**GitHub Actions** — CI/CD automation built into GitHub. Automatically runs tests and builds Docker images on every code push.

---

## 📅 Build Plan

### ✅ Week 1 — Foundation
- ✅ Set up Minikube (local Kubernetes cluster)
- ✅ Set up Docker
- ✅ Install and test Ollama + Mistral AI model
- ✅ Install Terraform

### ✅ Week 2 — Infrastructure as Code
- ✅ Write Terraform to provision Kubernetes namespaces
- ✅ Deploy sample app to Kubernetes

### ✅ Week 3 — AI Review Agent
- ✅ Build Python agent that fetches GitHub PR diff
- ✅ Send diff to local Ollama/Mistral for review
- ✅ Parse AI response and post back to GitHub as PR comment

### ✅ Week 4 — CI/CD Pipeline + Polish
- ✅ Build full GitHub Actions pipeline
- ✅ Write full documentation

---

## 📬 Connect With Me

[Diksha Rawat](https://linkedin.com/in/diksharawat) | LinkedIn  
[dev.to/diksharawat](https://dev.to/diksharawat) | Dev.to

---

*Built with curiosity and open source tools 🚀*