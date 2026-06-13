import random
import streamlit as st

from Generators.acceleration import generate_mcq_acc, generate_single_mcq_acc
from Generators.speed_distance_time import generate_sdt_mcqs, generate_single_mcq_sdt
from Generators.current import generate_mcq_current, generate_single_mcq_current
from Generators.ohms_law import generate_ohms_law_mcqs, generate_single_mcq_vir
from Generators.resistor_combinations import generate_resistor_combination_mcqs, generate_single_mcq_resistors
from Generators.forces import generate_mcq_forces, generate_single_mcq_forces
from Generators.projectiles import generate_projectile_mcqs, generate_projectile_mcq_set
from Generators.vectors2 import generate_mcq_vectors, generate_vector_scenario
from Generators.gas_laws import generate_gas_law_mcqs, generate_boyles_mcq, generate_charles_mcq, generate_gaylussac_mcq
from Generators.weight import generate_mcq_wmg, generate_single_mcq_wmg
from Generators.energy import generate_energy_quiz, generate_single_energy_question
from Generators.radiation_activity import generate_activity_mcqs, generate_single_mcq_activity
from Generators.potential_divider_generator import generate_potential_divider_mcq, generate_single_potential_divider_mcq
from Generators.transistor_generator import generate_fixed_5v_potential_divider_quiz
from Generators.transistor_generator import generate_single_mcq as generate_single_mcq_transistor
from Generators.complex_circuit_generator import generate_parallel_series_quiz
from Generators.complex_circuit_generator import generate_single_mcq as generate_single_mcq_complex
from Generators.mixed_voltage import generate_circuit_quiz, generate_single_circuit_question
from Generators.pressure import generate_pressure_mcqs
from Generators.specific_heat_generator import generate_specific_heat_mcqs
from Generators.radiation import generate_radiation_scenarios, generate_forward_scenario, generate_reverse_scenario
from Generators.half_life import generate_half_life_mcqs, generate_forward_activity, generate_backward_activity, generate_half_life
from Generators.wave_speed import generate_wave_speed_mcqs
from Generators.period_frequency import generate_period_frequency_mcqs
from Generators.waves_combined import generate_waves_combined_mcqs
from Generators.electrical_power import generate_mcq_power, generate_mcq_pet, generate_single_mcq_power, generate_single_mcq_pet


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
# TOPIC TEST GENERATORS
# One callable per generator; each returns a single question
# item (dict for a regular question, list for a scenario).
# =========================================================

TOPIC_TEST_GENERATORS = {
    "Dynamics": [
        generate_single_mcq_sdt,
        generate_single_mcq_acc,
        generate_single_mcq_forces,
        generate_projectile_mcq_set,        # scenario (list)
        generate_vector_scenario,           # scenario (list)
        generate_single_mcq_wmg,
        generate_single_energy_question,
    ],
    "Electricity": [
        generate_single_mcq_current,
        generate_single_mcq_vir,
        generate_single_mcq_resistors,
        generate_single_mcq_power,
        generate_single_mcq_pet,
        generate_single_potential_divider_mcq,
        generate_single_mcq_transistor,
        generate_single_mcq_complex,
        generate_single_circuit_question,
    ],
    "Radiation": [
        lambda: random.choice([generate_forward_scenario, generate_reverse_scenario])(),
        lambda: random.choice([generate_forward_activity, generate_backward_activity, generate_half_life])(),
        generate_single_mcq_activity,
    ],
    "Waves": [
        lambda: generate_wave_speed_mcqs(num=1)[0],
        lambda: generate_period_frequency_mcqs(num=1)[0],
        lambda: generate_waves_combined_mcqs(num=1)[0],
    ],
    "Properties of Matter": [
        lambda: random.choice([generate_boyles_mcq, generate_charles_mcq, generate_gaylussac_mcq])(),
        lambda: generate_pressure_mcqs(num=1)[0],
        lambda: generate_specific_heat_mcqs(num=1)[0],
    ],
}


def generate_topic_test(unit_name, num_questions=10):
    gens = TOPIC_TEST_GENERATORS[unit_name]
    questions = [g() for g in gens]
    while len(questions) < num_questions:
        questions.append(random.choice(gens)())
    random.shuffle(questions)
    return questions


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

mode = st.radio("Mode:", ["Topic Quiz", "Topic Test (10 questions)"], horizontal=True)

unit_choice = st.selectbox("Choose a unit:", list(units.keys()))

if mode == "Topic Quiz":
    topic_choice = st.selectbox("Choose a topic:", list(units[unit_choice].keys()))
    if st.button("Generate New Quiz"):
        st.session_state.quiz = init_quiz(unit_choice, topic_choice)
        st.rerun()
else:
    st.caption("Generates 10 questions — at least one from every generator in the unit.")
    if st.button("Generate Topic Test"):
        st.session_state.quiz = {
            "unit": unit_choice,
            "topic": f"{unit_choice} Topic Test",
            "questions": generate_topic_test(unit_choice),
            "index": 0,
            "score": 0,
            "submitted": {},
            "scenario_results": [],
            "current_scenario": None,
            "completed": False,
            "wrong_answers": [],
        }
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
    total = sum(
        len(q) if isinstance(q, list) else 1
        for q in quiz["questions"]
    )
    st.write(f"Score: {quiz['score']} / {total}")

    wrong = quiz.get("wrong_answers", [])
    if wrong:
        st.markdown("---")
        st.subheader("Review: Incorrect Answers")
        for entry in wrong:
            label = entry["question_number"]
            with st.expander(f"Q{label} — {entry['question']}"):
                st.error(f"Your answer: {entry['your_answer']}")
                st.success(f"Correct answer: {entry['correct_answer']}")
                if entry.get("mistake"):
                    st.warning(f"Key issue: {entry['mistake']}")
                if entry.get("summary"):
                    st.info(entry["summary"])
                st.markdown("**Working:**")
                for step in entry.get("working", []):
                    if step["type"] == "latex":
                        st.latex(step["content"])
                    else:
                        st.write(step["content"])
    else:
        st.success("Perfect score — no incorrect answers to review!")

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
        if quiz["current_scenario"]:
            for result in quiz["current_scenario"]["results"]:
                if not result["correct"]:
                    quiz["wrong_answers"].append({
                        "question_number": f"Scenario {result['scenario'] + 1}, Part {result['part']}",
                        **{k: result[k] for k in ("question", "your_answer", "correct_answer", "summary", "mistake", "working", "correct")}
                    })
        quiz["index"] += 1
        quiz["submitted"] = {}
        quiz["current_scenario"] = None

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
