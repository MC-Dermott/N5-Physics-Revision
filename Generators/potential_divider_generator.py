import random
from utils.mcq_utils import format_mcq


# =========================================================
# Helpers
# =========================================================

def generate_resistance():
    """
    0.5 kΩ to 5.0 kΩ in 0.5 kΩ steps
    """
    return random.randint(1, 10) * 0.5


def generate_voltage():
    """
    0.5V to 8.5V in 0.5V steps
    """
    return random.randint(1, 17) * 0.5


def make_distractors(correct):
    """
    Generate EXACTLY 3 unique distractors
    """

    distractors = set()

    while len(distractors) < 3:

        variation = random.choice([
            -2,
            -1,
            -0.5,
            0.5,
            1,
            2
        ])

        value = round(correct + variation, 2)

        if value > 0 and value != correct:
            distractors.add(value)

    return list(distractors)


# =========================================================
# Working builders
# =========================================================

def make_working_current(v, r_total):

    return [

        {
            "type": "text",
            "content": "First calculate the total current using Ohm’s Law:"
        },

        {
            "type": "latex",
            "content": r"I = \frac{V}{R}"
        },

        {
            "type": "latex",
            "content": rf"I = \frac{{{v}}}{{{r_total}}}"
        }
    ]


def make_working_voltage(i, r, result):

    return [

        {
            "type": "text",
            "content": "Now calculate the voltage across the resistor:"
        },

        {
            "type": "latex",
            "content": r"V = IR"
        },

        {
            "type": "latex",
            "content": rf"V = {i} \times {r}"
        },

        {
            "type": "latex",
            "content": rf"V = {result}\ \mathrm{{V}}"
        }
    ]


# =========================================================
# TYPE 1
# =========================================================

def generate_type1_question():

    while True:

        r1 = generate_resistance()
        r2 = generate_resistance()
        v_supply = generate_voltage()

        r_total = r1 + r2

        current = round(v_supply / r_total, 3)

        target = random.choice(["R1", "R2"])

        if target == "R1":
            r_used = r1
            correct = round(current * r1, 2)
        else:
            r_used = r2
            correct = round(current * r2, 2)

        if correct <= 0:
            continue

        question = f"""
A potential divider circuit contains two resistors in series:

- R1 = {r1} kΩ
- R2 = {r2} kΩ
- Supply voltage = {v_supply} V

Calculate the voltage across {target}.
"""

        full_working = (
            make_working_current(v_supply, r_total)
            + make_working_voltage(current, r_used, correct)
        )

        distractors = make_distractors(correct)

        options_data = [

            {
                "value": correct,
                "summary": "Correct!",
                "mistake": None,
                "working": full_working
            },

            {
                "value": distractors[0],
                "summary": "Incorrect.",
                "mistake": "You may have used Ohm’s Law incorrectly.",
                "working": full_working
            },

            {
                "value": distractors[1],
                "summary": "Incorrect.",
                "mistake": "Check your voltage divider calculation.",
                "working": full_working
            },

            {
                "value": distractors[2],
                "summary": "Incorrect.",
                "mistake": "You may have used the wrong resistance.",
                "working": full_working
            }
        ]

        return (
            question,
            correct,
            options_data,
            "V",
            "images/potential_divider.png"
        )


# =========================================================
# TYPE 2
# =========================================================

def generate_type2_question():

    while True:

        r1 = generate_resistance()
        r2 = generate_resistance()
        v_total = generate_voltage()

        r_total = r1 + r2

        current = round(v_total / r_total, 3)

        v_r1 = round(current * r1, 2)
        v_r2 = round(current * r2, 2)

        given = random.choice(["R1", "R2"])

        if given == "R1":

            given_voltage = v_r1
            correct = v_r2
            r_used = r2

        else:

            given_voltage = v_r2
            correct = v_r1
            r_used = r1

        if correct <= 0 or given_voltage <= 0:
            continue

        question = f"""
A potential divider circuit contains two resistors in series:

- R1 = {r1} kΩ
- R2 = {r2} kΩ

The voltage across {given} is {given_voltage} V.

Calculate the voltage across the other resistor.
"""

        full_working = (
            make_working_current(v_total, r_total)
            + make_working_voltage(current, r_used, correct)
        )

        distractors = make_distractors(correct)

        options_data = [

            {
                "value": correct,
                "summary": "Correct!",
                "mistake": None,
                "working": full_working
            },

            {
                "value": distractors[0],
                "summary": "Incorrect.",
                "mistake": "You may have assumed equal voltage division.",
                "working": full_working
            },

            {
                "value": distractors[1],
                "summary": "Incorrect.",
                "mistake": "Check your use of Ohm’s Law.",
                "working": full_working
            },

            {
                "value": distractors[2],
                "summary": "Incorrect.",
                "mistake": "You may have used the wrong resistor.",
                "working": full_working
            }
        ]

        return (
            question,
            correct,
            options_data,
            "V",
            "images/potential_divider.png"
        )


# =========================================================
# RANDOM SELECTOR
# =========================================================

def generate_single_potential_divider_mcq():

    return random.choice([
        generate_type1_question,
        generate_type2_question
    ])()


# =========================================================
# QUIZ GENERATOR
# =========================================================

def generate_potential_divider_mcq(num_questions=5):

    questions = []

    for _ in range(num_questions):

        raw = generate_single_potential_divider_mcq()

def generate_potential_divider_mcq(num_questions=5):

    questions = []

    for _ in range(num_questions):

        raw = generate_single_potential_divider_mcq()

        question, correct, options_data, unit, diagram = raw

        formatted = format_mcq(
            question,
            correct,
            options_data,
            unit
        )

        formatted["diagram"] = diagram

        questions.append(formatted)

    return questions
