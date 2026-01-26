# 🐟 Setting Up Streamlit Cloud Secrets

Step-by-step guide to configure secrets for deploying to Streamlit Cloud.

---

## 📋 What You Need

Before starting, gather these credentials:

✅ **TurboPuffer API Key** - Get from https://turbopuffer.com  
✅ **Vertex AI Service Account JSON** - Located at:  
   `/home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/batch_pipeline/gen-lang-client-0683226472-915fd4f9a2a7.json`  
✅ **Voyage API Key** - Get from https://www.voyageai.com  
✅ **OpenAI API Key** - Get from https://platform.openai.com

---

## 🔑 Step 1: Get Vertex AI Service Account JSON

On your local machine, read the service account file:

```bash
cat /home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/batch_pipeline/gen-lang-client-0683226472-915fd4f9a2a7.json
```

You'll see something like:

```json
{
  "type": "service_account",
  "project_id": "gen-lang-client-0683226472",
  "private_key_id": "915fd4f9a2a7...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBg...\n-----END PRIVATE KEY-----\n",
  "client_email": "vertex-embeddings@gen-lang-client-0683226472.iam.gserviceaccount.com",
  "client_id": "1234567890",
  ...
}
```

**Keep this open** - you'll need these values in Step 3.

---

## 🚀 Step 2: Access Streamlit Cloud Secrets

1. Go to https://share.streamlit.io/
2. Sign in with your **bellapp** GitHub account
3. Find your deployed app in the dashboard
4. Click **⚙️ Settings** → **Secrets**

---

## 📝 Step 3: Copy-Paste Secrets Configuration

Copy the template below and **replace the placeholder values** with your actual credentials:

```toml
# ========================================
# TURBOPUFFER CONFIGURATION
# ========================================
TURBOPUFFER_API_KEY = "tp-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DEFAULT_REGION = "aws-us-east-1"

# ========================================
# VERTEX AI CONFIGURATION
# ========================================
VERTEX_PROJECT_ID = "gen-lang-client-0683226472"
VERTEX_REGION = "us-central1"
VERTEX_MODEL_NAME = "text-multilingual-embedding-002"

# Service Account JSON as TOML
# IMPORTANT: Copy values from your local JSON file
[VERTEX_SERVICE_ACCOUNT]
type = "service_account"
project_id = "gen-lang-client-0683226472"
private_key_id = "paste_from_json_file"
private_key = "-----BEGIN PRIVATE KEY-----\nPASTE_YOUR_FULL_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "vertex-embeddings@gen-lang-client-0683226472.iam.gserviceaccount.com"
client_id = "paste_from_json_file"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "paste_from_json_file"
universe_domain = "googleapis.com"

# ========================================
# VOYAGE AI CONFIGURATION
# ========================================
VOYAGE_API_KEY = "pa-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# ========================================
# OPENAI CONFIGURATION
# ========================================
OPENAI_API_KEY = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# ========================================
# DEFAULT NAMESPACES - TITLES
# ========================================
GEMINI_TITLES_NAMESPACE = "compare-titles-vertex-multilingual-v4-20260125"
VOYAGE_TITLES_NAMESPACE = "compare-titles-voyage-4-profile_v4-20260122_152531"
OPENAI_TITLES_NAMESPACE = "compare-titles-openai-small-profile_v4-20260122_152429"

# ========================================
# DEFAULT NAMESPACES - SKILLS
# ========================================
GEMINI_SKILLS_NAMESPACE = "compare-skills-v12-vertex-multilingual-20260126"
VOYAGE_SKILLS_NAMESPACE = "compare-skills-v12-voyage-4-profile_v4-20260126_100700"
OPENAI_SKILLS_NAMESPACE = "compare-skills-v12-openai-small-profile_v4-20260126_100700"
```

---

## ⚠️ Critical: Private Key Format

The `private_key` field is **the most common source of errors**. Follow these rules:

### ✅ CORRECT Format:

```toml
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n"
```

**Key points:**
- Single line (no line breaks in the string itself)
- Use `\n` for newlines (backslash-n)
- Keep `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----`
- Quote marks on both ends

### ❌ WRONG Format:

```toml
# DON'T DO THIS - Multi-line won't work in TOML
private_key = "-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...
-----END PRIVATE KEY-----"
```

---

## 🔄 Step 4: Convert JSON to TOML

Here's how to map each field from your JSON file:

| JSON Field | TOML Field | Example |
|------------|-----------|---------|
| `"type"` | `type = "..."` | `type = "service_account"` |
| `"project_id"` | `project_id = "..."` | `project_id = "gen-lang-client-0683226472"` |
| `"private_key_id"` | `private_key_id = "..."` | `private_key_id = "915fd4f9a2a7..."` |
| `"private_key"` | `private_key = "..."` | **See format above** |
| `"client_email"` | `client_email = "..."` | `client_email = "vertex@...iam.gserviceaccount.com"` |
| `"client_id"` | `client_id = "..."` | `client_id = "1234567890"` |
| `"auth_uri"` | `auth_uri = "..."` | Usually `"https://accounts.google.com/o/oauth2/auth"` |
| `"token_uri"` | `token_uri = "..."` | Usually `"https://oauth2.googleapis.com/token"` |
| `"auth_provider_x509_cert_url"` | `auth_provider_x509_cert_url = "..."` | Usually `"https://www.googleapis.com/oauth2/v1/certs"` |
| `"client_x509_cert_url"` | `client_x509_cert_url = "..."` | Paste from JSON |
| `"universe_domain"` | `universe_domain = "..."` | Usually `"googleapis.com"` |

---

## 🧪 Step 5: Test in Python (Optional)

If you want to verify your TOML format locally before deploying:

```python
import toml

secrets_content = """
[VERTEX_SERVICE_ACCOUNT]
type = "service_account"
project_id = "gen-lang-client-0683226472"
private_key = "-----BEGIN PRIVATE KEY-----\\nYOUR_KEY\\n-----END PRIVATE KEY-----\\n"
...
"""

# Parse TOML
config = toml.loads(secrets_content)
print(config['VERTEX_SERVICE_ACCOUNT'])
```

If it prints without errors, your format is correct!

---

## ✅ Step 6: Save and Deploy

1. **Paste** your completed secrets into Streamlit Cloud
2. Click **"Save"**
3. Streamlit will automatically **reboot** your app
4. Check app logs for any authentication errors

---

## 🐛 Troubleshooting

### Error: "Unable to authenticate your request"

**Cause**: Service account credentials are incorrect or malformed.

**Solutions**:
1. Double-check `private_key` format (must be single line with `\n`)
2. Verify `client_email` matches your service account
3. Confirm `project_id` is correct
4. Make sure quotes are properly closed

### Error: "TURBOPUFFER_API_KEY not found"

**Cause**: Secret name mismatch or typo.

**Solution**: Ensure the secret is named exactly `TURBOPUFFER_API_KEY` (case-sensitive)

### Error: "Dimension mismatch"

**Cause**: Namespace doesn't match the model dimensions.

**Solution**: 
- Verify Vertex AI namespaces use 768 dimensions
- Verify Voyage namespaces use 1024 dimensions
- Verify OpenAI namespaces use 1536 dimensions

### Error: "Module 'toml' not found"

**Cause**: Testing script missing dependency.

**Solution**: `pip install toml` (only needed for local testing)

---

## 🔐 Security Checklist

Before deploying:

- [ ] **Never** commit `.env` files to git
- [ ] **Never** commit service account JSON files to git
- [ ] `.gitignore` includes `.env` and `*.json`
- [ ] All secrets are in Streamlit Cloud secrets, not in code
- [ ] Service account has **minimal permissions** (only what's needed)
- [ ] API keys are from **production** accounts (not test keys)

---

## 📚 Quick Reference

| Secret Type | Format | Where to Get It |
|-------------|--------|-----------------|
| `TURBOPUFFER_API_KEY` | `"tp-..."` | https://turbopuffer.com/settings |
| `VERTEX_SERVICE_ACCOUNT` | TOML section | Local JSON file |
| `VOYAGE_API_KEY` | `"pa-..."` | https://www.voyageai.com/dashboard |
| `OPENAI_API_KEY` | `"sk-proj-..."` | https://platform.openai.com/api-keys |
| Namespace names | `"compare-..."` | Your `.env` file |

---

## 🎉 You're Ready!

Once all secrets are configured correctly, your app will:

✅ Authenticate with Vertex AI  
✅ Connect to TurboPuffer  
✅ Generate embeddings with all 3 models  
✅ Run searches successfully  

**Next**: Follow the [DEPLOYMENT.md](./DEPLOYMENT.md) guide to complete the deployment!

---

**Need Help?**
- Streamlit Secrets Docs: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- Vertex AI Auth: https://cloud.google.com/docs/authentication
- TOML Format: https://toml.io/
