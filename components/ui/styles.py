"""
UI styles for the CISSP Tutor & Exam Platform.
"""
import streamlit as st

def load_css():
    """Load custom CSS styles."""
    st.markdown("""
        <style>
        /* Main containers */
        .stApp {
            background-color: #f5f7fa;
        }

        .question-container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* Card styling */
        .card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            border: 1px solid #eaecef;
            transition: transform 0.2s ease;
        }

        .card:hover {
            transform: translateY(-2px);
        }

        /* Button styling */
        .custom-button {
            background-color: #1E6091;
            color: white;
            padding: 0.6rem 1.2rem;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .custom-button:hover {
            background-color: #154870;
            transform: translateY(-1px);
        }

        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #1E6091;
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            white-space: pre-wrap;
            background-color: white;
            border-radius: 4px;
            color: #1E6091;
            border: 1px solid #eaecef;
        }

        .stTabs [aria-selected="true"] {
            background-color: #1E6091;
            color: white;
        }

        /* Section headers */
        h2 {
            color: #1E6091;
            font-weight: 600;
            margin-bottom: 1.5rem;
        }

        /* Answer options */
        .answer-option {
            background: white;
            padding: 1rem;
            border-radius: 6px;
            border: 1px solid #eaecef;
            margin-bottom: 0.8rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .answer-option:hover {
            background-color: #f8f9fa;
            border-color: #1E6091;
        }

        .answer-option.selected {
            background-color: #e6f7ff;
            border-color: #1E6091;
        }

        /* Navigation menu */
        .side-nav {
            padding: 1rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        .nav-item {
            padding: 0.8rem;
            border-radius: 4px;
            color: #1E6091;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .nav-item:hover {
            background-color: #f8f9fa;
        }

        .nav-item.active {
            background-color: #e6f7ff;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)