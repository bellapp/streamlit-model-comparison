# Vertex AI Authentication Guide

## 🐟 Quick Setup (Recommended)

Your service account file exists at:
```
/home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/batch_pipeline/gen-lang-client-0683226472-915fd4f9a2a7.json
```

### Option 1: Update `.env` with Full Path ✅ (Easiest)

Edit your `.env` file:
```bash
VERTEX_SERVICE_ACCOUNT_FILE=/home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/batch_pipeline/gen-lang-client-0683226472-915fd4f9a2a7.json
```

### Option 2: Copy File to App Directory

```bash
cd /home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/streamlit_model_comparison
cp ../batch_pipeline/gen-lang-client-0683226472-915fd4f9a2a7.json .
```

Then in `.env`:
```bash
VERTEX_SERVICE_ACCOUNT_FILE=gen-lang-client-0683226472-915fd4f9a2a7.json
```

### Option 3: Use gcloud CLI

```bash
gcloud auth application-default login
```

Then remove or comment out `VERTEX_SERVICE_ACCOUNT_FILE` from `.env`.

### Option 4: Environment Variable

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/batch_pipeline/gen-lang-client-0683226472-915fd4f9a2a7.json
```

## 🔍 How the App Finds Your Service Account

The app automatically searches for your service account file in these locations (in order):

1. **Exact path** from `VERTEX_SERVICE_ACCOUNT_FILE`
2. **Absolute path** (if relative path provided)
3. **Relative to app directory** (`streamlit_model_comparison/`)
4. **Relative to batch_pipeline** (`../batch_pipeline/`)
5. **Current working directory**

## ✅ Verify Authentication

After updating your `.env`, test it:

```bash
cd /home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/streamlit_model_comparison
./run.sh
```

You should see the app load without authentication errors!

## 🚨 Troubleshooting

### Error: "Unable to authenticate your request"
- Check that `VERTEX_SERVICE_ACCOUNT_FILE` path is correct
- Verify the JSON file exists and is readable
- Ensure the service account has necessary permissions

### Error: "Service account file not found"
- Use the full absolute path in `.env`
- Or copy the file to the app directory

### Error: "Permission denied"
- Check file permissions: `chmod 600 your-service-account.json`
- Verify you're the owner: `ls -la your-service-account.json`

## 📋 Current Configuration

Your current `.env` has:
```
VERTEX_PROJECT_ID=gen-lang-client-0683226472
VERTEX_REGION=us-central1
VERTEX_SERVICE_ACCOUNT_FILE=gen-lang-client-0683226472-915fd4f9a2a7.json  # ← Update this to full path!
VERTEX_MODEL_NAME=text-multilingual-embedding-002
```

## 🎯 Recommended Fix

**Update line 17 in your `.env`:**

```bash
# OLD
VERTEX_SERVICE_ACCOUNT_FILE=gen-lang-client-0683226472-915fd4f9a2a7.json

# NEW
VERTEX_SERVICE_ACCOUNT_FILE=/home/abdelaazizbellout/Projects/wiggli-labs-test/vector_turbopuffer/batch_pipeline/gen-lang-client-0683226472-915fd4f9a2a7.json
```

Then restart the app!
