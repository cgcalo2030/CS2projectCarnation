import json, os
from datetime import datetime

DATA_FILE = "study_data.json"
DEFAULT_GOAL = 10
BAR_LEN = 20

# ------------------ Storage ------------------

def load():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                return json.load(f)
        except:
            print("⚠️ Corrupted data file. Starting fresh.")
    return {"subjects": {}, "last_reset": today()}

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def today():
    return datetime.now().strftime("%Y-%m-%d")

# ------------------ Helpers ------------------

def weekly_reset(data):
    try:
        last = datetime.strptime(data["last_reset"], "%Y-%m-%d")
        if (datetime.now() - last).days >= 7:
            for s in data["subjects"].values():
                s["studied"] = 0
            data["last_reset"] = today()
            save(data)
            print("\n🌟 Weekly goals reset!")
    except:
        data["last_reset"] = today()

def bar(percent):
    filled = int((percent/100)*BAR_LEN)
    return "[" + "█"*filled + "░"*(BAR_LEN-filled) + "]"

def progress(sub):
    goal = sub.get("goal", DEFAULT_GOAL)
    studied = sub.get("studied", 0)
    pct = min(100, studied/goal*100)
    if pct >= 100: status = "✅ Complete"
    elif pct >= 75: status = "On Track"
    elif pct >= 50: status = "Progress"
    else: status = "Needs Focus"
    return pct, status

# ------------------ UI Functions ------------------

def show(data):
    subjects = data["subjects"]
    if not subjects:
        print("\n📚 No subjects yet.")
        return
    
    print("\n" + "="*60)
    print("SMART STUDY PLANNER".center(60))
    print("="*60)
    print(f"{'Subject':<15}{'Goal':<8}{'Studied':<10}{'Progress':<20}{'Status'}")
    print("-"*60)

    for name, s in subjects.items():
        pct, status = progress(s)
        print(f"{name:<15}{s['goal']:<8}{s['studied']:<10}{bar(pct)} {int(pct)}% {status}")

    print("-"*60)
    print("Last Reset:", data["last_reset"])
    print("="*60)

# ------------------ Actions ------------------

def add_subject(data):
    name = input("New subject name: ").strip()
    if not name:
        print("❌ Empty name.")
        return
    if name in data["subjects"]:
        print("⚠ Already exists.")
        return
    
    try:
        goal = float(input("Weekly goal (hrs): "))
    except:
        print("❌ Invalid number.")
        return
    
    data["subjects"][name] = {"goal": goal, "studied": 0}
    save(data)
    print(f"Added {name} ✔")

def log_time(data):
    subs = list(data["subjects"].keys())
    if not subs:
        print("No subjects.")
        return

    for i, s in enumerate(subs, 1):
        print(f"{i}. {s}")

    try:
        subject = subs[int(input("Choose subject #: ")) - 1]
        hrs = float(input("Hours studied: "))
    except:
        print("❌ Invalid input.")
        return
    
    data["subjects"][subject]["studied"] += hrs
    save(data)

    pct, _ = progress(data["subjects"][subject])
    print(f"Logged! Now at {pct:.0f}%")

def edit_subject(data):
    subs = list(data["subjects"].keys())
    if not subs:
        print("No subjects.")
        return

    for i, s in enumerate(subs, 1):
        print(f"{i}. {s}")

    try:
        name = subs[int(input("Choose subject #: ")) - 1]
    except:
        print("❌ Invalid.")
        return

    print("\n1. Rename\n2. Change Goal\n3. Delete")
    c = input("Choice: ")

    if c == "1":
        new = input("New name: ").strip()
        if new and new not in subs:
            data["subjects"][new] = data["subjects"].pop(name)
            save(data)
            print("Renamed ✔")

    elif c == "2":
        try:
            new_goal = float(input("New goal hours: "))
            data["subjects"][name]["goal"] = new_goal
            save(data)
            print("Goal updated ✔")
        except:
            print("❌ Invalid.")

    elif c == "3":
        del data["subjects"][name]
        save(data)
        print("Deleted ✔")

# ------------------ Main App ------------------

def main():
    data = load()
    weekly_reset(data)

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        show(data)

        print("\n1. Add Subject")
        print("2. Log Study Time")
        print("3. Edit/Delete Subject")
        print("4. Exit")

        choice = input("Choice: ").strip()
        if choice == "1": add_subject(data)
        elif choice == "2": log_time(data)
        elif choice == "3": edit_subject(data)
        elif choice == "4":
            print("Goodbye! 👋")
            break
        input("\nEnter to continue...")

if __name__ == "__main__":
    main()
