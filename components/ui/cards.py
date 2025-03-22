"""
Card-based UI components for the CISSP Tutor & Exam Platform.
Implements modern card layouts, tabbed interfaces, and other visual components.
"""
import streamlit as st

def render_card(title, content, key=None, expanded=True, card_class=""):
    """
    Render a card with a title and content.
    
    Args:
        title: Card title
        content: Card content (HTML string)
        key: Unique key for the card (for state management)
        expanded: Whether the card is expanded by default
        card_class: Additional CSS class for the card
    """
    card_id = f"card_{key}" if key else f"card_{hash(title)}"
    
    card_html = f'''
    <div class="card {card_class}" id="{card_id}">
        <div class="card-header">
            {title}
        </div>
        <div class="card-body">
            {content}
        </div>
    </div>
    '''
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_grid(columns=2):
    """
    Create a grid layout with the specified number of columns.
    
    Args:
        columns: Number of columns in the grid
        
    Returns:
        List of column objects
    """
    return st.columns(columns)

def render_tabbed_content(tabs, content_dict, key=None):
    """
    Render content in a tabbed interface.
    
    Args:
        tabs: List of tab names
        content_dict: Dictionary mapping tab names to content functions
        key: Unique key for the tabs
    """
    if key:
        tab_objects = st.tabs(tabs, key=key)
    else:
        tab_objects = st.tabs(tabs)
    
    for i, tab in enumerate(tabs):
        with tab_objects[i]:
            if tab in content_dict:
                content_dict[tab]()

def render_concept_map(title, sections):
    """
    Render a visual concept map.
    
    Args:
        title: Main concept title
        sections: List of dictionaries with 'title' and 'items' keys
    """
    concept_map_html = f'''
    <div class="concept-map">
        <div class="concept-title">
            {title}
        </div>
    '''
    
    # If there are more than 2 sections, create a grid
    if len(sections) > 2:
        concept_map_html += '<div class="grid-2col">'
    
    # Add each section
    for section in sections:
        concept_map_html += f'''
        <div class="concept-section">
            <h4>{section['title']}</h4>
            <ul>
        '''
        
        for item in section['items']:
            concept_map_html += f'<li>{item}</li>'
        
        concept_map_html += '''
            </ul>
        </div>
        '''
    
    # Close grid if needed
    if len(sections) > 2:
        concept_map_html += '</div>'
    
    concept_map_html += '</div>'
    
    st.markdown(concept_map_html, unsafe_allow_html=True)

def render_knowledge_check(question, options, correct_index=None, explanation=None, key=None):
    """
    Render a knowledge check component.
    
    Args:
        question: Question text
        options: List of option texts
        correct_index: Index of the correct option (if revealed)
        explanation: Explanation text (shown after answering)
        key: Unique key for the component
    """
    component_key = key if key else f"quiz_{hash(question)}"
    
    # Initialize session state for this quiz
    if f"{component_key}_selected" not in st.session_state:
        st.session_state[f"{component_key}_selected"] = None
    
    if f"{component_key}_checked" not in st.session_state:
        st.session_state[f"{component_key}_checked"] = False
    
    # Create the quiz container
    st.markdown(f'''
    <div class="quiz-container" id="{component_key}">
        <h3>Quick Knowledge Check</h3>
        <p>{question}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Create option buttons
    for i, option in enumerate(options):
        # Determine button state
        is_selected = st.session_state[f"{component_key}_selected"] == i
        is_correct = correct_index is not None and i == correct_index
        is_incorrect = st.session_state[f"{component_key}_checked"] and is_selected and not is_correct
        
        button_class = "quiz-option"
        if is_selected:
            button_class += " selected"
        if st.session_state[f"{component_key}_checked"]:
            if is_correct:
                button_class += " correct"
            elif is_incorrect:
                button_class += " incorrect"
        
        # Create a unique key for each option button
        option_key = f"{component_key}_option_{i}"
        
        if st.button(option, key=option_key, disabled=st.session_state[f"{component_key}_checked"]):
            st.session_state[f"{component_key}_selected"] = i
            st.rerun()
    
    # Add check answer and explain buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Check Answer", key=f"{component_key}_check", 
                    disabled=st.session_state[f"{component_key}_selected"] is None or 
                             st.session_state[f"{component_key}_checked"]):
            st.session_state[f"{component_key}_checked"] = True
            st.rerun()
    
    with col2:
        if st.button("Explain Further", key=f"{component_key}_explain", 
                    disabled=not st.session_state[f"{component_key}_checked"]):
            if explanation:
                st.info(explanation)

def render_floating_button(text, icon=None, key=None):
    """
    Render a floating action button.
    
    Args:
        text: Button text or tooltip
        icon: Icon to display (emoji)
        key: Unique key for the button
    """
    button_id = key if key else f"floating_btn_{hash(text)}"
    button_content = icon if icon else text
    
    st.markdown(f'''
    <div class="floating-btn" id="{button_id}" title="{text}">
        {button_content}
    </div>
    ''', unsafe_allow_html=True)
    
    # JavaScript for button click handling
    st.markdown(f'''
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        const floatingBtn = document.getElementById('{button_id}');
        if (floatingBtn) {{
            floatingBtn.addEventListener('click', function() {{
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: '{button_id}_clicked'
                }}, '*');
            }});
        }}
    }});
    </script>
    ''', unsafe_allow_html=True)
