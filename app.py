import streamlit as st

from Generators.acceleration import generate_mcq_acc
from Generators.current import generate_mcq_current
from Generators.forces import generate_mcq_forces
from Generators.projectiles import generate_projectile_mcqs
from Generators.vectors2 import generate_mcq_vectors


# =========================================================
# Topics
# =========================================================
question_generators = {
    "Acceleration Questions": generate_mcq_acc,
    "Current Questions": generate_mcq_current,
    "Forces Questions": generate_mcq_forces,
    "Projectile Questions": generate_projectile_mcqs,
    "Simple Vectors Questions": generate_mcq_vectors
}


# =========================================================
# Init quiz
# =========================================================
def init_quiz(topic):

    return {
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
# Feedback renderer
# =========================================================
def render_feedback(q, selected_letter, correct):

    fb = q["feedback"][selected_letter]

    # -----------------------------------------------------
    # Correct / Incorrect
    # -----------------------------------------------------
    if correct:

        st.success("Correct!")

    else:

        st.error(
            f"Incorrect. Correct answer: "
            f"{q['choices'][q['answer']]}"
        )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------
    st.info(fb["summary"])

    # -----------------------------------------------------
    # Key mistake
    # -----------------------------------------------------
    if fb.get("mistake"):

        st.warning(
            f"Key issue: {fb['mistake']}"
        )

    # -----------------------------------------------------
    # Working
    # -----------------------------------------------------
    st.markdown("### Working")

    for step in fb["working"]:

        if step["type"] == "text":

            st.write(step["content"])

        elif step["type"] == "latex":

            st.latex(step["content"])

        else:

            st.write(step["content"])


# =========================================================
# Session state
# =========================================================
if "quiz" not in st.session_state:

    st.session_state.quiz = init_quiz(
        "Acceleration Questions"
    )

quiz = st.session_state.quiz


# =========================================================
# UI
# =========================================================
st.title("Physics Revision Tool")

topic_choice = st.selectbox(
    "Choose a topic:",
    list(question_generators.keys())
)

if st.button("Generate New Quiz"):

    st.session_state.quiz = init_quiz(
        topic_choice
    )

    st.rerun()

quiz = st.session_state.quiz


# =========================================================
# Completion screen
# =========================================================
if quiz["completed"]:

    total_questions = sum(
        len(q) if isinstance(q, list) else 1
        for q in quiz["questions"]
    )

    st.subheader("Quiz Complete 🎉")

    st.write(
        f"Final Score: "
        f"{quiz['score']} / {total_questions}"
    )

    # =====================================================
    # Wrong answer review
    # =====================================================
    if quiz["wrong_answers"]:

        st.subheader("Review Your Mistakes")

        for i, r in enumerate(
            quiz["wrong_answers"],
            start=1
        ):

            # -------------------------------------------------
            # Heading
            # -------------------------------------------------
            if r.get("scenario") is not None:

                st.markdown(
                    f"## Scenario {r['scenario'] + 1} "
                    f"— Question {r['part']}"
                )

            else:

                st.markdown(
                    f"## Question "
                    f"{r.get('question_number', i)}"
                )

            # -------------------------------------------------
            # Question
            # -------------------------------------------------
            st.write(r["question"])

            # -------------------------------------------------
            # Answers
            # -------------------------------------------------
            st.error(
                f"Your answer: "
                f"{r['your_answer']}"
            )

            st.success(
                f"Correct answer: "
                f"{r['correct_answer']}"
            )

            # -------------------------------------------------
            # Summary
            # -------------------------------------------------
            st.info(r["summary"])

            # -------------------------------------------------
            # Mistake
            # -------------------------------------------------
            if r["mistake"]:

                st.warning(
                    f"Key issue: "
                    f"{r['mistake']}"
                )

            # -------------------------------------------------
            # Working
            # -------------------------------------------------
            st.markdown("### Working")

            for step in r["working"]:

                if step["type"] == "text":

                    st.write(step["content"])

                elif step["type"] == "latex":

                    st.latex(step["content"])

                else:

                    st.write(step["content"])

            st.divider()

    st.stop()


# =========================================================
# Current item
# =========================================================
current_item = quiz["questions"][quiz["index"]]


# =========================================================
# PROJECTILE SCENARIOS
# =========================================================
if isinstance(current_item, list):

    scenario_id = quiz["index"]

    st.header(
        f"Scenario {scenario_id + 1}"
    )

    st.info(
    "These questions are linked. "
    "You may use previous answers "
    "for later parts."
)

    # -----------------------------------------------------
    # Init scenario storage
    # -----------------------------------------------------
    if quiz["current_scenario"] is None:

        quiz["current_scenario"] = {
            "scenario": scenario_id,
            "results": []
        }

    # =====================================================
    # Scenario questions
    # =====================================================
    for part_num, q in enumerate(
        current_item,
        start=1
    ):

        st.markdown(
            f"## Question {part_num}"
        )

        st.write(q["question"])

        key = f"{scenario_id}_{part_num}"

        # -------------------------------------------------
        # Already answered
        # -------------------------------------------------
        if key in quiz["submitted"]:

            result = quiz["submitted"][key]

            render_feedback(
                q,
                result["selected"],
                result["correct"]
            )

            st.divider()

            continue

        # -------------------------------------------------
        # Answer selection
        # -------------------------------------------------
        selected = st.radio(
            "Select your answer:",
            list(
                q["choices_display"].values()
            ),
            key=key
        )

        selected_letter = selected[0]

        # -------------------------------------------------
        # Submit answer
        # -------------------------------------------------
        if st.button(
            f"Submit Question {part_num}",
            key=f"btn_{key}"
        ):

            correct = (
                selected_letter
                == q["answer"]
            )

            quiz["submitted"][key] = {
                "correct": correct,
                "selected": selected_letter
            }

            if correct:

                quiz["score"] += 1

            fb = q["feedback"][selected_letter]

            # -------------------------------------------------
            # Result data
            # -------------------------------------------------
            result_data = {

                "scenario":
                    scenario_id,

                "part":
                    part_num,

                "question":
                    q["question"],

                "your_answer":
                    q["choices"][
                        selected_letter
                    ],

                "correct_answer":
                    q["choices"][
                        q["answer"]
                    ],

                "summary":
                    fb["summary"],

                "mistake":
                    fb.get("mistake"),

                "working":
                    fb["working"],

                "correct":
                    correct
            }

            # -------------------------------------------------
            # Store scenario result
            # -------------------------------------------------
            quiz["current_scenario"]["results"].append(
                result_data
            )

            # -------------------------------------------------
            # Store wrong answers
            # -------------------------------------------------
            if not correct:

                quiz["wrong_answers"].append(
                    result_data
                )

            st.rerun()

        st.divider()

    # =====================================================
    # Next scenario
    # =====================================================
    if st.button("Next Scenario"):

        if quiz["current_scenario"] is not None:

            quiz["scenario_results"].append(
                quiz["current_scenario"]
            )

            quiz["current_scenario"] = None

        quiz["index"] += 1

        quiz["submitted"] = {}

        if quiz["index"] >= len(
            quiz["questions"]
        ):

            quiz["completed"] = True

        st.rerun()


# =========================================================
# SINGLE QUESTION TOPICS
# =========================================================
else:

    q = current_item

    st.subheader(
        f"Question "
        f"{quiz['index'] + 1} "
        f"of "
        f"{len(quiz['questions'])}"
    )

    st.write(q["question"])

    key = f"single_{quiz['index']}"

    # -----------------------------------------------------
    # Already answered
    # -----------------------------------------------------
    if key in quiz["submitted"]:

        result = quiz["submitted"][key]

        render_feedback(
            q,
            result["selected"],
            result["correct"]
        )

        # -------------------------------------------------
        # Next question
        # -------------------------------------------------
        if st.button("Next Question"):

            quiz["index"] += 1

            if quiz["index"] >= len(
                quiz["questions"]
            ):

                quiz["completed"] = True

            st.rerun()

    # -----------------------------------------------------
    # Not submitted yet
    # -----------------------------------------------------
    else:

        selected = st.radio(
            "Select your answer:",
            list(
                q["choices_display"].values()
            ),
            key=key
        )

        selected_letter = selected[0]

        # -------------------------------------------------
        # Submit answer
        # -------------------------------------------------
        if st.button("Submit Answer"):

            correct = (
                selected_letter
                == q["answer"]
            )

            quiz["submitted"][key] = {
                "correct": correct,
                "selected": selected_letter
            }

            if correct:

                quiz["score"] += 1

            else:

                fb = q["feedback"][
                    selected_letter
                ]

                result_data = {

                    "question_number":
                        quiz["index"] + 1,

                    "question":
                        q["question"],

                    "your_answer":
                        q["choices"][
                            selected_letter
                        ],

                    "correct_answer":
                        q["choices"][
                            q["answer"]
                        ],

                    "summary":
                        fb["summary"],

                    "mistake":
                        fb.get("mistake"),

                    "working":
                        fb["working"],

                    "correct":
                        False
                }

                quiz["wrong_answers"].append(
                    result_data
                )

            st.rerun()
