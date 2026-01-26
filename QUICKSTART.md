# 🐟 Quick Start - Streamlit Model Comparison Deploy

This is a **standalone deployment repository** for the Streamlit Model Comparison App.

---

## 📁 Repository Structure

```
streamlit_model_comparison_deploy/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── deploy.sh                # Deployment helper script
├── .gitignore               # Git ignore rules
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── env_example.txt         # Environment variables template
├── README.md               # Full documentation
├── DEPLOYMENT.md           # Deployment guide
├── SECRETS_SETUP.md        # Secrets configuration
├── DEPLOYMENT_CHECKLIST.md # Step-by-step checklist
└── AUTHENTICATION.md      # Vertex AI auth guide
```

---

## 🚀 Quick Deploy (3 Steps)

### Step 1: Initialize Git Repository

```bash
cd /home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/streamlit_model_comparison_deploy

# Initialize git (if not already done)
git init

# Or run the deploy script
./deploy.sh
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `streamlit-model-comparison`
3. Owner: `bellapp`
4. Description: "Compare embedding models (Vertex AI, Voyage, OpenAI) side-by-side"
5. Visibility: **Public** (or Private if preferred)
6. **Don't** initialize with README, .gitignore, or license
7. Click **"Create repository"**

### Step 3: Push to GitHub

```bash
cd /home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/streamlit_model_comparison_deploy

# Add all files
git add .

# Commit
git commit -m "Initial commit: Streamlit Model Comparison App

Features:
- Compare Vertex AI, Voyage, OpenAI embeddings
- Titles and Skills search
- Slider + number input (1-1000 results)
- Enter key search
- New Google Gen AI SDK"

# Add remote (replace YOUR_USERNAME if different)
git remote add origin https://github.com/bellapp/streamlit-model-comparison.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🌐 Deploy to Streamlit Cloud

### Option A: Using deploy.sh

```bash
./deploy.sh
```

Follow the instructions it prints.

### Option B: Manual Steps

1. **Go to Streamlit Cloud**: https://share.streamlit.io
2. **Sign in** with GitHub (bellapp account)
3. **Click "New app"**
4. **Configure**:
   - Repository: `bellapp/streamlit-model-comparison`
   - Branch: `main`
   - Main file: `app.py`
   - Python version: `3.10` or `3.11`
5. **Add Secrets** (see [SECRETS_SETUP.md](./SECRETS_SETUP.md)):
   - `TURBOPUFFER_API_KEY`
   - `[VERTEX_SERVICE_ACCOUNT]` section
   - `VOYAGE_API_KEY` (optional)
   - `OPENAI_API_KEY` (optional)
   - All namespace configurations
6. **Click "Deploy"**
7. **Wait** 2-5 minutes for build
8. **Done!** 🎉

---

## 🔐 Required Secrets

Before deploying, you need these API keys:

| Secret | Required | Where to Get |
|--------|----------|--------------|
| `TURBOPUFFER_API_KEY` | ✅ Yes | https://turbopuffer.com |
| `VERTEX_SERVICE_ACCOUNT` | ✅ Yes | Google Cloud Console |
| `VOYAGE_API_KEY` | ⚠️ Optional | https://voyageai.com |
| `OPENAI_API_KEY` | ⚠️ Optional | https://platform.openai.com |

**See [SECRETS_SETUP.md](./SECRETS_SETUP.md) for detailed setup instructions.**

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](./README.md) | Full app documentation |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Complete deployment guide |
| [SECRETS_SETUP.md](./SECRETS_SETUP.md) | Secrets configuration |
| [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) | Step-by-step checklist |
| [AUTHENTICATION.md](./AUTHENTICATION.md) | Vertex AI authentication |

---

## ✅ Pre-Deployment Checklist

- [ ] Git repository initialized
- [ ] GitHub repository created (`bellapp/streamlit-model-comparison`)
- [ ] Code pushed to GitHub
- [ ] All secrets gathered (API keys, service account)
- [ ] Streamlit Cloud account ready
- [ ] Secrets configured in Streamlit Cloud

---

## 🎯 After Deployment

Your app will be available at:

```
https://YOUR_APP_NAME.streamlit.app
```

Or the default URL:

```
https://share.streamlit.io/bellapp/streamlit-model-comparison/main/app.py
```

---

## 🆘 Troubleshooting

### "Repository not found"
- Check repository name: `bellapp/streamlit-model-comparison`
- Verify you're signed in with the correct GitHub account

### "API key not found"
- Go to Streamlit Cloud → Settings → Secrets
- Add missing keys (see [SECRETS_SETUP.md](./SECRETS_SETUP.md))

### "Build failed"
- Check `requirements.txt` has all dependencies
- Verify Python version (3.10 or 3.11)
- Check app logs in Streamlit Cloud dashboard

---

## 🔄 Updating the App

After making changes:

```bash
cd /home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/streamlit_model_comparison_deploy

# Make your changes
nano app.py  # or use your editor

# Commit and push
git add .
git commit -m "Update: [description of changes]"
git push origin main

# Streamlit Cloud will auto-deploy! ✨
```

---

## 📞 Need Help?

- **Deployment issues**: See [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Secrets setup**: See [SECRETS_SETUP.md](./SECRETS_SETUP.md)
- **Authentication**: See [AUTHENTICATION.md](./AUTHENTICATION.md)
- **Streamlit docs**: https://docs.streamlit.io

---

**Ready to deploy?** Run `./deploy.sh` or follow the steps above! 🚀
