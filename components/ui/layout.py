"""Layout components for the CISSP Tutor & Exam Platform."""
import streamlit as st
from .styles import apply_custom_styles # Assuming styles.py exists and contains CSS

def initialize_layout():
    apply_custom_styles()
    st.set_page_config(
        page_title="CISSP Tutor",
        page_icon="📚",
        layout="wide"
    )

def render_progress(current, total):
    progress = (current / total) * 100
    st.markdown(f"""
        <div class='progress-bar'>
            <div class='progress-bar-fill' style='width: {progress}%;'></div>
        </div>
        <p style='text-align: center; color: #666;'>{current}/{total} completed</p>
    """, unsafe_allow_html=True)

def render_knowledge_check(question, options, correct_index):
    st.markdown("<div class='knowledge-check'>", unsafe_allow_html=True)
    st.markdown(f"### {question}")

    for i, option in enumerate(options):
        if st.button(f"Option {i + 1}", key=f"option_{i}"):
            if i == correct_index:
                st.success("Correct! 🎉")
            else:
                st.error("Try again!")

    st.markdown("</div>", unsafe_allow_html=True)

def render_concept_card(title, content):
    st.markdown(f"""
        <div class='card'>
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)


def render_enhanced_layout():
    """Render the enhanced UI layout with modern design."""
    initialize_layout()
    st.markdown('<div class="main">', unsafe_allow_html=True)

    # Header section
    st.title("CISSP Tutor & Exam Platform")

    # Navigation tabs
    tabs = ["Study", "Practice Exam", "Progress", "Resources"]
    st.markdown(
        '<div class="nav-tabs">' +
        ''.join([f'<div class="nav-tab{"" if i else " active"}">{tab}</div>' for i, tab in enumerate(tabs)]) +
        '</div>',
        unsafe_allow_html=True
    )

    # Welcome message
    st.markdown("""
    <div class="stCard">
        <h2>Welcome to Your CISSP Study Journey</h2>
        <p>Track your progress, practice with exam questions, and master CISSP concepts.</p>
    </div>
    """, unsafe_allow_html=True)

    # Help button
    st.markdown(
        '<div class="floating-help">?</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>CISSP Tutor & Exam Platform</h1>
            <p style='font-size: 1.2rem; color: #666;'>Your AI-powered study companion</p>
        </div>
    """, unsafe_allow_html=True)

def render_side_navigation():
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
        render_progress(progress, 100) # Using render_progress for each section
        st.markdown(f"""
            <div class="nav-item{' active' if section == 'Risk Management' else ''}">
                {section}
            </div>
        """, unsafe_allow_html=True)


def render_main_content():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.write("## Current Topic: Risk Management")

    # Example usage of new components
    render_concept_card("Key Concepts", "Risk management fundamentals and methodologies...")
    render_knowledge_check("What is risk?", ["A. Probability x Impact", "B. Threat x Vulnerability", "C. Asset x Control", "D. All of the above"], 0) # Example question

    st.markdown('</div>', unsafe_allow_html=True)