"""Streamlit frontend for hierarchical software planner."""
import streamlit as st
from conversation_tree import conversation as conv
from conversation_tree import llm_interface as llm

def initialize_session_state():
    """Initializes the session state variables."""
    if "current_node" not in st.session_state:
        st.session_state.current_node = None
    if "should_rerun" not in st.session_state:
        st.session_state.should_rerun = False

def display_thread(node: conv.ConversationNode):
    """Display the entire conversation thread leading to this node."""
    # Get the path from root to current node
    thread = node.get_thread()

    # Display each node in the path
    for thread_node in thread:
        st.write("---")
        st.markdown("**Prompt:**")
        st.write(thread_node.get_prompt())
        st.markdown("**Response:**")
        st.write(thread_node.get_response())

def main():
    initialize_session_state()

    # Handle rerun flag
    if st.session_state.should_rerun:
        st.session_state.should_rerun = False
        st.rerun()

    st.title("Software Project Planner")
    
    if st.session_state.current_node is None:
        # Initial project setup
        st.write("Let's plan your software project.")
        project_description = st.text_input("What would you like to build?")
        
        if project_description.strip() and st.button("Start Planning"):
            initial_prompt = f"""Project Goal: {project_description}
            
            Please provide a high-level breakdown of the main components needed for this project."""
            
            st.session_state.current_node = conv.ConversationNode(initial_prompt)
            st.session_state.current_node.generate_response_from_llm()
            st.rerun()
    else:
        # Display full conversation thread
        display_thread(st.session_state.current_node)
        
        # Navigation for existing children
        current_node = st.session_state.current_node
        if current_node.get_children():
            st.write("---")
            st.subheader("Existing branches:")
            for idx, child in enumerate(current_node.get_children()):
                if st.button(f"➡️ {child.get_prompt()[:100]}...", key=f"child_{idx}"):
                    st.session_state.current_node = child
                    st.rerun()
        
        # Add new branch
        st.write("---")
        st.subheader("Add new branch")
        with st.form(key="new_branch"):
            prompt = st.text_input(
                "What aspect would you like to explore or break down further?",
                key="new_prompt"
            )
            
            if st.form_submit_button("Add Branch"):
                if prompt.strip():
                    try:
                        new_node = current_node.add_child(prompt)
                        new_node.generate_response_from_llm()
                        st.session_state.current_node = new_node
                        st.session_state.should_rerun = True
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        # Navigation buttons
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            if current_node.get_parent() and st.button("⬆️ Go Back"):
                st.session_state.current_node = current_node.get_parent()
                st.rerun()
        with col2:
            if st.button("🏠 Start Over"):
                st.session_state.clear()
                st.rerun()

if __name__ == "__main__":
    main()