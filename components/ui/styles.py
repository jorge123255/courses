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
        /* Modern Typography */
        h1, h2, h3 { font-family: 'Inter', sans-serif; }

        /* Card Styling */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            background: #1f67d6;
            color: white;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background: #1855b3;
            transform: translateY(-1px);
        }

        /* Input Fields */
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #e0e2e6;
            padding: 0.5rem;
        }

        /* Progress Indicators */
        .progress-indicator {
            display: flex;
            align-items: center;
            margin: 1rem 0;
        }
        .progress-step {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #e0e2e6;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 0.5rem;
        }
        .progress-step.completed {
            background: #1f67d6;
            color: white;
        }

        /* Quiz Components */
        .quiz-option {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            border: 1px solid #e0e2e6;
            cursor: pointer;
            transition: all 0.3s;
        }
        .quiz-option:hover {
            background: #f8f9fa;
        }
        .quiz-option.selected {
            background: #e3f2fd;
            border-color: #1f67d6;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_custom_styles():
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }

    .card:hover {
        transform: translateY(-2px);
    }

    .explanation-card {
        background: #f8f9fa;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background-color: #4CAF50;
        color: white;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-1px);
    }

    .knowledge-check {
        background: #e3f2fd;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .progress-bar {
        height: 8px;
        background: #ddd;
        border-radius: 4px;
        margin: 1rem 0;
    }

    .progress-bar-fill {
        height: 100%;
        background: #4CAF50;
        border-radius: 4px;
        transition: width 0.3s;
    }

    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }

        .card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_quiz_option(text, is_selected=False):
    return f"""
        <div class="quiz-option{'selected' if is_selected else ''}">
            {text}
        </div>
    """