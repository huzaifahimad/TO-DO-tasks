import streamlit as st
import requests
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="TODO App",
    page_icon="✅",
    layout="wide"
)

# API base URL
API_URL = "http://localhost:8000"

# App title and description
st.title("✅ TODO Application")
st.markdown("A simple TODO app built with Streamlit and FastAPI")

# Initialize session state for form inputs
if "task_title" not in st.session_state:
    st.session_state.task_title = ""
if "task_description" not in st.session_state:
    st.session_state.task_description = ""

# Sidebar for creating new tasks
with st.sidebar:
    st.header("➕ Create New Task")
    
    title = st.text_input(
        "Task Title",
        value=st.session_state.task_title,
        placeholder="Enter task title..."
    )
    
    description = st.text_area(
        "Task Description",
        value=st.session_state.task_description,
        placeholder="Enter task description...",
        height=100
    )
    
    if st.button("Add Task", type="primary", use_container_width=True):
        if title.strip():
            try:
                response = requests.post(
                    f"{API_URL}/tasks",
                    json={
                        "title": title,
                        "description": description if description else None,
                        "completed": False
                    }
                )
                if response.status_code == 201:
                    st.success("✓ Task created successfully!")
                    st.session_state.task_title = ""
                    st.session_state.task_description = ""
                    st.rerun()
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure the backend is running on http://localhost:8000")
        else:
            st.warning("Please enter a task title")

# Main content area
st.divider()
st.header("📋 My Tasks")

try:
    # Fetch all tasks
    response = requests.get(f"{API_URL}/tasks")
    
    if response.status_code == 200:
        tasks = response.json()
        
        if not tasks:
            st.info("No tasks yet. Create your first task in the sidebar! 🚀")
        else:
            # Display task statistics
            col1, col2, col3 = st.columns(3)
            completed = sum(1 for task in tasks if task.get("completed"))
            
            with col1:
                st.metric("Total Tasks", len(tasks))
            with col2:
                st.metric("Completed", completed)
            with col3:
                st.metric("Remaining", len(tasks) - completed)
            
            st.divider()
            
            # Display tasks
            for task in tasks:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
                    
                    # Task info
                    with col1:
                        # Toggle completion status
                        new_completed = st.checkbox(
                            task["title"],
                            value=task.get("completed", False),
                            label_visibility="visible",
                            key=f"task_{task['id']}"
                        )
                        
                        if new_completed != task.get("completed", False):
                            try:
                                update_response = requests.put(
                                    f"{API_URL}/tasks/{task['id']}",
                                    json={"completed": new_completed}
                                )
                                if update_response.status_code == 200:
                                    st.rerun()
                            except:
                                st.error("Failed to update task")
                        
                        # Display description if exists
                        if task.get("description"):
                            st.markdown(f"*{task['description']}*")
                        
                        # Display timestamps
                        created_at = task.get("created_at", "Unknown")
                        st.caption(f"Created: {created_at}")
                    
                    # Delete button
                    with col2:
                        st.write("")  # Spacer
                    
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_{task['id']}", use_container_width=True):
                            try:
                                delete_response = requests.delete(f"{API_URL}/tasks/{task['id']}")
                                if delete_response.status_code == 200:
                                    st.success("Task deleted!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete task")
                            except:
                                st.error("Failed to delete task")
    else:
        st.error(f"Error fetching tasks: {response.status_code}")

except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to the API")
    st.info("Make sure the backend is running on http://localhost:8000")
    st.info("Run this command in the terminal: `uvicorn main:app --reload`")

# Footer
st.divider()
st.markdown("""
---
**TODO App** | Built with [Streamlit](https://streamlit.io) and [FastAPI](https://fastapi.tiangolo.com/)
""")
