"""
UI styles for the CISSP Tutor & Exam Platform.
"""
import streamlit as st

def load_css():
    """Load custom CSS styles."""
    st.markdown("""
    <style>
    /* CSS Variables */
    :root {
        --primary: #1E6091;
        --primary-light: #B3CDE0;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-800: #1f2937;
        --radius-sm: 4px;
        --radius-md: 6px;
        --radius-lg: 8px;
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
        --transition-standard: all 0.2s ease;
    }

    /* Global Styles */
    .stApp {
        background-color: var(--gray-50);
    }

    /* Header */
    .cissp-header {
        background-color: white;
        padding: 1rem;
        border-bottom: 1px solid var(--gray-200);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }

    .header-title h1 {
        color: var(--primary);
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }

    /* Navigation */
    .nav-tabs {
        display: flex;
        gap: 1rem;
    }

    .nav-tab {
        padding: 0.5rem 1rem;
        color: var(--gray-800);
        text-decoration: none;
        border-radius: var(--radius-md);
        transition: var(--transition-standard);
    }

    .nav-tab:hover {
        background-color: var(--gray-100);
    }

    .nav-tab.active {
        background-color: var(--primary-light);
        color: var(--primary);
    }

    /* User Profile */
    .user-profile {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .user-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background-color: var(--primary-light);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Cards */
    .card {
        background-color: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: var(--transition-standard);
    }

    .card:hover {
        box-shadow: var(--shadow-md);
    }

    /* Question Display */
    .question-container {
        background-color: white;
        border-radius: var(--radius-lg);
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
    }

    .question-text {
        font-size: 1.1rem;
        color: var(--gray-800);
        margin-bottom: 1.5rem;
    }

    .options-container {
        display: grid;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .option-button {
        background-color: white;
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-md);
        padding: 1rem;
        text-align: left;
        transition: var(--transition-standard);
        cursor: pointer;
    }

    .option-button:hover {
        background-color: var(--gray-100);
        border-color: var(--primary-light);
    }

    .option-button.selected {
        background-color: var(--primary-light);
        border-color: var(--primary);
        color: var(--primary);
    }

    /* Progress Indicators */
    .progress-container {
        background-color: white;
        border-radius: var(--radius-md);
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .progress-bar {
        height: 8px;
        background-color: var(--gray-200);
        border-radius: var(--radius-sm);
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background-color: var(--primary);
        transition: width 0.3s ease;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .nav-tabs {
            display: none;
        }

        .header-title h1 {
            font-size: 1.2rem;
        }

        .card {
            padding: 1rem;
        }

        .question-container {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)