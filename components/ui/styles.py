"""CSS styles for the CISSP Tutor & Exam Platform."""
import streamlit as st

def load_css():
    """Load custom CSS styles."""
    st.markdown("""
    <style>
    /* Main Layout */
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Navigation */
    .nav-tabs {
        display: flex;
        gap: 1rem;
        padding: 1rem 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 2rem;
    }

    .nav-tab {
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .nav-tab:hover {
        background: #f0f7ff;
    }

    .nav-tab.active {
        background: #1a73e8;
        color: white;
    }

    /* Cards */
    .stCard {
        border-radius: 8px;
        border: 1px solid #eee;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }

    .stCard:hover {
        transform: translateY(-2px);
    }

    /* Buttons */
    .stButton>button {
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        background: #1a73e8;
        color: white;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: #1557b0;
        transform: translateY(-1px);
    }

    /* Questions */
    .question-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 4px solid #1a73e8;
    }

    /* Progress Bars */
    .stProgress > div > div {
        background-color: #1a73e8;
    }

    /* Custom Components */
    .floating-help {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: #1a73e8;
        color: white;
        width: 50px;
        height: 50px;
        border-radius: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }

        .nav-tabs {
            flex-wrap: wrap;
        }
    }
    </style>
    """, unsafe_allow_html=True)