#!/usr/bin/env python3
"""
🛡️ Dharma Platform - Enhanced Streamlit Cloud Entry Point
Main entry point for Streamlit Cloud deployment with Reddit integration
"""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def main():
    st.set_page_config(
        page_title="🛡️ Dharma Platform - Anti-Nationalist Detection",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    try:
        # Import and run the enhanced immersive dashboard
        from enhanced_immersive_dashboard import main as dashboard_main
        dashboard_main()
    except ImportError as e:
        st.error(f"Enhanced dashboard import error: {e}")
        st.info("Falling back to basic dashboard...")
        
        try:
            # Fallback to basic dashboard
            from streamlit_live_dashboard import main as basic_dashboard_main
            basic_dashboard_main()
        except ImportError as e2:
            st.error(f"Basic dashboard import error: {e2}")
            st.title("🛡️ Dharma Platform")
            st.subheader("Anti-Nationalist Content Detection System")
            st.error("Dashboard modules not found. Please check the deployment.")
            st.info("Required files: enhanced_immersive_dashboard.py, streamlit_live_dashboard.py")
    except Exception as e:
        st.error(f"Application error: {e}")
        st.info("Please check the logs and try again.")

if __name__ == "__main__":
    main()