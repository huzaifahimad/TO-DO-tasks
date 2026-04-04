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
if "task_start_date" not in st.session_state:
    st.session_state.task_start_date = None
if "task_end_date" not in st.session_state:
    st.session_state.task_end_date = None
if "task_priority" not in st.session_state:
    st.session_state.task_priority = None
if "task_progress_status" not in st.session_state:
    st.session_state.task_progress_status = None

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
    
    # Date inputs
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=st.session_state.task_start_date,
            help="When should this task start?"
        )
    with col2:
        end_date = st.date_input(
            "End Date", 
            value=st.session_state.task_end_date,
            help="When should this task be completed?"
        )
    
    # Priority and Progress Status
    col3, col4 = st.columns(2)
    with col3:
        priority = st.selectbox(
            "Priority",
            options=[None, "low", "medium", "high"],
            format_func=lambda x: "Select Priority" if x is None else x.title(),
            help="Task priority level"
        )
    with col4:
        progress_status = st.selectbox(
            "Progress Status",
            options=[None, "not_started", "in_progress", "completed", "on_hold"],
            format_func=lambda x: "Select Status" if x is None else x.replace("_", " ").title(),
            help="Current progress status"
        )
    
    if st.button("Add Task", type="primary", use_container_width=True):
        if title.strip():
            try:
                # Convert dates to datetime objects if provided
                start_datetime = None
                end_datetime = None
                
                if start_date:
                    from datetime import datetime
                    start_datetime = datetime.combine(start_date, datetime.min.time())
                if end_date:
                    from datetime import datetime
                    end_datetime = datetime.combine(end_date, datetime.min.time())
                
                response = requests.post(
                    f"{API_URL}/tasks",
                    json={
                        "title": title,
                        "description": description if description else None,
                        "completed": False,
                        "start_date": start_datetime.isoformat() if start_datetime else None,
                        "end_date": end_datetime.isoformat() if end_datetime else None,
                        "priority": priority,
                        "progress_status": progress_status
                    }
                )
                if response.status_code == 201:
                    st.success("✓ Task created successfully!")
                    st.session_state.task_title = ""
                    st.session_state.task_description = ""
                    st.session_state.task_start_date = None
                    st.session_state.task_end_date = None
                    st.session_state.task_priority = None
                    st.session_state.task_progress_status = None
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
        all_tasks = response.json()
        
        if not all_tasks:
            st.info("No tasks yet. Create your first task in the sidebar! 🚀")
        else:
            # Filters
            st.subheader("🔍 Filters")
            col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
            
            with col_filter1:
                priority_filter = st.multiselect(
                    "Priority",
                    options=["low", "medium", "high"],
                    default=[],
                    help="Filter by priority"
                )
            
            with col_filter2:
                status_filter = st.multiselect(
                    "Progress Status", 
                    options=["not_started", "in_progress", "completed", "on_hold"],
                    default=[],
                    format_func=lambda x: x.replace("_", " ").title(),
                    help="Filter by progress status"
                )
            
            with col_filter3:
                show_completed = st.checkbox("Show Completed", value=True, help="Include completed tasks")
            
            with col_filter4:
                sort_by = st.selectbox(
                    "Sort by",
                    options=["created_at", "priority", "start_date", "end_date"],
                    format_func=lambda x: x.replace("_", " ").title(),
                    help="Sort tasks by"
                )
            
            # Apply filters
            tasks = all_tasks
            
            if priority_filter:
                tasks = [t for t in tasks if t.get("priority") in priority_filter]
            
            if status_filter:
                tasks = [t for t in tasks if t.get("progress_status") in status_filter]
            
            if not show_completed:
                tasks = [t for t in tasks if not t.get("completed", False)]
            
            # Apply sorting
            if sort_by == "priority":
                priority_order = {"high": 0, "medium": 1, "low": 2}
                tasks.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 3))
            elif sort_by == "start_date":
                tasks.sort(key=lambda x: x.get("start_date") or "", reverse=True)
            elif sort_by == "end_date":
                tasks.sort(key=lambda x: x.get("end_date") or "", reverse=True)
            else:  # created_at
                tasks.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
            # Display task statistics
            col1, col2, col3 = st.columns(3)
            completed = sum(1 for task in tasks if task.get("completed"))
            
            with col1:
                st.metric("Filtered Tasks", len(tasks))
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
                        
                        # Display additional fields
                        metadata = []
                        
                        # Priority
                        if task.get("priority"):
                            priority_colors = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                            priority_icon = priority_colors.get(task["priority"], "⚪")
                            metadata.append(f"{priority_icon} {task['priority'].title()}")
                        
                        # Progress Status
                        if task.get("progress_status"):
                            status_icons = {
                                "not_started": "⏳",
                                "in_progress": "🔄", 
                                "completed": "✅",
                                "on_hold": "⏸️"
                            }
                            status_icon = status_icons.get(task["progress_status"], "❓")
                            metadata.append(f"{status_icon} {task['progress_status'].replace('_', ' ').title()}")
                        
                        # Dates
                        if task.get("start_date"):
                            from datetime import datetime
                            try:
                                start_dt = datetime.fromisoformat(task["start_date"].replace('Z', '+00:00'))
                                metadata.append(f"📅 Start: {start_dt.strftime('%Y-%m-%d')}")
                            except:
                                metadata.append(f"📅 Start: {task['start_date']}")
                        
                        if task.get("end_date"):
                            from datetime import datetime
                            try:
                                end_dt = datetime.fromisoformat(task["end_date"].replace('Z', '+00:00'))
                                metadata.append(f"🎯 End: {end_dt.strftime('%Y-%m-%d')}")
                            except:
                                metadata.append(f"🎯 End: {task['end_date']}")
                        
                        if metadata:
                            st.caption(" | ".join(metadata))
                        
                        # Display timestamps
                        created_at = task.get("created_at", "Unknown")
                        st.caption(f"Created: {created_at}")
                    
                    # Edit and Delete buttons
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{task['id']}", use_container_width=True):
                            st.session_state[f"edit_mode_{task['id']}"] = True
                    
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
                    
                    # Edit form (shown when edit button is clicked)
                    if st.session_state.get(f"edit_mode_{task['id']}", False):
                        st.divider()
                        with st.expander("Edit Task", expanded=True):
                            # Edit form fields
                            edit_title = st.text_input(
                                "Title", 
                                value=task.get("title", ""), 
                                key=f"edit_title_{task['id']}"
                            )
                            edit_description = st.text_area(
                                "Description", 
                                value=task.get("description", ""), 
                                key=f"edit_desc_{task['id']}"
                            )
                            
                            # Date inputs for editing
                            edit_col1, edit_col2 = st.columns(2)
                            with edit_col1:
                                # Parse existing start date
                                existing_start = None
                                if task.get("start_date"):
                                    try:
                                        from datetime import datetime
                                        existing_start = datetime.fromisoformat(task["start_date"].replace('Z', '+00:00')).date()
                                    except:
                                        pass
                                edit_start_date = st.date_input(
                                    "Start Date",
                                    value=existing_start,
                                    key=f"edit_start_{task['id']}"
                                )
                            
                            with edit_col2:
                                # Parse existing end date
                                existing_end = None
                                if task.get("end_date"):
                                    try:
                                        from datetime import datetime
                                        existing_end = datetime.fromisoformat(task["end_date"].replace('Z', '+00:00')).date()
                                    except:
                                        pass
                                edit_end_date = st.date_input(
                                    "End Date", 
                                    value=existing_end,
                                    key=f"edit_end_{task['id']}"
                                )
                            
                            # Priority and Progress Status for editing
                            edit_col3, edit_col4 = st.columns(2)
                            with edit_col3:
                                edit_priority = st.selectbox(
                                    "Priority",
                                    options=["low", "medium", "high"],
                                    index=["low", "medium", "high"].index(task.get("priority", "low")) if task.get("priority") in ["low", "medium", "high"] else 0,
                                    key=f"edit_priority_{task['id']}"
                                )
                            with edit_col4:
                                status_options = ["not_started", "in_progress", "completed", "on_hold"]
                                current_status = task.get("progress_status", "not_started")
                                status_index = status_options.index(current_status) if current_status in status_options else 0
                                edit_progress_status = st.selectbox(
                                    "Progress Status",
                                    options=status_options,
                                    format_func=lambda x: x.replace("_", " ").title(),
                                    index=status_index,
                                    key=f"edit_status_{task['id']}"
                                )
                            
                            # Save and Cancel buttons
                            save_col, cancel_col = st.columns(2)
                            with save_col:
                                if st.button("💾 Save Changes", key=f"save_{task['id']}", use_container_width=True):
                                    try:
                                        # Convert dates to datetime objects
                                        start_datetime = None
                                        end_datetime = None
                                        
                                        if edit_start_date:
                                            from datetime import datetime
                                            start_datetime = datetime.combine(edit_start_date, datetime.min.time())
                                        if edit_end_date:
                                            from datetime import datetime
                                            end_datetime = datetime.combine(edit_end_date, datetime.min.time())
                                        
                                        update_response = requests.put(
                                            f"{API_URL}/tasks/{task['id']}",
                                            json={
                                                "title": edit_title,
                                                "description": edit_description if edit_description else None,
                                                "start_date": start_datetime.isoformat() if start_datetime else None,
                                                "end_date": end_datetime.isoformat() if end_datetime else None,
                                                "priority": edit_priority,
                                                "progress_status": edit_progress_status
                                            }
                                        )
                                        if update_response.status_code == 200:
                                            st.success("✓ Task updated successfully!")
                                            st.session_state[f"edit_mode_{task['id']}"] = False
                                            st.rerun()
                                        else:
                                            st.error(f"Failed to update task: {update_response.status_code}")
                                    except Exception as e:
                                        st.error(f"Error updating task: {str(e)}")
                            
                            with cancel_col:
                                if st.button("❌ Cancel", key=f"cancel_{task['id']}", use_container_width=True):
                                    st.session_state[f"edit_mode_{task['id']}"] = False
                                    st.rerun()
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
