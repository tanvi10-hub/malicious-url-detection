# 🚀 Deployment Guide

This guide covers deployment options for the Malicious URL Detector on various platforms.

## 📋 Prerequisites

- Python 3.9 or higher
- Git
- pip (Python package manager)
- Models files (`rf_model_v2.pkl`, `label_encoder.pkl`)

## 🔧 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/malicious-url-detection.git
cd malicious-url-detection
```

### 2. Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your configuration
# IMPORTANT: Change SECRET_KEY for production
```

### 5. Provide model files (choose one option)

**Option A: Keep files local (development)**

Place model files in the `models/` directory:

```
models/
├── rf_model_v2.pkl
└── label_encoder.pkl
```

**Option B: Download at startup (recommended for GitHub deploys)**

Do not commit large model files. Upload them to cloud storage (or GitHub Releases)
and set these environment variables:

```bash
AUTO_DOWNLOAD_MODELS=true
MODEL_URL=https://your-host/path/rf_model_v2.pkl
ENCODER_URL=https://your-host/path/label_encoder.pkl
```

### 6. Run the application

```bash
python src/app.py
```

Access at: `http://localhost:5000`

---

## 🌐 Deployment Platforms

### **Heroku**

#### Setup

1. Create Heroku account at [heroku.com](https://www.heroku.com)
2. Install Heroku CLI

#### Deploy

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Add model files
# Option 1: Use Git LFS (Large File Storage)
git lfs install
git add models/*.pkl
git commit -m "Add model files"

# Option 2: Download from cloud storage (see section below)

# Deploy
git push heroku main
```

#### Model Storage on Heroku

Since Heroku has limited storage and deploys, store models on cloud storage:

1. **Direct download URLs (recommended)**
   - Host model artifacts in cloud object storage or GitHub Releases
   - Set `AUTO_DOWNLOAD_MODELS=true`, `MODEL_URL`, and `ENCODER_URL`
   - The app downloads models on startup if local files are missing

2. **AWS S3**
   ```python
   # Update config.py to download from S3
   import boto3
   s3 = boto3.client('s3')
   ```

3. **Azure Blob Storage**
   ```python
   from azure.storage.blob import BlobClient
   ```

---

### **Docker & Docker Compose**

#### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000

CMD ["gunicorn", "--worker-class=sync", "--workers=4", "--timeout=120", "--bind=0.0.0.0:5000", "src.app:app"]
```

#### Build and run locally

```bash
docker build -t url-detector .
docker run -p 5000:5000 --env-file .env url-detector
```

#### Push to Docker Hub

```bash
docker tag url-detector yourusername/url-detector:latest
docker push yourusername/url-detector:latest
```

---

### **Google Cloud Run**

#### Setup

```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### Deploy

```bash
# Create Dockerfile (see Docker section above)

# Deploy to Cloud Run
gcloud run deploy url-detector \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,SECRET_KEY=your-secret-key
```

---

### **AWS (Elastic Beanstalk)**

#### Setup

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 url-detector
```

#### Deploy

```bash
# Create Procfile (already included)

# Deploy
eb create url-detector-env
eb deploy

# Monitor
eb status
eb logs
```

---

### **GitHub Pages (Static - For documentation)**

Create GitHub Actions workflow to deploy docs:

```yaml
# .github/workflows/deploy-docs.yml
name: Deploy Docs
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS/SSL certificates
- [ ] Use environment variables for all secrets
- [ ] Set up rate limiting for API endpoints
- [ ] Configure CORS appropriately
- [ ] Enable logging and monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Use secret management (AWS Secrets Manager, etc.)
- [ ] Run security scanning (Bandit, Safety)

### Generate Strong Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📊 Monitoring & Logging

### Application Monitoring

```python
# Add to app.py for production monitoring
from flask_logging import setup_logging

setup_logging(app)
```

### Error Tracking (Sentry)

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.1
)
```

### Performance Monitoring

```bash
pip install newrelic
```

---

## 🧪 CI/CD Pipeline

GitHub Actions workflow is configured in `.github/workflows/ci.yml`:

- **Linting**: Python syntax and style checks (Flake8)
- **Testing**: Unit tests (Pytest)
- **Security**: Dependency scanning (Safety, Bandit)
- **Build**: Application startup verification

View logs: GitHub Actions tab in repository

---

## 📈 Scaling Considerations

### Load Balancing

Use Gunicorn with multiple workers:

```bash
gunicorn --workers=4 --worker-class=sync --threads=2 src.app:app
```

### Caching

Implement model caching with `@lru_cache`:

```python
@lru_cache(maxsize=1)
def load_models():
    # Models loaded once and cached
    return model, encoder
```

### Database (If needed)

Consider SQLAlchemy for persistent storage:

```bash
pip install flask-sqlalchemy
```

---

## 🐛 Troubleshooting

### Models not loading

```bash
# Check file paths
python -c "from config import current_config; print(current_config.MODEL_PATH)"

# Verify files exist
ls -la models/
```

### Port already in use

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### CORS issues

```python
# Add to app.py
from flask_cors import CORS
CORS(app)
```

### Import errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

---

## 📞 Support

For deployment issues:

1. Check GitHub Issues
2. Review logs with `heroku logs --tail`
3. Test locally with `FLASK_ENV=development`
4. Run security checks with `bandit -r src/`

---

## 📝 Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | production | Environment mode |
| `SECRET_KEY` | - | Flask secret key (MUST change) |
| `PORT` | 5000 | Port to listen on |
| `HOST` | 0.0.0.0 | Host to bind to |
| `MODEL_PATH` | models/rf_model_v2.pkl | Path to ML model |
| `ENCODER_PATH` | models/label_encoder.pkl | Path to label encoder |
| `LOG_LEVEL` | INFO | Logging level |
| `AUTO_DOWNLOAD_MODELS` | false | Download model artifacts if missing |
| `MODEL_URL` | - | Direct URL to `rf_model_v2.pkl` |
| `ENCODER_URL` | - | Direct URL to `label_encoder.pkl` |
| `MODEL_DOWNLOAD_TIMEOUT` | 120 | Download timeout in seconds |

---

Happy Deploying! 🚀
