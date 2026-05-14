import random

from utils.mcq_utils import format_mcq


# =========================================================
# Helpers
# =========================================================

def generate_resistance():
    """
    Resistance values:
    0.5 kΩ to 5.0 kΩ
    """

    return random.randint(1, 10) * 0.5


def generate_voltage():
    """
    Supply voltages:
    1V to 9V
    """

    return random.randint(1, 9)


def make_distractors(correct):

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
# Question Type 1
# Supply voltage given
# Ask for voltage across random resistor
# =========================================================

def generate_parallel_series_voltage_question():

    # =====================================
    # Resistances
    # =====================================

    rs = generate_resistance()

    rp1 = generate_resistance()

    rp2 = generate_resistance()

    supply_voltage = generate_voltage()

    # =====================================
    # Parallel equivalent resistance
    # =====================================

    parallel_resistance = round(
        (rp1 * rp2) / (rp1 + rp2),
        2
    )

    total_resistance = round(
        rs + parallel_resistance,
        2
    )

    # =====================================
    # Circuit current
    # =====================================

    current = supply_voltage / total_resistance

    # =====================================
    # Voltages
    # =====================================

    voltage_series = round(
        current * rs,
        2
    )

    voltage_parallel = round(
        supply_voltage - voltage_series,
        2
    )

    # =====================================
    # Random resistor target
    # =====================================

    target = random.choice([
        "series",
        "parallel1",
        "parallel2"
    ])

    if target == "series":

        correct_voltage = voltage_series
        resistor_name = "the series resistor"

    elif target == "parallel1":

        correct_voltage = voltage_parallel
        resistor_name = "parallel resistor R1"

    else:

        correct_voltage = voltage_parallel
        resistor_name = "parallel resistor R2"

    # =====================================
    # Answers
    # =====================================

    distractors = make_distractors(correct_voltage)

    all_answers = distractors + [correct_voltage]

    random.shuffle(all_answers)

    letters = ["A", "B", "C", "D"]

    choices = {
        letter: f"{value} V"
        for letter, value in zip(letters, all_answers)
    }

    correct_letter = letters[
        all_answers.index(correct_voltage)
    ]

    # =====================================
    # Question
    # =====================================

    question = f"""
A circuit contains:

- A series resistor of {rs} kΩ
- Two parallel resistors:
    - R1 = {rp1} kΩ
    - R2 = {rp2} kΩ

The supply voltage is {supply_voltage} V.

What is the voltage across {resistor_name}?
"""

    # =====================================
    # Feedback
    # =====================================

    feedback = {}

    for letter in letters:

        if letter == correct_letter:

            summary = (
                "Correct. First calculate the equivalent "
                "parallel resistance."
            )

            mistake = None

        else:

            summary = (
                "Incorrect. You must first find the parallel "
                "equivalent resistance."
            )

            mistake = (
                "You may have treated the parallel resistors as series."
            )

        feedback[letter] = {

            "summary": summary,

            "mistake": mistake,

            "working": [

                {
                    "type": "text",
                    "content": (
                        "Find the equivalent parallel resistance:"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"R_p = "
                        f"\\frac{{{rp1} \\times {rp2}}}"
                        f"{{{rp1} + {rp2}}}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"R_p = {parallel_resistance}\\ k\\Omega"
                    )
                },

                {
                    "type": "text",
                    "content": (
                        "Find the total resistance:"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"R_t = {rs} + {parallel_resistance}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"R_t = {total_resistance}\\ k\\Omega"
                    )
                },

                {
                    "type": "text",
                    "content": (
                        "Calculate current:"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"I = \\frac{{{supply_voltage}}}"
                        f"{{{total_resistance}}}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"I = {round(current,2)}\\ mA"
                    )
                },

                {
                    "type": "text",
                    "content": (
                        "Find the voltage:"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"V = {correct_voltage}\\ V"
                    )
                }
            ]
        }

    return (
        question,
        choices,
        correct_letter,
        feedback
    )


# =========================================================
# Question Type 2
# Voltage across parallel resistor given
# Ask for voltage across series resistor
# =========================================================

def generate_series_voltage_from_parallel_question():

    # =====================================
    # Resistances
    # =====================================

    rs = generate_resistance()

    rp1 = generate_resistance()

    rp2 = generate_resistance()

    # =====================================
    # Choose parallel voltage
    # Multiples of 0.5 V
    # =====================================

    parallel_voltage = random.choice([
        x * 0.5
        for x in range(1, 11)
    ])

    # =====================================
    # Parallel current
    # =====================================

    current1 = parallel_voltage / rp1

    current2 = parallel_voltage / rp2

    total_current = current1 + current2

    # =====================================
    # Voltage across series resistor
    # =====================================

    series_voltage = round(
        total_current * rs,
        2
    )

    # keep total voltage <= 9V
    if parallel_voltage + series_voltage > 9:
        return generate_series_voltage_from_parallel_question()

    # =====================================
    # Answers
    # =====================================

    distractors = make_distractors(series_voltage)

    all_answers = distractors + [series_voltage]

    random.shuffle(all_answers)

    letters = ["A", "B", "C", "D"]

    choices = {
        letter: f"{value} V"
        for letter, value in zip(letters, all_answers)
    }

    correct_letter = letters[
        all_answers.index(series_voltage)
    ]

    # =====================================
    # Question
    # =====================================

    question = f"""
A circuit contains:

- A series resistor of {rs} kΩ
- Two parallel resistors:
    - R1 = {rp1} kΩ
    - R2 = {rp2} kΩ

The voltage across R1 is {parallel_voltage} V.

What is the voltage across the series resistor?
"""

    # =====================================
    # Feedback
    # =====================================

    feedback = {}

    for letter in letters:

        if letter == correct_letter:

            summary = (
                "Correct. The voltage across both parallel "
                "resistors is the same."
            )

            mistake = None

        else:

            summary = (
                "Incorrect. Use the parallel currents to "
                "find the total current."
            )

            mistake = (
                "You may not have added the branch currents correctly."
            )

        feedback[letter] = {

            "summary": summary,

            "mistake": mistake,

            "working": [

                {
                    "type": "text",
                    "content": (
                        "Voltage across both parallel resistors "
                        "is the same."
                    )
                },

                {
                    "type": "text",
                    "content": (
                        "Find branch currents:"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"I_1 = \\frac{{{parallel_voltage}}}{{{rp1}}}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"I_2 = \\frac{{{parallel_voltage}}}{{{rp2}}}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"I_t = {round(current1,2)} + {round(current2,2)}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"I_t = {round(total_current,2)}\\ mA"
                    )
                },

                {
                    "type": "text",
                    "content": (
                        "Use Ohm's law on the series resistor:"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"V = IR"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"V = {round(total_current,2)}"
                        f"\\times {rs}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"V = {series_voltage}\\ V"
                    )
                }
            ]
        }

    return (
        question,
        choices,
        correct_letter,
        feedback
    )


# =========================================================
# Mixed Quiz Generator
# =========================================================

def generate_parallel_series_mcqs(num_questions=5):

    generators = [

        generate_parallel_series_voltage_question,

        generate_series_voltage_from_parallel_question
    ]

    questions = []

    for _ in range(num_questions):

        raw_question = random.choice(
            generators
        )()

        formatted_question = format_mcq(
            *raw_question
        )

        questions.append(
            formatted_question
        )

    return questions
