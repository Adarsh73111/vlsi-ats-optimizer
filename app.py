import streamlit as st
import pdfplumber
from groq import Groq
import os
import json
import time

# Set up clean page styling
st.set_page_config(
    page_title="Deep-Tech ATS Optimizer", 
    page_icon="⚙️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fetch API Key
API_KEY = os.getenv("GROQ_API_KEY")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("⚙️ ATS Parameters")
    st.markdown("Adjust the AI parsing engine settings.")
    
    role_level = st.selectbox(
        "Target Role Level", 
        ["Intern / Entry-Level", "Mid-Level", "Senior / Architecture"]
    )
    
    strictness = st.slider(
        "Scoring Strictness", 
        min_value=1, max_value=10, value=7,
        help="Higher strictness heavily penalizes missing hardware frameworks (like UVM) or specific EDA tools."
    )
    st.write("---")
    st.caption("Powered by Groq & LLaMA 3.3")

if not API_KEY:
    st.sidebar.error("⚠️ GROQ_API_KEY environment variable not found.")

# --- MAIN APP HEADER ---
st.title("⚙️ Silicon & Deep-Tech ATS Optimizer")
st.markdown("Optimize your engineering resume for complex technical roles (VLSI, Digital/Analog Design, and Hardware Verification).")
st.write("---")

# Split Columns Layout
col1, col2 = st.columns(2)

with col1:
    st.header("1. Candidate Profile")
    uploaded_file = st.file_uploader("Upload your technical resume (PDF only)", type="pdf")
    resume_text = ""
    
    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            resume_text = "\n".join(pages)
            
        with st.expander("Preview Parsed Text"):
            st.text(resume_text)

with col2:
    st.header("2. Target Requirement")
    job_desc = st.text_area(
        "Paste the Job Description (JD) here:", 
        height=200,
        placeholder="Paste requirements highlighting SystemVerilog, Vivado, UVM, FPGA architecture, etc..."
    )
    
    analyze_btn = st.button("Analyze & Optimize Match", type="primary", use_container_width=True)

# --- PROCESSING ENGINE ---
if analyze_btn:
    if not API_KEY:
        st.error("Cannot run analysis without an authenticated API key.")
    elif uploaded_file and job_desc:
        
        # Granular Status Container
        with st.status("Initializing deep-tech analysis...", expanded=True) as status:
            st.write("📄 Extracting and normalizing PDF text...")
            time.sleep(0.5) # UI pacing
            st.write("🧠 Connecting to Groq LLaMA-3.3 engine...")
            time.sleep(0.5)
            st.write(f"⚖️ Applying {role_level} benchmarks at strictness level {strictness}/10...")
            
            try:
                client = Groq(api_key=API_KEY)
                
                # Upgraded System Prompt
                system_prompt = (
                    f"You are an expert Senior Silicon Design and Hardware Verification Engineering Manager. "
                    f"You are evaluating this candidate for a {role_level} position. The ATS strictness level is {strictness} out of 10. "
                    f"If the strictness is 7 or higher, deduct points aggressively if specific hardware description languages (Verilog/SystemVerilog), "
                    f"verification methodologies (UVM), or EDA tools are missing from the resume but present in the JD. "
                    f"You must output your complete analysis strictly as a JSON object containing exactly these keys: \n"
                    f"1. 'score' (integer 0-100).\n"
                    f"2. 'summary_suggestion' (A 2-sentence professional summary tailored to this specific job).\n"
                    f"3. 'missing_keywords' (list of missing hardware concepts).\n"
                    f"4. 'bullet_improvements' (list of objects with 'original_bullet' and 'optimized_bullet'). "
                    f"CRITICAL: Every 'optimized_bullet' MUST use the STAR framework (Situation, Task, Action, Result) and quantify technical metrics (e.g., area reduction, power efficiency, simulation time)."
                )
                
                user_content = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_desc}"
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                
                # Parse JSON
                result = json.loads(chat_completion.choices[0].message.content)
                status.update(label="Analysis Complete!", state="complete", expanded=False)
                
                # --- RESULTS DASHBOARD ---
                st.write("---")
                
                # Top Row: Score & Summary
                score = result.get("score", 0)
                score_col, summary_col = st.columns([1, 2])
                
                with score_col:
                    st.metric(
                        label="ATS Match Score", 
                        value=f"{score}/100", 
                        delta="Strong Match" if score >= 75 else f"{score - 75} points from target",
                        delta_color="normal" if score >= 75 else "inverse"
                    )
                
                with summary_col:
                    st.info(f"**Suggested Professional Summary:**\n\n{result.get('summary_suggestion', 'N/A')}")
                
                st.write("---")
                
                # Middle Row: Keywords
                st.subheader("🔍 Missing High-Value Technical Keywords")
                missing = result.get("missing_keywords", [])
                if missing:
                    st.markdown(" ".join([f"`{kw}`" for kw in missing]))
                else:
                    st.success("No critical technical keywords are missing!")
                
                st.write("---")
                
                # Bottom Row: STAR Bullets
                st.subheader("💡 STAR Method Bullet Enhancements")
                improvements = result.get("bullet_improvements", [])
                if improvements:
                    for idx, imp in enumerate(improvements):
                        with st.container():
                            st.markdown(f"**Project/Experience {idx+1}:**")
                            st.caption(f"❌ *Generic:* {imp.get('original_bullet')}")
                            st.markdown(f"✅ *STAR Optimized:* {imp.get('optimized_bullet')}")
                            st.write("")
                
                # Export Feature
                st.write("---")
                st.download_button(
                    label="📥 Download Action Plan (JSON)",
                    data=json.dumps(result, indent=4),
                    file_name="vlsi_resume_optimization.json",
                    mime="application/json",
                    use_container_width=True
                )
                    
            except Exception as e:
                status.update(label="Analysis Failed", state="error")
                st.error(f"An error occurred during interpretation: {e}")
    else:
        st.error("⚠️ Please provide both a PDF resume and a target job description to run the analysis.")