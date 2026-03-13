# 🤖 Local AI Pipeline Orchestrator
> **Status: 🚧 In Progress** — Building a fully local CI/CD pipeline with AI-powered code review

![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![DevOps](https://img.shields.io/badge/Domain-DevOps%20%2B%20AI-blue)
![Stack](https://img.shields.io/badge/Stack-Kubernetes%20%7C%20Docker%20%7C%20Terraform%20%7C%20Ollama-green)

---

## 💡 What This Project Is About

Most teams rely on expensive cloud AI APIs (like OpenAI) to automate code reviews.
This project builds the same thing — but **100% locally on your own machine**, with zero cloud cost and zero data leaving your network.

When a developer opens a Pull Request:
```
Developer opens PR
      ↓
GitHub Actions triggers the pipeline
      ↓
Docker builds the application
      ↓
Kubernetes (minikube) deploys it
      ↓
Local AI model (Mistral via Ollama) reviews the code diff
      ↓
AI posts a detailed review comment back on the PR
```

---

## 🎯 Why I Am Building This

- To demonstrate **AI + DevOps** skills in a single project
- To show that AI-powered tooling doesn't require expensive cloud APIs
- To learn and document **Kubernetes, Terraform, CI/CD and local LLMs** hands-on
- To build something that solves a **real problem** companies face

---

## 🛠 Tech Stack

| Tool | Purpose | Status |
|------|---------|--------|
| **Docker** | Containerise the application | ✅ Done |
| **Minikube** | Run Kubernetes locally on laptop | ✅ Done |
| **Ollama** | Run AI model locally | 🚧 In Progress |
| **Mistral** | The AI model that reviews code | 🚧 In Progress |
| **Terraform** | Provision Kubernetes resources as code | ⬜ Upcoming |
| **GitHub Actions** | CI/CD pipeline automation | ⬜ Upcoming |
| **Python** | AI review agent code | ⬜ Upcoming |

---

## 📅 Build Plan

### ✅ Week 1 — Foundation
- [x] Set up Minikube (local Kubernetes cluster)
- [x] Set up Docker
- [ ] Install and test Ollama + Mistral AI model
- [ ] Install Terraform

### ⬜ Week 2 — Infrastructure as Code
- [ ] Write Terraform to provision Kubernetes namespaces
- [ ] Set up RBAC (role-based access control) via Terraform
- [ ] Deploy sample app to Kubernetes

### ⬜ Week 3 — AI Review Agent
- [ ] Build Python agent that fetches GitHub PR diff
- [ ] Send diff to local Ollama/Mistral for review
- [ ] Parse AI response and post back to GitHub as PR comment

### ⬜ Week 4 — CI/CD Pipeline + Polish
- [ ] Build full GitHub Actions pipeline
- [ ] Record demo GIF
- [ ] Write full documentation

---

## 🧠 Key Concepts I Am Learning

**Kubernetes** — Container orchestration. Manages deploying, scaling and running containers across a cluster of machines.

**Terraform** — Infrastructure as Code tool. Instead of manually setting up servers or clusters, you write configuration files and Terraform creates everything automatically.

**Ollama** — A tool that lets you run open-source AI models (like Mistral) locally on your own machine, without needing cloud AI APIs.

**Mistral** — An open-source AI language model that is good at understanding and reviewing code. Runs via Ollama on a standard laptop.

**GitHub Actions** — CI/CD automation built into GitHub. Automatically runs tests, builds Docker images and deploys to Kubernetes on every code push.

---

## 🏗 Project Structure (planned)

```
local-ai-pipeline/
├── .github/
│   └── workflows/
│       └── pipeline.yml      # CI/CD pipeline
├── terraform/
│   ├── main.tf               # K8s namespaces + RBAC
│   └── variables.tf
├── k8s/
│   └── deployment.yaml       # Kubernetes manifests
├── agent/
│   └── review.py             # AI code review agent
├── app/
│   ├── main.py               # Sample Flask app
│   └── Dockerfile
└── README.md
```

---

## 💬 Follow Along

I am building this step by step and documenting everything I learn.
If you are also learning DevOps + AI, feel free to star ⭐ the repo and follow along!

---

## 📬 Connect With Me

- [Diksha Rawat](https://linkedin.com/in/diksharawat) | LinkedIn

---

*This project is actively being built. Last updated: March 2026*
