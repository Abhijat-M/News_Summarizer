import streamlit as st
import requests
import time
from newspaper import Article
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Page title layout
c1, c2 = st.columns([0.32, 2])

with c1:
    st.image("images/newspaper.png", width=85)

with c2:
    st.title("FastNews Article Summarizer")

st.markdown("**Generate summaries using advanced abstractive summarization with a faster, modern model.**")

# Sidebar content
st.sidebar.subheader("About the app")
st.sidebar.info("Now using 🤗HuggingFace's [distilbart-cnn-12-6](https://huggingface.co/sshleifer/distilbart-cnn-12-6)  model for faster inference.\
                \nSource code available [here](https://github.com/ivnlee/streamlit-text-summarizer)")   
st.sidebar.write("\n\n")
st.sidebar.markdown("**API Key Setup:**")
st.sidebar.markdown("* Store your key securely in a `.env` file")
st.sidebar.markdown("* Get a free key from [HuggingFace](https://huggingface.co/join)") 
st.sidebar.divider()
st.sidebar.write("Supports English articles not behind paywalls.")
st.sidebar.caption("Created by [Ivan Lee](https://ivan-lee.medium.com/)  using [Streamlit](https://streamlit.io/)🎈.")   

# Inputs 
st.subheader("Enter article URL")
url = st.text_input("URL:", "https://") 

# Use new faster model
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6" 
headers = {"Authorization": f"Bearer {API_KEY}"}

# Fetch article button
if st.button("Fetch and Summarize"):
    if not API_KEY:
        st.error("Please add your HuggingFace API key to .env file")
    
    else:
        try:
            # Fetch article
            article = Article(url)
            article.download()
            article.parse()
            
            with st.spinner('Processing article...'):
                time.sleep(2)
                
                # Call summarization API
                response = requests.post(API_URL, 
                                        headers=headers, 
                                        json={
                                            "inputs": article.text[:1024],
                                            "parameters": {
                                                "truncation": True,
                                                "max_length": 512,
                                                "min_length": 30
                                            }
                                        })
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Check for errors in response
                    if isinstance(result, list) and len(result) > 0 and "summary_text" in result[0]:
                        summary = result[0]['summary_text']
                        st.divider()
                        st.subheader("Summary")
                        st.write(f"**{article.title}**")
                        st.write(summary)
                    else:
                        st.error(f"Unexpected response format: {result}")
                else:
                    error_msg = response.json().get('error', 'Unknown error')
                    st.error(f"API Error ({response.status_code}): {error_msg}")

        except Exception as e:
            st.error(f"Error processing article: {str(e)}")