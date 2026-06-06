# ⚙️ Silicon & Deep-Tech ATS Optimizer

An AI-powered Applicant Tracking System (ATS) analyzer and resume optimizer built specifically for hardware engineering, VLSI design, and electronics roles. 

Unlike generic ATS parsers tailored for software engineering, this tool uses advanced LLMs to evaluate deep-tech competencies—such as hardware description languages (Verilog, SystemVerilog), verification methodologies (UVM), and EDA tools (Vivado, Cadence).

## ✨ Key Features
* **Domain-Specific Parsing:** Accurately extracts and evaluates complex hardware terminology and architectural metrics.
* **Dynamic Scoring Strictness:** Adjustable ATS rigorously penalizes missing frameworks based on the target role level (Intern, Mid-Level, Senior).
* **STAR Method Bullet Enhancements:** Automatically rewrites generic project descriptions into quantified, technical achievements using the Situation, Task, Action, Result framework.
* **Summary Generation:** Drafts highly targeted professional summaries aligned directly with the pasted job description.
* **Export Action Plan:** Download the complete JSON evaluation for offline review and resume updating.

## 🛠️ Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Pure Python UI architecture)
* **AI/Inference Engine:** [Groq](https://groq.com/) API utilizing the ultra-fast `LLaMA-3.3-70b-versatile` model.
* **Document Processing:** `pdfplumber` for layout-aware text extraction from technical PDFs.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Adarsh73111/vlsi-ats-optimizer.git](https://github.com/Adarsh73111/vlsi-ats-optimizer.git)
   cd vlsi-ats-optimizer