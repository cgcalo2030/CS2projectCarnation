import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "study_data.json"

# ------------------ Data Handling ------------------

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                return json.load(f)
        except:
            pass
    return {"subjects": {}, "last_reset": datetime.now().strftime("%Y-%m-%d")}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ UI Setup ------------------

st.set_page_config(page_title="Study Planner", page_icon="📚", layout="wide")

# Initialize Session State to keep data fresh
if 'data' not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# ------------------ Sidebar (Management) ------------------

with st.sidebar:
    st.header("⚙️ Manage Subjects")
    
    with st.expander("➕ Add New"):
        new_name = st.text_input("Name").strip().title()
        new_goal = st.number_input("Goal (hrs)", min_value=0.5, value=10.0, step=0.5)
        if st.button("Add Subject", use_container_width=True):
            if new_name and new_name not in data["subjects"]:
                data["subjects"][new_name] = {"goal": new_goal, "studied": 0}
                save_data(data)
                st.rerun()
            else:
                st.error("Invalid name or already exists.")

    if data["subjects"]:
        with st.expander("✏️ Edit / Delete"):
            target = st.selectbox("Select Subject", list(data["subjects"].keys()))
            col1, col2 = st.columns(2)
            if col1.button("🗑️ Delete", use_container_width=True):
                del data["subjects"][target]
                save_data(data)
                st.rerun()
            
            new_g = st.number_input("Update Goal", min_value=0.5, value=float(data["subjects"][target]["goal"]))
            if st.button("Update Goal", use_container_width=True):
                data["subjects"][target]["goal"] = new_g
                save_data(data)
                st.rerun()

# ------------------ Main Dashboard ------------------

st.title("📚 Smart Study Planner")
st.caption(f"Last Reset: {data['last_reset']}")

if not data["subjects"]:
    st.info("Add a subject in the sidebar to get started! 🚀")
else:
    # 1. Quick Log Section
    st.subheader("⏱️ Log Study Time")
    log_col1, log_col2, log_col3 = st.columns([2, 1, 1])
    
    with log_col1:
        sub_to_log = st.selectbox("Subject", list(data["subjects"].keys()), label_visibility="collapsed")
    with log_col2:
        hrs_to_add = st.number_input("Hours", min_value=0.1, step=0.5, label_visibility="collapsed")
    with log_col3:
        if st.button("Log Time", use_container_width=True, type="primary"):
            data["subjects"][sub_to_log]["studied"] += hrs_to_add
            save_data(data)
            st.success(f"Logged {hrs_to_add}h for {sub_to_log}!")
            st.rerun()

    st.divider()

    # 2. Visual Progress Cards
    st.subheader("📊 Your Progress")
    cols = st.columns(3) # Grid layout
    for i, (name, s) in enumerate(data["subjects"].items()):
        with cols[i % 3]:
            pct = min(1.0, s['studied'] / s['goal'])
            with st.container(border=True):
                st.markdown(f"### {name}")
                st.metric("Studied", f"{s['studied']}h", f"Goal: {s['goal']}h", delta_color="off")
                st.progress(pct)
                st.caption(f"{int(pct*100)}% Complete")

    # 3. Interactive Chart
    st.divider()
    st.subheader("📈 Visual Comparison")
    chart_data = {
        "Subject": list(data["subjects"].keys()),
        "Hours Studied": [s["studied"] for s in data["subjects"].values()],
        "Goal": [s["goal"] for s in data["subjects"].values()]
    }
    st.bar_chart(chart_data, x="Subject", y=["Hours Studied", "Goal"])
