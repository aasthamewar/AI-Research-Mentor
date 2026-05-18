import streamlit as st
import requests


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Research Mentor",
    page_icon="📘",
    layout="wide"
)


# ---------------- TITLE ----------------
st.title("📘 AI Research Mentor")
st.caption(
    "Upload research papers and learn them step-by-step in beginner-friendly language."
)


# ---------------- SIDEBAR (INFO ONLY) ----------------
with st.sidebar:
    st.header("🎯 What This Tool Does")
    st.write("""
    - Explains papers in beginner language
    - Extracts key concepts
    - Explains architectures and workflows
    - Identifies datasets used
    - Finds research challenges
    - Helps understand papers step-by-step
    """)


# ---------------- SESSION STATE ----------------
if "paper_uploaded" not in st.session_state:
    st.session_state.paper_uploaded = False

if "last_response" not in st.session_state:
    st.session_state.last_response = ""


# ---------------- MAIN SCREEN FILE UPLOAD ----------------
# Only show the file uploader if a paper hasn't been successfully indexed yet
if not st.session_state.paper_uploaded:
    st.markdown("---")
    st.subheader("📂 Upload Research Paper")
    uploaded_file = st.file_uploader(
        "Choose a PDF file to begin analysis",
        type=["pdf"]
    )

    if uploaded_file is not None:
        files = {
            "file": uploaded_file
        }

        with st.spinner("Processing and parsing paper sections..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/upload-paper",
                    files=files
                )
                
                if response.status_code == 200:
                    st.session_state.paper_uploaded = True
                    st.rerun()  # Refresh page to transition to main interface smoothly
                else:
                    st.error("Failed to upload paper. Please check backend server.")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI backend server (127.0.0.1:8000).")


# ---------------- MAIN EXPERIENCE ----------------
if st.session_state.paper_uploaded:

    st.markdown("---")
    st.success("✅ Research paper loaded and structurally indexed.")

    st.subheader("🧠 What would you like to understand?")

    col1, col2, col3 = st.columns(3)

    with col1:
        beginner_btn = st.button("📖 Beginner Explanation", use_container_width=True)
        concepts_btn = st.button("💡 Key Concepts", use_container_width=True)
        challenges_btn = st.button("⚠️ Challenges", use_container_width=True)

    with col2:
        architecture_btn = st.button("🏗️ Architecture Flow", use_container_width=True)
        dataset_btn = st.button("📊 Dataset Used", use_container_width=True)
        applications_btn = st.button("🌍 Applications", use_container_width=True)

    with col3:
        methodology_btn = st.button("⚙️ Methodology", use_container_width=True)
        conclusion_btn = st.button("📌 Conclusion", use_container_width=True)
        gaps_btn = st.button("🔬 Research Gaps", use_container_width=True)


    # ---------------- QUERY ROUTING ----------------
    query = None

    if beginner_btn:
        query = "Explain this research paper in beginner-friendly language."
    elif concepts_btn:
        query = "What are the key concepts discussed in this paper?"
    elif challenges_btn:
        query = "What challenges are discussed in this paper?"
    elif architecture_btn:
        query = "Explain the architecture or system flow proposed in the paper."
    elif dataset_btn:
        query = "What dataset is used in this paper?"
    elif applications_btn:
        query = "What are the real-world applications of this paper?"
    elif methodology_btn:
        query = "Explain the methodology used in this paper."
    elif conclusion_btn:
        query = "Summarize the conclusion of this paper."
    elif gaps_btn:
        query = "What future research gaps or limitations are mentioned?"


    # ---------------- CUSTOM QUESTION ----------------
    st.markdown("---")
    custom_question = st.text_input(
        "Or ask your own custom research question:"
    )

    if custom_question:
        query = custom_question


    # ---------------- ASK API ----------------
    if query:
        with st.spinner("Analyzing context and generating answer..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "question": query
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    # st.session_state.last_response = data["answer"]
                    answer = data["answer"]
                    st.markdown("---")
                    st.subheader("📝 Answer")
                    # --- NEW MERMAID RENDERING ENGINE ENGINE ---
                    if "```mermaid" in answer:
                        import streamlit.components.v1 as components
                        
                        # Find the boundaries of the mermaid markdown blocks
                        start_mermaid = answer.find("```mermaid")
                        end_mermaid = answer.find("```", start_mermaid + 10)

                        if start_mermaid != -1 and end_mermaid != -1:
                            # 1. Extract and write the text explanation BEFORE the diagram
                            text_before_diagram = answer[:start_mermaid].strip()
                            if text_before_diagram:
                                st.write(text_before_diagram)
                            
                            # 2. Isolate just the raw mermaid string syntax
                            mermaid_code = answer[start_mermaid+10 : end_mermaid].strip()
                            
                            # 3. Render it inside a safe HTML/JS iframe container
                            st.subheader("📊 Architecture Diagram")
                            components.html(
                                f"""
                                <div class="mermaid" style="display: flex; justify-content: center;">
                                {mermaid_code}
                                </div>
                                <script type="module">
                                  import mermaid from '[https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs](https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs)';
                                  mermaid.initialize({{ 
                                      startOnLoad: true, 
                                      theme: 'dark'  // Matches your dark dashboard theme nicely!
                                  }});
                                </script>
                                """,
                                height=450,
                                scrolling=True
                            )
                            
                            # 4. Write any remaining follow-up text AFTER the diagram block
                            text_after_diagram = answer[end_mermaid+3:].strip()
                            if text_after_diagram:
                                st.write(text_after_diagram)
                        else:
                            # Fallback if markdown indices match weirdly
                            st.write(answer)
                    else:
                        # Standard text display if no diagram generated by Llama
                        st.write(answer)

                    st.markdown("---")
                    st.subheader("📚 Verified Sources")
                    
                    # Handles dictionary metadata formats gracefully
                    for source in data["sources"]:
                        if isinstance(source, dict):
                            doc = source.get("document", "Unknown Document")
                            sec = source.get("section", "N/A")
                            idx = source.get("chunk_index", "")
                            st.write(f"- **{doc}** | Section: *{sec.capitalize()}* (Chunk {idx})")
                        else:
                            st.write(f"- {source}")
                else:
                    st.error("Failed to get response from AI backend.")
            except requests.exceptions.ConnectionError:
                st.error("Backend connection lost.")
                
    