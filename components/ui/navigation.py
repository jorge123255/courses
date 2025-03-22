"""
Navigation components for the CISSP Tutor & Exam Platform.
Implements persistent top navigation and sidebar navigation with progress tracking.
"""
import streamlit as st

def render_header():
    """Render the persistent header with main navigation tabs."""
    # Custom CSS for header styling
    st.markdown("""
    <div class="cissp-header">
        <div class="header-title">
            <h1>CISSP Tutor</h1>
        </div>
        <div class="nav-tabs">
            <a href="#" class="nav-tab active" id="learn-tab">Learn</a>
            <a href="#" class="nav-tab" id="practice-tab">Practice Exam</a>
            <a href="#" class="nav-tab" id="progress-tab">My Progress</a>
            <a href="#" class="nav-tab" id="resources-tab">Resources</a>
        </div>
        <div class="user-profile">
            <div class="user-avatar">
                <span>👤</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # JavaScript for tab switching
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Get all tabs
        const tabs = document.querySelectorAll('.nav-tab');
        
        // Add click event to each tab
        tabs.forEach(tab => {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all tabs
                tabs.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Send message to Streamlit
                const tabId = this.id;
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: tabId
                }, '*');
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)

def render_sidebar_navigation(current_section=None):
    """
    Render the sidebar navigation with learning sections and progress tracking.
    
    Args:
        current_section: The currently active section
    """
    # Progress container
    st.sidebar.markdown("""
    <div class="progress-container">
        <h3>Your Progress</h3>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
        <small>35% Complete</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Learning sections
    st.sidebar.markdown("<h3>Learning Sections</h3>", unsafe_allow_html=True)
    
    # Define sections with their completion status
    sections = [
        {"name": "Security Fundamentals", "icon": "📘", "status": "completed"},
        {"name": "Risk Management", "icon": "📊", "status": "completed"},
        {"name": "Security and Risk Management", "icon": "🔒", "status": "active"},
        {"name": "Asset Security", "icon": "💼", "status": ""},
        {"name": "Security Architecture", "icon": "🏗️", "status": ""},
        {"name": "Network Security", "icon": "🌐", "status": ""},
        {"name": "Identity Management", "icon": "👤", "status": ""},
        {"name": "Security Assessment", "icon": "📝", "status": ""},
        {"name": "Security Operations", "icon": "⚙️", "status": ""},
        {"name": "Software Development Security", "icon": "💻", "status": ""}
    ]
    
    # Render each section as a clickable link
    for i, section in enumerate(sections):
        section_id = section["name"].lower().replace(" ", "_")
        if current_section and current_section == section_id:
            section["status"] = "active"
        
        # Create section link with appropriate styling
        section_class = f"section-link {section['status']}"
        completion_indicator = "✓" if section["status"] == "completed" else ""
        
        st.sidebar.markdown(f"""
        <a href="#{section_id}" class="{section_class}" id="nav_{section_id}">
            <span class="icon">{section["icon"]}</span>
            {section["name"]}
            <span class="completion-indicator">{completion_indicator}</span>
        </a>
        """, unsafe_allow_html=True)
    
    # JavaScript for section navigation
    st.sidebar.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Get all section links
        const sectionLinks = document.querySelectorAll('.section-link');
        
        // Add click event to each section link
        sectionLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Get section ID from link ID
                const sectionId = this.id.replace('nav_', '');
                
                // Send message to Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: sectionId
                }, '*');
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)

def render_breadcrumbs(path_items):
    """
    Render breadcrumb navigation.
    
    Args:
        path_items: List of (name, link) tuples representing the path
    """
    breadcrumbs_html = '<div class="breadcrumbs">'
    
    for i, (name, link) in enumerate(path_items):
        if i < len(path_items) - 1:
            breadcrumbs_html += f'<a href="{link}">{name}</a> &gt; '
        else:
            breadcrumbs_html += f'<span>{name}</span>'
    
    breadcrumbs_html += '</div>'
    
    st.markdown(breadcrumbs_html, unsafe_allow_html=True)

def render_progress_indicators(steps, current_step):
    """
    Render progress indicators for learning journey.
    
    Args:
        steps: List of step names
        current_step: Index of the current step (0-based)
    """
    indicators_html = '<div class="progress-indicators">'
    
    for i, step in enumerate(steps):
        status = ""
        if i < current_step:
            status = "completed"
        elif i == current_step:
            status = "active"
        
        indicators_html += f'''
        <div class="progress-indicator {status}">
            <div class="indicator-bubble">{i+1}</div>
            <div class="indicator-label">{step}</div>
        </div>
        '''
    
    indicators_html += '</div>'
    
    st.markdown(indicators_html, unsafe_allow_html=True)
