# app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from typing import List

# Import your project's classes and functions
from models.document import Documento
from pipeline import BVG_RAG_Pipeline
from evaluator import EvaluadorPipeline
from reranker import Reordenador
from data_loader import cargar_documentos

# Load environment variables from .env file
load_dotenv()

# --- Caching Configuration ---
# @st.cache_resource prevents heavy models from reloading on every interaction.
@st.cache_resource
def initialize_systems(api_key: str):
    """Loads models and initializes pipelines only once."""
    documents = cargar_documentos()
    cohere_reranker = Reordenador(api_key=api_key)
    # The pipeline expects the reranker object, not the key
    main_pipeline = BVG_RAG_Pipeline(documentos=documents, reordenador=cohere_reranker)
    evaluator = EvaluadorPipeline(documentos=documents)
    return main_pipeline, evaluator, documents

# --- User Interface (UI) ---

st.set_page_config(layout="wide", page_title="Advanced RAG Demo")

st.title("🤖 Advanced RAG Pipeline Demo")
st.markdown("This application demonstrates how an advanced search architecture (Hybrid + Re-ranking) drastically improves the quality of answers.")

# --- API Key Loading ---
# Load the API key from the environment instead of asking the user
cohere_api_key = os.getenv("COHERE_API_KEY")

if not cohere_api_key:
    st.error("COHERE_API_KEY not found in your .env file. Please create a .env file and add your Cohere API key to it.")
    st.stop()

# Initialize systems (will run only once thanks to caching)
try:
    pipeline, evaluator, documents = initialize_systems(cohere_api_key)
except Exception as e:
    st.error(f"Error initializing systems with the provided API Key: {e}")
    st.stop()


st.header("1. Ask a Question")
user_query = st.text_input("Example: 'How much is a monthly ticket for AB?' or 'yearly pass for AB area'", "a monthly ticket for AB")

st.header("2. Select the Correct Answer (for Evaluation)")
st.caption("To calculate the ranking metrics, we need to know which document is considered the correct answer ('ground truth').")

doc_options = {f"{i}: {doc.texto[:80]}...": doc for i, doc in enumerate(documents)}
# Set a default correct answer for the default query
selected_doc_key = st.selectbox("Choose the correct document:", options=doc_options.keys(), index=1)
ground_truth_doc = doc_options[selected_doc_key]


if st.button("Get Answer and Evaluate", type="primary"):
    if user_query:
        with st.spinner("Processing... Stage 1 (Hybrid Search) and Stage 2 (Re-ranking) in progress..."):
            
            # --- Final Answer Section ---
            st.subheader("✅ Best Answer (Result from the Full Pipeline)")
            final_results = pipeline.ejecutar(user_query, candidatos_iniciales=10, resultados_finales=1)
            
            if final_results:
                st.success(f"**Text:** {final_results[0].texto}")
                st.write(f"**Metadata:** `{final_results[0].metadata}`")
            else:
                st.warning("The full pipeline did not find a relevant answer.")

            st.divider()

            # --- Evaluation Section ---
            st.subheader("📊 Comparison of Search Strategies (Stage 1)")
            st.caption("This table shows how well each initial search method found the correct document. A higher Reciprocal Rank (closer to 1.0) is better.")
            evaluation_df = evaluator.evaluar_pregunta(user_query, ground_truth_doc)
            st.dataframe(evaluation_df, use_container_width=True)
            
    else:
        st.warning("Please enter a question.")
