import streamlit as st
import conversation as conv
import llm_interface as llm

# Initialize the Conversation Tree
if "current_node" not in st.session_state:
    st.session_state.current_node = None

# App UI
st.title("Conversation Tree")

if st.session_state.current_node is None:
    # Prompt user for the main goal of their project
    st.subheader("Initialize Your Project")
    main_goal = st.text_input("What is the main goal of your project?")
    if main_goal.strip() and st.button("Start Project"):
        main_goal_prompt = llm.generate_initial_prompt(main_goal)
        st.session_state.current_node = conv.ConversationNode(main_goal_prompt)
        # Query the LLM for the first response
        st.session_state.current_node.generate_response_from_llm()
        st.rerun()
else:
    # Display Current Node
    current_node = st.session_state.current_node
    st.subheader("Current Node")
    st.write(f"**Prompt:** {current_node.get_prompt()}")
    st.write(f"**Response:** {current_node.get_response()}")

    # Display Children
    if current_node.get_children():
        st.subheader("Branches")
        for idx, child in enumerate(current_node.get_children()):
            if st.button(f"Go to Branch {idx + 1}: {child.get_prompt()}"):
                st.session_state.current_node = child
                st.rerun()
    else:
        st.write("No branches yet. Add one below!")

    # Add New Branch
    st.subheader("Add New Branch")
    new_prompt = st.text_input("Enter your prompt:")
    if new_prompt.strip() and st.button("Submit Prompt"):
        new_response = llm.query_llm(new_prompt)
        new_node = current_node.add_child(new_prompt, new_response)
        st.session_state.current_node = new_node
        st.rerun()

    # Navigate Upwards
    if st.button("Go Back"):
        st.session_state.current_node = current_node.get_parent()
        st.rerun()

    # Restart Option
    if st.button("Restart Conversation"):
        del st.session_state.current_node
        st.rerun()
