import streamlit as st
import json
import os
from datetime import datetime
import plotly.graph_objects as go

DATA_FILE = "study_data.json"
DEFAULT_GOAL = 10


# ------------------ Helpers ------------------

def today():
    return datetime.now().strftime("%Y-%m-%d")


def load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                return json.load(f)
        except:
            st.warning("Corrupted data file. Starting fresh.")

    return {"subjects": {}, "last_reset": today()}


def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ------------------ Weekly Reset ------------------

def weekly_reset(data):
    try:
        last = datetime.strptime(data["last_reset"], "%Y-%m-%d")

        if (datetime.now() - last).days >= 7:
            for s in data["subjects"].values():
                s["studied"] = 0

            data["last_reset"] = today()
            save(data)

            st.success("🌟 Weekly goals reset!")

    except:
        data["last_reset"] = today()
        save(data)


# ------------------ Progress Logic ------------------

def progress(sub):
    goal = sub.get("goal", DEFAULT_GOAL)
    studied = sub.get("studied", 0)

    pct = min(100, studied / goal * 100)

    if pct >= 100:
        status = "✅ Complete"
    elif pct >= 75:
        status = "On Track"
    elif pct >= 50:
        status = "Progress"
    else:
        status = "Needs Focus"

    return pct, status


# ------------------ App Setup ------------------

st.set_page_config("Smart Study Planner", "📚", layout="wide")

if "data" not in st.session_state:
    st.session_state.data = load()

data = st.session_state.data

weekly_reset(data)


# ------------------ Sidebar Controls ------------------

with st.sidebar:

    st.header("Manage Subjects")

    # ADD SUBJECT
    st.subheader("Add Subject")

    name = st.text_input("Subject Name")
    goal = st.number_input("Weekly Goal", min_value=1.0, value=10.0)

    if st.button("Add Subject"):

        name = name.strip().title()

        if not name:
            st.error("Empty subject name")

        elif name in data["subjects"]:
            st.warning("Subject already exists")

        else:
            data["subjects"][name] = {
                "goal": goal,
                "studied": 0
            }

            save(data)
            st.rerun()


    # EDIT SUBJECT
    if data["subjects"]:

        st.subheader("Edit Subject")

        selected = st.selectbox(
            "Select Subject",
            list(data["subjects"].keys())
        )

        new_goal = st.number_input(
            "Update Goal",
            min_value=1.0,
            value=float(data["subjects"][selected]["goal"])
        )

        if st.button("Update Goal"):
            data["subjects"][selected]["goal"] = new_goal
            save(data)
            st.rerun()

        new_name = st.text_input("Rename Subject")

        if st.button("Rename"):

            new_name = new_name.strip().title()

            if new_name and new_name not in data["subjects"]:

                data["subjects"][new_name] = data["subjects"].pop(selected)
                save(data)
                st.rerun()

        if st.button("Delete Subject"):
            del data["subjects"][selected]
            save(data)
            st.rerun()


# ------------------ Main Dashboard ------------------

st.title("📚 Smart Study Planner")

st.caption(f"Last Reset: {data['last_reset']}")

if not data["subjects"]:

    st.info("No subjects yet. Add one from the sidebar!")

else:

    # LOG STUDY TIME
    st.subheader("Log Study Time")

    col1, col2, col3 = st.columns([2,1,1])

    with col1:
        subject = st.selectbox(
            "Subject",
            list(data["subjects"].keys()),
            label_visibility="collapsed"
        )

    with col2:
        hours = st.number_input(
            "Hours",
            min_value=0.1,
            step=0.5,
            label_visibility="collapsed"
        )

    with col3:
        if st.button("Log Time"):

            data["subjects"][subject]["studied"] += hours
            save(data)

            pct, _ = progress(data["subjects"][subject])

            st.success(f"Logged! Now at {pct:.0f}%")
            st.rerun()


    st.divider()


    # SUBJECT TABLE VIEW (CLI-style converted to cards)

    st.subheader("Progress Overview")

    cols = st.columns(3)

    for i, (name, s) in enumerate(data["subjects"].items()):

        pct, status = progress(s)

        with cols[i % 3]:

            with st.container(border=True):

                st.markdown(f"### {name}")

                st.metric(
                    "Studied",
                    f"{s['studied']}h",
                    f"Goal: {s['goal']}h",
                    delta_color="off"
                )

                st.progress(pct/100)

                st.caption(f"{int(pct)}% • {status}")


    st.divider()


    # CLI-style comparison chart

    st.subheader("Goal vs Studied")

    subjects = list(data["subjects"].keys())

    studied_vals = [
        s["studied"] for s in data["subjects"].values()
    ]

    goals = [
        s["goal"] for s in data["subjects"].values()
    ]

    fig = go.Figure(data=[

        go.Bar(name="Studied", x=subjects, y=studied_vals),

        go.Bar(name="Goal", x=subjects, y=goals)

    ])

    fig.update_layout(barmode="group")

    st.plotly_chart(fig, use_container_width=True)
