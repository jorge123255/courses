
"""
Layout components for the CISSP Tutor.
"""
import streamlit as st

def render_enhanced_layout():
    """Render the enhanced UI layout."""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="nav-header">
            <h1>CISSP Tutor & Exam Platform</h1>
            <p>Your comprehensive study companion for CISSP certification</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content area with cards
    for domain in ["Security and Risk Management", "Asset Security", "Security Engineering"]:
        st.markdown(f"""
            <div class="content-card">
                <h3>{domain}</h3>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 60%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
