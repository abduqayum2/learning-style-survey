import streamlit as st
import json
from datetime import datetime
import sys
import os

# ---------------- DATA ----------------
version_float = 1.0

questions = [
    {"q": "How confident are you in identifying your strongest learning style?",
     "opts": [("Very confident", 0), ("Somewhat confident", 1), ("Unsure", 2), ("Not confident at all", 3)]},
    {"q": "How often do you reflect on which study methods work best for you?",
     "opts": [("Regularly", 0), ("Sometimes", 1), ("Rarely", 2), ("Never", 3)]},
    {"q": "When learning something new, how quickly can you choose the most suitable approach?",
     "opts": [("Immediately", 0), ("After some thought", 1), ("After trial and error", 2), ("I usually cannot decide", 3)]},
    {"q": "How well can you describe the difference between visual, auditory, and hands-on learning?",
     "opts": [("Very clearly", 0), ("Fairly well", 1), ("Vaguely", 2), ("I cannot distinguish them", 3)]},
    {"q": "How often do you notice that a particular study method is not working and switch to another?",
     "opts": [("Always", 0), ("Often", 1), ("Rarely", 2), ("Never", 3)]},
    {"q": "How frequently do you use diagrams, charts, or colour-coding when studying?",
     "opts": [("Very frequently", 0), ("Sometimes", 1), ("Rarely", 2), ("Never", 3)]},
    {"q": "How often do you listen to recorded lectures or explain topics aloud to reinforce understanding?",
     "opts": [("Regularly", 0), ("Occasionally", 1), ("Seldom", 2), ("Never", 3)]},
    {"q": "When preparing for an exam, how structured is your study plan?",
     "opts": [("Fully structured with a clear timetable", 0), ("Somewhat planned", 1), ("Loosely organized", 2), ("No plan at all", 3)]},
    {"q": "How often do you practise problems or build things by hand to understand a concept?",
     "opts": [("Very often", 0), ("Sometimes", 1), ("Rarely", 2), ("Never", 3)]},
    {"q": "How effectively do you use note-taking techniques suited to your learning style?",
     "opts": [("Very effectively", 0), ("Moderately", 1), ("Somewhat poorly", 2), ("Not effectively at all", 3)]},
    {"q": "After receiving a low grade, how often do you change your study approach for the next assessment?",
     "opts": [("Always", 0), ("Usually", 1), ("Occasionally", 2), ("Never", 3)]},
    {"q": "How frequently do you seek feedback from peers or instructors about your study habits?",
     "opts": [("Regularly", 0), ("Sometimes", 1), ("Rarely", 2), ("Never", 3)]},
    {"q": "How well do you adapt your revision strategy when studying different subjects?",
     "opts": [("Very well", 0), ("Adequately", 1), ("Poorly", 2), ("Not at all", 3)]},
    {"q": "How often do you set specific learning goals before each study session?",
     "opts": [("Always", 0), ("Often", 1), ("Rarely", 2), ("Never", 3)]},
    {"q": "How satisfied are you with the results your current study methods produce?",
     "opts": [("Very satisfied", 0), ("Somewhat satisfied", 1), ("Dissatisfied", 2), ("Very dissatisfied", 3)]},
    {"q": "How well does your usual study environment match your learning preferences?",
     "opts": [("Perfectly", 0), ("Mostly", 1), ("Somewhat", 2), ("Not at all", 3)]},
    {"q": "How often do you use digital tools or apps that support your preferred learning style?",
     "opts": [("Frequently", 0), ("Sometimes", 1), ("Rarely", 2), ("Never", 3)]},
    {"q": "How effectively do you manage distractions during study sessions?",
     "opts": [("Very effectively", 0), ("Fairly well", 1), ("Poorly", 2), ("Very poorly", 3)]},
    {"q": "How often do you review and summarise material after a lecture or class?",
     "opts": [("After every class", 0), ("Most of the time", 1), ("Occasionally", 2), ("Never", 3)]},
    {"q": "How confident are you that your current study strategies will help you succeed academically?",
     "opts": [("Very confident", 0), ("Fairly confident", 1), ("Slightly doubtful", 2), ("Not confident at all", 3)]}
]

psych_states = {
    "Excellent Awareness": (0, 10),
    "Good Awareness": (11, 20),
    "Moderate Awareness": (21, 30),
    "Developing Awareness": (31, 40),
    "Low Awareness": (41, 50),
    "Very Low Awareness": (51, 60)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    stripped = name.strip()
    if len(stripped) == 0:
        return False
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -'")
    for ch in stripped:
        if ch not in allowed:
            return False
    return True

def validate_dob(dob: str) -> bool:
    try:
        parsed = datetime.strptime(dob.strip(), "%Y-%m-%d")
        if parsed > datetime.now():
            return False
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def get_description(state: str) -> str:
    descriptions = {
        "Excellent Awareness": "You have a strong understanding of your learning style and apply highly effective study strategies.",
        "Good Awareness": "You know your learning preferences well and use suitable strategies most of the time.",
        "Moderate Awareness": "You have a reasonable understanding but could benefit from exploring more study techniques.",
        "Developing Awareness": "Your strategy use is inconsistent. Consider taking a learning style assessment and attending study skills workshops.",
        "Low Awareness": "You struggle to identify effective study methods. Structured guidance from an academic advisor is recommended.",
        "Very Low Awareness": "You experience significant difficulty with study strategies. Seek immediate academic support and mentorship."
    }
    return descriptions.get(state, "No description available.")

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Learning Style Awareness Survey")
st.title("📝 Learning Style Awareness and Study Strategy Effectiveness Scale")

st.info("This survey evaluates your understanding of your preferred learning styles and how well you apply effective study strategies. Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):

    # Validate inputs
    errors = []
    if not validate_name(name):
        errors.append("Invalid given name. Only letters, hyphens, apostrophes, and spaces are allowed.")
    if not validate_name(surname):
        errors.append("Invalid surname. Only letters, hyphens, apostrophes, and spaces are allowed.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.strip().isdigit():
        errors.append("Student ID must contain only digits.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            score = next(s for label, s in q["opts"] if label == choice)
            total_score += score
            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)
        description = get_description(status)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score} / 60")
        st.markdown(f"**Description:** {description}")

        st.markdown("---")
        st.markdown("### Score Ranges")
        for state, (low, high) in psych_states.items():
            st.markdown(f"- **{low}–{high}:** {state}")

        # Save results to JSON
        record = {
            "survey": "Learning Style Awareness and Study Strategy Effectiveness Scale",
            "name": name.strip(),
            "surname": surname.strip(),
            "dob": dob.strip(),
            "student_id": sid.strip(),
            "date_taken": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_score": total_score,
            "result": status,
            "description": description,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid.strip()}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
