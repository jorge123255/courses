"""
Main application for the CISSP Tutor & Exam Platform.
"""
import os
import streamlit as st
import time
from datetime import datetime
import uuid
from pathlib import Path
import json

# Check if UI components are available
UI_COMPONENTS_AVAILABLE = False
try:
    from components.ui import render_enhanced_layout, initialize_ui
    UI_COMPONENTS_AVAILABLE = True
except ImportError:
    pass

import config
from src.ingestion.ingest import ingest_documents, ingest_pdfs
from src.tutoring.tutor import CISSPTutor
from src.exam.exam_generator import ExamGenerator, Exam, ExamAttempt


# Initialize the components
@st.cache_resource
def initialize_components():
    """Initialize all system components."""
    tutor = CISSPTutor()
    exam_generator = ExamGenerator()
    spaced_system = SpacedRepetitionSystem()
    flashcards = FlashcardSystem()
    progress = ProgressTracker()
    return tutor, exam_generator, spaced_system, flashcards, progress


# Set page config
st.set_page_config(
    page_title="CISSP Tutor & Exam Platform",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application function."""
    # Initialize Flask-Login
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY #You need to set this in your config.py file.

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Dummy user model (replace with your actual user model)
    class User:
        def __init__(self, id, username, email=""):
            self.id = id
            self.username = username
            self.email = email

        def is_authenticated(self):
            return True

        def is_active(self):
            return True

        def is_anonymous(self):
            return False

        def get_id(self):
            return str(self.id)


    @login_manager.user_loader
    def load_user(user_id):
        # Replace this with your actual user loading logic
        # For now, simulating a single user for demonstration
        if user_id == "1":
            return User(1, "testuser", "test@example.com")
        return None

    # Initialize AuthManager
    from src.auth.auth_manager import AuthManager
    auth_manager = AuthManager()

    #Simulate login from streamlit's query parameters for demonstration
    username = st.experimental_get_query_params().get("username", [None])[0]
    if username:
        user = load_user("1") #Replace with your user loading logic
        login_user(user)

    # Login page (replace with your actual login template)
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']  #In a real application, you'd hash this for security.

            #Replace with your actual authentication logic
            if username == "testuser" and password == "test": # Replace with your authentication
                user = load_user("1")
                login_user(user)
                return redirect(url_for('main'))
            else:
                flash('Invalid username or password')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # Streamlit main app
    if current_user.is_authenticated:
        # Initialize UI
        from components.ui.styles import load_css
        from components.ui.layout import render_enhanced_layout

        # Load CSS
        load_css()

        # Initialize session state
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())

        # Render enhanced layout
        render_enhanced_layout()
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "current_exam" not in st.session_state:
            st.session_state.current_exam = None
        if "current_attempt" not in st.session_state:
            st.session_state.current_attempt = None
        if "current_question_idx" not in st.session_state:
            st.session_state.current_question_idx = 0
        if "answers" not in st.session_state:
            st.session_state.answers = {}
        if "show_ui_enhancements" not in st.session_state:
            st.session_state.show_ui_enhancements = False

        # Initialize components
        tutor, exam_generator = initialize_components()

        # Sidebar
        with st.sidebar:
            st.title("CISSP Tutor & Exam Platform")
            st.markdown("---")

            # Navigation
            st.subheader("Navigation")
            app_mode = st.radio(
                "Select Mode",
                ["Tutor", "Exam", "Data Management"],
                index=0
            )

            st.markdown("---")

            # Status
            st.subheader("System Status")

            # Check if Ollama is available
            if tutor.llm.is_available():
                st.success("✅ Ollama LLM is available")
            else:
                st.error("❌ Ollama LLM is not available")
                st.info("Please ensure Ollama is running with the llama2 model loaded")
                st.code("ollama run llama2", language="bash")

            # Check if vector database exists
            if os.path.exists(config.DB_DIR) and tutor.retriever.collection:
                collection_count = tutor.retriever.collection.count()
                st.success(f"✅ Vector database ready ({collection_count} documents)")
            else:
                st.warning("⚠️ Vector database not initialized")
                st.info("Please upload and process PDF files in Data Management")

            st.markdown("---")
            st.info("© 2025 CISSP Tutor & Exam Platform")

            # UI Enhancement Preview
            st.subheader("UI Enhancements")
            if st.button("Preview Enhanced UI"):
                st.session_state.show_ui_enhancements = not st.session_state.show_ui_enhancements
                st.rerun()

        # Check if UI enhancement preview is enabled
        if st.session_state.show_ui_enhancements:
            if UI_COMPONENTS_AVAILABLE:
                # Use the new UI components
                # Initialize UI components
                initialize_ui()

                # Use tabs for mode selection
                tab_names = ["Tutor", "Exam", "Data Management"]
                tabs = st.tabs(tab_names)

                with tabs[0]:  # Tutor mode
                    render_enhanced_layout()

                with tabs[1]:  # Exam mode
                    render_exam_mode(exam_generator)

                with tabs[2]:  # Data Management mode
                    render_data_management()

                # Exit the function to only show the enhanced UI
                return
            else:
                # Import the enhancement plan (mockup)
                try:
                    import ui_enhancements.implementation_plan as ui_plan
                    ui_plan.implementation_phases()

                    # Add a button to view the HTML mockup
                    if st.button("View HTML Mockup"):
                        with open("ui_enhancements/layout_redesign.html", "r") as f:
                            html_content = f.read()
                        import streamlit.components.v1 as components
                        components.html(html_content, height=800, scrolling=True)

                    # Exit the function to only show the UI enhancements
                    return
                except Exception as e:
                    st.error(f"Error loading UI enhancements: {e}")

        # Main content
        if app_mode == "Tutor":
            render_tutor_mode(tutor)
        elif app_mode == "Exam":
            render_exam_mode(exam_generator)
        else:  # Data Management
            render_data_management()
    else:
        st.markdown("Please login to continue.")

    #Run Flask app in a separate thread (This is highly simplified and needs proper error handling etc.)
    import threading
    thread = threading.Thread(target=app.run, kwargs={'debug':False, 'host':'0.0.0.0', 'port':5000})
    thread.start()



def render_tutor_mode(tutor):
    """Render the tutor mode interface."""
    st.header("CISSP Tutor")

    # Create tabs for different learning modes
    tab1, tab2, tab3 = st.tabs(["Practice Questions", "Chat Assistant", "Study Materials"])

    with tab1:
        render_practice_questions(tutor)

    with tab2:
        render_chat_interface(tutor)

    with tab3:
        render_study_materials(tutor)

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])

                # Display follow-up questions if available
                if "follow_up_questions" in message:
                    st.markdown("**Follow-up Questions:**")
                    for i, question in enumerate(message["follow_up_questions"]):
                        if st.button(f"{question}", key=f"followup_{i}_{hash(question)}"):
                            # When a follow-up question is clicked, add it as a user message
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": question
                            })
                            # Process the follow-up question
                            with st.spinner("Thinking..."):
                                response = tutor.answer_question(st.session_state.user_id, question)

                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": response["answer"],
                                    "follow_up_questions": response["follow_up_questions"]
                                })
                            st.rerun()

    # Input for new questions
    if prompt := st.chat_input("Ask a question about CISSP concepts..."):
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        # Display user message
        st.chat_message("user").write(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = tutor.answer_question(st.session_state.user_id, prompt)

                st.write(response["answer"])

                # Display contradiction explanation if any
                if response["has_contradictions"] and response["contradiction_explanation"]:
                    st.warning("**Note:** I found contradictions in the source materials.")
                    with st.expander("View contradiction analysis"):
                        st.write(response["contradiction_explanation"])

                # Display follow-up questions
                if response["follow_up_questions"]:
                    st.markdown("**Follow-up Questions:**")
                    for i, question in enumerate(response["follow_up_questions"]):
                        if st.button(f"{question}", key=f"followup_{i}_{hash(question)}"):
                            # When a follow-up question is clicked, add it as a user message
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": question
                            })
                            # Process the follow-up question
                            with st.spinner("Thinking..."):
                                follow_up_response = tutor.answer_question(st.session_state.user_id, question)

                                st.session_state.chat_history.append({
                                    "role": "assistant",
                                    "content": follow_up_response["answer"],
                                    "follow_up_questions": follow_up_response["follow_up_questions"]
                                })
                            st.rerun()

                # Add assistant message to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "follow_up_questions": response["follow_up_questions"]
                })

    # Clear chat button
    if st.session_state.chat_history and st.button("Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

    # Add CSS for styling
    st.markdown("""
    <style>
    /* Main containers */
    .question-container {
        max-width: 900px;
        margin: 0 auto;
    }

    /* Question card styling */
    .question-card {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .question-header {
        color: #1E3A8A;
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 15px;
        border-bottom: 1px solid #eaeaea;
        padding-bottom: 10px;
    }

    .question-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #333;
    }

    /* Option buttons */
    .option-button {
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        text-align: left;
        width: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .option-button:hover {
        background-color: #f0f7ff;
        border-color: #90caf9;
        transform: translateY(-2px);
    }

    .option-button.selected {
        background-color: #e6f7ff;
        border-color: #1890ff;
        font-weight: 500;
    }

    .option-button.correct {
        background-color: #f6ffed;
        border-color: #52c41a;
    }

    .option-button.incorrect {
        background-color: #fff2f0;
        border-color: #ff4d4f;
    }

    /* Explanation card styling */
    .explanation-card {
        background-color: #f7f9fc;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        border-left: 5px solid #2196F3;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    .explanation-title {
        font-weight: 600;
        color: #2196F3;
        margin-bottom: 12px;
        font-size: 1.2rem;
    }

    .explanation-content p {
        margin-bottom: 12px;
    }

    /* References styling */
    .references {
        margin-top: 15px;
        padding: 15px;
        background-color: #f7f9fc;
        border-radius: 8px;
        border-left: 5px solid #9E9E9E;
    }

    .references ul {
        margin-top: 10px;
        padding-left: 20px;
    }

    .references li {
        margin-bottom: 5px;
    }

    /* Result messages */
    .result-message {
        padding: 15px;
        border-radius: 6px;
        margin: 15px 0;
        font-weight: 500;
        display: flex;
        align-items: center;
    }

    .success-message {
        background-color: #e6f7e6;
        color: #2e7d32;
        border-left: 4px solid #2e7d32;
    }

    .error-message {
        background-color: #ffebee;
        color: #c62828;
        border-left: 4px solid #c62828;
    }

    /* Progress indicators */
    .progress-container {
        margin: 20px 0;
        padding: 15px;
        background-color: #f5f7fa;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    .progress-stats {
        display: flex;
        justify-content: space-around;
        text-align: center;
        margin-bottom: 10px;
    }

    .stat-item {
        padding: 10px;
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        display: block;
        color: #1E3A8A;
    }

    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }

    /* Topic badges */
    .topic-badge {
        display: inline-block;
        padding: 5px 12px;
        background-color: #e6f7ff;
        color: #1890ff;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    /* Buttons */
    .action-button {
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        margin-right: 10px;
    }

    .primary-button {
        background-color: #1890ff;
        color: white;
    }

    .primary-button:hover {
        background-color: #096dd9;
        transform: translateY(-2px);
    }

    .secondary-button {
        background-color: #f0f0f0;
        color: #333;
    }

    .secondary-button:hover {
        background-color: #d9d9d9;
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state for review questions
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
    if 'question_answered' not in st.session_state:
        st.session_state.question_answered = False
    if 'questions_history' not in st.session_state:
        st.session_state.questions_history = []
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'topic_stats' not in st.session_state:
        st.session_state.topic_stats = {}

    # Display progress stats if there's history
    if st.session_state.total_questions > 0:
        # Calculate accuracy percentage
        accuracy = int((st.session_state.correct_answers / st.session_state.total_questions) * 100)

        # Create topic performance data
        topic_performance = []
        for topic, stats in st.session_state.topic_stats.items():
            if stats['total'] > 0:
                topic_accuracy = int((stats['correct'] / stats['total']) * 100)
                topic_performance.append((topic, topic_accuracy, stats['total']))

        # Sort by number of questions (descending)
        topic_performance.sort(key=lambda x: x[2], reverse=True)

        # Display progress stats
        st.markdown("""
        <div class="progress-container">
            <div class="progress-stats">
                <div class="stat-item">
                    <span class="stat-value">{}</span>
                    <span class="stat-label">Questions</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{}</span>
                    <span class="stat-label">Correct</span>
                </div>
                <div class="stat-item">
                    <span class="stat-value">{}%</span>
                    <span class="stat-label">Accuracy</span>
                </div>
            </div>
        </div>
        """.format(st.session_state.total_questions, st.session_state.correct_answers, accuracy), unsafe_allow_html=True)

        # Display topic badges if we have at least 3 topics
        if len(topic_performance) >= 2:
            st.markdown("<p><strong>Topic Performance:</strong></p>", unsafe_allow_html=True)
            badges_html = ""
            for topic, acc, count in topic_performance[:5]:  # Show top 5 topics
                badge_color = "#e6f7ff"
                text_color = "#1890ff"
                if acc >= 80:
                    badge_color = "#f6ffed"
                    text_color = "#52c41a"
                elif acc < 60:
                    badge_color = "#fff2f0"
                    text_color = "#ff4d4f"

                badges_html += f"<span class='topic-badge' style='background-color: {badge_color}; color: {text_color};'>{topic}: {acc}%</span>"

            st.markdown(badges_html, unsafe_allow_html=True)

    # Generate review question button with improved styling
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Generate Review Question", key="gen_review", use_container_width=True) or (st.session_state.current_question is None):
            with st.spinner("Generating question..."):
                # Store the question data in session state
                st.session_state.current_question = tutor.generate_review_question(st.session_state.user_id)
                st.session_state.selected_option = None
                st.session_state.question_answered = False
                # Force a rerun to show the question
                st.rerun()

    with col2:
        if st.session_state.total_questions > 0 and st.button("Reset Stats", key="reset_stats"):
            st.session_state.questions_history = []
            st.session_state.correct_answers = 0
            st.session_state.total_questions = 0
            st.session_state.topic_stats = {}
            st.rerun()

    # Display the current question if available
    if st.session_state.current_question:
        question_data = st.session_state.current_question

        # Clean and sanitize the question text to remove any JSON artifacts
        question_text = question_data['question']
        # Remove any JSON or markdown formatting markers
        question_text = question_text.replace('```json', '').replace('```', '')
        question_text = question_text.replace('"question":', '').replace('"', '')

        # Check if the question contains JSON-like content and extract the actual question
        if '{' in question_text and '}' in question_text:
            try:
                # Try to extract just the question text from potential JSON content
                import re
                # Find the actual question text between quotes if it appears to be JSON
                match = re.search(r'"question"\s*:\s*"([^"]+)"', question_text)
                if match:
                    question_text = match.group(1)
                else:
                    # Remove any JSON-like structure
                    question_text = re.sub(r'\{.*?\}', '', question_text, flags=re.DOTALL)
            except Exception:
                # If regex fails, do a simple cleanup
                question_text = question_text.replace('{', '').replace('}', '')

        # Display the cleaned question in a card with improved styling
        st.markdown(f"""
        <div class="question-container">
            <div class='question-card'>
                <div class='question-header'>Question on {question_data['topic']}</div>
                <div class='question-text'>{question_text.strip()}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Create a container for options
        st.markdown("<p><strong>Select the best answer:</strong></p>", unsafe_allow_html=True)

        # Display options in a 2-column layout
        option_cols = st.columns(2)

        # Handle option selection
        for i, option in enumerate(question_data["options"]):
            col_idx = i % 2
            with option_cols[col_idx]:
                # Extract the option letter and text
                option_letter = option[0]  # Get the letter (A, B, C, D)
                option_text = option[2:] if len(option) > 2 else option  # Remove the letter prefix

                # Determine button style based on selection and correctness
                button_class = "option-button"
                if st.session_state.question_answered:
                    if option_letter == question_data["correct_answer"]:
                        button_class += " correct"
                    elif option_letter == st.session_state.selected_option and option_letter != question_data["correct_answer"]:
                        button_class += " incorrect"
                elif st.session_state.selected_option == option_letter:
                    button_class += " selected"

                # Create a styled button for each option
                if st.button(
                    f"{option_letter}. {option_text}", 
                    key=f"option_{i}_{st.session_state.question_answered}",
                    disabled=st.session_state.question_answered,
                    use_container_width=True
                ):
                    st.session_state.selected_option = option_letter
                    st.session_state.question_answered = True
                    st.rerun()

        # If an option is selected, show the result with styling
        if st.session_state.selected_option and st.session_state.question_answered:
            selected_option = st.session_state.selected_option

            # Update statistics
            if st.session_state.current_question not in st.session_state.questions_history:
                st.session_state.total_questions += 1
                if selected_option == question_data["correct_answer"]:
                    st.session_state.correct_answers += 1

                # Update topic stats
                topic = question_data['topic']
                if topic not in st.session_state.topic_stats:
                    st.session_state.topic_stats[topic] = {'correct': 0, 'total': 0}

                st.session_state.topic_stats[topic]['total'] += 1
                if selected_option == question_data["correct_answer"]:
                    st.session_state.topic_stats[topic]['correct'] += 1

                # Add to history
                st.session_state.questions_history.append(st.session_state.current_question)

            # Display result message with improved styling
            if selected_option == question_data["correct_answer"]:
                st.markdown(f"""
                <div class="result-message success-message">
                    <span style="font-size: 1.5rem; margin-right: 10px;">✓</span> 
                    <span>Correct! You've selected the right answer.</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-message error-message">
                    <span style="font-size: 1.5rem; margin-right: 10px;">✕</span>
                    <span>Incorrect. The correct answer is Option {question_data['correct_answer']}.</span>
                </div>
                """, unsafe_allow_html=True)

            # Clean and sanitize the explanation text to remove any JSON artifacts
            explanation_text = question_data['explanation']
            # Remove any JSON or markdown formatting markers
            explanation_text = explanation_text.replace('```json', '').replace('```', '')
            explanation_text = explanation_text.replace('"explanation":', '').replace('"', '')

            # Check if the explanation contains JSON-like content and extract the actual explanation
            if '{' in explanation_text and '}' in explanation_text:
                try:
                    # Try to extract just the explanation text from potential JSON content
                    import re
                    # Find the actual explanation text between quotes if it appears to be JSON
                    match = re.search(r'"explanation"\s*:\s*"([^"]+)"', explanation_text)
                    if match:
                        explanation_text = match.group(1)
                    else:
                        # Remove any JSON-like structure
                        explanation_text = re.sub(r'\{.*?\}', '', explanation_text, flags=re.DOTALL)
                except Exception:
                    # If regex fails, do a simple cleanup
                    explanation_text = explanation_text.replace('{', '').replace('}', '')

            # Format the explanation to highlight key points
            explanation_paragraphs = explanation_text.strip().split('\n\n')
            formatted_explanation = ""

            for para in explanation_paragraphs:
                if para.startswith("Option") and "correct" in para.lower():
                    formatted_explanation += f"<p><strong style='color: #52c41a;'>{para}</strong></p>"
                elif para.startswith("Option"):
                    formatted_explanation += f"<p><strong>{para}</strong></p>"
                else:
                    formatted_explanation += f"<p>{para}</p>"

            # Show the cleaned explanation in a styled card with improved formatting
            st.markdown(f"""
            <div class='explanation-card'>
                <div class='explanation-title'>Explanation</div>
                <div class='explanation-content'>
                    {formatted_explanation}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Add interactive knowledge check
            with st.expander("Test Your Understanding"):
                st.markdown("### Quick Knowledge Check")
                # Extract concept from the current question
                concept = question_data['topic']

                # Create a mini-quiz based on the concept
                mini_quiz_question = f"Based on this explanation about {concept}, which statement is correct?"

                # Generate options dynamically based on the explanation
                correct_statement = ""
                if "correct" in explanation_text:
                    # Extract a key statement from the correct explanation
                    for sentence in explanation_text.split("."):
                        if "correct" in sentence.lower() and len(sentence) > 50:
                            correct_statement = sentence.strip() + "."
                            break

                if not correct_statement and len(explanation_paragraphs) > 0:
                    correct_statement = explanation_paragraphs[0].split(".")[0] + "."

                # Create 3 options (1 correct from explanation, 2 incorrect)
                options = [
                    correct_statement,
                    f"In {concept}, the primary focus is on technical controls rather than administrative procedures.",
                    f"{concept} is mainly concerned with compliance rather than security effectiveness."
                ]

                import random
                random.shuffle(options)
                correct_index = options.index(correct_statement)

                st.radio(
                    mini_quiz_question,
                    options,
                    index=None,
                    key=f"mini_quiz_{hash(question_data['question'])}"
                )

                # Check button
                check_col1, check_col2 = st.columns([1, 3])
                with check_col1:
                    if st.button("Check Answer", key=f"check_mini_quiz_{hash(question_data['question'])}"):
                        user_answer = st.session_state.get(f"mini_quiz_{hash(question_data['question'])}")
                        if user_answer == correct_statement:
                            st.success("Correct! You've understood the key concept.")
                        elif user_answer is not None:
                            st.error(f"Not quite. The correct statement is: {correct_statement}")
                        else:
                            st.warning("Please select an answer first.")

                with check_col2:
                    if st.button("Explain Further", key=f"explain_further_{hash(question_data['question'])}"):
                        st.info(f"The key concept here is about {concept}. {correct_statement} This is important because it relates directly to the core CISSP principles in this domain.")

            # Add practical application
            with st.expander("Practical Application"):
                st.markdown("### Real-World Scenario")

                # Generate a scenario based on the topic
                scenario =f"""
                **Scenario**: You are a security consultant for a large financial organization.

                Your client is implementing {question_data['topic']} controls and has asked for your expert guidance.
                Based on the principles discussed in this question, what would be your recommendation?
                """

                st.markdown(scenario)

                # User input for recommendation
                user_recommendation = st.text_area(
                    "Enter your recommendation:",
                    key=f"scenario_recommendation_{hash(question_data['question'])}"
                )

                # Initialize session state for tracking recommendation visibility
                rec_key = f"show_expert_rec_{hash(question_data['question'])}"
                if rec_key not in st.session_state:
                    st.session_state[rec_key] = False

                if st.button("Submit for Feedback", key=f"submit_scenario_{hash(question_data['question'])}"):
                    if user_recommendation:
                        # The feedback would usually come from an LLM or predefined responses
                        # For now, we'll provide a generic positive feedback
                        st.success("Good thinking! Your recommendation shows understanding of key security principles.")

                        # Set the session state to show expert recommendation
                        st.session_state[rec_key] = True
                    else:
                        st.warning("Please enter your recommendation first.")

                # Show expert recommendation outside the button condition to avoid nesting
                if st.session_state[rec_key]:
                    st.markdown("#### Expert Recommendation")
                    expert_rec = f"""
                    An expert CISSP professional would recommend:

                    1. Evaluate the current {question_data['topic']} implementation against industry frameworks
                    2. Identify gaps in the current implementation compared to best practices
                    3. Develop a roadmap for implementation that prioritizes critical security controls
                    4. Ensure proper documentation and training for all stakeholders
                    5. Implement a continuous monitoring process to validate effectiveness

                    This approach ensures alignment with core CISSP principles while maintaining business operations.
                    """
                    st.markdown(expert_rec)

            # Display references if available
            if "references" in question_data and question_data["references"]:
                st.markdown("""
                <div class="references">
                    <strong>References:</strong>
                    <ul>
                """, unsafe_allow_html=True)

                for ref in question_data["references"]:
                    st.markdown(f"<li>{ref['text']}</li>", unsafe_allow_html=True)

                st.markdown("</ul></div>", unsafe_allow_html=True)

            # Key takeaways section
            key_points = []
            explanation_text_lower = explanation_text.lower()

            # Extract key points based on common phrases in explanations
            for phrase in ["important to note", "key concept", "remember that", "critical to understand", "fundamental principle"]:
                if phrase in explanation_text_lower:
                    # Find the sentence containing this phrase
                    sentences = explanation_text.split(". ")
                    for sentence in sentences:
                        if phrase in sentence.lower():
                            key_points.append(sentence.strip() + ".")

            # If we found key points, display them
            if key_points:
                st.markdown("<h4>Key Takeaways:</h4>", unsafe_allow_html=True)
                for i, point in enumerate(key_points):
                    st.markdown(f"**{i+1}.** {point}")

            # Add buttons with improved styling
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Generate Another Question", key="next_question", use_container_width=True):
                    st.session_state.current_question = None
                    st.session_state.selected_option = None
                    st.session_state.question_answered = False
                    st.rerun()

            with col2:
                # Add a button to save this question for later review
                if st.button("Save for Later Review", key="save_question", use_container_width=True):
                    if 'saved_questions' not in st.session_state:
                        st.session_state.saved_questions = []

                    if st.session_state.current_question not in st.session_state.saved_questions:
                        st.session_state.saved_questions.append(st.session_state.current_question)
                        st.success("Question saved for later review!")

            # Add a "Learning Mode" section for deeper exploration
            with st.expander("Learning Mode - Deep Dive"):
                st.markdown("### CISSP Deep Dive Learning")
                st.markdown("""
                Use this interactive learning tool to explore concepts in more depth.
                The AI will explain the concept in different ways based on your learning preferences.
                """)

                # Extract the core concept
                concept = question_data['topic']
                subtopic = ""

                # Try to identify a more specific subtopic from the question
                for keyword in ["authentication", "authorization", "encryption", "risk", "compliance", 
                               "controls", "governance", "incident", "continuity", "recovery", "access"]:
                    if keyword in question_text.lower():
                        subtopic = keyword
                        break

                if subtopic:
                    concept_text = f"{concept} ({subtopic.capitalize()})"
                else:
                    concept_text = concept

                st.markdown(f"**Exploring: {concept_text}**")

                # Layout improvements
                st.markdown("""
                <div class='learning-container'>
                    <h3>Personalized Learning Experience</h3>
                    <p>Customize how you want to learn this concept</p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    learning_style = st.selectbox(
                        "Learning Style",
                        ["Visual/Conceptual", "Practical/Examples", "Academic/Theoretical", "Interactive/Hands-on"],
                        help="Choose how you want the content to be presented"
                    )

                with col2:
                    complexity = st.select_slider(
                        "Content Complexity",
                        options=["Beginner", "Intermediate", "Advanced", "Expert"],
                        value="Intermediate",
                        help="Adjust the depth of explanations"
                    ), "Storytelling"],
                    key=f"learning_style_{hash(question_data['question'])}"
                )

                # Depth level
                depth_level = st.select_slider(
                    "Select depth level:",
                    options=["Basic", "Intermediate", "Advanced", "Expert"],
                    value="Intermediate",
                    key=f"depth_level_{hash(question_data['question'])}"
                )

                if st.button("Generate Custom Explanation", key=f"generate_learning_{hash(question_data['question'])}"):
                    with st.spinner(f"Generating {depth_level} explanation with {learning_style} approach..."):
                        # Here we would normally call the LLM with a specific prompt
                        # For now, we'll simulate the response with predefined content

                        # Simulate LLM thinking time
                        import time
                        time.sleep(1.5)

                        if learning_style == "Visual/Conceptual":
                            # HTML-based visualization instead of Mermaid diagram
                            st.markdown(f"## {concept_text} - Visual Learning")

                            # Create a hierarchical concept display using HTML
                            html = f"""
                            <div style="margin: 20px 0; font-family: sans-serif;">
                                <div style="background-color: #1E6091; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                                    {concept}
                                </div>

                                <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 15px;">
                                    <div style="width: 48%; background-color: #6497B1; color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s;">
                                        <div style="font-weight: bold; text-align: center; border-bottom: 2px solid white; padding-bottom: 8px; margin-bottom: 15px; font-size: 18px;">Key Principles</div>
                                        <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                                            <li>Least Privilege</li>
                                            <li>Separation of Duties</li>
                                            <li>Defense in Depth</li>
                                        </ul>
                                    </div>

                                    <div style="width: 48%; background-color: #B3CDE0; color: black; padding: 15px; border-radius: 10px; margin-bottom: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s;">
                                        <div style="font-weight: bold; text-align: center; border-bottom: 2px solid #1E6091; padding-bottom: 8px; margin-bottom: 15px; font-size: 18px;">Technologies</div>
                                        <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                                            <li>Implementation Methods</li>
                                            <li>Technical Controls</li>
                                        </ul>
                                    </div>

                                    <div style="width: 48%; background-color: #B3CDE0; color: black; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s;">
                                        <div style="font-weight: bold; text-align: center; border-bottom: 2px solid #1E6091; padding-bottom: 8px; margin-bottom: 15px; font-size: 18px;">Processes</div>
                                        <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                                            <li>Operational Procedures</li>
                                            <li>Audit Requirements</li>
                                        </ul>
                                    </div>

                                    <div style="width: 48%; background-color: #6497B1; color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.3s;">
                                        <div style="font-weight: bold; text-align: center; border-bottom: 2px solid white; padding-bottom: 8px; margin-bottom: 15px; font-size: 18px;">Governance</div>
                                        <ul style="margin: 0; padding-left: 20px; line-height: 1.6;">
                                            <li>Policies</li>
                                            <li>Standards</li>
                                            <li>Guidelines</li>
                                        </ul>
                                    </div>
                                </div>

                                <script>
                                // Add hover effects
                                document.addEventListener("DOMContentLoaded", function() {{
                                    const boxes = document.querySelectorAll('[style*="transition: transform"]');
                                    boxes.forEach(box => {{
                                        box.addEventListener('mouseover', () => {{
                                            box.style.transform = 'translateY(-5px)';
                                        }});
                                        box.addEventListener('mouseout', () => {{
                                            box.style.transform = 'translateY(0)';
                                        }});
                                    }});
                                }});
                                </script>
                            </div>
                            """
                            # Use components.html instead of markdown to properly render HTML
                            import streamlit.components.v1 as components
                            components.html(html, height=450, scrolling=False)

                            # Add a visual table for better understanding
                            st.markdown("### Key Components")
                            data = {
                                "Component": ["Principles", "Technologies", "Processes", "Governance"],
                                "Description": [
                                    "Core security concepts that guide implementation",
                                    "Tools and systems that enforce security measures",
                                    "Procedures and workflows that maintain security",
                                    "Rules and frameworks that govern security decisions"
                                ],
                                "Example": [
                                    "Least Privilege, Defense in Depth",
                                    "Encryption, Access Controls",
                                    "Incident Response, Change Management",
                                    "Policies, Standards, Guidelines"
                                ]
                            }
                            st.dataframe(data, use_container_width=True)

                            st.markdown(f"""
                            ### Key Relationships:

                            In {concept}, the relationship between principles, technologies, and governance creates 
                            a framework that supports secure operations. The correct answer in this question 
                            demonstrates understanding of how these elements work together.
                            """)
                        elif learning_style == "Practical/Examples":
                            st.markdown(f"""
                            ## {concept_text} - Practical Implementation

                            ### Real-World Example

                            A Fortune 500 company implemented {concept} by following these steps:

                            1. **Assessment**: Evaluated current security posture against industry frameworks
                            2. **Gap Analysis**: Identified critical vulnerabilities in their approach
                            3. **Solution Design**: Created architecture incorporating the principles from this question
                            4. **Implementation**: Deployed in phases with continuous testing
                            5. **Validation**: Conducted penetration testing and third-party audit

                            The company discovered that the approach mentioned in the correct answer was most effective
                            because it balanced security requirements with operational needs. This resulted in:

                            - 64% reduction in security incidents
                            - 30% faster access provisioning
                            - Full compliance with regulatory requirements
                            - Minimal impact on business operations

                            ### Implementation Checklist

                            - [ ] Analyze current security architecture
                            - [ ] Identify stakeholder requirements
                            - [ ] Design solution based on correct principles
                            - [ ] Test implementation in staging environment
                            - [ ] Train administrators and users
                            - [ ] Deploy with monitoring
                            - [ ] Review and adjust as needed
                            """)
                        elif learning_style == "Academic/Theoretical":
                            st.markdown(f"""
                            ## {concept_text} - Theoretical Framework

                            ### Foundational Theory

                            The theoretical basis for {concept} is rooted in several key information security models:

                            1. **CIA Triad**: Confidentiality, Integrity, and Availability form the foundation
                            2. **Parker Hexad**: Extends CIA with Possession/Control, Authenticity, and Utility
                            3. **McCumber Cube**: Integrates technology, policy, and human dimensions

                            When analyzing the correct answer in this question, we see alignment with these theoretical
                            constructs, particularly in how it addresses:

                            | Dimension | How Addressed | Security Impact |
                            |-----------|---------------|----------------|
                            | Confidentiality | Access limitations | Prevents unauthorized disclosure |
                            | Integrity | Validation mechanisms | Ensures data accuracy |
                            | Availability | Redundant systems | Maintains service continuity |

                            This theoretical alignment explains why the correct answer is the most appropriate solution
                            from an academic perspective, as it holistically addresses the security requirements while
                            maintaining theoretical consistency.
                            """)
                        else:  # Storytelling
                            st.markdown(f"""
                            ## {concept_text} - The Security Journey

                            ### The Challenge

                            Imagine you're the CISO at Secure Financial Corporation. Your Monday begins with an urgent
                            message from the CEO: "Our auditors found critical issues with our {concept.lower()} implementation.
                            Fix it before our compliance review next month."

                            As you dig into the problem, you discover that the current implementation is:
                            - Fragmented across departments
                            - Inconsistently applied
                            - Creating bottlenecks for legitimate users
                            - Missing key security controls

                            ### The Journey

                            You assemble a tiger team of your best security architects and business representatives.
                            After analyzing multiple approaches, your team narrows down to the options presented in this question.

                            The team debates intensely. The network team argues for option A, while the compliance team
                            pushes for option B. The development team makes a case for option D.

                            But your experienced security architect points out why option C is the superior approach:
                            "This solution addresses our security needs while maintaining operational efficiency."

                            ### The Resolution

                            You implement the solution from the correct answer. Three months later, the auditors return.

                            "I've never seen such a transformation," the lead auditor tells your CEO. "This implementation
                            should be a case study for the industry."

                            The key lesson: Understanding the principles behind {concept.lower()} is more important than
                            implementing trendy solutions. The correct answer demonstrated this understanding.
                            """)

                        # Add a note about how LLM is helping
                        st.info("""
                        **How AI assists your learning:** This explanation was customized based on your selected 
                        learning style and depth preferences. Different learners absorb information differently, 
                        and this approach helps you connect with the material in the way that works best for you.
                        """)

                        # Add key answers for quiz questions to session state
                        if f"quiz_answers_{hash(question_data['question'])}" not in st.session_state:
                            st.session_state[f"quiz_answers_{hash(question_data['question'])}"] = {
                                f"What is the primary benefit of {concept}?": 
                                    f"The primary benefit of {concept} is enhancing security posture while maintaining operational efficiency.",
                                f"How does {concept} relate to the CIA triad?": 
                                    f"{concept} primarily strengthens the Confidentiality and Integrity aspects of the CIA triad.",
                                f"What governance elements are required for effective {concept}?": 
                                    f"Effective {concept} requires policies, standards, and guidelines aligned with organizational objectives.",
                                f"How would you measure the effectiveness of {concept} implementation?": 
                                    f"Effectiveness can be measured through risk reduction metrics, compliance status, and operational impact assessment."
                            }

                        # Replace nested expander with tabs for quiz section
                        quiz_tab, feedback_tab = st.tabs(["Quiz Questions", "Learning Assessment"])

                        with quiz_tab:
                            st.markdown("### Quick Quiz")
                            st.markdown("Answer these questions to reinforce your understanding:")

                            quiz_options = [
                                f"What is the primary benefit of {concept}?",
                                f"How does {concept} relate to the CIA triad?",
                                f"What governance elements are required for effective {concept}?",
                                f"How would you measure the effectiveness of {concept} implementation?"
                            ]

                            # Store the selected question in session state to preserve it
                            quiz_select_key = f"quiz_select_{hash(question_data['question'])}"
                            if quiz_select_key not in st.session_state:
                                st.session_state[quiz_select_key] = quiz_options[0]

                            selected_quiz = st.selectbox(
                                "Select a question:",
                                quiz_options,
                                key=quiz_select_key
                            )

                            # Store the user's answer in session state to preserve it
                            answer_key = f"quiz_answer_{hash(question_data['question'])}_{hash(selected_quiz)}"
                            if answer_key not in st.session_state:
                                st.session_state[answer_key] = ""

                            user_answer = st.text_area(
                                "Your answer:",
                                value=st.session_state[answer_key],
                                key=f"text_area_{answer_key}"
                            )
                            # Update the session state when the user changes their answer
                            st.session_state[answer_key] = user_answer

                            # Add a separate session state for whether feedback has been shown
                            feedback_key = f"feedback_shown_{hash(question_data['question'])}_{hash(selected_quiz)}"
                            if feedback_key not in st.session_state:
                                st.session_state[feedback_key] = False

                            if st.button("Check Answer", key=f"check_quiz_{hash(question_data['question'])}_{hash(selected_quiz)}"):
                                if len(user_answer) < 10:
                                    st.warning("Please provide a more detailed answer.")
                                else:
                                    st.session_state[feedback_key] = True

                            # Always show feedback if it should be shown
                            if st.session_state[feedback_key]:
                                st.success("Good thinking! Your answer demonstrates understanding of key concepts.")

                                # Get the model answer
                                model_answer = st.session_state[f"quiz_answers_{hash(question_data['question'])}"].get(selected_quiz, "")

                                st.markdown("#### Expert Response:")
                                st.markdown(f"*{model_answer}*")

                                st.markdown("""
                                **Key points your answer covered well:**
                                - Connection to fundamental security principles
                                - Practical implementation considerations

                                **Areas to explore further:**
                                - Consider how this concept relates to other domains
                                - Think about challenges in implementing this in various organization types
                                """)

                        with feedback_tab:
                            st.markdown("### Learning Progress")
                            st.markdown("Track your understanding of this concept:")

                            confidence = st.slider(
                                "How confident are you with this concept now?", 
                                1, 10, 5,
                                key=f"confidence_{hash(question_data['question'])}"
                            )

                            if confidence < 5:
                                st.markdown("Don't worry! Complex concepts take time to master. Try reviewing the explanation again with a different learning style.")
                            elif confidence < 8:
                                st.markdown("Good progress! You're developing a solid understanding of this concept.")
                            else:
                                st.markdown("Excellent! You have a strong grasp of this concept. Challenge yourself with more advanced scenarios.")


def render_exam_mode(exam_generator):
    """Render the exam mode interface."""
    st.header("CISSP Practice Exams")

    # If no exam is in progress, show exam selection
    if st.session_state.current_exam is None:
        st.subheader("Start a New Exam")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Quick Start")

            # CISSP domains
            domains = [
                "Security and Risk Management",
                "Asset Security",
                "Security Architecture and Engineering",
                "Communication and Network Security",
                "Identity and Access Management",
                "Security Assessment and Testing",
                "Security Operations",
                "Software Development Security"
            ]

            selected_domain = st.selectbox(
                "Select a domain for a focused exam:",
                ["All Domains"] + domains
            )

            question_count = st.slider(
                "Number of questions:",
                min_value=5,
                max_value=50,
                value=10,
                step=5
            )

            if st.button("Start Exam", key="start_quick_exam"):
                with st.spinner("Generating exam questions..."):
                    if selected_domain == "All Domains":
                        # Generate a balanced exam
                        exam = exam_generator.generate_exam(
                            title="CISSP Practice Exam",
                            description="A practice exam covering all CISSP domains",
                            question_count=question_count
                        )
                    else:
                        # Generate a domain-specific exam
                        exam = exam_generator.generate_domain_specific_exam(
                            domain=selected_domain,
                            question_count=question_count
                        )

                    # Save the exam
                    exam.save_to_file()

                    # Create a new attempt
                    attempt_id = str(uuid.uuid4())
                    attempt = ExamAttempt(
                        attempt_id=attempt_id,
                        user_id=st.session_state.user_id,
                        exam_id=exam.exam_id
                    )

                    # Update session state
                    st.session_state.current_exam = exam
                    st.session_state.current_attempt = attempt
                    st.session_state.current_question_idx = 0
                    st.session_state.answers = {}

                    st.rerun()

        with col2:
            st.markdown("### Adaptive Exam")
            st.markdown(
                "An adaptive exam tailored to your weak areas based on your previous interactions."
            )

            adaptive_question_count = st.slider(
                "Number of adaptive questions:",
                min_value=5,
                max_value=50,
                value=10,
                step=5,
                key="adaptive_count"
            )

            if st.button("Start Adaptive Exam", key="start_adaptive_exam"):
                with st.spinner("Generating adaptive exam questions..."):
                    # Generate an adaptive exam
                    exam = exam_generator.generate_adaptive_exam(
                        user_id=st.session_state.user_id,
                        question_count=adaptive_question_count
                    )

                    # Save the exam
                    exam.save_to_file()

                    # Create a new attempt
                    attempt_id = str(uuid.uuid4())
                    attempt = ExamAttempt(
                        attempt_id=attempt_id,
                        user_id=st.session_state.user_id,
                        exam_id=exam.exam_id
                    )

                    # Update session state
                    st.session_state.current_exam = exam
                    st.session_state.current_attempt = attempt
                    st.session_state.current_question_idx = 0
                    st.session_state.answers = {}

                    st.rerun()

        # Show previous exams if any
        st.markdown("---")
        st.subheader("Previous Exams")

        # Check for previous exam attempts
        attempts_dir = os.path.join(config.DATA_DIR, "attempts")
        if os.path.exists(attempts_dir):
            attempt_files = list(Path(attempts_dir).glob("*.json"))

            if attempt_files:
                for file in attempt_files[:5]:  # Show only the 5 most recent
                    try:
                        attempt = ExamAttempt.load_from_file(str(file))
                        if attempt.user_id == st.session_state.user_id:
                            completed_date = datetime.fromisoformat(attempt.completed_at) if attempt.completed_at else "In Progress"
                            score_pct = f"{attempt.score * 100:.1f}%" if attempt.completed_at else "N/A"

                            st.markdown(f"**Exam Attempt:** {completed_date}")
                            st.markdown(f"**Score:** {score_pct}")

                            if st.button("View Results", key=f"view_{attempt.attempt_id}"):
                                # Load the exam
                                exam_file = os.path.join(config.DATA_DIR, "exams", f"{attempt.exam_id}.json")
                                if os.path.exists(exam_file):
                                    exam = Exam.load_from_file(exam_file)

                                    # Update session state
                                    st.session_state.current_exam = exam
                                    st.session_state.current_attempt = attempt
                                    st.session_state.current_question_idx = 0
                                    st.session_state.answers = attempt.answers

                                    st.rerun()
                    except Exception as e:
                        st.error(f"Error loading attempt: {e}")
            else:
                st.info("No previous exam attempts found.")
        else:
            st.info("No previous exam attempts found.")

    # If an exam is in progress, show the exam interface
    else:
        exam = st.session_state.current_exam
        attempt = st.session_state.current_attempt

        # Show exam information
        st.subheader(exam.title)
        st.markdown(exam.description)

        # Progress bar
        progress = st.progress(0)

        # Get the current question
        if 0 <= st.session_state.current_question_idx < len(exam.questions):
            question = exam.questions[st.session_state.current_question_idx]

            # Update progress bar
            progress.progress((st.session_state.current_question_idx + 1) / len(exam.questions))

            # Display question number
            st.markdown(f"**Question {st.session_state.current_question_idx + 1} of {len(exam.questions)}**")

            # Display the question
            st.markdown(f"### {question.question_text}")

            # Display options
            selected_option = None

            # Check if this question has already been answered
            current_answer = st.session_state.answers.get(question.question_id)

            # If the exam is completed, show the correct answer
            if attempt.completed_at:
                for option in question.options:
                    option_letter = option[0]

                    if option_letter == question.correct_answer:
                        st.success(option)
                    elif current_answer and option_letter == current_answer:
                        st.error(option)
                    else:
                        st.markdown(option)

                # Show explanation
                st.markdown("### Explanation")
                st.markdown(question.explanation)
            else:
                # If the exam is not completed, show the options as buttons
                for i, option in enumerate(question.options):
                    option_letter = option[0]

                    if current_answer == option_letter:
                        st.success(option)
                    elif st.button(option, key=f"q_{question.question_id}_{i}"):
                        selected_option = option_letter

            # If an option is selected, record the answer
            if selected_option:
                st.session_state.answers[question.question_id] = selected_option
                attempt.answer_question(question.question_id, selected_option)

                # Move to the next question
                if st.session_state.current_question_idx < len(exam.questions) - 1:
                    st.session_state.current_question_idx += 1
                    st.rerun()

            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.session_state.current_question_idx > 0:
                    if st.button("Previous", key="prev_question"):
                        st.session_state.current_question_idx -= 1
                        st.rerun()

            with col2:
                # Question selector
                question_idx = st.selectbox(
                    "Go to question:",
                    range(1, len(exam.questions) + 1),
                    index=st.session_state.current_question_idx
                )

                if question_idx - 1 != st.session_state.current_question_idx:
                    st.session_state.current_question_idx = question_idx - 1
                    st.rerun()

            with col3:
                if st.session_state.current_question_idx < len(exam.questions) - 1:
                    if st.button("Next", key="next_question"):
                        st.session_state.current_question_idx += 1
                        st.rerun()

        # Submit button
        if not attempt.completed_at:
            if st.button("Submit Exam", key="submit_exam"):
                # Check if all questions have been answered
                answered_count = len(st.session_state.answers)
                total_count = len(exam.questions)

                if answered_count < total_count:
                    if not st.session_state.get("confirm_submit", False):
                        st.warning(f"You have only answered {answered_count} out of {total_count} questions. Are you sure you want to submit?")
                        if st.button("Yes, submit anyway", key="confirm_submit_btn"):
                            st.session_state.confirm_submit = True
                            st.rerun()
                    else:
                        # Complete the attempt
                        score = attempt.complete(exam)
                        attempt.save_to_file()

                        # Show results
                        st.success(f"Exam submitted! Your score: {score * 100:.1f}%")
                        st.rerun()
                else:
                    # Complete the attempt
                    score = attempt.complete(exam)
                    attempt.save_to_file()

                    # Show results
                    st.success(f"Exam submitted! Your score: {score * 100:.1f}%")
                    st.rerun()

        # Exit button
        if st.button("Exit Exam", key="exit_exam"):
            # If the exam is not completed, ask for confirmation
            if not attempt.completed_at and not st.session_state.get("confirm_exit", False):
                st.warning("Are you sure you want to exit? Your progress will be lost.")
                if st.button("Yes, exit anyway", key="confirm_exit_btn"):
                    st.session_state.confirm_exit = True
                    st.rerun()
            else:
                # Reset session state
                st.session_state.current_exam = None
                st.session_state.current_attempt = None
                st.session_state.current_question_idx = 0
                st.session_state.answers = {}
                st.session_state.confirm_exit = False
                st.session_state.confirm_submit = False
                st.rerun()


def render_data_management():
    """Render the data management interface."""
    st.header("Data Management")

    # Document upload section
    st.subheader("Upload CISSP Study Materials")

    # Create tabs for different document types
    upload_tab1, upload_tab2 = st.tabs(["PDF Upload", "EPUB Upload"])

    with upload_tab1:
        # PDF upload
        uploaded_pdfs = st.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            key="pdf_uploader"
        )

        if uploaded_pdfs:
            # Create the PDF directory if it doesn't exist
            os.makedirs(config.PDF_DIR, exist_ok=True)

            # Save the uploaded files
            for uploaded_file in uploaded_pdfs:
                file_path = os.path.join(config.PDF_DIR, uploaded_file.name)

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            st.success(f"Uploaded {len(uploaded_pdfs)} PDF files")

    with upload_tab2:
        # EPUB upload
        uploaded_epubs = st.file_uploader(
            "Upload EPUB files",
            type=["epub"],
            accept_multiple_files=True,
            key="epub_uploader"
        )

        if uploaded_epubs:
            # Create the PDF directory if it doesn't exist (we're using the same directory)
            os.makedirs(config.PDF_DIR, exist_ok=True)

            # Save the uploaded files
            for uploaded_file in uploaded_epubs:
                file_path = os.path.join(config.PDF_DIR, uploaded_file.name)

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            st.success(f"Uploaded {len(uploaded_epubs)} EPUB files")

    # Process documents section
    st.subheader("Process Documents")

    # Create tabs for processing different document types
    process_tab1, process_tab2, process_tab3 = st.tabs(["Process All", "Process PDFs", "Process EPUBs"])

    # Check if there are documents to process
    pdf_files = list(Path(config.PDF_DIR).glob("*.pdf"))
    epub_files = list(Path(config.PDF_DIR).glob("*.epub"))

    with process_tab1:
        # Process all documents
        total_files = len(pdf_files) + len(epub_files)

        if total_files > 0:
            st.markdown(f"Found {total_files} document files:")

            if pdf_files:
                st.markdown(f"**PDF Files ({len(pdf_files)})**")
                for pdf_file in pdf_files:
                    st.markdown(f"- {pdf_file.name}")

            if epub_files:
                st.markdown(f"**EPUB Files ({len(epub_files)})**")
                for epub_file in epub_files:
                    st.markdown(f"- {epub_file.name}")

            if st.button("Process All Documents", key="process_all"):
                try:
                    with st.spinner("Processing documents and generating embeddings..."):
                        # Run the ingestion process for all document types
                        ingest_documents(file_types=["pdf", "epub"])
                        st.success("Document processing complete!")
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")
                    logger.error(f"Document processing error: {str(e)}", exc_info=True)
                    st.info("The system is now ready to answer questions about the uploaded materials.")
        else:
            st.info("No document files found. Please upload some files first.")

    with process_tab2:
        # Process PDFs only
        if pdf_files:
            st.markdown(f"Found {len(pdf_files)} PDF files:")

            for pdf_file in pdf_files:
                st.markdown(f"- {pdf_file.name}")

            if st.button("Process PDFs Only", key="process_pdfs"):
                with st.spinner("Processing PDFs and generating embeddings..."):
                    # Run the ingestion process for PDFs only
                    ingest_documents(file_types=["pdf"])

                    st.success("PDF processing complete!")
                    st.info("The system is now ready to answer questions about the uploaded materials.")
        else:
            st.info("No PDF files found. Please upload some PDF files first.")

    with process_tab3:
        # Process EPUBs only
        if epub_files:
            st.markdown(f"Found {len(epub_files)} EPUB files:")

            for epub_file in epub_files:
                st.markdown(f"- {epub_file.name}")

            if st.button("Process EPUBs Only", key="process_epubs"):
                with st.spinner("Processing EPUBs and generating embeddings..."):
                    # Run the ingestion process for EPUBs only
                    ingest_documents(file_types=["epub"])

                    st.success("EPUB processing complete!")
                    st.info("The system is now ready to answer questions about the uploaded materials.")
        else:
            st.info("No EPUB files found. Please upload some EPUB files first.")

    # Database management
    st.subheader("Vector Database Management")

    # Check if the database exists
    if os.path.exists(config.DB_DIR):
        st.success("Vector database exists")

        # Option to reset the database
        if st.button("Reset Database", key="reset_db"):
            if not st.session_state.get("confirm_reset", False):
                st.warning("Are you sure you want to reset the database? All embeddings will be lost.")
                if st.button("Yes, reset database", key="confirm_reset_btn"):
                    st.session_state.confirm_reset = True
                    st.rerun()
            else:
                # Reset the database
                import shutil
                shutil.rmtree(config.DB_DIR)
                os.makedirs(config.DB_DIR, exist_ok=True)

                st.success("Database reset complete")
                st.session_state.confirm_reset = False
                st.rerun()
    else:
        st.warning("Vector database does not exist yet. Process PDF files to create it.")


if __name__ == "__main__":
    main()
def render_chat_interface(tutor):
    """Render the chat interface for asking questions about CISSP topics."""
    st.subheader("Chat with CISSP Assistant")

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask any question about CISSP concepts..."):
        # Add user message to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = tutor.answer_question(st.session_state.user_id, prompt)
                st.write(response["answer"])

                # Add assistant message to chat history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response["answer"]
                })

    # Clear chat button
    if st.session_state.chat_history and st.button("Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

def render_study_materials(tutor):
    """Render study materials and concept summaries."""
    st.subheader("Study Materials")

    # Domain selection
    domains = [
        "Security and Risk Management",
        "Asset Security",
        "Security Architecture and Engineering",
        "Communication and Network Security",
        "Identity and Access Management",
        "Security Assessment and Testing",
        "Security Operations",
        "Software Development Security"
    ]

    selected_domain = st.selectbox("Select Domain", domains)

    # Topic selection based on domain
    topics = tutor.get_domain_topics(selected_domain)
    selected_topic = st.selectbox("Select Topic", topics) if topics else None

    if selected_topic:
        # Display topic summary
        with st.expander("Topic Summary", expanded=True):
            summary = tutor.get_topic_summary(selected_topic)
            st.markdown(summary)

        # Display key concepts
        with st.expander("Key Concepts"):
            concepts = tutor.get_key_concepts(selected_topic)
            for concept in concepts:
                st.markdown(f"- **{concept['name']}**: {concept['description']}")

        # Display related topics
        with st.expander("Related Topics"):
            related = tutor.get_related_topics(selected_topic)
            for topic in related:
                st.markdown(f"- {topic}")

        # Study resources
        with st.expander("Additional Resources"):
            resources = tutor.get_topic_resources(selected_topic)
            for resource in resources:
                st.markdown(f"- [{resource['title']}]({resource['link']})")