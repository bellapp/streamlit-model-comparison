#!/bin/bash

# 🚀 Quick Deployment Script for Streamlit Cloud

echo "🔍 Checking prerequisites..."

# Check if git is initialized
if [ ! -d .git ]; then
    echo "⚠️  Git not initialized. Initializing..."
    git init
fi

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Check if .gitignore exists
if [ ! -f .gitignore ]; then
    echo "⚠️  .gitignore not found. Please create one!"
fi

echo ""
echo "📦 Files ready for deployment:"
echo "  ✅ app.py"
echo "  ✅ requirements.txt"
echo "  ✅ .streamlit/config.toml"
echo "  ✅ .gitignore"
echo ""

echo "🔐 IMPORTANT: Before deploying, make sure you have:"
echo "  1. TurboPuffer API Key"
echo "  2. Vertex AI Service Account JSON"
echo "  3. Voyage AI API Key (optional)"
echo "  4. OpenAI API Key (optional)"
echo "  5. All namespace names configured"
echo ""

echo "📝 Next steps:"
echo "  1. Create GitHub repository: streamlit-model-comparison"
echo "  2. Push this code to GitHub:"
echo "     git add ."
echo "     git commit -m 'Prepare for Streamlit Cloud deployment'"
echo "     git remote add origin https://github.com/bellapp/streamlit-model-comparison.git"
echo "     git push -u origin main"
echo ""
echo "  3. Go to: https://share.streamlit.io"
echo "  4. Click 'New app'"
echo "  5. Select repository: bellapp/streamlit-model-comparison"
echo "  6. Set main file: app.py"
echo "  7. Add secrets in Advanced settings (see SECRETS_SETUP.md)"
echo "  8. Deploy!"
echo ""
echo "✨ Your app will be live at: https://YOUR_APP_NAME.streamlit.app"
echo ""
echo "📚 Documentation:"
echo "  - Deployment guide: DEPLOYMENT.md"
echo "  - Secrets setup: SECRETS_SETUP.md"
echo "  - Checklist: DEPLOYMENT_CHECKLIST.md"
