# 🚀 DevOps Portfolio

Welcome to my DevOps portfolio! This repository showcases my skills in modern software development practices, containerization, CI/CD, and monitoring.

## 🎯 About Me

I'm a DevOps engineer passionate about automation, reliability, and continuous improvement. This portfolio demonstrates my hands-on experience with industry-standard tools and practices.

## 🛠️ Skills

### Core Competencies
- **Containerization**: Docker, Docker Compose, multi-stage builds
- **CI/CD**: GitHub Actions, automated testing, deployment pipelines
- **Monitoring**: Prometheus, Grafana, metrics collection
- **Programming**: Python, Bash scripting
- **Version Control**: Git, branching strategies, code review

### Tools & Technologies
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📁 Projects

### 1. [URL Shortener API](projects/url-shortener/)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Docker](https://img.shields.io/badge/docker-ready-blue)

A full-stack DevOps project demonstrating:
- RESTful API with Flask
- Multi-stage Docker builds
- Automated testing with pytest
- CI/CD pipeline with GitHub Actions
- Monitoring with Prometheus & Grafana
- Deployment to Render (PaaS)

**Key Features:**
- URL shortening with custom codes
- Click tracking and statistics
- Health check endpoints
- Prometheus metrics integration
- Zero-downtime deployments

[View Project →](projects/url-shortener/)

## 🏗️ Architecture

```text
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   GitHub    │────▶│ GitHub Actions│────▶│  Docker Hub │
│   Repo      │     │  (CI/CD)     │     │  Registry   │
└─────────────┘     └──────────────┘     └─────────────┘
                                                   │
                                                   ▼
                                           ┌─────────────┐
                                           │   Render    │
                                           │  (PaaS)     │
                                           └─────────────┘
                                                   │
                                                   ▼
                                           ┌─────────────┐
                                           │  URL Short  │
                                           │    API      │
                                           └─────────────┘
                                                   │
                           ┌───────────────────────┼───────────────────┐
                           ▼                       ▼                   ▼
                   ┌─────────────┐         ┌─────────────┐     ┌─────────────┐
                   │ Prometheus  │         │   Grafana   │     │   SQLite    │
                   │  (Metrics)  │────────▶│ (Dashboard) │     │   (DB)      │
                   └─────────────┘         └─────────────┘     └─────────────┘
```

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Git

### Run Locally

```bash
# Clone the repository
git clone [https://github.com/CassavaIsLife/my-devops-portfolio.git](https://github.com/CassavaIsLife/my-devops-portfolio.git)
cd my-devops-portfolio

# Run the URL shortener with monitoring stack
cd projects/url-shortener
docker compose up -d

# Access the services:
# API: http://localhost:5000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

## 🧪 Testing

```bash
cd projects/url-shortener
pip install -r requirements.txt
pytest -v
```

## 📊 CI/CD Pipeline

The CI/CD pipeline automatically:
1. Runs unit tests on every push
2. Builds Docker image with multi-stage build
3. Pushes to Docker Hub
4. Deploys to Render (PaaS)
5. Monitors application metrics

## 🔍 Monitoring

Each project includes:
- Prometheus metrics endpoint at `/metrics`
- Grafana dashboards for visualization
- Health check endpoints
- Performance metrics

## 📈 GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=CassavaIsLife&show_icons=true&theme=radical)

## 📫 Contact
``
- **Email**: [gustinchulu@gmail.com](mailto:gustinchulu@gmail.com)
- **GitHub**: [@CassavaIsLife](https://github.com/CassavaIsLife)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
⭐️ If you find this portfolio helpful, please star the repository!