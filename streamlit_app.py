#!/usr/bin/env python3
"""
Main Streamlit App for Cloud Deployment
Entry point for Dharma Platform Live Anti-Nationalist Dashboard
"""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import the dashboard
try:
    from streamlit_live_dashboard import main as dashboard_main
    
    if __name__ == "__main__":
        dashboard_main()
        
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("Please ensure all required files are present in the repository.")
    
    # Fallback: Show basic info
    st.title("Dharma Platform - Live Anti-Nationalist Dashboard")
    st.write("This dashboard searches YouTube for anti-nationalist content and provides threat analysis.")
    st.write("Please check the deployment configuration and try again.")