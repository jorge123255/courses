
"""
Layout components for the CISSP Tutor & Exam Platform.
"""
import streamlit as st

def render_enhanced_layout():
    """Render the enhanced layout with improved UI components."""
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="header">
            <h1>CISSP Tutor & Exam Platform</h1>
            <div class="nav-tabs">
                <a href="#" class="nav-tab active">Learn</a>
                <a href="#" class="nav-tab">Practice</a>
                <a href="#" class="nav-tab">Progress</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown('<div class="side-nav">', unsafe_allow_html=True)
        render_navigation()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        render_content()

def render_navigation():
    """Render the side navigation menu."""
    sections = [
        "Security Fundamentals",
        "Risk Management",
        "Asset Security",
        "Security Architecture",
        "Network Security",
        "Identity Management",
        "Security Assessment",
        "Security Operations"
    ]
    
    for section in sections:
        st.markdown(
            f'<div class="nav-item{"" if section != "Risk Management" else " active"}">{section}</div>',
            unsafe_allow_html=True
        )

def render_content():
    """Render the main content area."""
    tab1, tab2, tab3 = st.tabs(["Study", "Practice", "Review"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("Risk Management")
        st.markdown("Learn about risk assessment, analysis, and mitigation strategies.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Progress tracking
        st.progress(0.65)
        st.markdown("65% Complete")
        
        # Content cards
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Key Concepts")
        st.markdown("- Risk identification\n- Risk analysis\n- Risk evaluation\n- Risk treatment")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        render_practice_section()
    
    with tab3:
        render_review_section()

def render_practice_section():
    """Render the practice questions section."""
    st.markdown('<div class="question-container">', unsafe_allow_html=True)
    st.subheader("Practice Questions")
    st.markdown("Test your knowledge with practice questions.")
    
    # Sample question
    st.markdown("**Question 1:** What is the primary purpose of risk assessment?")
    
    options = [
        "To identify and evaluate potential risks",
        "To implement security controls",
        "To develop security policies",
        "To train security personnel"
    ]
    
    for i, option in enumerate(options):
        st.markdown(
            f'<div class="answer-option{"" if i != 0 else " selected"}">{option}</div>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_review_section():
    """Render the review section."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Review Summary")
    st.markdown("- Completed modules: 6/10\n- Average score: 85%\n- Time spent: 4.5 hours")
    st.markdown('</div>', unsafe_allow_html=True)
