"""
Layout components for the CISSP Tutor & Exam Platform.
"""
import streamlit as st

def render_enhanced_layout():
    """Render the enhanced layout with improved UI components."""
    st.markdown("""
        <style>
        .main-nav { background: #f0f2f6; padding: 1rem; border-radius: 10px; }
        .nav-item { padding: 0.5rem; margin: 0.2rem 0; cursor: pointer; transition: all 0.3s; }
        .nav-item:hover { background: #e0e2e6; border-radius: 5px; }
        .nav-item.active { background: #1f67d6; color: white; border-radius: 5px; }
        .content-card { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .progress-bar { height: 8px; background: #e0e2e6; border-radius: 4px; margin: 1rem 0; }
        .progress-fill { height: 100%; background: #1f67d6; border-radius: 4px; }
        </style>
    """, unsafe_allow_html=True)

    # Top navigation
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <h1>CISSP Tutor</h1>
            <div style="display: flex; gap: 1rem;">
                <div class="nav-item active">Learn</div>
                <div class="nav-item">Practice</div>
                <div class="nav-item">Progress</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Main content area with side navigation
    col1, col2 = st.columns([1, 3])

    with col1:
        render_side_navigation()

    with col2:
        render_main_content()

def render_side_navigation():
    """Render improved side navigation with progress tracking."""
    st.markdown('<div class="main-nav">', unsafe_allow_html=True)

    sections = [
        ("Security Fundamentals", 80),
        ("Risk Management", 60),
        ("Asset Security", 40),
        ("Security Architecture", 30),
        ("Network Security", 20),
        ("Identity Management", 10),
        ("Security Assessment", 0),
        ("Security Operations", 0)
    ]

    for section, progress in sections:
        st.markdown(f"""
            <div class="nav-item{'active' if section == 'Risk Management' else ''}">
                <div>{section}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_main_content():
    """Render main content area with card-based layout."""
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.write("## Current Topic: Risk Management")

    # Create tabs for different learning modes
    tab1, tab2, tab3 = st.tabs(["Learn", "Practice", "Review"])

    with tab1:
        st.write("### Key Concepts")
        st.write("Risk management fundamentals and methodologies...")

    with tab2:
        st.write("### Practice Questions")
        st.write("Test your knowledge with interactive questions...")

    with tab3:
        st.write("### Review Materials")
        st.write("Summary and additional resources...")

    st.markdown('</div>', unsafe_allow_html=True)