# 🐟 Model Comparison Tool

A Streamlit application to compare search results from different embedding models (Gemini, Voyage, OpenAI) side-by-side using TurboPuffer namespaces.

## Features

- **Multi-Model Comparison**: Compare results from up to 3 different embedding models simultaneously
- **Titles & Skills Search**: Search for both job titles and skills with separate namespaces
- **Side-by-Side Display**: View results from each model in parallel columns for easy comparison
- **Performance Metrics**: Track and compare average distances, search times, and result counts
- **Visual Scoring**: Color-coded distances (excellent/good/fair) for quick quality assessment
- **Export Results**: Download comparison results as JSON for further analysis
- **Flexible Configuration**: Easily configure namespaces and search parameters
- **Environment Defaults**: Pre-configure namespaces in `.env` for quick access

## Supported Models

1. **Vertex AI** (via Google Gen AI SDK)
   - Model: `text-multilingual-embedding-002`
   - Dimensions: **768 (fixed)**
   - Multilingual: 100+ languages
   - Enterprise-ready with GCP authentication

2. **Voyage AI** (`voyage-4`)
   - Dimensions: **1024**
   - High-quality semantic search

3. **OpenAI** (`text-embedding-3-small`)
   - Dimensions: **1536**
   - Fast and cost-effective
   
**⚠️ Important**: 
- Each model produces different dimension sizes
- Embeddings from different models are NOT interchangeable
- Vertex AI uses the NEW Google Gen AI SDK (replaces deprecated Vertex AI SDK)

## Installation

1. **Clone or navigate to the project directory**

```bash
cd streamlit_model_comparison
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Copy the `env_example.txt` file to `.env` and fill in your API keys:

```bash
cp env_example.txt .env
```

Edit `.env` with your actual API keys:

```env
# Required API Keys
GOOGLE_API_KEY=your_google_api_key_here
VOYAGE_API_KEY=your_voyage_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
TURBOPUFFER_API_KEY=your_turbopuffer_api_key_here

# Optional: Set default namespaces to avoid entering them each time
GEMINI_NAMESPACE=compare-titles-gemini-profile_v4-20250122
VOYAGE_NAMESPACE=compare-titles-voyage-profile_v4-20250122
OPENAI_NAMESPACE=compare-titles-openai-small-profile_v4-20250122
TURBOPUFFER_REGION=aws-us-east-1
```

## Usage

### 1. Start the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 2. Configure Namespaces

**Option A: Set in `.env` file (Recommended)**

Add your namespace names to `.env` - they'll be loaded automatically.

For **Titles** search:
```env
GEMINI_TITLES_NAMESPACE=compare-titles-gemini-profile_v12-20250126
VOYAGE_TITLES_NAMESPACE=compare-titles-voyage-profile_v12-20250126
OPENAI_TITLES_NAMESPACE=compare-titles-openai-small-profile_v12-20250126
```

For **Skills** search:
```env
GEMINI_SKILLS_NAMESPACE=compare-skills-gemini-profile_v12-20250126
VOYAGE_SKILLS_NAMESPACE=compare-skills-voyage-profile_v12-20250126
OPENAI_SKILLS_NAMESPACE=compare-skills-openai-small-profile_v12-20250126
```

**Option B: Enter in the app sidebar**

If not set in `.env`, or to override the defaults, enter namespaces in the sidebar:
- **Gemini Namespace**: e.g., `compare-titles-gemini-profile_v4-20250122`
- **Voyage Namespace**: e.g., `compare-titles-voyage-profile_v4-20250122`
- **OpenAI Namespace**: e.g., `compare-titles-openai-small-profile_v4-20250122`

You can configure 1, 2, or all 3 models.

### 3. Select Search Type

Choose what you want to search for:
- **Titles**: Job titles like "Senior Python Developer", "Data Scientist"
- **Skills**: Technical skills like "Python", "React", "Machine Learning"

The app will automatically load the appropriate namespaces based on your selection.

### 4. Enter Search Query

Type your query in the search box. Examples:

**For Titles:**
- "Senior Python Developer"
- "Full Stack Engineer"
- "Data Scientist"

**For Skills:**
- "Python"
- "React.js"
- "Machine Learning"

### 5. Compare Results

Click **"🚀 Compare Models"** to:
- Generate embeddings for your query using each model
- Search the corresponding TurboPuffer namespace
- Display results side-by-side with scores
- Show performance metrics and comparison summary

## Understanding the Results

### Score Colors (Cosine Distance)
**Important**: TurboPuffer uses cosine_distance where **lower is better** (range: 0-2)
- 🟢 **Green (Excellent)**: Distance ≤ 0.3 - Very strong match
- 🟡 **Yellow (Good)**: Distance ≤ 0.7 - Good match
- 🔴 **Red (Fair)**: Distance > 0.7 - Weaker match

### Important Notes
- **Gemini** (`gemini-embedding-001`) and **OpenAI** (`text-embedding-3-small`) both produce 1536-dimensional vectors
- However, their embeddings are **NOT compatible** - you cannot mix them or compare vectors from different models
- Make sure each namespace contains vectors from only ONE model

### Metrics Displayed
- **Results Count**: Number of matches found
- **Avg Score**: Average similarity score across all results
- **Max/Min Score**: Range of similarity scores
- **Search Time**: Time taken to embed and search

### Best Model Analysis
The app automatically identifies:
- 🥇 Model with highest average score
- ⚡ Fastest model for your query

## Example Workflow

1. **Prepare Your Namespaces**
   - Run the batch pipeline to create embeddings with different models
   - Note the namespace names created for each model

2. **Compare Models**
   - Open the Streamlit app
   - Enter the namespace names in the sidebar
   - Type a search query
   - Review side-by-side results

3. **Analyze Performance**
   - Check which model finds the most relevant results
   - Compare average scores across models
   - Consider speed vs. accuracy trade-offs
   - Export results for documentation

## Advanced Configuration

### TurboPuffer Region
Select the appropriate region where your namespaces are hosted:
- `aws-eu-central-1`
- `aws-us-east-1` (default)
- `gcp-us-central1`

**Tip**: Set `TURBOPUFFER_REGION` in `.env` to pre-select your region.

### Number of Results
Adjust the slider to retrieve 1-20 results per model.

## Troubleshooting

### "No results found"
- Verify the namespace name is correct
- Ensure the namespace contains data
- Check that embeddings were successfully uploaded

### "Error with [model]"
- Verify the API key for that model is set in `.env`
- Check that the API key has sufficient credits/quota
- Ensure the model name matches the embedding model used

### Connection Errors
- Verify TURBOPUFFER_API_KEY is correct
- Check your internet connection
- Confirm the region matches where your namespaces are stored

## Architecture

```
User Query
    ↓
[Embedding Generation]
    ├─→ Gemini (768d)
    ├─→ Voyage (1024d)
    └─→ OpenAI (1536d)
    ↓
[TurboPuffer Search]
    ├─→ Namespace 1
    ├─→ Namespace 2
    └─→ Namespace 3
    ↓
[Side-by-Side Display]
    └─→ Comparison & Analysis
```

## Export Format

Downloaded JSON includes:
```json
{
  "query": "Senior Python Developer",
  "timestamp": "2026-01-22T10:30:00",
  "models": {
    "gemini": {
      "namespace": "compare-titles-gemini-...",
      "results": [...],
      "search_time": 0.45
    },
    ...
  }
}
```

## Tips for Best Results

1. **Use Descriptive Queries**: More specific queries often yield better comparisons
2. **Test Various Queries**: Try different types of titles and skills
3. **Compare Score Distributions**: Look at avg, max, and min scores together
4. **Consider Use Case**: Choose models based on your specific requirements (speed, accuracy, cost)

## License

Part of the Wiggli Labs Test project.
