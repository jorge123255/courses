"""CSS styles for the CISSP Tutor & Exam Platform."""
import streamlit as st

def load_css():
    """Load custom CSS styles."""
    st.markdown("""
    <style>
    /* Study Materials Styling */
    .study-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #2196F3;
    }

    .concept-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        border: 1px solid #e9ecef;
    }

    .topic-header {
        color: #1a237e;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e3f2fd;
    }

    .concept-title {
        color: #1565c0;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 8px;
    }

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

def apply_custom_styles():
    st.markdown("""
        <style>
        .learning-container {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        }

        .stSelectbox {
            background-color: white;
            border-radius: 5px;
            padding: 5px;
        }

        .knowledge-card {
            background-color: white;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .concept-map {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            margin: 15px 0;
        }

        .interactive-element {
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .interactive-element:hover {
            transform: scale(1.02);
        }
        </style>
    """, unsafe_allow_html=True)