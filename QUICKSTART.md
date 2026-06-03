# Quick Start Guide

## 1️⃣ Installation (5 min)

```bash
# Clone
git clone https://github.com/your-username/enterprise-ai-accounting-finance-assistant.git
cd enterprise-ai-accounting-finance-assistant

# Python env
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Dependencies
pip install -r requirements.txt
```

## 2️⃣ Get API Key (2 min)

**Option A: Gemini (Recommended)**
- Go to https://aistudio.google.com/app/apikey
- Click "Create API Key"
- Copy the key

**Option B: Groq**
- Go to https://console.groq.com/keys
- Create key
- Copy it

## 3️⃣ Configure (1 min)

```bash
# Copy template
cp .env.example .env

# Edit .env with your key
# Linux/Mac:
nano .env

# Windows:
# Right-click .env > Edit
```

Example .env:
```
AI_PROVIDER=gemini
GEMINI_API_KEY=YOUR_KEY_HERE
```

## 4️⃣ Generate Demo Data (2 min)

```bash
python scripts/generate_demo_data.py
```

Creates realistic 12-month financial data in `data/` folder.

## 5️⃣ Build Vector Store (optional, for Chat)

```bash
python scripts/build_vector_store.py
```

Creates ChromaDB store for RAG questions. Takes ~30 sec.

## 6️⃣ Run App (1 min)

```bash
streamlit run app.py
```

App opens at: http://localhost:8501

## ✨ Try These First

### On Home Page
- See configuration status
- Check data loaded

### On Chat IA Page
- Ask: "What is the monthly close procedure?"
- Ask: "What accounting controls must we do?"

### On Comptabilité Page
- See balance sheet
- View account balances
- Check for anomalies

### On Fournisseurs Page
- See top suppliers
- Check overdue invoices
- Payment performance

### On Trésorerie Page
- Cash flow trend
- 30-day forecast
- Reconciliation status

### On Budget Page
- Budget vs Real by cost center
- Variance analysis
- Monthly trends

## 🆘 Troubleshooting

### "streamlit: command not found"
```bash
# Make sure you're in venv
source venv/bin/activate
pip install streamlit
```

### "API key not configured"
- Check .env file exists
- Check GEMINI_API_KEY or GROQ_API_KEY is set
- No spaces around = sign

### "No data found"
```bash
# Run data generator
python scripts/generate_demo_data.py
# Check data/ folder has CSV files
ls data/
```

### "Chat not working"
```bash
# Build vector store
python scripts/build_vector_store.py
# Check docs/ folder has markdown files
ls docs/
```

## 🚀 Next Steps

1. **Customize data**: Edit `scripts/generate_demo_data.py`
2. **Add procedures**: Add .md files to `docs/` folder
3. **Extend analyzers**: Add methods to analyzer classes in `src/`
4. **Connect real data**: Replace CSV loader with database/API
5. **Deploy**: Push to GitHub → Streamlit Cloud (free!)

## 📚 Full Documentation

- [README.md](README.md) - Complete guide
- [Architecture](assets/architecture_description.md) - Technical details
- [Power BI Guide](powerbi/README_powerbi.md) - For dashboards

## 💡 Pro Tips

- Use Gemini API (more generous free tier)
- Keep .env in .gitignore (done!)
- Generate fresh data weekly for demos
- Explore RAG with questions about your domain

---

**Questions?** Check README.md or raise an issue on GitHub!
