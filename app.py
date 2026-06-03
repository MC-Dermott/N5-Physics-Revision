import streamlit as st

from Generators.acceleration import generate_mcq_acc
from Generators.speed_distance_time import generate_sdt_mcqs
from Generators.current import generate_mcq_current
from Generators.ohms_law import generate_ohms_law_mcqs
from Generators.resistor_combinations import generate_resistor_combination_mcqs
from Generators.forces import generate_mcq_forces
from Generators.projectiles import generate_projectile_mcqs
from Generators.vectors2 import generate_mcq_vectors
from Generators.gas_laws import generate_gas_law_mcqs
from Generators.weight import generate_mcq_wmg
from Generators.energy import generate_energy_quiz
from Generators.radiation_activity import generate_activity_mcqs
from Generators.potential_divider_generator import generate_potential_divider_mcq
from Generators.transistor_generator import generate_fixed_5v_potential_divider_quiz
from Generators.complex_circuit_generator import generate_parallel_series_quiz
from Generators.mixed_voltage import generate_circuit_quiz
from Generators.pressure import generate_pressure_mcqs
from Generators.specific_heat_generator import generate_specific_heat_mcqs
from Generators.radiation import generate_radiation_scenarios
from Generators.half_life import generate_half_life_mcqs
from Generators.wave_speed import generate_wave_speed_mcqs
from Generators.period_frequency import generate_period_frequency_mcqs
from Generators.waves_combined import generate_waves_combined_mcqs
from Generators.electrical_power import generate_mcq_power, generate_mcq_pet


# =========================================================
# UNIT SETUP
# =========================================================

units = {
    "Dynamics": {
        "Speed, Distance and Time Questions": generate_sdt_mcqs,
        "Acceleration Questions": generate_mcq_acc,
        "Forces Questions": generate_mcq_forces,
        "Projectile Questions": generate_projectile_mcqs,
        "Simple Vectors Questions": generate_mcq_vectors,
        "Weight questions": generate_mcq_wmg,
        "Energy Questions": generate_energy_quiz
    },

    "Electricity": {
        "Current Questions": generate_mcq_current,
        "Ohm's Law Questions": generate_ohms_law_mcqs,
        "Resistor Combinations": generate_resistor_combination_mcqs,
        "Electrical Power Questions": generate_mcq_power,
        "Power from Energy Questions": generate_mcq_pet,
        "Potential Divider Questions": generate_potential_divider_mcq,
        "Transistor Questions": generate_fixed_5v_potential_divider_quiz,
        "Complex Circuit Questions": generate_parallel_series_quiz,
        "Mixed Voltage": generate_circuit_quiz
    },

    "Radiation": {
        "Radiation Questions": generate_radiation_scenarios,
        "Half-Life Questions": generate_half_life_mcqs,
        "Activity Questions": generate_activity_mcqs,
    },

    "Waves": {
        "Wave Speed Questions": generate_wave_speed_mcqs,
        "Period and Frequency Questions": generate_period_frequency_mcqs,
        "Waves Combined Questions": generate_waves_combined_mcqs,
    },

    "Properties of Matter": {
        "Gas Law Questions": generate_gas_law_mcqs,
        "Pressure Questions": generate_pressure_mcqs,
        "Specific Heat & Latent Heat Questions": generate_specific_heat_mcqs
    }
}


question_generators = {
    topic: generator
    for topics in units.values()
    for topic, generator in topics.items()
}


# =========================================================
# INIT
# =========================================================

def init_quiz(unit, topic):
    return {
        "unit": unit,
        "topic": topic,
        "questions": question_generators[topic](),
        "index": 0,
        "score": 0,
        "submitted": {},
        "scenario_results": [],
        "current_scenario": None,
        "completed": False,
        "wrong_answers": []
    }


# =========================================================
# SCAFFOLD HELPERS
# =========================================================

def answer_is_correct(user_input, expected):
    """2% relative tolerance; handles commas, spaces, scientific notation."""
    try:
        student = float(str(user_input).replace(',', '').strip())
        if abs(expected) < 1e-9:
            return abs(student) < 0.01
        return abs(student - expected) / abs(expected) <= 0.02
    except (ValueError, TypeError, AttributeError):
        return False


def render_notes(q):
    notes = q.get("notes", "")
    if notes:
        with st.expander("📚 Summary Notes"):
            st.markdown(notes)


def render_scaffold(q, key_prefix):
    steps = q.get("scaffold", [])
    if not steps:
        return
    with st.expander("🔍 Step-by-step scaffold"):
        for i, step in enumerate(steps):
            st.markdown(f"**Step {i+1}:** {step['question']}")

            # Hint-only step — no numerical input required
            if step.get("answer") is None:
                if i < len(steps) - 1:
                    st.divider()
                continue

            input_key = f"scaf_{key_prefix}_{i}_inp"
            checked_key = f"scaf_{key_prefix}_{i}_chk"
            correct_key = f"scaf_{key_prefix}_{i}_ok"
            col1, col2 = st.columns([3, 1])
            with col1:
                user_val = st.text_input(
                    f"Answer (in {step['unit']}):",
                    key=input_key,
                    label_visibility="visible"
                )
            with col2:
                st.write("")
                st.write("")
                if st.button("Check", key=f"scaf_{key_prefix}_{i}_btn"):
                    ok = answer_is_correct(user_val, step["answer"])
                    st.session_state[checked_key] = True
                    st.session_state[correct_key] = ok
            if st.session_state.get(checked_key):
                if st.session_state.get(correct_key):
                    st.success("✓ Correct!")
                else:
                    st.error("✗ Not quite — check your working and try again.")
            if i < len(steps) - 1:
                st.divider()


# =========================================================
# IMAGE HELPER
# =========================================================

def render_diagram(q):
    """
    Safely renders diagram if present
    """
    if q.get("diagram"):
        st.image(
            q["diagram"],
            use_container_width=True
        )


# =========================================================
# FEEDBACK
# =========================================================

def render_feedback(q, selected_letter, correct):

    fb = q["feedback"][selected_letter]

    if correct:
        st.success("Correct!")
    else:
        st.error(
            f"Incorrect. Correct answer: {q['choices'][q['answer']]}"
        )

    if fb.get("mistake"):
        st.warning(f"Key issue: {fb['mistake']}")

    st.markdown("### Working")

    for step in fb["working"]:
        if step["type"] == "text":
            st.write(step["content"])
        elif step["type"] == "latex":
            st.latex(step["content"])
        else:
            st.write(step["content"])


# =========================================================
# UI SETUP
# =========================================================

st.title("Physics Revision Tool")

unit_choice = st.selectbox("Choose a unit:", list(units.keys()))
topic_choice = st.selectbox("Choose a topic:", list(units[unit_choice].keys()))

if st.button("Generate New Quiz"):
    st.session_state.quiz = init_quiz(unit_choice, topic_choice)
    st.rerun()

if "quiz" not in st.session_state:
    st.session_state.quiz = init_quiz(
        list(units.keys())[0],
        list(units[list(units.keys())[0]].keys())[0]
    )

quiz = st.session_state.quiz


# =========================================================
# COMPLETION SCREEN
# =========================================================

if quiz["completed"]:
    st.subheader("Quiz Complete 🎉")
    st.write(f"Score: {quiz['score']}")

    st.stop()


# =========================================================
# CURRENT QUESTION
# =========================================================

current_item = quiz["questions"][quiz["index"]]


# =========================================================
# SCENARIO QUESTIONS
# =========================================================

if isinstance(current_item, list):

    scenario_id = quiz["index"]

    st.header(f"Scenario {scenario_id + 1}")

    if quiz["current_scenario"] is None:
        quiz["current_scenario"] = {
            "scenario": scenario_id,
            "results": []
        }

    for part_num, q in enumerate(current_item, start=1):

        st.markdown(f"## Question {part_num}")

        # ✅ IMAGE ADDED HERE
        render_diagram(q)

        st.write(q["question"])

        render_notes(q)
        render_scaffold(q, f"{scenario_id}_{part_num}")

        key = f"{scenario_id}_{part_num}"

        if key in quiz["submitted"]:

            result = quiz["submitted"][key]

            render_feedback(q, result["selected"], result["correct"])

            st.divider()
            continue

        options = list(q["choices_display"].keys())

        selected_letter = st.radio(
            "Select your answer:",
            options,
            format_func=lambda x: q["choices_display"][x],
            key=key
        )

        if st.button(f"Submit Question {part_num}", key=f"btn_{key}"):

            correct = selected_letter == q["answer"]

            quiz["submitted"][key] = {
                "correct": correct,
                "selected": selected_letter
            }

            if correct:
                quiz["score"] += 1

            fb = q["feedback"][selected_letter]

            quiz["current_scenario"]["results"].append({
                "scenario": scenario_id,
                "part": part_num,
                "question": q["question"],
                "your_answer": q["choices"][selected_letter],
                "correct_answer": q["choices"][q["answer"]],
                "summary": fb["summary"],
                "mistake": fb.get("mistake"),
                "working": fb["working"],
                "correct": correct
            })

            st.rerun()

        st.divider()

    if st.button("Next Scenario"):
        quiz["index"] += 1
        quiz["submitted"] = {}

        if quiz["index"] >= len(quiz["questions"]):
            quiz["completed"] = True

        st.rerun()


# =========================================================
# SINGLE QUESTIONS
# =========================================================

else:

    q = current_item

    st.subheader(
        f"Question {quiz['index'] + 1} of {len(quiz['questions'])}"
    )

    # ✅ IMAGE ADDED HERE
    render_diagram(q)

    st.write(q["question"])

    render_notes(q)
    render_scaffold(q, f"single_{quiz['index']}")

    key = f"single_{quiz['index']}"

    if key in quiz["submitted"]:

        result = quiz["submitted"][key]

        render_feedback(q, result["selected"], result["correct"])

        if st.button("Next Question"):

            quiz["index"] += 1

            if quiz["index"] >= len(quiz["questions"]):
                quiz["completed"] = True

            st.rerun()

    else:

        options = list(q["choices_display"].keys())

        selected_letter = st.radio(
            "Select your answer:",
            options,
            format_func=lambda x: q["choices_display"][x],
            key=key
        )

        if st.button("Submit Answer"):

            correct = selected_letter == q["answer"]

            quiz["submitted"][key] = {
                "correct": correct,
                "selected": selected_letter
            }

            if correct:
                quiz["score"] += 1
            else:
                fb = q["feedback"][selected_letter]

                quiz["wrong_answers"].append({
                    "question_number": quiz["index"] + 1,
                    "question": q["question"],
                    "your_answer": q["choices"][selected_letter],
                    "correct_answer": q["choices"][q["answer"]],
                    "summary": fb["summary"],
                    "mistake": fb.get("mistake"),
                    "working": fb["working"],
                    "correct": False
                })

            st.rerun()
