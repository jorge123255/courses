
"""
Layout components for the CISSP Tutor & Exam Platform.
"""
import streamlit as st

def render_enhanced_layout():
    """Render the enhanced layout with improved UI components."""
    # Header
    st.markdown("""
    <div class="cissp-header">
        <div class="header-title">
            <h1>CISSP Tutor & Exam Platform</h1>
        </div>
        <div class="nav-tabs">
            <a href="#" class="nav-tab active">Learn</a>
            <a href="#" class="nav-tab">Practice</a>
            <a href="#" class="nav-tab">Progress</a>
            <a href="#" class="nav-tab">Resources</a>
        </div>
        <div class="user-profile">
            <div class="user-avatar">👤</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Main content area with improved styling
    st.markdown('<div class="content-container">', unsafe_allow_html=True)

    # Add tabs for main navigation
    tab1, tab2, tab3 = st.tabs(["Study Material", "Practice Questions", "Progress"])
    
    with tab1:
        st.markdown("### CISSP Study Materials")
        render_study_materials()
    
    with tab2:
        st.markdown("### Practice Questions")
        render_practice_section()
    
    with tab3:
        st.markdown("### Your Progress")
        render_progress_section()

    st.markdown('</div>', unsafe_allow_html=True)

def render_study_materials():
    """Render the study materials section."""
    # Create a clean card layout for study materials
    st.markdown("""
    <div class="card">
        <h3>Security and Risk Management</h3>
        <p>Master the fundamental concepts of information security and risk management.</p>
    </div>
    """, unsafe_allow_html=True)

def render_practice_section():
    """Render the practice questions section."""
    # Display practice options in a grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>Quick Practice</h3>
            <p>Test your knowledge with randomly selected questions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>Domain-Specific Practice</h3>
            <p>Focus on questions from specific CISSP domains.</p>
        </div>
        """, unsafe_allow_html=True)

def render_progress_section():
    """Render the progress tracking section."""
    # Display progress statistics
    st.markdown("""
    <div class="progress-container">
        <h3>Overall Progress</h3>
        <div class="progress-bar">
            <div class="progress-fill" style="width: 65%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
