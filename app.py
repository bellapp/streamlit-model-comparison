#!/usr/bin/env python3
"""
🐟 Model Comparison App - Compare Embedding Models Side-by-Side
Compare search results from different embedding models (Vertex AI, Voyage, OpenAI)
using TurboPuffer namespaces
"""

import streamlit as st
import os
import sys
import json
import time
from typing import List, Dict, Tuple
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import turbopuffer as tpuf
    import voyageai
    from google import genai
    from google.genai import types as genai_types
    from openai import OpenAI
except ImportError as e:
    st.error(f"Missing dependency: {e}")
    st.error("Install with: pip install turbopuffer voyageai google-genai openai")
    st.stop()

# Load environment variables (works for both local .env and Streamlit Cloud secrets)
load_dotenv()

def get_env(key: str, default: str = None) -> str:
    """
    Get environment variable from either .env file (local) or Streamlit secrets (cloud).
    Priority: Streamlit secrets > .env file > default value
    """
    # Try Streamlit secrets first (cloud deployment)
    try:
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except Exception:
        # Secrets file doesn't exist or error accessing it - fall back to env vars
        pass
    # Fall back to environment variables (.env file for local)
    return os.getenv(key, default)

# Page configuration
st.set_page_config(
    page_title="Model Comparison Tool",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    .model-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .model-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .model-vertex {
        border-left-color: #4285f4;
        background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);
    }
    .model-voyage {
        border-left-color: #ff7f0e;
        background: linear-gradient(135deg, #fff3e0 0%, #ffffff 100%);
    }
    .model-openai {
        border-left-color: #10a37f;
        background: linear-gradient(135deg, #e0f2f1 0%, #ffffff 100%);
    }
    .result-item {
        background-color: white;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 3px solid #ddd;
        transition: all 0.2s;
    }
    .result-item:hover {
        background-color: #f0f2f6;
        border-left-color: #666;
        transform: translateX(3px);
    }
    .score-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .score-excellent {
        background: linear-gradient(135deg, #d4edda 0%, #a8e6a8 100%);
        color: #155724;
    }
    .score-good {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe699 100%);
        color: #856404;
    }
    .score-fair {
        background: linear-gradient(135deg, #f8d7da 0%, #f5b7bb 100%);
        color: #721c24;
    }
    .metric-card {
        background: linear-gradient(135deg, #e7f3ff 0%, #cfe9ff 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Improve sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a5f 0%, #2c5282 50%, #1e3a5f 100%);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stTextInput > label,
    [data-testid="stSidebar"] .stSelectbox > label,
    [data-testid="stSidebar"] .stSlider > label {
        color: #e0e7ff !important;
        font-weight: 500;
    }
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    [data-testid="stSidebar"] input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    /* Better button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)


class EmbeddingModelClient:
    """Unified client for different embedding models"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate API client"""
        if self.model_name.startswith('vertex'):
            # Vertex AI configuration using NEW Google Gen AI SDK
            project_id = get_env('VERTEX_PROJECT_ID', 'gen-lang-client-0683226472')
            region = get_env('VERTEX_REGION', 'us-central1')
            service_account_file = get_env('VERTEX_SERVICE_ACCOUNT_FILE')
            
            # Check for service account in Streamlit secrets (cloud deployment)
            service_account_from_secrets = None
            if hasattr(st, 'secrets') and 'VERTEX_SERVICE_ACCOUNT' in st.secrets:
                try:
                    # Convert Streamlit secrets to JSON format and save temporarily
                    import tempfile
                    service_account_dict = dict(st.secrets['VERTEX_SERVICE_ACCOUNT'])
                    
                    # Create temporary JSON file for service account
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                        json.dump(service_account_dict, f)
                        service_account_from_secrets = f.name
                except Exception as e:
                    st.warning(f"⚠️ Failed to load service account from secrets: {e}")
            
            # Try to locate service account file in common locations
            service_account_file_found = service_account_from_secrets
            if not service_account_file_found and service_account_file:
                possible_paths = [
                    service_account_file,  # As specified
                    os.path.abspath(service_account_file),  # Relative to current dir
                    os.path.join(os.path.dirname(__file__), service_account_file),  # Relative to app
                    os.path.join(os.path.dirname(__file__), '..', 'batch_pipeline', service_account_file),  # batch_pipeline
                    os.path.join(os.getcwd(), service_account_file),  # Current working directory
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        service_account_file_found = path
                        break
                
                if not service_account_file_found:
                    st.error(f"❌ Service account file not found: {service_account_file}\nSearched in: {', '.join(possible_paths)}")
                    raise FileNotFoundError(f"Service account file not found: {service_account_file}")
            
            # Create Gen AI client with Vertex AI backend
            try:
                if service_account_file_found:
                    # Set environment variable for service account
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_file_found
                
                # Initialize Gen AI client with Vertex AI
                self.client = genai.Client(
                    vertexai=True,
                    project=project_id,
                    location=region,
                    http_options=genai_types.HttpOptions(api_version='v1')
                )
                # Store model name for embedding
                self.vertex_model = get_env('VERTEX_MODEL_NAME', 'text-multilingual-embedding-002')
                
            except Exception as e:
                st.error(f"❌ Vertex AI authentication failed. Please either:\n1. Set VERTEX_SERVICE_ACCOUNT_FILE in .env\n2. Run: `gcloud auth application-default login`\n3. Set GOOGLE_APPLICATION_CREDENTIALS env var\n\nError: {e}")
                raise
        elif self.model_name.startswith('voyage'):
            api_key = get_env('VOYAGE_API_KEY') or get_env('VOYAGEAI_API_KEY')
            if api_key:
                self.client = voyageai.Client(api_key=api_key)
            else:
                st.error("❌ `VOYAGE_API_KEY` not found in secrets!")
        elif self.model_name.startswith('openai'):
            api_key = get_env('OPENAI_API_KEY')
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                st.error("❌ `OPENAI_API_KEY` not found in secrets!")
    
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for query text with retry logic"""
        if not self.client:
            raise ValueError(f"Client not initialized for {self.model_name}")
        
        if self.model_name.startswith('vertex'):
            # Vertex AI using NEW Google Gen AI SDK
            # Model: text-multilingual-embedding-002 (768 dimensions)
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.client.models.embed_content(
                        model=self.vertex_model,
                        contents=text,
                        config=genai_types.EmbedContentConfig(
                            task_type="RETRIEVAL_QUERY"
                        )
                    )
                    return response.embeddings[0].values
                except Exception as e:
                    error_str = str(e)
                    # Check if it's a rate limit error
                    if '429' in error_str or 'quota' in error_str.lower() or 'rate limit' in error_str.lower():
                        if attempt < max_retries - 1:
                            wait_time = (attempt + 1) * 5  # 5, 10, 15 seconds
                            st.warning(f"⏳ Vertex AI rate limit hit. Waiting {wait_time}s before retry {attempt + 2}/{max_retries}...")
                            time.sleep(wait_time)
                        else:
                            raise Exception(f"Vertex AI rate limit exceeded. Please wait a moment and try again, or remove Vertex namespace to test other models.")
                    else:
                        raise
        
        elif self.model_name.startswith('voyage'):
            model = "voyage-4"
            result = self.client.embed(
                [text],
                model=model,
                input_type="query"
            )
            return result.embeddings[0]
        
        elif self.model_name.startswith('openai'):
            model = "text-embedding-3-small"
            result = self.client.embeddings.create(
                input=text,
                model=model
            )
            return result.data[0].embedding
        
        raise ValueError(f"Unknown model: {self.model_name}")


class TurbopufferSearcher:
    """Search TurboPuffer namespaces"""
    
    def __init__(self, api_key: str, region: str = "aws-eu-central-1"):
        self.tpuf = tpuf.Turbopuffer(api_key=api_key, region=region)
    
    def search(self, namespace: str, query_vector: List[float], top_k: int = 10, model_name: str = "") -> List[Dict]:
        """
        Search for similar items in namespace.
        
        Args:
            namespace: TurboPuffer namespace to search
            query_vector: Query embedding vector
            top_k: Number of results to return
            model_name: Name of the model (for better error messages)
        
        Returns:
            List of {id, text, score} dicts
        """
        try:
            ns = self.tpuf.namespace(namespace)
            
            result = ns.query(
                rank_by=("vector", "ANN", query_vector),
                top_k=top_k,
                include_attributes=['text']
            )
            
            formatted = []
            rows = result.rows if hasattr(result, 'rows') else result
            
            for row in rows:
                # Convert row to dict
                if hasattr(row, 'model_dump'):
                    row_dict = row.model_dump()
                elif hasattr(row, 'dict'):
                    row_dict = row.dict()
                else:
                    row_dict = {}
                
                # Extract text
                text = row_dict.get("text", "N/A")
                if text == "N/A" and hasattr(row, 'attributes') and row.attributes:
                    text = row.attributes.get("text", "N/A")
                if text == "N/A" and hasattr(row, 'text'):
                    text = row.text
                
                # Extract ID and score
                rid = row_dict.get("id", getattr(row, 'id', "N/A"))
                score = row_dict.get("$dist", 0)
                
                formatted.append({
                    "id": rid,
                    "text": text,
                    "score": score
                })
            
            return formatted
            
        except Exception as e:
            error_msg = str(e)
            
            # Check for dimension mismatch
            if "Invalid query dimensions" in error_msg or "dimensions=" in error_msg:
                # Extract dimensions from error message
                import re
                query_dims = re.search(r'Query has dimensions=(\d+)', error_msg)
                index_dims = re.search(r'index has dimensions=(\d+)', error_msg)
                
                if query_dims and index_dims:
                    q_dim = query_dims.group(1)
                    i_dim = index_dims.group(1)
                    
                    # Map dimensions to models
                    dim_to_model = {
                        "768": "Vertex AI (text-multilingual-embedding-002)",
                        "1024": "Voyage (voyage-4) or Cohere",
                        "1536": "OpenAI (text-embedding-3-small)",
                        "3072": "OpenAI (text-embedding-3-large)"
                    }
                    
                    query_model = dim_to_model.get(q_dim, f"Unknown ({q_dim}d)")
                    index_model = dim_to_model.get(i_dim, f"Unknown ({i_dim}d)")
                    
                    st.error(f"""
⚠️ **Dimension Mismatch for {model_name.upper() if model_name else 'Model'}**

Namespace: `{namespace}`

- **Your query embedding**: {q_dim} dimensions → {query_model}
- **Namespace contains**: {i_dim} dimensions → {index_model}

**💡 Solution**: This namespace was created with **{index_model}**, not {model_name}.

**Fix options:**
1. Use the correct {model_name} namespace
2. OR move this namespace to the "{index_model.split()[0].lower()}" field in the sidebar
3. OR check your namespace naming - it might be mislabeled
                    """)
                else:
                    st.error(f"❌ Error searching namespace '{namespace}': {error_msg}")
            else:
                st.error(f"❌ Error searching namespace '{namespace}': {error_msg}")
            
            return []


def get_score_class(score: float) -> str:
    """
    Get CSS class based on score.
    TurboPuffer uses cosine_distance where LOWER is BETTER (0-2 range).
    """
    if score <= 0.3:  # Very close match
        return "score-excellent"
    elif score <= 0.7:  # Good match
        return "score-good"
    else:  # score > 0.7 - Weaker match
        return "score-fair"


def display_model_results(model_name: str, results: List[Dict], search_time: float, color_class: str):
    """Display results for a single model"""
    st.markdown(f'<div class="model-card {color_class}">', unsafe_allow_html=True)
    
    # Header with icon based on model
    model_icons = {
        'vertex': '🔵',
        'voyage': '🟠',
        'openai-small': '🟢'
    }
    icon = model_icons.get(model_name, '🤖')
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {icon} {model_name.upper()}")
    with col2:
        st.metric("⏱️", f"{search_time:.2f}s")
    
    # Results
    if not results:
        st.warning("⚠️ No results found")
        st.info("💡 Possible reasons:\n- Namespace might be empty\n- No matches above similarity threshold\n- Check namespace configuration")
    else:
        st.success(f"✅ Found {len(results)} results")
        
        # Display each result with better formatting
        for i, result in enumerate(results, 1):
            score = result['score']
            text = result.get('text', 'N/A')
            score_class = get_score_class(score)
            
            # Determine score emoji (lower distance = better match)
            if score <= 0.3:
                score_emoji = "🟢"  # Excellent match
            elif score <= 0.7:
                score_emoji = "🟡"  # Good match
            else:
                score_emoji = "🔴"  # Weaker match
            
            # Truncate long text
            display_text = text if len(text) <= 80 else text[:77] + "..."
            
            # Create expandable result card
            with st.container():
                col_text, col_score = st.columns([4, 1])
                with col_text:
                    st.markdown(f"**{i}.** {display_text}")
                with col_score:
                    st.markdown(f"<div style='text-align: right;'>{score_emoji} <strong>{score:.4f}</strong></div>", unsafe_allow_html=True)
                
                # Show full text in expander if truncated
                if len(text) > 80:
                    with st.expander("📄 View full text"):
                        st.text(text)
                
                st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)


def compare_model_performance(results_dict: Dict[str, List[Dict]]) -> pd.DataFrame:
    """
    Create comparison metrics DataFrame.
    Note: TurboPuffer uses cosine_distance where LOWER is BETTER.
    """
    metrics = []
    
    for model_name, results in results_dict.items():
        if not results:
            metrics.append({
                'Model': model_name,
                'Results': 0,
                'Avg Distance': 999.0,  # High value = worst
                'Best Distance': 999.0,
                'Worst Distance': 999.0
            })
        else:
            scores = [r['score'] for r in results]
            metrics.append({
                'Model': model_name,
                'Results': len(results),
                'Avg Distance': sum(scores) / len(scores) if scores else 999.0,
                'Best Distance': min(scores) if scores else 999.0,  # Min = best
                'Worst Distance': max(scores) if scores else 999.0   # Max = worst
            })
    
    return pd.DataFrame(metrics)


def main():
    # Header
    st.markdown('<h1 class="main-header">🐟 ⚖️ Model Comparison Tool</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align: center; color: #666; font-size: 1.1rem;">
    Compare search results from Vertex AI, Voyage, and OpenAI embedding models side-by-side
    </p>
    """, unsafe_allow_html=True)
    
    # Check API keys
    turbopuffer_key = get_env('TURBOPUFFER_API_KEY')
    if not turbopuffer_key:
        st.error("❌ TURBOPUFFER_API_KEY not found in environment variables or Streamlit secrets")
        st.info("💡 For local development: Add to `.env` file. For Streamlit Cloud: Add to app secrets.")
        st.stop()
    
    # Load default values from environment or Streamlit secrets
    default_vertex_titles_ns = get_env('GEMINI_TITLES_NAMESPACE') or get_env('VERTEX_TITLES_NAMESPACE', '')
    default_voyage_titles_ns = get_env('VOYAGE_TITLES_NAMESPACE') or get_env('VOYAGE_NAMESPACE', '')
    default_openai_titles_ns = get_env('OPENAI_TITLES_NAMESPACE') or get_env('OPENAI_NAMESPACE', '')
    
    default_vertex_skills_ns = get_env('GEMINI_SKILLS_NAMESPACE') or get_env('VERTEX_SKILLS_NAMESPACE', '')
    default_voyage_skills_ns = get_env('VOYAGE_SKILLS_NAMESPACE', '')
    default_openai_skills_ns = get_env('OPENAI_SKILLS_NAMESPACE', '')
    
    default_region = get_env('TURBOPUFFER_REGION') or get_env('DEFAULT_REGION', 'aws-us-east-1')
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Search Type Selection
        st.subheader("🎯 Search Type")
        search_type = st.radio(
            "What do you want to search for?",
            options=["Titles", "Skills"],
            index=0,
            help="Choose whether to search job titles or skills"
        )
        
        st.divider()
        
        # Search Form (with Enter key support)
        with st.form(key='search_form', clear_on_submit=False):
            st.subheader("🔍 Search Query")
            placeholder = "e.g., Senior Python Developer" if search_type == "Titles" else "e.g., Python, React, Machine Learning"
            query_text = st.text_input(
                f"Enter a {search_type.lower()[:-1]} to search",
                placeholder=placeholder,
                help=f"Type your search and press Enter ⏎ or click the button below"
            )
            
            st.caption("💡 Tip: Press **Enter** or click the button to start searching")
            
            # Submit button (Enter key will trigger this)
            search_button_form = st.form_submit_button("🚀 Compare Models", use_container_width=True, type="primary")
        
        st.divider()
        
        # Namespace Configuration
        st.subheader(f"📦 Model Namespaces ({search_type})")
        
        # Select appropriate defaults based on search type
        if search_type == "Titles":
            default_vertex = default_vertex_titles_ns
            default_voyage = default_voyage_titles_ns
            default_openai = default_openai_titles_ns
            env_vars = "GEMINI_TITLES_NAMESPACE (or VERTEX_TITLES_NAMESPACE), VOYAGE_TITLES_NAMESPACE, OPENAI_TITLES_NAMESPACE"
        else:  # Skills
            default_vertex = default_vertex_skills_ns
            default_voyage = default_voyage_skills_ns
            default_openai = default_openai_skills_ns
            env_vars = "GEMINI_SKILLS_NAMESPACE (or VERTEX_SKILLS_NAMESPACE), VOYAGE_SKILLS_NAMESPACE, OPENAI_SKILLS_NAMESPACE"
        
        if default_vertex or default_voyage or default_openai:
            st.success(f"✓ Default {search_type.lower()} namespaces loaded from .env")
        else:
            st.info(f"💡 Tip: Set {env_vars} in .env")
        
        with st.expander("ℹ️ Model Info & Tips"):
            st.markdown("""
            **Model Dimensions:**
            - **Vertex AI**: 768d (text-multilingual-embedding-002) - fixed
            - **Voyage**: 1024d (voyage-4)
            - **OpenAI**: 1536d (text-embedding-3-small)
            
            **⚠️ Important Notes:**
            - Gemini & OpenAI can both use 1536d but are NOT compatible
            - Each namespace must contain only ONE model's vectors
            - **Titles and Skills use separate namespaces!**
            - If you get dimension errors, check "Advanced: Gemini Dimensions"
            
            **💡 Rate Limits:**
            - **Gemini**: 3000 req/min (free tier)
            - **Voyage**: 300 req/min
            - **OpenAI**: 3000 req/min
            
            **Tip**: If you hit a rate limit, clear that model's namespace field to test the others!
            """)
        
        vertex_namespace = st.text_input(
            f"Vertex AI {search_type} Namespace",
            value=default_vertex,
            placeholder=f"compare-{search_type.lower()}-vertex-multilingual-v4-20260125",
            help=f"Namespace containing Vertex AI (text-multilingual-embedding-002) {search_type.lower()} embeddings"
        )
        
        voyage_namespace = st.text_input(
            f"Voyage {search_type} Namespace",
            value=default_voyage,
            placeholder=f"compare-{search_type.lower()}-voyage-profile_v12-20250126",
            help=f"Namespace containing Voyage {search_type.lower()} embeddings"
        )
        
        openai_namespace = st.text_input(
            f"OpenAI {search_type} Namespace",
            value=default_openai,
            placeholder=f"compare-{search_type.lower()}-openai-small-profile_v12-20250126",
            help=f"Namespace containing OpenAI {search_type.lower()} embeddings"
        )
        
        st.divider()
        
        # Search Parameters
        st.subheader("⚙️ Search Parameters")
        
        # Initialize session state for top_k if not exists
        if 'top_k_value' not in st.session_state:
            st.session_state.top_k_value = 10
        
        # Create two columns for slider and number input
        col_slider, col_number = st.columns([2, 1])
        
        with col_slider:
            top_k_slider = st.slider(
                "Number of results per model",
                min_value=1,
                max_value=1000,
                value=st.session_state.top_k_value,
                help="Drag slider or type exact number → (max: 1000)",
                key="top_k_slider"
            )
        
        with col_number:
            st.markdown("<br>", unsafe_allow_html=True)  # Align with slider label
            top_k_number = st.number_input(
                "Or type number",
                min_value=1,
                max_value=1000,
                value=st.session_state.top_k_value,
                step=1,
                help="Type exact number of results",
                key="top_k_number",
                label_visibility="visible"
            )
        
        # Update session state based on which control changed
        if top_k_slider != st.session_state.top_k_value:
            st.session_state.top_k_value = top_k_slider
            top_k = top_k_slider
        elif top_k_number != st.session_state.top_k_value:
            st.session_state.top_k_value = top_k_number
            top_k = top_k_number
        else:
            top_k = st.session_state.top_k_value
        
        regions = ["aws-eu-central-1", "aws-us-east-1", "gcp-us-central1"]
        default_index = regions.index(default_region) if default_region in regions else 1
        region = st.selectbox(
            "TurboPuffer Region",
            options=regions,
            index=default_index,
            help="TurboPuffer region where namespaces are stored (from .env: TURBOPUFFER_REGION)"
        )
        
        # Info about Vertex AI
        with st.expander("ℹ️ Vertex AI Configuration"):
            st.info("""
            **Vertex AI Model**: `text-multilingual-embedding-002`
            - **Dimensions**: 768 (fixed)
            - **Languages**: Multilingual support (100+ languages)
            - **GCP Project**: Set via `VERTEX_PROJECT_ID` (default: gen-lang-client-0683226472)
            - **Region**: Set via `VERTEX_REGION` (default: us-central1)
            - **Auth**: Service account via `VERTEX_SERVICE_ACCOUNT_FILE` or default credentials
            """)
        
        st.divider()
    
    # Main content (triggered by form submission or button click)
    if search_button_form:
        if not query_text.strip():
            st.warning("⚠️ Please enter a search query")
            return
        
        # Check which models have namespaces configured
        models_config = []
        
        if vertex_namespace and vertex_namespace.strip():
            models_config.append(('vertex', vertex_namespace.strip()))
        if voyage_namespace and voyage_namespace.strip():
            models_config.append(('voyage', voyage_namespace.strip()))
        if openai_namespace and openai_namespace.strip():
            models_config.append(('openai-small', openai_namespace.strip()))
        
        if not models_config:
            st.warning("⚠️ Please configure at least one model namespace")
            return
        
        st.info(f"🔍 Searching for {search_type}: **{query_text}**")
        st.info(f"📊 Comparing **{len(models_config)}** models across {search_type.lower()} namespaces")
        
        # Initialize searcher
        searcher = TurbopufferSearcher(turbopuffer_key, region)
        
        # Store results
        all_results = {}
        all_times = {}
        
        # Search each model
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, (model_name, namespace) in enumerate(models_config):
            status_text.text(f"Searching {model_name.upper()}...")
            
            try:
                # Generate query embedding
                start_time = time.time()
                
                # Create embedding client
                client = EmbeddingModelClient(model_name)
                
                query_vector = client.embed_query(query_text)
                
                # Search namespace (pass model_name for better error messages)
                results = searcher.search(namespace, query_vector, top_k=top_k, model_name=model_name)
                search_time = time.time() - start_time
                
                all_results[model_name] = results
                all_times[model_name] = search_time
                
            except Exception as e:
                error_msg = str(e)
                # Special handling for rate limits
                if '429' in error_msg or 'quota' in error_msg.lower() or 'rate limit' in error_msg.lower():
                    st.warning(f"⚠️ **{model_name.upper()} Rate Limit**")
                    st.info(f"💡 **Tip**: Clear the {model_name} namespace field in the sidebar to test other models while waiting.")
                    st.error(f"Details: {error_msg}")
                else:
                    st.error(f"❌ Error with {model_name}: {error_msg}")
                
                all_results[model_name] = []
                all_times[model_name] = 0
            
            progress_bar.progress((idx + 1) / len(models_config))
        
        status_text.empty()
        progress_bar.empty()
        
        # Display Summary Metrics - HIDDEN
        # st.markdown("---")
        # st.markdown("## 📊 Comparison Summary")
        
        comparison_df = compare_model_performance(all_results)
        
        # # Find best model (LOWEST average distance = best)
        # best_idx = comparison_df['Avg Distance'].idxmin()
        # best_model_name = comparison_df.loc[best_idx, 'Model']
        # best_distance = comparison_df.loc[best_idx, 'Avg Distance']
        
        # # Display quick winner if there are results (distance < 999 means valid results)
        # if best_distance < 999:
        #     col1, col2, col3 = st.columns([1, 2, 1])
        #     with col2:
        #         st.success(f"🏆 **Best Performer**: {best_model_name.upper()} with avg distance {best_distance:.4f} (lower is better)")
        
        # st.markdown("### Model Performance")
        
        # # Display metrics in columns with icons
        # cols = st.columns(len(models_config))
        # model_icons = {'vertex': '🔵', 'voyage': '🟠', 'openai-small': '🟢'}
        
        # for idx, (model_name, _) in enumerate(models_config):
        #     with cols[idx]:
        #         model_data = comparison_df[comparison_df['Model'] == model_name].iloc[0]
        #         icon = model_icons.get(model_name, '🤖')
                
        #         # Determine if this is the best model (lowest distance = best)
        #         is_best = model_name == best_model_name and best_distance < 999
        #         border_color = "#FFD700" if is_best else "#e7f3ff"
                
        #         st.markdown(f'''
        #         <div style="background: linear-gradient(135deg, {border_color}20 0%, #ffffff 100%); 
        #                     padding: 1.2rem; border-radius: 12px; text-align: center; 
        #                     border: {"3px solid #FFD700" if is_best else "2px solid #e0e0e0"};
        #                     box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        #             <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        #             <div style="font-size: 1.1rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;">
        #                 {model_name.upper()}
        #             </div>
        #             <div style="font-size: 2rem; font-weight: 700; color: #1f77b4; margin-bottom: 0.3rem;">
        #                 {model_data['Avg Distance']:.4f}
        #             </div>
        #             <div style="font-size: 0.9rem; color: #666;">
        #                 {model_data['Results']} results • {all_times.get(model_name, 0):.2f}s
        #             </div>
        #             <div style="font-size: 0.75rem; color: #999; margin-top: 0.3rem;">
        #                 lower distance = better match
        #             </div>
        #             {'<div style="margin-top: 0.5rem; color: #FFD700; font-weight: 600;">👑 Winner</div>' if is_best else ''}
        #         </div>
        #         ''', unsafe_allow_html=True)
        
        # # Display detailed comparison table
        # with st.expander("📈 Detailed Metrics", expanded=True):
        #     st.caption("💡 Remember: Lower distance = better match (cosine_distance ranges from 0-2)")
        #     # Style the dataframe with gradient if matplotlib is available
        #     try:
        #         styled_df = comparison_df.style.format({
        #             'Avg Distance': '{:.4f}',
        #             'Best Distance': '{:.4f}',
        #             'Worst Distance': '{:.4f}'
        #         }).background_gradient(subset=['Avg Distance'], cmap='RdYlGn_r')  # Reversed colormap
        #         st.dataframe(styled_df, width='stretch')
        #     except ImportError:
        #         # Fallback if matplotlib not available
        #         styled_df = comparison_df.style.format({
        #             'Avg Distance': '{:.4f}',
        #             'Best Distance': '{:.4f}',
        #             'Worst Distance': '{:.4f}'
        #         })
        #         st.dataframe(styled_df, width='stretch')
        
        # Display results side by side
        st.markdown("---")
        st.markdown("## 🔎 Detailed Results by Model")
        st.caption("Scroll through each model's top matches with similarity scores")
        
        cols = st.columns(len(models_config))
        for idx, (model_name, _) in enumerate(models_config):
            with cols[idx]:
                color_classes = {
                    'vertex': 'model-vertex',
                    'voyage': 'model-voyage',
                    'openai-small': 'model-openai'
                }
                display_model_results(
                    model_name,
                    all_results.get(model_name, []),
                    all_times.get(model_name, 0),
                    color_classes.get(model_name, '')
                )
        
        # Additional Analysis
        st.markdown("---")
        st.markdown("## 📈 Performance Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🎯 Accuracy")
            best_model = comparison_df.loc[comparison_df['Avg Distance'].idxmin(), 'Model']
            best_distance = comparison_df['Avg Distance'].min()
            st.metric("Best Model", best_model.upper(), f"{best_distance:.4f} (lower=better)")
            
        with col2:
            st.markdown("### ⚡ Speed")
            if all_times:
                fastest = min(all_times.items(), key=lambda x: x[1] if x[1] > 0 else float('inf'))
                st.metric("Fastest", fastest[0].upper(), f"{fastest[1]:.2f}s")
            
        with col3:
            st.markdown("### 📊 Coverage")
            total_results = sum(len(r) for r in all_results.values() if r)
            st.metric("Total Results", total_results, f"across {len(models_config)} models")
        
        # Export results
        st.markdown("---")
        with st.expander("💾 Export Results"):
            export_data = {
                'query': query_text,
                'timestamp': datetime.now().isoformat(),
                'models': {
                    model_name: {
                        'namespace': ns,
                        'results': all_results.get(model_name, []),
                        'search_time': all_times.get(model_name, 0)
                    }
                    for model_name, ns in models_config
                }
            }
            st.download_button(
                "📥 Download Results (JSON)",
                data=json.dumps(export_data, indent=2),
                file_name=f"model_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )


if __name__ == "__main__":
    main()
