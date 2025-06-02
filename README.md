# 📰 Diplomatic Briefing Summarizer

AI-powered tool that generates policy-ready summaries in formal diplomatic format. Built with Flask and Hugging Face's NLP models.

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

- **Structured Briefings**: Formal output with:
  - Core Issue Analysis
  - Stakeholder Identification
  - Impact Assessment
  - Actionable Recommendations
- **Fact-Driven**: Maintains strict neutrality with verifiable data
- **Professional Tone**: Suitable for government/organizational briefings
- **Web Interface**: Clean UI with error handling
- **API Integration**: Uses advanced NLP models

## 🛠️ Installation

### Requirements

- Python 3.8+
- Hugging Face API key ([get free key](https://huggingface.co/join))

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/your-repo/summarizer.git 
cd summarizer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
echo "HUGGINGFACE_API_KEY=your_api_key_here" > .env
