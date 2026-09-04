# URL Shortener API

A containerized URL shortener with full DevOps pipeline, demonstrating modern software development practices.

## ✨ Features

- Shorten URLs with automatic short code generation
- Redirect to original URLs (302)
- Track click statistics
- Health check endpoint
- Prometheus metrics integration
- SQLite database (zero configuration)
- Containerized with multi-stage Docker build
- Automated CI/CD pipeline

## 🏗️ Tech Stack

- **Backend**: Python 3.11, Flask
- **Database**: SQLite
- **Container**: Docker (multi-stage build)
- **CI/CD**: GitHub Actions
- **Deployment**: Render (PaaS)
- **Monitoring**: Prometheus, Grafana
- **Testing**: pytest

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shorten` | Create short URL |
| GET | `/{short_code}` | Redirect to original URL |
| GET | `/stats/{short_code}` | Get URL statistics |
| GET | `/health` | Health check |
| GET | `/metrics` | Prometheus metrics |

### Example Usage

```bash
# Create short URL
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "[https://example.com](https://example.com)"}'

# Response
{
  "short_code": "Ab3xY9",
  "short_url": "/Ab3xY9",
  "original_url": "[https://example.com](https://example.com)"
}
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)

### Run with Docker Compose
```bash
docker compose up -d
```

### Run Locally
```bash
pip install -r requirements.txt
python app.py
```

## 🧪 Testing

```bash
pytest -v
```

## 📊 Monitoring

The application exposes Prometheus metrics at `/metrics`. A Grafana dashboard is available for visualization.

Access monitoring:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## 🔄 CI/CD Pipeline

The pipeline runs on every push to main:
1. Run tests
2. Build Docker image
3. Push to Docker Hub
4. Deploy to Render

## 📁 Project Structure

```text
url-shortener/
├── app.py              # Main application
├── test_app.py         # Unit tests
├── Dockerfile          # Multi-stage Docker build
├── docker-compose.yml  # Local development with monitoring
├── prometheus.yml      # Prometheus configuration
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔒 Security Features

- Non-root user in Docker container
- Multi-stage build to minimize attack surface
- Input validation for URLs
- SQLite parameterized queries (prevents SQL injection)
- Health check endpoint for orchestration

## 📈 Future Improvements

- [ ] Add Redis for caching
- [ ] Implement rate limiting
- [ ] Add authentication
- [ ] Move to PostgreSQL for production
- [ ] Add Kubernetes deployment manifests