# Enterprise AI Assistant - Deployment Guides

## 🚀 Streamlit Cloud (FREE - Recommended)

### 1. Prerequisites
- GitHub account
- Repository pushed to GitHub
- Free Streamlit account

### 2. Deploy Steps

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select "GitHub" as source
4. Authorize GitHub access
5. Choose repository
6. Select `app.py` as main file
7. Click "Deploy"

### 3. Add API Key to Streamlit Cloud

1. Go to your app dashboard
2. Click "Settings" (gear icon)
3. Go to "Secrets"
4. Add your keys:
```
AI_PROVIDER = "gemini"
GEMINI_API_KEY = "your_key_here"
```

### 4. Auto-Deploy

- Every `git push` to main auto-deploys
- Takes ~2 minutes
- View logs in dashboard

---

## 🐳 Docker (Local or Cloud)

### Build Image
```bash
docker build -t finance-assistant:latest .
```

### Run Locally
```bash
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your_key \
  -e AI_PROVIDER=gemini \
  finance-assistant:latest
```

### With docker-compose
```bash
# Create .env file first
cp .env.example .env
# Edit .env with your API key

# Run
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop
docker-compose down
```

---

## ☁️ Azure Container Apps

### Prerequisites
- Azure account
- Azure CLI installed
- Container Registry

### Steps

```bash
# Login to Azure
az login

# Create resource group
az group create --name finance-assistant --location eastus

# Create container registry
az acr create --resource-group finance-assistant \
  --name assistantregistry --sku Basic

# Build & push image
az acr build --registry assistantregistry \
  --image finance-assistant:latest .

# Create container app
az containerapp create \
  --name finance-assistant \
  --resource-group finance-assistant \
  --image assistantregistry.azurecr.io/finance-assistant:latest \
  --environment my-environment \
  --ingress external \
  --target-port 8501 \
  --secrets gemini-key=$GEMINI_API_KEY \
  --env-vars AI_PROVIDER=gemini GEMINI_API_KEY=secretref:gemini-key
```

---

## AWS (Lambda + Elastic Container Registry)

### Push to ECR
```bash
# Create ECR repository
aws ecr create-repository --repository-name finance-assistant

# Login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Tag & push
docker tag finance-assistant:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/finance-assistant:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/finance-assistant:latest
```

### Run on EC2
```bash
# SSH to EC2
ssh -i your-key.pem ec2-user@your-instance-ip

# Install Docker
sudo yum install docker -y
sudo service docker start

# Pull & run
sudo docker run -d \
  -p 8501:8501 \
  -e GEMINI_API_KEY=your_key \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/finance-assistant:latest
```

---

## 🖥️ On-Premise / Self-Hosted

### Linux Server

```bash
# SSH to server
ssh user@your-server.com

# Install Python & dependencies
sudo apt-get update
sudo apt-get install python3.11 python3-pip git -y

# Clone repo
git clone https://github.com/your-username/enterprise-ai-accounting-finance-assistant.git
cd enterprise-ai-accounting-finance-assistant

# Setup Python env
python3 -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env  # Add your API key

# Generate data
python scripts/generate_demo_data.py

# Build RAG
python scripts/build_vector_store.py

# Run with supervisor/systemd
# (Optional: systemd service file below)
```

### Systemd Service File

Create `/etc/systemd/system/finance-assistant.service`:

```ini
[Unit]
Description=Finance Assistant Streamlit App
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/finance-assistant
Environment="PATH=/opt/finance-assistant/venv/bin"
ExecStart=/opt/finance-assistant/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable & start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable finance-assistant
sudo systemctl start finance-assistant
```

---

## 🔐 Security Best Practices

### Before Deploying

- [ ] Never commit .env file
- [ ] Generate new API keys (not dev keys)
- [ ] Enable API key restrictions (to your domain/app only)
- [ ] Set up rate limiting
- [ ] Consider behind auth proxy
- [ ] Enable HTTPS/SSL

### On the Server

- [ ] Use secrets manager (AWS Secrets, Azure Key Vault)
- [ ] Never store secrets in environment variables hardcoded
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Firewall rules (allow only needed ports)
- [ ] Monitor API usage & costs

---

## 🚨 Monitoring & Logging

### Streamlit Cloud
- Dashboard shows app status
- Logs visible in Streamlit dashboard

### Docker
```bash
docker logs -f container_name
```

### Self-Hosted
```bash
tail -f /var/log/finance-assistant.log
```

### Errors to Watch
- API quota exceeded → Rate limit or upgrade plan
- Memory high → Check data size
- Response slow → Check LLM provider status

---

## 🆘 Troubleshooting

### App won't start
```bash
# Check dependencies
pip install -r requirements.txt

# Verify Python version
python --version  # Should be 3.11+

# Run in debug mode
streamlit run app.py --logger.level=debug
```

### API errors
```bash
# Check API key
echo $GEMINI_API_KEY  # Should show key

# Test API connection
python -c "import google.generativeai; google.generativeai.configure(api_key='KEY'); print('✓ API OK')"
```

### Data not loading
```bash
# Generate fresh data
python scripts/generate_demo_data.py

# Check file permissions
ls -la data/
```

---

## 📊 Performance Tips

- Use Gemini API (faster, more quota)
- Cache data with @st.cache_resource
- Limit historical data to last 12 months
- Use indexed columns in CSV
- Consider database for large datasets

---

For production deployments, also consider:
- Load balancer
- Database backend (PostgreSQL)
- Caching layer (Redis)
- CDN for static assets
- Backup strategy
- Disaster recovery plan
