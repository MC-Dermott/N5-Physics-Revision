import random

from utils.mcq_utils import format_mcq


# =========================================================
# Helpers
# =========================================================

def generate_resistance():
    """
    Resistance values:
    0.5 Ω to 5.0 Ω
    """

    return random.randint(1, 10) * 0.5


def generate_voltage():
    """
    Supply voltages:
    1V to 9V
    """

    return random.randint(1, 9)


def make_distractors(correct):
    """
    Generate sensible incorrect answers
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
# Question Type 1
# Supply voltage given
# =========================================================

def generate_voltage_divider_question():

    # =====================================
    # Circuit values
    # =====================================

    supply_voltage = generate_voltage()

    fixed_resistance = generate_resistance()

    variable_resistance = generate_resistance()

    total_resistance = (
        fixed_resistance +
        variable_resistance
    )

    # =====================================
    # Choose target resistor
    # =====================================

    target = random.choice([
        "fixed",
        "variable"
    ])

    if target == "fixed":

        target_resistance = fixed_resistance

        resistor_name = (
            "the fixed resistor"
        )

    else:

        target_resistance = variable_resistance

        resistor_name = (
            "the variable resistor"
        )

    # =====================================
    # Correct answer
    # =====================================

    correct_voltage = round(

        supply_voltage *

        target_resistance /

        total_resistance,

        2
    )

    # =====================================
    # Answers
    # =====================================

    distractors = make_distractors(
        correct_voltage
    )

    all_answers = (
        distractors +
        [correct_voltage]
    )

    random.shuffle(all_answers)

    letters = ["A", "B", "C", "D"]

    choices = {

        letter: f"{value} V"

        for letter, value in zip(
            letters,
            all_answers
        )
    }

    correct_letter = letters[
        all_answers.index(correct_voltage)
    ]

    # =====================================
    # Question
    # =====================================

    question = f"""
A voltage divider circuit contains two resistors connected in series.

- Fixed resistor = {fixed_resistance} Ω
- Variable resistor = {variable_resistance} Ω
- Supply voltage = {supply_voltage} V

What is the voltage across {resistor_name}?
"""

    # =====================================
    # Feedback
    # =====================================

    feedback = {}

    for letter in letters:

        if letter == correct_letter:

            summary = (
                "Correct. Voltage is shared in "
                "proportion to resistance."
            )

            mistake = None

        else:

            summary = (
                "Incorrect. Use the voltage divider "
                "relationship."
            )

            mistake = (
                "You may not have used the total "
                "resistance correctly."
            )

        feedback[letter] = {

            "summary": summary,

            "mistake": mistake,

            "working": [

                {
                    "type": "text",
                    "content": (
                        "Find the total resistance."
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"R_t = "
                        f"{fixed_resistance}"
                        f"+"
                        f"{variable_resistance}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"R_t = "
                        f"{total_resistance}"
                        f"\\ \\Omega"
                    )
                },

                {
                    "type": "text",
                    "content": (
                        "Use the voltage divider equation."
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        "\\frac{V_1}{V_2}"
                        "="
                        "\\frac{R_1}{R_2}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"V = "
                        f"{supply_voltage}"
                        f"\\times"
                        f"\\frac{{{target_resistance}}}"
                        f"{{{total_resistance}}}"
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
# One resistor voltage given
# =========================================================

def generate_missing_voltage_question():

    # =====================================
    # Resistances
    # =====================================

    fixed_resistance = generate_resistance()

    variable_resistance = generate_resistance()

    total_resistance = (
        fixed_resistance +
        variable_resistance
    )

    # =====================================
    # Generate valid voltages
    # =====================================

    possible_supply_voltages = [

        v * 0.5

        for v in range(1, 19)
    ]

    valid_cases = []

    for supply_voltage in possible_supply_voltages:

        fixed_voltage = round(

            supply_voltage *

            fixed_resistance /

            total_resistance,

            2
        )

        variable_voltage = round(

            supply_voltage *

            variable_resistance /

            total_resistance,

            2
        )

        # Must be multiples of 0.5
        if (

            fixed_voltage * 2 ==
            int(fixed_voltage * 2)

            and

            variable_voltage * 2 ==
            int(variable_voltage * 2)
        ):

            valid_cases.append(

                (
                    supply_voltage,
                    fixed_voltage,
                    variable_voltage
                )
            )

    # fallback safety
    if not valid_cases:

        return generate_missing_voltage_question()

    (
        supply_voltage,
        fixed_voltage,
        variable_voltage

    ) = random.choice(valid_cases)

    # =====================================
    # Choose target resistor
    # =====================================

    target = random.choice([
        "fixed",
        "variable"
    ])

    if target == "fixed":

        given_voltage = variable_voltage

        answer_voltage = fixed_voltage

        target_name = "fixed resistor"

        given_name = "variable resistor"

    else:

        given_voltage = fixed_voltage

        answer_voltage = variable_voltage

        target_name = "variable resistor"

        given_name = "fixed resistor"

    # =====================================
    # Answers
    # =====================================

    distractors = make_distractors(
        answer_voltage
    )

    all_answers = (
        distractors +
        [answer_voltage]
    )

    random.shuffle(all_answers)

    letters = ["A", "B", "C", "D"]

    choices = {

        letter: f"{value} V"

        for letter, value in zip(
            letters,
            all_answers
        )
    }

    correct_letter = letters[
        all_answers.index(answer_voltage)
    ]

    # =====================================
    # Question
    # =====================================

    question = f"""
A voltage divider circuit contains two resistors connected in series.

- Fixed resistor = {fixed_resistance} Ω
- Variable resistor = {variable_resistance} Ω

The voltage across the {given_name} is {given_voltage} V.

What is the voltage across the {target_name}?
"""

    # =====================================
    # Feedback
    # =====================================

    feedback = {}

    for letter in letters:

        if letter == correct_letter:

            summary = (
                "Correct. Voltage divides in "
                "proportion to resistance."
            )

            mistake = None

        else:

            summary = (
                "Incorrect. Use the resistance ratio "
                "to determine the missing voltage."
            )

            mistake = (
                "You may not have used the "
                "voltage ratio correctly."
            )

        feedback[letter] = {

            "summary": summary,

            "mistake": mistake,

            "working": [

                {
                    "type": "text",
                    "content": (
                        "Use the voltage ratio."
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        "\\frac{V_f}{V_v}"
                        "="
                        "\\frac{R_f}{R_v}"
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"\\frac{{V}}{{{given_voltage}}}"
                        "="
                        f"\\frac{{{fixed_resistance}}}"
                        f"{{{variable_resistance}}}"
                    )
                },

                {
                    "type": "text",
                    "content": (
                        "Solve for the missing voltage."
                    )
                },

                {
                    "type": "latex",
                    "content": (
                        f"V = {answer_voltage}\\ V"
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

def generate_voltage_divider_mcqs(
    num_questions=5
):

    generators = [

        generate_voltage_divider_question,

        generate_missing_voltage_question
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
