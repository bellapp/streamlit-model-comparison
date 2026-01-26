# 🐟 Streamlit Cloud Deployment Checklist

Use this checklist to ensure smooth deployment to Streamlit Cloud.

---

## 📋 Pre-Deployment Checklist

### Local Testing
- [ ] App runs locally without errors (`./run.sh`)
- [ ] All 3 models work (Vertex AI, Voyage, OpenAI)
- [ ] Titles search works
- [ ] Skills search works
- [ ] Slider and number input sync correctly
- [ ] Enter key triggers search
- [ ] No console errors or warnings

### Code Preparation
- [ ] All secrets use `get_env()` instead of `os.getenv()`
- [ ] No hardcoded API keys in code
- [ ] `.gitignore` excludes sensitive files
- [ ] `requirements.txt` includes all dependencies
- [ ] No deprecated packages (use `google-genai`, not `google-cloud-aiplatform`)

### Files Ready
- [ ] `app.py` - Main application file ✅
- [ ] `requirements.txt` - Dependencies ✅
- [ ] `.gitignore` - Excludes secrets ✅
- [ ] `.streamlit/config.toml` - Theme configuration ✅
- [ ] `README.md` - Documentation ✅
- [ ] `DEPLOYMENT.md` - Deployment guide ✅
- [ ] `SECRETS_SETUP.md` - Secrets configuration guide ✅

### Secrets Gathered
- [ ] `TURBOPUFFER_API_KEY` copied
- [ ] Vertex AI service account JSON file read
- [ ] `VOYAGE_API_KEY` copied
- [ ] `OPENAI_API_KEY` copied
- [ ] All namespace names copied from `.env`

---

## 🚀 Deployment Steps

### Step 1: Push to GitHub ✅

```bash
cd /home/abdelaazizbellout/Projects/wiggli-labs-test

# Review changes
git status vector_turbopuffer/streamlit_model_comparison/

# Stage all files
git add vector_turbopuffer/streamlit_model_comparison/

# Commit
git commit -m "Add Streamlit model comparison app for cloud deployment

- Compare Vertex AI, Voyage, OpenAI embeddings side-by-side
- Support for both titles and skills search
- Slider + number input for results (1-1000)
- Enter key search functionality
- Migrated to new Google Gen AI SDK
- Streamlit Cloud secrets support
- Comprehensive deployment documentation"

# Push to bellapp repository
git push origin main
```

**Status**: ⏳ Waiting for execution

### Step 2: Create Streamlit Cloud App 🌐

1. Go to https://share.streamlit.io/
2. Sign in with **bellapp** GitHub account
3. Click **"New app"**
4. Configure:
   - Repository: `bellapp/wiggli-labs-test`
   - Branch: `main`
   - Main file: `vector_turbopuffer/streamlit_model_comparison/app.py`
   - Python: `3.10` or `3.11`

**Status**: ⏳ Pending

### Step 3: Configure Secrets 🔑

Follow [SECRETS_SETUP.md](./SECRETS_SETUP.md) to add all secrets:

- [ ] `TURBOPUFFER_API_KEY`
- [ ] `VERTEX_PROJECT_ID`
- [ ] `VERTEX_REGION`
- [ ] `VERTEX_MODEL_NAME`
- [ ] `[VERTEX_SERVICE_ACCOUNT]` section (all fields)
- [ ] `VOYAGE_API_KEY`
- [ ] `OPENAI_API_KEY`
- [ ] All 6 namespace configurations
- [ ] `DEFAULT_REGION`

**Status**: ⏳ Pending

### Step 4: Deploy 🚀

1. Click **"Deploy"** in Streamlit Cloud
2. Wait for build (2-5 minutes)
3. Monitor logs for errors

**Status**: ⏳ Pending

---

## ✅ Post-Deployment Verification

### Functional Testing
- [ ] App loads without authentication errors
- [ ] Sidebar shows all configuration options
- [ ] Vertex AI model initializes successfully
- [ ] Voyage AI model initializes successfully
- [ ] OpenAI model initializes successfully

### Search Testing
- [ ] **Titles search**: Enter a job title, press Enter
  - [ ] Vertex AI returns results
  - [ ] Voyage returns results
  - [ ] OpenAI returns results
  - [ ] Results display correctly
  - [ ] Scores show distance metrics

- [ ] **Skills search**: Select "Skills", enter a skill
  - [ ] Vertex AI returns results
  - [ ] Voyage returns results
  - [ ] OpenAI returns results
  - [ ] Results display correctly

### UI Testing
- [ ] Slider works (drag to change results)
- [ ] Number input works (type to change results)
- [ ] Slider and number input stay synchronized
- [ ] Enter key triggers search
- [ ] Results limit adjustable (1-1000)
- [ ] Comparison summary is hidden
- [ ] Dark theme applied correctly

### Error Handling Testing
- [ ] Dimension mismatch shows helpful error
- [ ] Rate limits trigger retry logic
- [ ] Invalid namespace shows clear error
- [ ] Missing API key shows helpful message

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Authentication error (Vertex AI) | Check `VERTEX_SERVICE_ACCOUNT` in secrets, verify `private_key` format |
| "API key not found" | Verify secret name matches exactly (case-sensitive) |
| Dimension mismatch | Confirm namespace dimensions match model (768/1024/1536) |
| Import errors | Check `requirements.txt` has all packages with correct versions |
| App won't start | Check logs in Streamlit Cloud dashboard |
| Secrets not loading | Ensure using `get_env()`, not `os.getenv()` |

---

## 📊 Performance Benchmarks

Expected performance after deployment:

| Metric | Target | Notes |
|--------|--------|-------|
| **Cold start** | < 30s | First load after deployment |
| **Warm load** | < 5s | Subsequent page loads |
| **Search latency** | 1-3s | Per model, 10 results |
| **Memory usage** | < 500MB | Streamlit default limit |
| **Concurrent users** | 10+ | Free tier supports multiple users |

---

## 🎯 Success Criteria

Deployment is successful when:

✅ App URL is publicly accessible  
✅ All 3 models authenticate successfully  
✅ Searches return correct results  
✅ No errors in Streamlit Cloud logs  
✅ UI is responsive and functional  
✅ Enter key triggers search  
✅ Results limit slider/input works  

---

## 📝 Deployment Notes

**Repository**: `https://github.com/bellapp/wiggli-labs-test`  
**Branch**: `main`  
**App Path**: `vector_turbopuffer/streamlit_model_comparison/app.py`  
**Python Version**: `3.10` or `3.11`  
**Dependencies**: 8 packages (see `requirements.txt`)  

**Models**:
- Vertex AI: `text-multilingual-embedding-002` (768d)
- Voyage AI: `voyage-4` (1024d)
- OpenAI: `text-embedding-3-small` (1536d)

**Features**:
- Dual search (Titles & Skills)
- 3-model comparison
- Results limit: 1-1000
- Enter key search
- Synchronized slider/input
- Clean UI (hidden comparison summary)

---

## 🔄 Update Workflow

After deployment, to update the app:

```bash
# Make changes locally
nano app.py

# Test locally
./run.sh

# Commit and push
git add .
git commit -m "Update: [description]"
git push origin main

# Streamlit Cloud auto-deploys! ✨
```

To update secrets:
1. Streamlit Cloud dashboard → Settings → Secrets
2. Edit values
3. Save → Auto-reboot

---

## 📈 Monitoring

After deployment, monitor:

- **Streamlit Cloud Dashboard**: App status, logs, resource usage
- **GitHub Actions**: Build status (if configured)
- **App Logs**: Check for errors or warnings
- **User Feedback**: Test with actual users

---

## 🎉 Completion

When all checkboxes are ✅, your app is:

🌐 **Live** on Streamlit Cloud  
🔐 **Secure** with proper secrets management  
⚡ **Fast** and responsive  
📊 **Functional** with all features working  
📚 **Documented** for future updates  

**Congratulations!** Your Model Comparison App is production-ready! 🚀

---

**Last Updated**: January 2026  
**Deployed By**: bellapp  
**Platform**: Streamlit Cloud
