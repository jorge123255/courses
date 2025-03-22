"""
CSS styles for the CISSP Tutor & Exam Platform.
Implements the visual design system with consistent colors, typography, and components.
"""
import streamlit as st

def load_css():
    """Load CSS styles for the application."""
    st.markdown("""
    <style>
    /* CSS Variables - Modern Design System */
    :root {
        /* Modern color palette */
        --primary: #2563eb; /* Vibrant blue */
        --primary-light: #60a5fa;
        --primary-dark: #1e40af;
        --secondary: #e0f2fe;
        --accent: #8b5cf6; /* Purple accent */
        --success: #10b981; /* Modern green */
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #06b6d4;
        
        /* Neutral palette */
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-400: #9ca3af;
        --gray-500: #6b7280;
        --gray-600: #4b5563;
        --gray-700: #374151;
        --gray-800: #1f2937;
        --gray-900: #111827;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
        
        /* Transitions & Animations */
        --transition-standard: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-fast: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
        --transition-bounce: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        
        /* Border radius */
        --radius-sm: 0.25rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --radius-full: 9999px;
    }
    
    /* Header - Modern Glassmorphism Style */
    .cissp-header {
        background-color: rgba(37, 99, 235, 0.95);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        color: white;
        padding: 16px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: var(--shadow-md);
        position: sticky;
        top: 0;
        z-index: 100;
        margin: -1rem -1rem 1rem -1rem;
        width: calc(100% + 2rem);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header-title h1 {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.025em;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .nav-tabs {
        display: flex;
        gap: 12px;
    }
    
    .nav-tab {
        padding: 8px 16px;
        color: rgba(255,255,255,0.85);
        text-decoration: none;
        border-radius: var(--radius-full);
        transition: var(--transition-bounce);
        font-weight: 500;
        position: relative;
    }
    
    .nav-tab:hover {
        color: white;
        transform: translateY(-2px);
    }
    
    .nav-tab.active {
        background-color: rgba(255,255,255,0.18);
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .nav-tab.active::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 24px;
        height: 3px;
        background-color: white;
        border-radius: var(--radius-full);
        animation: fadeIn 0.3s ease-out forwards;
    }
    
    /* User profile section - Modern Avatar */
    .user-profile {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: var(--radius-full);
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--primary);
        font-weight: bold;
        box-shadow: var(--shadow-md);
        border: 2px solid rgba(255, 255, 255, 0.8);
        transition: var(--transition-bounce);
        overflow: hidden;
    }
    
    .user-avatar:hover {
        transform: scale(1.05);
        box-shadow: var(--shadow-lg);
    }
    
    /* Sidebar */
    .progress-container {
        margin-bottom: 24px;
        background-color: var(--gray-100);
        padding: 16px;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
    }
    
    .progress-bar {
        height: 8px;
        background-color: var(--secondary);
        border-radius: var(--radius-sm);
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background-color: var(--primary);
        border-radius: var(--radius-sm);
        width: 35%;
        transition: width 1s ease-in-out;
    }
    
    .section-link {
        padding: 12px;
        border-radius: var(--radius-sm);
        color: var(--gray-800);
        text-decoration: none;
        transition: var(--transition-standard);
        position: relative;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }
    
    .section-link:hover, .section-link.active {
        background-color: var(--secondary);
        color: var(--primary);
    }
    
    .section-link.completed {
        border-left: 3px solid var(--success);
        padding-left: 9px; /* Adjust for border */
    }
    
    .section-link.active {
        border-left: 3px solid var(--primary);
        padding-left: 9px; /* Adjust for border */
        font-weight: bold;
        background-color: rgba(179, 205, 224, 0.4);
    }
    
    .section-link .icon {
        width: 16px;
        height: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .section-link .completion-indicator {
        margin-left: auto;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
    }
    
    .section-link.completed .completion-indicator {
        background-color: var(--success);
        color: white;
    }
    
    /* Breadcrumbs */
    .breadcrumbs {
        display: flex;
        gap: 8px;
        align-items: center;
        margin-bottom: 12px;
        font-size: 0.875rem;
        color: var(--gray-800);
    }
    
    .breadcrumbs a {
        color: var(--primary);
        text-decoration: none;
    }
    
    .breadcrumbs span {
        color: var(--gray-800);
    }
    
    /* Cards */
    .card {
        background-color: white;
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-sm);
        margin-bottom: 24px;
        transition: var(--transition-standard);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .card-header {
        padding: 18px 24px;
        border-bottom: 1px solid var(--gray-200);
        font-weight: 600;
        background: linear-gradient(to right, var(--gray-50), white);
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 1.1rem;
        letter-spacing: -0.01em;
        color: var(--gray-800);
    }
    
    .card-body {
        padding: 24px;
    }
    
    /* Concept Map */
    .concept-map {
        background-color: white;
        border-radius: var(--radius-md);
        padding: 20px;
        box-shadow: var(--shadow-sm);
    }
    
    .concept-title {
        background-color: var(--primary);
        color: white;
        padding: 12px;
        border-radius: var(--radius-sm);
        text-align: center;
        margin-bottom: 20px;
        font-weight: 600;
        box-shadow: var(--shadow-sm);
    }
    
    .concept-section {
        background-color: var(--primary-light);
        color: white;
        padding: 12px;
        border-radius: var(--radius-sm);
        margin-bottom: 12px;
        transition: var(--transition-standard);
        box-shadow: var(--shadow-sm);
    }
    
    .concept-section:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    .concept-section h4 {
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.3);
        padding-bottom: 8px;
        margin-bottom: 10px;
    }
    
    /* Quiz - Floating Card Style */
    .quiz-container {
        position: sticky;
        bottom: 24px;
        background-color: white;
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-xl);
        padding: 24px;
        z-index: 90;
        border: 1px solid var(--gray-200);
        transition: var(--transition-bounce);
        margin-top: 32px;
        max-width: 95%;
        margin-left: auto;
        margin-right: auto;
    }
    
    .quiz-container:hover {
        box-shadow: 0 -8px 30px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .quiz-container h3 {
        margin-bottom: 12px;
        color: var(--primary);
    }
    
    .quiz-option {
        display: block;
        width: 100%;
        text-align: left;
        padding: 16px 20px;
        margin-bottom: 12px;
        background-color: var(--gray-50);
        border: 1px solid var(--gray-200);
        border-radius: var(--radius-lg);
        cursor: pointer;
        transition: var(--transition-bounce);
        font-size: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .quiz-option:hover {
        background-color: var(--secondary);
        transform: translateY(-2px) scale(1.01);
        box-shadow: var(--shadow-md);
    }
    
    .quiz-option.selected {
        background-color: var(--primary-light);
        color: white;
        border-color: var(--primary);
        box-shadow: 0 0 0 1px var(--primary-light), var(--shadow-md);
    }
    
    .quiz-option::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background-color: var(--primary);
        opacity: 0;
        transition: var(--transition-standard);
    }
    
    .quiz-option:hover::before {
        opacity: 0.5;
    }
    
    .quiz-option.selected::before {
        opacity: 1;
    }
    
    .quiz-option.correct {
        background-color: rgba(76, 175, 80, 0.15);
        border-color: var(--success);
        position: relative;
        padding-left: 36px;
    }
    
    .quiz-option.correct::before {
        content: '✓';
        position: absolute;
        left: 12px;
        color: var(--success);
        font-weight: bold;
    }
    
    .quiz-option.incorrect {
        background-color: rgba(244, 67, 54, 0.15);
        border-color: var(--danger);
        position: relative;
        padding-left: 36px;
    }
    
    .quiz-option.incorrect::before {
        content: '✗';
        position: absolute;
        left: 12px;
        color: var(--danger);
        font-weight: bold;
    }
    
    /* Progress indicators */
    .progress-indicators {
        display: flex;
        margin-bottom: 24px;
        gap: 16px;
    }
    
    .progress-indicator {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
    }
    
    .progress-indicator::after {
        content: '';
        position: absolute;
        height: 2px;
        background-color: var(--gray-200);
        width: 100%;
        top: 14px;
        left: 50%;
        z-index: 0;
    }
    
    .progress-indicator:last-child::after {
        display: none;
    }
    
    .indicator-bubble {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background-color: var(--gray-200);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
        color: var(--gray-800);
        font-weight: bold;
        transition: var(--transition-standard);
    }
    
    .progress-indicator.completed .indicator-bubble {
        background-color: var(--success);
        color: white;
    }
    
    .progress-indicator.active .indicator-bubble {
        background-color: var(--primary);
        color: white;
        box-shadow: 0 0 0 4px rgba(30, 96, 145, 0.2);
    }
    
    .indicator-label {
        font-size: 0.8rem;
        color: var(--gray-800);
        text-align: center;
    }
    
    /* Floating button - Modern Material Style */
    .floating-btn {
        position: fixed;
        bottom: 28px;
        right: 28px;
        width: 60px;
        height: 60px;
        background-color: var(--primary);
        color: white;
        border-radius: var(--radius-full);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow-lg);
        cursor: pointer;
        z-index: 100;
        transition: var(--transition-bounce);
        font-size: 24px;
    }
    
    .floating-btn:hover {
        transform: translateY(-4px) scale(1.08);
        box-shadow: var(--shadow-xl);
        background-color: var(--primary-dark);
    }
    
    .floating-btn::after {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: var(--radius-full);
        background-color: var(--primary);
        z-index: -1;
        opacity: 0.3;
        transform: scale(0);
        transition: transform 0.3s ease-out;
    }
    
    .floating-btn:hover::after {
        transform: scale(1.35);
    }
    
    /* Grid layout */
    .grid-2col {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 24px;
    }
    
    /* Animation effects - Enhanced Animations */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInRight {
        0% { opacity: 0; transform: translateX(20px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes scaleIn {
        0% { opacity: 0; transform: scale(0.95); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    
    .animate-slide-in {
        animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    
    .animate-scale-in {
        animation: scaleIn 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    
    .animate-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    }
    
    /* Responsive styles */
    @media (max-width: 768px) {
        .grid-2col {
            grid-template-columns: 1fr;
        }
        
        .cissp-header {
            padding: 8px 16px;
            flex-wrap: wrap;
        }
        
        .header-title h1 {
            font-size: 1.25rem;
        }
        
        .nav-tabs {
            gap: 4px;
        }
        
        .nav-tab {
            padding: 6px 10px;
            font-size: 0.875rem;
        }
        
        .quiz-container {
            bottom: 10px;
            left: 10px;
            right: 10px;
            padding: 15px;
        }
        
        .floating-btn {
            bottom: 10px;
            right: 10px;
            width: 48px;
            height: 48px;
        }
    }
    
    /* Streamlit specific overrides - Modern UI */
    .stApp {
        background-color: #f8fafc;
        background-image: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Adjust sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: white;
        box-shadow: inset -1px 0 0 rgba(0,0,0,0.05);
    }
    
    /* Improve button styling */
    .stButton > button {
        border-radius: var(--radius-md);
        font-weight: 500;
        transition: var(--transition-bounce);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    
    /* Improve tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-md) var(--radius-md) 0 0;
        padding: 10px 16px;
        transition: var(--transition-standard);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        border-bottom: 2px solid var(--primary) !important;
        font-weight: 600;
    }
    
    /* Improve text inputs */
    .stTextInput > div > div > input {
        border-radius: var(--radius-md);
        border: 1px solid var(--gray-300);
        padding: 12px 16px;
        transition: var(--transition-standard);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
