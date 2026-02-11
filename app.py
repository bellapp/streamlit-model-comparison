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
    page_title="Embeedidng Model Comparison ",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Compact sidebar */
    [data-testid="stSidebar"] {
        padding-top: 1  rem;
    }
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    [data-testid="stSidebar"] h2 {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    [data-testid="stSidebar"] h3 {
        margin-top: 0.3rem;
        margin-bottom: 0.3rem;
        font-size: 1rem;
    }
    [data-testid="stSidebar"] .stRadio {
        margin-top: 0.3rem;
        margin-bottom: 0.3rem;
    }
    [data-testid="stSidebar"] .stTextInput {
        margin-top: 0.3rem;
        margin-bottom: 0.3rem;
    }
    [data-testid="stSidebar"] .stNumberInput {
        margin-top: 0.3rem;
        margin-bottom: 0.3rem;
    }
    [data-testid="stSidebar"] .stSelectbox {
        margin-top: 0.3rem;
        margin-bottom: 0.3rem;
    }
    [data-testid="stSidebar"] hr {
        margin: 0.5rem 0;
    }
    [data-testid="stSidebar"] .element-container {
        margin-bottom: 0.3rem;
    }
    
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
        background: transparent;
        padding: 0;
        border: none;
        margin-bottom: 2rem;
    }
    .model-vertex {
        /* No special styling */
    }
    .model-voyage {
        /* No special styling */
    }
    .model-openai {
        /* No special styling */
    }
    .result-item {
        background-color: transparent;
        padding: 0.4rem 0.5rem;
        margin: 0.2rem 0;
        border-radius: 6px;
        border-left: 2px solid rgba(255,255,255,0.2);
        transition: all 0.2s;
    }
    .result-item:hover {
        background-color: rgba(255,255,255,0.05);
        border-left-color: rgba(255,255,255,0.4);
        transform: translateX(2px);
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
    .timing-text {
        text-align: right;
        font-size: 0.85rem;
        color: #666;
        font-weight: 500;
        margin-top: 15px;
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
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_namespace_stats(self, namespace: str, region: str) -> Dict:
        """Get statistics for a namespace in a specific region"""
        try:
            # Create a new client instance for this specific region
            tpuf_client = tpuf.Turbopuffer(api_key=self.api_key, region=region)
            ns = tpuf_client.namespace(namespace)
            stats = {
                'approx_count': 0,
                'dimensions': 0,
                'storage_size': 'N/A',
                'region': region
            }
            
            try:
                meta = ns.metadata()
                
                # Debug: print metadata structure
                # print(f"\n=== Metadata Debug for {namespace} in {region} ===")
                # print(f"Type: {type(meta)}")
                # print(f"Dir: {[attr for attr in dir(meta) if not attr.startswith('_')]}")
                # if hasattr(meta, 'schema'):
                #     print(f"Schema: {meta.schema}")
                # if hasattr(meta, '__dict__'):
                #     print(f"Dict: {meta.__dict__}")
                
                # Handle NamespaceMetadata object (latest SDK as seen in terminal)
                if hasattr(meta, 'approx_row_count'):
                    stats['approx_count'] = meta.approx_row_count
                elif hasattr(meta, 'approx_count'):
                    stats['approx_count'] = meta.approx_count
                # Handle dictionary (older SDK or fallback)
                elif isinstance(meta, dict):
                    stats['approx_count'] = meta.get('approx_row_count', meta.get('approx_count', 0))
                
                # Extract dimensions from schema if not direct attribute
                import re
                if hasattr(meta, 'dimensions'):
                    stats['dimensions'] = meta.dimensions
                    print(f"Found dimensions attribute: {meta.dimensions}")
                elif hasattr(meta, 'schema') and isinstance(meta.schema, dict) and 'vector' in meta.schema:
                    # Extract from schema dict e.g. {'type': '[768]f32', ...}
                    vector_schema = meta.schema['vector']
                    v_type = vector_schema.get('type', '') if isinstance(vector_schema, dict) else ''
                    print(f"Vector type from schema: {v_type}")
                    match = re.search(r'\[(\d+)\]', v_type)
                    if match:
                        stats['dimensions'] = int(match.group(1))
                        print(f"Extracted dimensions: {stats['dimensions']}")
                elif hasattr(meta, 'schema_') and hasattr(meta.schema_.get('vector'), 'type'):
                    # Try schema_ with AttributeSchemaConfig
                    v_type = meta.schema_['vector'].type
                    print(f"Vector type from schema_: {v_type}")
                    match = re.search(r'\[(\d+)\]', v_type)
                    if match:
                        stats['dimensions'] = int(match.group(1))
                        print(f"Extracted dimensions from schema_: {stats['dimensions']}")
                elif isinstance(meta, dict) and 'dimensions' in meta:
                    stats['dimensions'] = meta.get('dimensions', 0)
                
                print(f"Final stats: {stats}")
                stats['region'] = region
            except Exception as e:
                print(f"Error getting metadata: {e}")
                stats['region'] = region
                pass
            
            return stats
        except Exception:
            return {'approx_count': 0, 'dimensions': 0, 'storage_size': 'N/A', 'region': region}

    def search(self, namespace: str, region: str, query_vector: List[float], top_k: int = 10, model_name: str = "") -> List[Dict]:
        """
        Search for similar items in namespace in a specific region.
        """
        try:
            # Create a new client instance for this specific region
            tpuf_client = tpuf.Turbopuffer(api_key=self.api_key, region=region)
            ns = tpuf_client.namespace(namespace)
            
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


def display_model_results(model_name: str, results: List[Dict], search_time: float, color_class: str, stats: Dict = None):
    """Display results for a single model"""
    
    # Header with icon based on model
    model_icons = {
        'vertex': '🔵',
        'voyage': '🟠',
        'openai-small': '🟢'
    }
    icon = model_icons.get(model_name, '🤖')
    
    # Model name header with inline metadata
    st.markdown(f"### {icon} {model_name.upper()}")
    
    if stats:
        st.markdown(f"""
        <div style="font-size: 0.9rem; color: #bbb; margin-bottom: 0.5rem; margin-top: -0.5rem;">
            ⏱️ <b>{search_time:.2f}s</b> &nbsp;|&nbsp; 
            📊 <b style="color: #4CAF50;">{stats.get('approx_count', 0):,}</b> docs &nbsp;|&nbsp; 
            📏 <b style="color: #2196F3;">{stats.get('dimensions', 0)}</b>d &nbsp;|&nbsp; 
            🌍 <b style="color: #FFB74D;">{stats.get('region', 'N/A')}</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-size: 0.9rem; color: #bbb; margin-bottom: 0.5rem; margin-top: -0.5rem;">⏱️ <b>{search_time:.2f}s</b></div>', unsafe_allow_html=True)
    
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
                
                if i < len(results):  # Only add divider if not last result
                    st.markdown("<div style='margin: 0.3rem 0; border-bottom: 1px solid rgba(255,255,255,0.1);'></div>", unsafe_allow_html=True)


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
    st.markdown('<h1 class="main-header"> ⚖️ Embedding Model Comparison </h1>', unsafe_allow_html=True)
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
    
    default_region = get_env('TURBOPUFFER_REGION') or get_env('DEFAULT_REGION', 'aws-eu-west-1')
    
    # Sidebar Configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Search Type Selection
        st.markdown("**🎯 Search Type**")
        search_type = st.radio(
            "What do you want to search for?",
            options=["Titles", "Skills"],
            index=0,
            help="Choose whether to search job titles or skills",
            label_visibility="collapsed"
        )
        
        # Search Form (with Enter key support)
        with st.form(key='search_form', clear_on_submit=False):
            st.markdown("**🔍 Search Query**")
            placeholder = "e.g., Senior Python Developer" if search_type == "Titles" else "e.g., Python, React, Machine Learning"
            query_text = st.text_input(
                f"Enter a {search_type.lower()[:-1]} to search",
                placeholder=placeholder,
                help=f"Type your search and press Enter ⏎ or click the button below"
            )
            
            # Move Search Parameters here (under text search input)
            st.markdown("**⚙️ Search Parameters**")
            
            # Simple number input only
            top_k = st.number_input(
                "Number of results per model",
                min_value=1,
                max_value=1000,
                value=10,
                step=1,
                help="Enter the number of results to return (max: 1000)"
            )
            
            st.caption("💡 Tip: Press **Enter** or click the button")
            
            # Submit button (Enter key will trigger this)
            search_button_form = st.form_submit_button("🚀 Compare Models", use_container_width=True, type="primary")
        
        # Namespace Configuration
        st.markdown(f"**📦 Model Namespaces ({search_type})**")
        
        # Select appropriate defaults based on search type
        if search_type == "Titles":
            default_vertex = default_vertex_titles_ns
            default_voyage = default_voyage_titles_ns
            default_openai = default_openai_titles_ns
        else:  # Skills
            default_vertex = default_vertex_skills_ns
            default_voyage = default_voyage_skills_ns
            default_openai = default_openai_skills_ns
        
        with st.expander("ℹ️ Info", expanded=False):
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
        
        regions = ["aws-eu-west-1", "aws-eu-central-1" ]
        
        # --- Vertex AI Namespace & Region ---
        st.markdown("**Vertex AI (Gemini)**")
        col_ns_v, col_reg_v = st.columns([2, 1])
        with col_ns_v:
            vertex_namespace = st.text_input(
                f"Namespace",
                value=default_vertex,
                key=f"vertex_ns_input_{search_type.lower()}",
                label_visibility="collapsed"
            )
        with col_reg_v:
            vertex_region = st.selectbox(
                "Reg V",
                options=regions,
                index=regions.index("aws-eu-central-1") if "aws-eu-central-1" in regions else 0,
                key=f"vertex_reg_input_{search_type.lower()}",
                label_visibility="collapsed"
            )
            
        # --- Voyage Namespace & Region ---
        st.markdown("**Voyage AI**")
        col_ns_voy, col_reg_voy = st.columns([2, 1])
        with col_ns_voy:
            voyage_namespace = st.text_input(
                f"Voyage NS",
                value=default_voyage,
                key=f"voyage_ns_input_{search_type.lower()}",
                label_visibility="collapsed"
            )
        with col_reg_voy:
            voyage_region = st.selectbox(
                "Reg Voy",
                options=regions,
                index=regions.index("aws-us-east-1") if "aws-us-east-1" in regions else 0,
                key=f"voyage_reg_input_{search_type.lower()}",
                label_visibility="collapsed"
            )
            
        # --- OpenAI Namespace & Region ---
        st.markdown("**OpenAI**")
        col_ns_o, col_reg_o = st.columns([2, 1])
        with col_ns_o:
            openai_namespace = st.text_input(
                f"OpenAI NS",
                value=default_openai,
                key=f"openai_ns_input_{search_type.lower()}",
                label_visibility="collapsed"
            )
        with col_reg_o:
            openai_region = st.selectbox(
                "Reg O",
                options=regions,
                index=regions.index("gcp-us-central1") if "gcp-us-central1" in regions else 0,
                key=f"openai_reg_input_{search_type.lower()}",
                label_visibility="collapsed"
            )
    
    # Main content (triggered by form submission or button click)
    if search_button_form:
        if not query_text.strip():
            st.warning("⚠️ Please enter a search query")
            return
        
        # Check which models have namespaces configured
        models_config = []
        
        if vertex_namespace and vertex_namespace.strip():
            models_config.append(('vertex', vertex_namespace.strip(), vertex_region))
        if voyage_namespace and voyage_namespace.strip():
            models_config.append(('voyage', voyage_namespace.strip(), voyage_region))
        if openai_namespace and openai_namespace.strip():
            models_config.append(('openai-small', openai_namespace.strip(), openai_region))
        
        if not models_config:
            st.warning("⚠️ Please configure at least one model namespace")
            return
        
        # Initialize searcher
        searcher = TurbopufferSearcher(turbopuffer_key)
        
        # Store results
        all_results = {}
        all_times = {}
        all_stats = {}
        
        # Search each model
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, (model_name, namespace, region) in enumerate(models_config):
            status_text.text(f"Searching {model_name.upper()}...")
            
            try:
                # Generate query embedding
                start_time = time.time()
                
                # Create embedding client
                client = EmbeddingModelClient(model_name)
                
                query_vector = client.embed_query(query_text)
                
                # Search namespace (pass model_name for better error messages)
                results = searcher.search(namespace, region, query_vector, top_k=top_k, model_name=model_name)
                search_time = time.time() - start_time
                
                all_results[model_name] = results
                all_times[model_name] = search_time
                
                # Fetch namespace stats
                all_stats[model_name] = searcher.get_namespace_stats(namespace, region)
                
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
                all_stats[model_name] = {'approx_count': 0, 'dimensions': 0, 'region': region}
            
            progress_bar.progress((idx + 1) / len(models_config))
        
        status_text.empty()
        progress_bar.empty()
        
        # Display Results
        st.markdown("---")
        st.markdown(f"### 🔍 Results for: `{query_text}`")
        
        cols = st.columns(len(models_config))
        for idx, (model_name, _, _) in enumerate(models_config):
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
                    color_classes.get(model_name, ''),
                    stats=all_stats.get(model_name)
                )
        
        # Export results
        st.markdown("---")
        with st.expander("💾 Export Results"):
            export_data = {
                'query': query_text,
                'timestamp': datetime.now().isoformat(),
                'models': {
                    model_name: {
                        'namespace': ns,
                        'region': reg,
                        'results': all_results.get(model_name, []),
                        'search_time': all_times.get(model_name, 0)
                    }
                    for model_name, ns, reg in models_config
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
