import streamlit as st
import requests

# API base URL
API_BASE_URL = "https://datafreak-navilaw-ai.hf.space"

# Page config with custom theme
st.set_page_config(
    page_title="Project Hifazat ⚖️", 
    page_icon="⚖️",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTitle {
        color: #2e4057;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("⚖️ Project Hifazat")
st.markdown("### Your trusted legal companion for women's rights in Pakistan")

# Mission Statement
st.markdown("""
    > Project Hifazat is dedicated to empowering women across Pakistan by providing 
    accessible legal guidance, support, and resources. We're here to help you understand 
    your rights and navigate the legal system with confidence.
""")

# Services Overview
st.markdown("""
#### 🤝 How We Can Help You:
- **Legal Advisory**: Get guidance on your rights and legal options
- **Legal Report Generation**: Receive detailed analysis of your legal situation
- **Case Outcome Prediction**: Understand potential outcomes of your case
""")

# Emergency Contact Box
st.sidebar.error("""
    ### Emergency Contacts 🆘
    - Women's Protection Helpline: 1043
    - Police Emergency: 15
    - Punjab Women's Helpline: 1043
    - Sindh Women's Helpline: 1094
    - KPK Women's Helpline: 091-9210392
    - Women's Protection Center: 0800-22227
""")

# Confidentiality Notice
st.sidebar.info("""
    ### Your Privacy Matters 🔒
    All conversations are confidential. We prioritize your safety and privacy at every step.
""")

# Main Interface
st.markdown("### How can we assist you today?")

# Query Input
query = st.text_area(
    "Share your legal concern with us (available in English & Urdu):",
    help="Your query will be handled with complete confidentiality"
)

# Option Selection
option = st.selectbox(
    "Select the type of assistance you need:", [
    "Legal Advisory",
    "Legal Report Generation",
    "Case Outcome Prediction"
], help="""
    - Legal Advisory: Get guidance on your rights and options
    - Legal Report: Receive a detailed analysis report
    - Case Prediction: Understand possible outcomes
""")

# Available Support Services
st.sidebar.markdown("""
    ### Support Services Available 🏥
    - Legal Aid Clinics
    - Women's Shelters
    - Counseling Services
    - Documentation Assistance
    - Court Accompaniment
""")

# Submit Button
if st.button("Get Assistance", help="Click to receive your personalized legal guidance"):
    if not query:
        st.warning("Please share your concern so we can assist you better.")
    else:
        with st.spinner("Analyzing your case..."):
            data = {"query": query}
            endpoint = ""
            
            # Determine endpoint based on option
            if option == "Legal Advisory":
                endpoint = "/legal-advisory/"
            elif option == "Legal Report Generation":
                endpoint = "/report-generator/"
            elif option == "Case Outcome Prediction":
                endpoint = "/case-outcome-prediction/"
            
            try:
                response = requests.post(f"{API_BASE_URL}{endpoint}", data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Analysis Complete")
                    
                    # Display results in a clean format
                    for key, value in result.items():
                        st.markdown(f"**{key.replace('_', ' ').title()}**")
                        st.markdown(f"{value}")
                        
                    # Safety reminder
                    st.info("""
                        Remember: Your safety is our priority. If you're in immediate danger,
                        please contact emergency services at 15 or the Women's Protection 
                        Helpline at 1043.
                    """)
                else:
                    st.error("We encountered an issue. Please try again or contact our support team.")
            except Exception as e:
                st.error("Connection error. Please check your internet connection and try again.")

# Footer
st.markdown("""
---
💪 **Project Hifazat:** Empowering women through legal awareness and support
""")

# Disclaimer
st.caption("""
    This service provides general legal information and guidance. For specific legal advice, 
    please consult with a qualified legal professional. In case of emergency, always contact 
    law enforcement or emergency services immediately.
""")