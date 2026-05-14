import random
from utils.mcq_utils import format_mcq

# =========================================================
# Helpers
# =========================================================

MAX_VOLTAGE = 9
STEP = 0.5


def generate_voltage():
    return random.randint(
        1,
        int((MAX_VOLTAGE - STEP) / STEP)
    ) * STEP


def generate_resistance():
    return random.randint(5, 50) * 10


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

def working_parallel(r2, r3, vp):

    return [
        {"type": "text", "content": "First find currents in the parallel branch (R2 and R3):"},
        {"type": "latex", "content": r"I = \frac{V}{R}"},
        {"type": "latex", "content": rf"I_2 = \frac{{{vp}}}{{{r2}}}, \quad I_3 = \frac{{{vp}}}{{{r3}}}"},
        {"type": "text", "content": "Total current in parallel section:"},
        {"type": "latex", "content": r"I_{total} = I_2 + I_3"}
    ]


def working_series(i, r1, v1):

    return [
        {"type": "text", "content": "Now calculate voltage across the series resistor (R1):"},
        {"type": "latex", "content": r"V = IR"},
        {"type": "latex", "content": rf"V = {i} \times {r1}"},
        {"type": "latex", "content": rf"V = {v1}\ \mathrm{{V}}"}
    ]


def parallel_eq(r2, r3):
    return (r2 * r3) / (r2 + r3)


# =========================================================
# TYPE 1
# =========================================================

def generate_type1():

    while True:

        r1 = generate_resistance()
        r2 = generate_resistance()
        r3 = generate_resistance()

        vp = generate_voltage()
        v1 = generate_voltage()

        v_total = vp + v1

        if v_total >= MAX_VOLTAGE:
            continue

        req = parallel_eq(r2, r3)
        i_total = vp / req

        r1_check = v1 / i_total

        if round(r1_check / 10) * 10 != r1:
            continue

        target = random.choice(["R1", "R2", "R3"])

        if target == "R1":
            correct = v1
        else:
            correct = vp

        question = f"""
A circuit contains R2 and R3 in parallel, in series with R1:

- R1 = {r1} Ω
- R2 = {r2} Ω
- R3 = {r3} Ω
- Supply voltage = {v_total} V

Calculate the voltage across {target}.
"""

        diagram = "images/complex_circuit.png"

        full_working = working_parallel(r2, r3, vp) + working_series(i_total, r1, v1)

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
                "mistake": "Check series-parallel voltage split.",
                "working": full_working
            },
            {
                "value": distractors[1],
                "summary": "Incorrect.",
                "mistake": "You may have used total voltage incorrectly.",
                "working": full_working
            },
            {
                "value": distractors[2],
                "summary": "Incorrect.",
                "mistake": "Re-check Ohm’s Law application.",
                "working": full_working
            }
        ]

        return question, correct, options_data, "V", diagram


# =========================================================
# TYPE 2
# =========================================================

def generate_type2():

    while True:

        r1 = generate_resistance()
        r2 = generate_resistance()
        r3 = generate_resistance()

        vp = generate_voltage()

        req = parallel_eq(r2, r3)
        i_total = vp / req

        v1 = i_total * r1

        if v1 >= MAX_VOLTAGE:
            continue

        if vp + v1 >= MAX_VOLTAGE:
            continue

        correct = round(v1, 2)

        question = f"""
A circuit contains R2 and R3 in parallel, in series with R1:

- R1 = {r1} Ω
- R2 = {r2} Ω
- R3 = {r3} Ω

Voltage across the parallel combination (R2 and R3) is {vp} V.

Calculate the voltage across R1.
"""

        diagram = "images/complex_circuit.png"

        full_working = working_parallel(r2, r3, vp) + working_series(i_total, r1, correct)

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
                "mistake": "You may have added voltages incorrectly.",
                "working": full_working
            },
            {
                "value": distractors[1],
                "summary": "Incorrect.",
                "mistake": "Check series voltage rules.",
                "working": full_working
            },
            {
                "value": distractors[2],
                "summary": "Incorrect.",
                "mistake": "You may have confused current and voltage.",
                "working": full_working
            }
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

def generate_parallel_series_quiz(num_questions=5):

    questions = []

    for _ in range(num_questions):

        raw = generate_single_mcq()

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
