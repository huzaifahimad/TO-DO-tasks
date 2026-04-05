import streamlit as st
import requests
from datetime import datetime, date
import time
import random
import os

# Configure the page with enhanced styling
st.set_page_config(
    page_title="TODO App Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

.slide-in {
    animation: slideIn 0.3s ease-out;
}

.bounce {
    animation: bounce 1s;
}

.pulse {
    animation: pulse 2s infinite;
}

.task-card {
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.task-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.priority-high {
    border-left: 4px solid #ff4757;
    background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
}

.priority-medium {
    border-left: 4px solid #ffa726;
    background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%);
}

.priority-low {
    border-left: 4px solid #4caf50;
    background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
}

.status-completed {
    background: linear-gradient(135deg, #a8e6cf 0%, #dcedc8 100%);
}

.status-in-progress {
    background: linear-gradient(135deg, #ffd3a5 0%, #fdffb6 100%);
}

.status-not-started {
    background: linear-gradient(135deg, #f7f1e3 0%, #e8e8e8 100%);
}

.status-on-hold {
    background: linear-gradient(135deg, #ffcccc 0%, #ffb3ba 100%);
}

.progress-bar {
    width: 100%;
    height: 8px;
    background-color: #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
    margin: 5px 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4CAF50, #45a049);
    border-radius: 4px;
    transition: width 0.5s ease;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
    padding: 20px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.success-animation {
    animation: bounce 0.6s;
}

.stButton>button {
    border-radius: 20px;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
}

.stTextInput>div>div>input, .stTextArea>div>textarea {
    border-radius: 10px;
    border: 2px solid #e0e0e0;
    transition: border-color 0.3s ease;
}

.stTextInput>div>div>input:focus, .stTextArea>div>textarea:focus {
    border-color: #4CAF50;
    box-shadow: 0 0 10px rgba(76, 175, 80, 0.2);
}
</style>
""", unsafe_allow_html=True)

# API base URL - use environment variable or default to localhost for development
API_URL = os.getenv("STREAMLIT_API_URL", "https://to-do-tasks-topaz.vercel.app").rstrip("/")

# App title and description with animation
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.title("🚀 TODO App Pro")
st.markdown("*Advanced task management with animations and visual enhancements*")
st.markdown('</div>', unsafe_allow_html=True)

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
if "show_success" not in st.session_state:
    st.session_state.show_success = False
if "success_message" not in st.session_state:
    st.session_state.success_message = ""

# Success message animation
if st.session_state.show_success:
    st.markdown(f'<div class="success-animation"><h3 style="color: #4CAF50;">{st.session_state.success_message}</h3></div>', unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.show_success = False
    st.rerun()

# Sidebar for creating new tasks with enhanced styling
with st.sidebar:
    st.markdown('<div class="slide-in">', unsafe_allow_html=True)
    st.header("➕ Create New Task")

    # Progress indicator for form completion
    form_fields = [st.session_state.task_title, st.session_state.task_description]
    completed_fields = sum(1 for field in form_fields if field and field.strip())
    progress_percentage = (completed_fields / len(form_fields)) * 100

    st.progress(progress_percentage / 100)
    st.caption(f"Form completion: {int(progress_percentage)}%")

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

    # Date inputs with icons
    st.markdown("📅 **Date Range**")
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

    # Priority and Progress Status with enhanced UI
    st.markdown("🎯 **Task Settings**")
    col3, col4 = st.columns(2)
    with col3:
        priority_options = {"low": "🟢 Low", "medium": "🟡 Medium", "high": "🔴 High"}
        priority = st.selectbox(
            "Priority",
            options=[None] + list(priority_options.keys()),
            format_func=lambda x: priority_options.get(x, "Select Priority") if x else "Select Priority",
            help="Task priority level"
        )
    with col4:
        status_options = {
            "not_started": "⏳ Not Started",
            "in_progress": "🔄 In Progress",
            "completed": "✅ Completed",
            "on_hold": "⏸️ On Hold"
        }
        progress_status = st.selectbox(
            "Progress Status",
            options=[None] + list(status_options.keys()),
            format_func=lambda x: status_options.get(x, "Select Status") if x else "Select Status",
            help="Current progress status"
        )

    # Enhanced submit button with animation
    if st.button("🚀 Add Task", type="primary", use_container_width=True):
        if title.strip():
            with st.spinner("Creating task..."):
                time.sleep(0.5)  # Simulate processing time

                try:
                    # Convert dates to datetime objects if provided
                    start_datetime = None
                    end_datetime = None

                    if start_date:
                        start_datetime = datetime.combine(start_date, datetime.min.time())
                    if end_date:
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
                        st.session_state.success_message = "✓ Task created successfully!"
                        st.session_state.show_success = True
                        st.session_state.task_title = ""
                        st.session_state.task_description = ""
                        st.session_state.task_start_date = None
                        st.session_state.task_end_date = None
                        st.session_state.task_priority = None
                        st.session_state.task_progress_status = None
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API. Make sure the backend is running on http://localhost:8000")
        else:
            st.error("❌ Please enter a task title")

    st.markdown('</div>', unsafe_allow_html=True)

# Main content area with enhanced styling
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.divider()
st.header("📋 My Tasks")

try:
    # Fetch all tasks with loading animation
    with st.spinner("Loading tasks..."):
        time.sleep(0.3)  # Simulate loading
        response = requests.get(f"{API_URL}/tasks")

    if response.status_code == 200:
        all_tasks = response.json()

        if not all_tasks:
            st.markdown("""
            <div style="text-align: center; padding: 50px;">
                <h2>🎯 No tasks yet!</h2>
                <p>Create your first task in the sidebar to get started.</p>
                <div class="pulse">🚀</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Enhanced filters with icons
            st.subheader("🔍 Smart Filters")
            col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)

            with col_filter1:
                priority_filter = st.multiselect(
                    "🎯 Priority",
                    options=["low", "medium", "high"],
                    default=[],
                    help="Filter by priority"
                )

            with col_filter2:
                status_filter = st.multiselect(
                    "📊 Progress Status",
                    options=["not_started", "in_progress", "completed", "on_hold"],
                    default=[],
                    format_func=lambda x: x.replace("_", " ").title(),
                    help="Filter by progress status"
                )

            with col_filter3:
                show_completed = st.checkbox("✅ Show Completed", value=True, help="Include completed tasks")

            with col_filter4:
                sort_options = {
                    "created_at": "📅 Newest First",
                    "priority": "🎯 Priority",
                    "start_date": "📅 Start Date",
                    "end_date": "🎯 End Date"
                }
                sort_by = st.selectbox(
                    "🔄 Sort by",
                    options=list(sort_options.keys()),
                    format_func=lambda x: sort_options[x],
                    help="Sort tasks by"
                )

            # Apply filters with animation
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

            # Enhanced metrics with gradient cards
            st.markdown('<div class="fade-in">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{len(tasks)}</h2>
                    <p>📋 Filtered Tasks</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                completed = sum(1 for task in tasks if task.get("completed"))
                completion_rate = (completed / len(tasks)) * 100 if tasks else 0
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{completed}</h2>
                    <p>✅ Completed ({completion_rate:.1f}%)</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                remaining = len(tasks) - completed
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{remaining}</h2>
                    <p>⏳ Remaining</p>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                high_priority = sum(1 for task in tasks if task.get("priority") == "high")
                st.markdown(f"""
                <div class="metric-card">
                    <h2>{high_priority}</h2>
                    <p>🔴 High Priority</p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.divider()
            
            # Display tasks with enhanced cards
            for i, task in enumerate(tasks):
                # Determine card styling based on priority and status
                priority_class = f"priority-{task.get('priority', 'low')}"
                status_class = f"status-{task.get('progress_status', 'not_started')}"

                # Add animation delay for staggered effect
                animation_delay = f"animation-delay: {i * 0.1}s;"

                st.markdown(f"""
                <div class="task-card {priority_class} {status_class} fade-in" style="{animation_delay}">
                """, unsafe_allow_html=True)

                with st.container():
                    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])

                    # Task info with enhanced display
                    with col1:
                        # Completion checkbox with animation
                        completed = task.get("completed", False)
                        checkbox_key = f"task_{task['id']}_{random.randint(1000, 9999)}"  # Unique key

                        if st.checkbox(
                            task["title"],
                            value=completed,
                            label_visibility="visible",
                            key=checkbox_key
                        ) != completed:
                            with st.spinner("Updating..."):
                                time.sleep(0.2)
                                try:
                                    update_response = requests.put(
                                        f"{API_URL}/tasks/{task['id']}",
                                        json={"completed": not completed}
                                    )
                                    if update_response.status_code == 200:
                                        st.success("✓ Status updated!")
                                        time.sleep(0.5)
                                        st.rerun()
                                except:
                                    st.error("Failed to update task")

                        # Enhanced description display
                        if task.get("description"):
                            st.markdown(f"📝 *{task['description']}*")

                        # Enhanced metadata display with icons and colors
                        metadata = []

                        # Priority badge with color
                        if task.get("priority"):
                            priority_colors = {"low": "#4CAF50", "medium": "#FF9800", "high": "#F44336"}
                            priority_icons = {"low": "🟢", "medium": "🟡", "high": "🔴"}
                            priority_icon = priority_icons.get(task["priority"], "⚪")
                            metadata.append(f'<span style="color: {priority_colors[task["priority"]]}; font-weight: bold;">{priority_icon} {task["priority"].title()}</span>')

                        # Progress status badge with color
                        if task.get("progress_status"):
                            status_icons = {
                                "not_started": "⏳",
                                "in_progress": "🔄",
                                "completed": "✅",
                                "on_hold": "⏸️"
                            }
                            status_colors = {
                                "not_started": "#9E9E9E",
                                "in_progress": "#2196F3",
                                "completed": "#4CAF50",
                                "on_hold": "#FF9800"
                            }
                            status_icon = status_icons.get(task["progress_status"], "❓")
                            status_text = task["progress_status"].replace("_", " ").title()
                            metadata.append(f'<span style="color: {status_colors[task["progress_status"]]}; font-weight: bold;">{status_icon} {status_text}</span>')

                        # Date information with overdue detection
                        if task.get("start_date"):
                            try:
                                start_dt = datetime.fromisoformat(task["start_date"].replace('Z', '+00:00'))
                                metadata.append(f"📅 Start: {start_dt.strftime('%b %d, %Y')}")
                            except:
                                metadata.append(f"📅 Start: {task['start_date']}")

                        if task.get("end_date"):
                            try:
                                end_dt = datetime.fromisoformat(task["end_date"].replace('Z', '+00:00'))
                                # Check if overdue
                                if end_dt.date() < date.today() and not task.get("completed"):
                                    metadata.append(f'<span style="color: #F44336; font-weight: bold;">🚨 Due: {end_dt.strftime("%b %d, %Y")} (Overdue!)</span>')
                                else:
                                    metadata.append(f"🎯 Due: {end_dt.strftime('%b %d, %Y')}")
                            except:
                                metadata.append(f"🎯 Due: {task['end_date']}")

                        if metadata:
                            st.markdown(" | ".join(metadata), unsafe_allow_html=True)

                        # Progress bar for tasks with dates
                        if task.get("start_date") and task.get("end_date"):
                            try:
                                start_dt = datetime.fromisoformat(task["start_date"].replace('Z', '+00:00'))
                                end_dt = datetime.fromisoformat(task["end_date"].replace('Z', '+00:00'))
                                today = datetime.now()

                                if task.get("completed"):
                                    progress = 100
                                elif today < start_dt:
                                    progress = 0
                                elif today > end_dt:
                                    progress = 100
                                else:
                                    total_days = (end_dt - start_dt).days
                                    elapsed_days = (today - start_dt).days
                                    progress = min(100, max(0, (elapsed_days / total_days) * 100)) if total_days > 0 else 0

                                st.markdown(f"""
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {progress}%"></div>
                                </div>
                                <small>Progress: {progress:.1f}%</small>
                                """, unsafe_allow_html=True)
                            except:
                                pass

                        # Display timestamps
                        created_at = task.get("created_at", "Unknown")
                        try:
                            created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                            st.caption(f"📆 Created: {created_dt.strftime('%b %d, %Y at %I:%M %p')}")
                        except:
                            st.caption(f"📆 Created: {created_at}")

                    # Action buttons with enhanced styling
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{task['id']}", use_container_width=True):
                            st.session_state[f"edit_mode_{task['id']}"] = True

                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_{task['id']}", use_container_width=True):
                            with st.spinner("Deleting..."):
                                time.sleep(0.3)
                                try:
                                    delete_response = requests.delete(f"{API_URL}/tasks/{task['id']}")
                                    if delete_response.status_code == 200:
                                        st.session_state.success_message = "🗑️ Task deleted successfully!"
                                        st.session_state.show_success = True
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete task")
                                except:
                                    st.error("Failed to delete task")

                    # Edit form with enhanced UI
                    if st.session_state.get(f"edit_mode_{task['id']}", False):
                        st.divider()
                        with st.expander("✏️ Edit Task", expanded=True):
                            # Edit form fields with current values
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

                            # Enhanced save and cancel buttons
                            save_col, cancel_col = st.columns(2)
                            with save_col:
                                if st.button("💾 Save Changes", key=f"save_{task['id']}", use_container_width=True, type="primary"):
                                    with st.spinner("Saving changes..."):
                                        time.sleep(0.5)
                                        try:
                                            # Convert dates to datetime objects
                                            start_datetime = None
                                            end_datetime = None

                                            if edit_start_date:
                                                start_datetime = datetime.combine(edit_start_date, datetime.min.time())
                                            if edit_end_date:
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
                                                st.session_state.success_message = "✓ Task updated successfully!"
                                                st.session_state.show_success = True
                                                st.session_state[f"edit_mode_{task['id']}"] = False
                                                st.rerun()
                                            else:
                                                st.error(f"❌ Failed to update task: {update_response.status_code}")
                                        except Exception as e:
                                            st.error(f"❌ Error updating task: {str(e)}")

                            with cancel_col:
                                if st.button("❌ Cancel", key=f"cancel_{task['id']}", use_container_width=True):
                                    st.session_state[f"edit_mode_{task['id']}"] = False
                                    st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error(f"Error fetching tasks: {response.status_code}")

except requests.exceptions.ConnectionError:
    st.error("❌ Cannot connect to the API")
    st.info("Make sure the backend is running on http://localhost:8000")
    st.info("Run this command in the terminal: `uvicorn main:app --reload`")

# Enhanced footer
st.divider()
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 10px; margin: 20px 0;">
    <h4 style="color: #333; margin-bottom: 10px;">🚀 TODO App Pro</h4>
    <p style="color: #666; margin: 5px 0;">Built with ❤️ using <a href="https://streamlit.io" style="color: #FF4B4B; text-decoration: none;">Streamlit</a> and <a href="https://fastapi.tiangolo.com/" style="color: #009688; text-decoration: none;">FastAPI</a></p>
    <p style="color: #666; margin: 5px 0; font-size: 0.9em;">Enhanced with animations and modern UI ✨</p>
    <div class="pulse" style="font-size: 1.5em; margin-top: 10px;">🎯📅🎨</div>
</div>
""", unsafe_allow_html=True)
