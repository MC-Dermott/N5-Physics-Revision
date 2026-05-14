import random
from utils.mcq_utils import format_mcq


# =========================================================
# Helpers
# =========================================================

SUPPLY_VOLTAGE = 5


def generate_resistance():
    return random.randint(1, 10) * 0.5


def make_distractors(correct):

    distractors = set()

    while len(distractors) < 3:

        variation = random.choice([-2, -1, -0.5, 0.5, 1, 2])
        value = round(correct + variation, 2)

        if value > 0 and value != correct:
            distractors.add(value)

    return list(distractors)


# =========================================================
# WORKING
# =========================================================

def working_current(r_total):

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
            "content": rf"I = \frac{{5}}{{{r_total}}}"
        }
    ]


def working_voltage(i, r, result):

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
# ONLY SUPPLY VOLTAGE GIVEN (5V)
# =========================================================

def generate_type1():

    while True:

        r_fixed = generate_resistance()
        r_variable = generate_resistance()

        r_total = r_fixed + r_variable

        current = round(SUPPLY_VOLTAGE / r_total, 3)

        target = random.choice(["fixed", "variable"])

        if target == "fixed":
            correct = round(current * r_fixed, 2)
            r_used = r_fixed
            name = "fixed resistor"
        else:
            correct = round(current * r_variable, 2)
            r_used = r_variable
            name = "variable resistor"

        if correct <= 0:
            continue

        # ❗ ONLY supply voltage is given
        question = f"""
A potential divider circuit has two resistors in series:

- Fixed resistor = {r_fixed} kΩ
- Variable resistor = {r_variable} kΩ
- Supply voltage = {SUPPLY_VOLTAGE} V

Calculate the voltage across the {name}.
"""

        diagram = "images/transistor_circuit.png"

        full_working = working_current(r_total) + working_voltage(current, r_used, correct)

        distractors = make_distractors(correct)

        options_data = [
            {"value": correct, "summary": "Correct!", "mistake": None, "working": full_working},
            {"value": distractors[0], "summary": "Incorrect.", "mistake": "Check voltage division.", "working": full_working},
            {"value": distractors[1], "summary": "Incorrect.", "mistake": "Check your Ohm’s Law step.", "working": full_working},
            {"value": distractors[2], "summary": "Incorrect.", "mistake": "You may have used the wrong resistor.", "working": full_working},
        ]

        return question, correct, options_data, "V", diagram


# =========================================================
# TYPE 2
# ONE RESISTOR VOLTAGE GIVEN (NO SUPPLY VOLTAGE)
# =========================================================

def generate_type2():

    while True:

        r_fixed = generate_resistance()
        r_variable = generate_resistance()

        r_total = r_fixed + r_variable

        current = round(SUPPLY_VOLTAGE / r_total, 3)

        fixed_v = round(current * r_fixed, 2)
        variable_v = round(current * r_variable, 2)

        given = random.choice(["fixed", "variable"])

        # ❗ IMPORTANT: we do NOT give supply voltage in the question
        # student must infer it via ratio or implied circuit understanding

        if given == "fixed":
            given_voltage = fixed_v
            correct = variable_v
            r_used = r_variable
            given_name = "fixed resistor"
            target_name = "variable resistor"
        else:
            given_voltage = variable_v
            correct = fixed_v
            r_used = r_fixed
            given_name = "variable resistor"
            target_name = "fixed resistor"

        if correct <= 0:
            continue

        question = f"""
A potential divider circuit has two resistors in series:

- Fixed resistor = {r_fixed} kΩ
- Variable resistor = {r_variable} kΩ

The voltage across the {given_name} is {given_voltage} V.

Calculate the voltage across the {target_name}.
"""

        diagram = "images/transistor_circuit.png"

        full_working = working_current(r_total) + working_voltage(current, r_used, correct)

        distractors = make_distractors(correct)

        options_data = [
            {"value": correct, "summary": "Correct!", "mistake": None, "working": full_working},
            {"value": distractors[0], "summary": "Incorrect.", "mistake": "Check voltage ratio in series.", "working": full_working},
            {"value": distractors[1], "summary": "Incorrect.", "mistake": "Check Ohm’s Law application.", "working": full_working},
            {"value": distractors[2], "summary": "Incorrect.", "mistake": "You may have confused resistors.", "working": full_working},
        ]

        return question, correct, options_data, "V", diagram


# =========================================================
# RANDOM SELECTOR
# =========================================================

def generate_single_mcq():

    return random.choice([
        generate_type1,
        generate_type2
    ])()


# =========================================================
# QUIZ GENERATOR
# =========================================================

def generate_fixed_5v_potential_divider_quiz(num_questions=5):

    questions = []

    for _ in range(num_questions):

        question, correct, options_data, unit, diagram = generate_single_mcq()

        formatted = format_mcq(question, correct, options_data, unit)

        formatted["diagram"] = diagram

        questions.append(formatted)

    return questions
