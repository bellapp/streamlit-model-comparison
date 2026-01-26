# 🐟 Streamlit Cloud Deployment Guide

Complete guide for deploying the Model Comparison App to Streamlit Cloud using the **bellapp** GitHub account.

---

## 📋 Prerequisites

✅ GitHub account: **bellapp**  
✅ Repository: `https://github.com/bellapp/wiggli-labs-test`  
✅ Streamlit Cloud account (sign up at https://streamlit.io/cloud)  
✅ API keys for: TurboPuffer, Vertex AI, Voyage AI, OpenAI  

---

## 🚀 Deployment Steps

### Step 1: Push Code to GitHub

```bash
cd /home/abdelaazizbellout/Projects/wiggli-labs-test

# Stage files for commit
git add vector_turbopuffer/streamlit_model_comparison/

# Commit changes
git commit -m "Add model comparison Streamlit app with cloud deployment support"

# Push to GitHub
git push origin main
```

### Step 2: Connect to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with **GitHub** (authorize access to bellapp repositories)
3. Click **"New app"**

### Step 3: Configure App Settings

Fill in the deployment form:

| Field | Value |
|-------|-------|
| **Repository** | `bellapp/wiggli-labs-test` |
| **Branch** | `main` |
| **Main file path** | `vector_turbopuffer/streamlit_model_comparison/app.py` |
| **App URL** (custom) | `your-custom-name` (optional) |
| **Python version** | `3.10` or `3.11` |

### Step 4: Configure Secrets

Click **"Advanced settings"** → **"Secrets"**

Copy and paste the content below, **replacing with your actual values**:

```toml
# TurboPuffer API Key
TURBOPUFFER_API_KEY = "your_actual_turbopuffer_api_key"

# Vertex AI Configuration
VERTEX_PROJECT_ID = "gen-lang-client-0683226472"
VERTEX_REGION = "us-central1"
VERTEX_MODEL_NAME = "text-multilingual-embedding-002"

# Vertex AI Service Account (TOML format for Streamlit secrets)
# IMPORTANT: Get the actual values from your service account JSON file
[VERTEX_SERVICE_ACCOUNT]
type = "service_account"
project_id = "gen-lang-client-0683226472"
private_key_id = "paste_your_private_key_id_here"
private_key = "-----BEGIN PRIVATE KEY-----\nPASTE_YOUR_FULL_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "paste_your_service_account_email@project.iam.gserviceaccount.com"
client_id = "paste_your_client_id_here"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "paste_your_cert_url_here"
universe_domain = "googleapis.com"

# Voyage AI
VOYAGE_API_KEY = "paste_your_voyage_api_key"

# OpenAI
OPENAI_API_KEY = "paste_your_openai_api_key"

# Default Namespaces - Titles
GEMINI_TITLES_NAMESPACE = "compare-titles-vertex-multilingual-v4-20260125"
VOYAGE_TITLES_NAMESPACE = "compare-titles-voyage-4-profile_v4-20260122_152531"
OPENAI_TITLES_NAMESPACE = "compare-titles-openai-small-profile_v4-20260122_152429"

# Default Namespaces - Skills
GEMINI_SKILLS_NAMESPACE = "compare-skills-v12-vertex-multilingual-20260126"
VOYAGE_SKILLS_NAMESPACE = "compare-skills-v12-voyage-4-profile_v4-20260126_100700"
OPENAI_SKILLS_NAMESPACE = "compare-skills-v12-openai-small-profile_v4-20260126_100700"

# TurboPuffer Region
DEFAULT_REGION = "aws-us-east-1"
```

#### 🔑 How to Get Vertex AI Service Account JSON Values

From your local file:
```bash
cat /home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/batch_pipeline/gen-lang-client-0683226472-915fd4f9a2a7.json
```

Copy each field from the JSON and paste into the TOML format above:
- `type` → typically "service_account"
- `project_id` → your GCP project ID
- `private_key_id` → the key ID string
- `private_key` → **entire** private key (keep the `\n` characters!)
- `client_email` → service account email
- `client_id` → numeric client ID
- etc.

**CRITICAL**: The `private_key` must be on a single line with `\n` for newlines:
```toml
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n"
```

### Step 5: Deploy!

1. Click **"Deploy"**
2. Wait for build to complete (2-5 minutes)
3. App will auto-launch when ready

---

## ✅ Verify Deployment

Once deployed, test the following:

### Basic Functionality
- [ ] App loads without errors
- [ ] Sidebar shows configuration options
- [ ] No missing API key errors

### Model Embedding
- [ ] Vertex AI embeddings generate successfully
- [ ] Voyage AI embeddings generate successfully
- [ ] OpenAI embeddings generate successfully

### Search Functionality
- [ ] Titles search works
- [ ] Skills search works
- [ ] Results display properly
- [ ] Slider and number input sync correctly

### Error Handling
- [ ] Dimension mismatch errors show helpful messages
- [ ] Rate limit errors trigger retry logic

---

## 🔧 Troubleshooting

### Issue: "TURBOPUFFER_API_KEY not found"

**Solution**: Add the key to Streamlit secrets:
1. Go to app settings → Secrets
2. Add: `TURBOPUFFER_API_KEY = "your_key"`
3. Save and reboot app

### Issue: "Unable to authenticate your request" (Vertex AI)

**Solution**: Check service account JSON in secrets:
1. Verify `VERTEX_SERVICE_ACCOUNT` section is complete
2. Ensure `private_key` has proper `\n` characters
3. Check `client_email` is correct
4. Verify `project_id` matches your GCP project

**Alternative**: Use Application Default Credentials:
- Set up ADC in Streamlit Cloud (advanced, not recommended)

### Issue: "Dimension mismatch" errors

**Solution**: Verify namespace dimensions:
1. Check your TurboPuffer namespaces
2. Ensure they match:
   - Vertex AI: 768 dimensions
   - Voyage: 1024 dimensions
   - OpenAI: 1536 dimensions

### Issue: Build fails with import errors

**Solution**: Check `requirements.txt`:
```bash
streamlit>=1.28.0
turbopuffer>=0.1.0
voyageai>=0.2.0
google-genai>=1.0.0
openai>=1.0.0
python-dotenv>=1.0.0
pandas>=2.0.0
matplotlib>=3.5.0
```

### Issue: App runs locally but not on cloud

**Solution**: 
1. Check you're using `get_env()` not `os.getenv()` for secrets
2. Verify all required secrets are in Streamlit Cloud
3. Check app logs in Streamlit Cloud dashboard

---

## 🔄 Updating the App

### Update Code

```bash
# Make changes locally
nano /home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/streamlit_model_comparison/app.py

# Test locally
cd vector_turbopuffer/streamlit_model_comparison
./run.sh

# Commit and push
git add .
git commit -m "Update model comparison app"
git push origin main

# Streamlit Cloud will auto-deploy changes!
```

### Update Secrets

1. Go to Streamlit Cloud dashboard
2. Select your app
3. Settings → Secrets
4. Update values
5. Save → App will automatically reboot

---

## 📊 App URLs

After deployment, your app will be available at:

**Public URL**: `https://share.streamlit.io/bellapp/wiggli-labs-test/main/vector_turbopuffer/streamlit_model_comparison/app.py`

**Custom URL** (if configured): `https://your-custom-name.streamlit.app`

---

## 🌟 Features Deployed

✅ **3-Model Comparison**: Vertex AI, Voyage, OpenAI  
✅ **Dual Search**: Titles and Skills  
✅ **Flexible Input**: Slider + Number input (1-1000 results)  
✅ **Enter Key Search**: Press Enter to start  
✅ **Smart Errors**: Helpful dimension mismatch messages  
✅ **Retry Logic**: Automatic retry on rate limits  
✅ **Clean UI**: Hidden comparison summary  
✅ **Dark Theme**: Modern Streamlit theme  

---

## 📝 Security Best Practices

### ✅ DO:
- Store ALL API keys in Streamlit secrets
- Use `.gitignore` to exclude `.env` files
- Never commit service account JSON files
- Use environment variables for configuration

### ❌ DON'T:
- Commit `.env` files to git
- Hardcode API keys in source code
- Share your secrets.toml publicly
- Push service account files to GitHub

---

## 📚 Additional Resources

- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Secrets Management**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- **Vertex AI Setup**: `/vector_turbopuffer/streamlit_model_comparison/AUTHENTICATION.md`
- **App Documentation**: `/vector_turbopuffer/streamlit_model_comparison/README.md`

---

## 🎉 You're Done!

Your Model Comparison App is now live on Streamlit Cloud! 🚀

**Share the URL** with your team to start comparing embedding models side-by-side.

---

**Last Updated**: January 2026  
**Deployed By**: bellapp GitHub account  
**Deployed To**: Streamlit Cloud
