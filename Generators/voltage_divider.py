import random
from utils.circuit_utils import (
    generate_resistance,
    generate_voltage,
    make_distractors
)


# =========================================================
# Helper (local only)
# =========================================================

def build_mcq(question, correct, distractors, feedback_template):
    all_answers = distractors + [correct]
    random.shuffle(all_answers)

    letters = ["A", "B", "C", "D"]

    choices = {
        letter: f"{value} V"
        for letter, value in zip(letters, all_answers)
    }

    correct_letter = letters[all_answers.index(correct)]

    return question, choices, correct_letter, feedback_template(correct_letter)


# =========================================================
# Question 1
# =========================================================

def generate_voltage_divider_question():

    supply_voltage = generate_voltage()
    fixed_resistance = generate_resistance()
    variable_resistance = generate_resistance()

    total_resistance = fixed_resistance + variable_resistance

    target = random.choice(["fixed", "variable"])

    if target == "fixed":
        target_resistance = fixed_resistance
        resistor_name = "the fixed resistor"
    else:
        target_resistance = variable_resistance
        resistor_name = "the variable resistor"

    correct_voltage = round(
        supply_voltage * target_resistance / total_resistance,
        2
    )

    distractors = make_distractors(correct_voltage)

    question = f"""
A voltage divider circuit contains two resistors connected in series.

- Fixed resistor = {fixed_resistance} Ω
- Variable resistor = {variable_resistance} Ω
- Supply voltage = {supply_voltage} V

What is the voltage across {resistor_name}?
"""

    def feedback(correct_letter):

        return {
            correct_letter: {
                "summary": "Correct. Voltage divides in proportion to resistance.",
                "mistake": None,
                "working": []
            }
        }

    return build_mcq(question, correct_voltage, distractors, feedback)


# =========================================================
# Question 2
# =========================================================

def generate_missing_voltage_question():

    fixed_resistance = generate_resistance()
    variable_resistance = generate_resistance()

    total_resistance = fixed_resistance + variable_resistance

    possible_supply_voltages = [v * 0.5 for v in range(1, 19)]

    valid_cases = []

    for supply_voltage in possible_supply_voltages:

        fixed_voltage = round(
            supply_voltage * fixed_resistance / total_resistance,
            2
        )

        variable_voltage = round(
            supply_voltage * variable_resistance / total_resistance,
            2
        )

        if fixed_voltage * 2 == int(fixed_voltage * 2) and \
           variable_voltage * 2 == int(variable_voltage * 2):

            valid_cases.append(
                (supply_voltage, fixed_voltage, variable_voltage)
            )

    if not valid_cases:
        return generate_missing_voltage_question()

    supply_voltage, fixed_voltage, variable_voltage = random.choice(valid_cases)

    target = random.choice(["fixed", "variable"])

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

    distractors = make_distractors(answer_voltage)

    question = f"""
A voltage divider circuit contains two resistors connected in series.

- Fixed resistor = {fixed_resistance} Ω
- Variable resistor = {variable_resistance} Ω

The voltage across the {given_name} is {given_voltage} V.

What is the voltage across the {target_name}?
"""

    def feedback(correct_letter):

        return {
            correct_letter: {
                "summary": "Correct. Voltage divides in proportion to resistance.",
                "mistake": None,
                "working": []
            }
        }

    return build_mcq(question, answer_voltage, distractors, feedback)
