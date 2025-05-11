import os
import streamlit as st
import py3Dmol
from Bio.PDB import PDBList
from google import generativeai as genai

# Streamlit UI setup
st.set_page_config(page_title="🧬 Protein Viewer", layout="wide")
st.title("🧬 AI-Powered Protein Structure Viewer")

# Get Gemini API key from user
api_key = st.sidebar.text_input("🔑 Enter your Gemini API Key", type="password")
if not api_key:
    st.warning("Please provide your Gemini API key to proceed.")
    st.stop()

# Initialize Gemini client
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Query Gemini for protein IDs
def query_pdb_ids(prompt):
    response = model.generate_content(
        f"List 5 PDB IDs of proteins that match: {prompt}. Output only PDB codes like: 1MBO, 6BB5"
    )
    return [p.strip().upper() for p in response.text.replace("\n", ",").split(",") if p.strip()]

# Fetch PDB structure
def fetch_pdb(pdb_id):
    pdbl = PDBList()
    filepath = pdbl.retrieve_pdb_file(pdb_id, pdir=".", file_format="pdb", overwrite=True)
    return open(filepath).read()

# Render with py3Dmol
def render_structure(pdb_str):
    view = py3Dmol.view(width=800, height=600)
    view.addModel(pdb_str, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})
    view.zoomTo()
    return view

# Sidebar input
prompt = st.sidebar.text_input("🧠 Describe the protein", placeholder="e.g. binds oxygen")

if prompt:
    with st.spinner("Asking Gemini..."):
        try:
            pdb_ids = query_pdb_ids(prompt)
            st.sidebar.success(f"Found {len(pdb_ids)} PDB IDs")
        except Exception as e:
            st.sidebar.error(f"Gemini error: {e}")
            pdb_ids = []
else:
    pdb_ids = []

# Viewer
pdb_choice = st.selectbox("Choose a PDB ID to visualize", pdb_ids or ["1MBO", "6BB5"])
if st.button("🔬 Load Protein Structure"):
    try:
        with st.spinner("Loading PDB file..."):
            structure = fetch_pdb(pdb_choice.lower())
            viewer = render_structure(structure)
            st.components.v1.html(viewer._make_html(), height=600)
    except Exception as e:
        st.error(f"Failed to load structure: {e}")
