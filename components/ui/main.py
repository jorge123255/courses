"""
Main UI component integration for the CISSP Tutor & Exam Platform.
Combines navigation, cards, and other UI components into a cohesive interface.
"""
import streamlit as st
from components.ui.navigation import render_header, render_sidebar_navigation, render_breadcrumbs, render_progress_indicators
from components.ui.cards import render_card, render_grid, render_tabbed_content, render_concept_map, render_knowledge_check, render_floating_button
from components.ui.styles import load_css

def initialize_ui():
    """Initialize the UI components and load CSS."""
    # Load CSS styles
    load_css()
    
    # Initialize session state for UI
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "learn-tab"
    
    if "active_section" not in st.session_state:
        st.session_state.active_section = "security_and_risk_management"
    
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1  # 0-based index
    
    if "show_ui_enhancements" not in st.session_state:
        st.session_state.show_ui_enhancements = True

def render_enhanced_layout():
    """Render the enhanced UI layout."""
    # Initialize UI components
    initialize_ui()
    
    # Render header
    render_header()
    
    # Render sidebar navigation
    render_sidebar_navigation(st.session_state.active_section)
    
    # Main content area
    render_main_content()
    
    # Floating help button
    render_floating_button("Help", "?", "help_button")

def render_main_content():
    """Render the main content area based on active tab."""
    # Breadcrumb navigation
    render_breadcrumbs([
        ("Home", "#"),
        ("Learning Modules", "#"),
        ("Security and Risk Management", "#")
    ])
    
    # Content header
    st.markdown("""
    <div class="content-header">
        <h2>Security and Risk Management</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Content tabs
    tab_names = ["Learn", "Practice", "Flashcards", "Assessment"]
    
    tabs = st.tabs(tab_names)
    
    with tabs[0]:  # Learn tab
        render_learn_content()
    
    with tabs[1]:  # Practice tab
        render_practice_content()
    
    with tabs[2]:  # Flashcards tab
        render_flashcards_content()
    
    with tabs[3]:  # Assessment tab
        render_assessment_content()

def render_learn_content():
    """Render the learning content."""
    # Progress indicators
    steps = ["Introduction", "Key Concepts", "Implementation", "Assessment"]
    render_progress_indicators(steps, st.session_state.current_step)
    
    # Content grid with two columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Visual concept map
        concept_map_content = render_concept_map_content()
        
        # Render as a card
        st.markdown("""
        <div class="card animate-fade-in">
            <div class="card-header">
                Visual Concept Map
                <button class="btn-secondary" style="padding: 4px 8px; font-size: 0.8rem;">Expand</button>
            </div>
            <div class="card-body">
        """, unsafe_allow_html=True)
        
        concept_map_content()
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        # Key components table
        st.markdown("""
        <div class="card animate-fade-in" style="animation-delay: 0.1s;">
            <div class="card-header">
                Key Components
                <button class="btn-secondary" style="padding: 4px 8px; font-size: 0.8rem;">Filter</button>
            </div>
            <div class="card-body">
                <table style="width:100%; border-collapse: collapse;">
                    <tr style="background-color: var(--gray-100);">
                        <th style="padding: 10px; text-align: left; border-bottom: 1px solid var(--gray-200);">Component</th>
                        <th style="padding: 10px; text-align: left; border-bottom: 1px solid var(--gray-200);">Description</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid var(--gray-200);"><strong>Principles</strong></td>
                        <td style="padding: 10px; border-bottom: 1px solid var(--gray-200);">Core security concepts that guide implementation</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid var(--gray-200);"><strong>Technologies</strong></td>
                        <td style="padding: 10px; border-bottom: 1px solid var(--gray-200);">Tools and systems that enforce security measures</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid var(--gray-200);"><strong>Processes</strong></td>
                        <td style="padding: 10px; border-bottom: 1px solid var(--gray-200);">Procedures and workflows that maintain security</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px;"><strong>Governance</strong></td>
                        <td style="padding: 10px;">Rules and frameworks that govern security decisions</td>
                    </tr>
                </table>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Key relationships section (full width)
    st.markdown("""
    <div class="card animate-fade-in" style="animation-delay: 0.2s;">
        <div class="card-header">
            Key Relationships
        </div>
        <div class="card-body">
            <p>In Security and Risk Management, the relationship between principles, technologies, and governance creates a framework that supports secure operations. The correct understanding of these relationships is essential for implementing effective security measures.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Knowledge check
    render_knowledge_check(
        "Based on this explanation about Security and Risk Management, which statement is correct?",
        [
            "The correct answer is D because, as stated in the NIST Cybersecurity Framework (CSF), Risk management involves not only identifying and assessing potential risks but also continuously monitoring and reviewing those assessments to ensure they remain accurate.",
            "Security and Risk Management is mainly concerned with compliance rather than security effectiveness.",
            "In Security and Risk Management, the primary focus is on technical controls rather than administrative procedures."
        ],
        correct_index=0,
        explanation="Risk management is a continuous process that involves identifying, assessing, and monitoring risks. The NIST CSF emphasizes the importance of this ongoing process rather than a one-time assessment.",
        key="srm_quiz"
    )

def render_concept_map_content():
    """Return a function that renders the concept map content."""
    def _render():
        sections = [
            {
                "title": "Key Principles",
                "items": ["Least Privilege", "Separation of Duties", "Defense in Depth"]
            },
            {
                "title": "Technologies",
                "items": ["Implementation Methods", "Technical Controls"]
            },
            {
                "title": "Processes",
                "items": ["Operational Procedures", "Audit Requirements"]
            }
        ]
        
        render_concept_map("Security and Risk Management", sections)
    
    return _render

def render_practice_content():
    """Render the practice content."""
    st.markdown("## Practice Questions")
    st.write("This section contains practice questions to test your understanding of Security and Risk Management concepts.")
    
    # Sample practice question
    st.markdown("""
    <div class="question-card">
        <div class="question-header">Question 1</div>
        <div class="question-text">
            <p>Which of the following best describes the principle of least privilege?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    options = [
        "Users should have the minimum level of access required to perform their job functions",
        "All users should have equal access to system resources",
        "Administrators should have full access to all systems",
        "Users should be granted access based on their seniority in the organization"
    ]
    
    selected_option = None
    for i, option in enumerate(options):
        if st.button(option, key=f"practice_q1_option_{i}"):
            selected_option = i
    
    if selected_option is not None:
        if selected_option == 0:
            st.success("Correct! The principle of least privilege states that users should have only the minimum level of access required to perform their job functions.")
        else:
            st.error("Incorrect. The principle of least privilege states that users should have only the minimum level of access required to perform their job functions.")

def render_flashcards_content():
    """Render the flashcards content."""
    st.markdown("## Flashcards")
    st.write("Review key concepts with these flashcards.")
    
    # Sample flashcard
    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False
    
    st.markdown("""
    <div class="card">
        <div class="card-header">
            Flashcard 1
            <span>1/10</span>
        </div>
        <div class="card-body" style="min-height: 200px; display: flex; align-items: center; justify-content: center;">
    """, unsafe_allow_html=True)
    
    if not st.session_state.show_answer:
        st.markdown("<h3>What is the principle of least privilege?</h3>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center;">
            <h3>Principle of Least Privilege</h3>
            <p>Users should have only the minimum level of access required to perform their job functions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Previous", key="prev_flashcard"):
            st.session_state.show_answer = False
    
    with col2:
        if st.button("Flip Card", key="flip_flashcard"):
            st.session_state.show_answer = not st.session_state.show_answer

def render_assessment_content():
    """Render the assessment content."""
    st.markdown("## Assessment")
    st.write("Test your knowledge with a comprehensive assessment.")
    
    st.markdown("""
    <div class="card">
        <div class="card-header">
            Security and Risk Management Assessment
        </div>
        <div class="card-body">
            <p>This assessment contains 10 questions covering all aspects of Security and Risk Management.</p>
            <p>You will have 20 minutes to complete the assessment.</p>
            <p>A score of 70% or higher is required to pass.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start Assessment", key="start_assessment"):
        st.session_state.assessment_started = True
    
    if st.session_state.get("assessment_started", False):
        st.markdown("### Question 1 of 10")
        st.markdown("""
        <div class="question-text">
            <p>Which of the following is NOT a component of the NIST Cybersecurity Framework?</p>
        </div>
        """, unsafe_allow_html=True)
        
        options = [
            "Identify",
            "Protect",
            "Authenticate",
            "Recover"
        ]
        
        for i, option in enumerate(options):
            st.button(option, key=f"assessment_q1_option_{i}")
