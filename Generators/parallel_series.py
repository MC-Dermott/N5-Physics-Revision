import random
from utils.circuit_utils import (
    generate_resistance,
    generate_voltage,
    make_distractors
)


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

def generate_parallel_series_voltage_question():

    rs = generate_resistance()
    rp1 = generate_resistance()
    rp2 = generate_resistance()

    supply_voltage = generate_voltage()

    parallel_resistance = round((rp1 * rp2) / (rp1 + rp2), 2)
    total_resistance = round(rs + parallel_resistance, 2)

    current = supply_voltage / total_resistance

    voltage_series = round(current * rs, 2)
    voltage_parallel = round(supply_voltage - voltage_series, 2)

    target = random.choice(["series", "parallel1", "parallel2"])

    if target == "series":
        correct_voltage = voltage_series
        resistor_name = "series resistor"
    else:
        correct_voltage = voltage_parallel
        resistor_name = "parallel resistor"

    distractors = make_distractors(correct_voltage)

    question = f"""
A circuit contains:

- Series resistor = {rs} kΩ
- Parallel resistors R1 = {rp1} kΩ, R2 = {rp2} kΩ
- Supply voltage = {supply_voltage} V

What is the voltage across {resistor_name}?
"""

    def feedback(correct_letter):
        return {
            correct_letter: {
                "summary": "Correct. Use equivalent resistance.",
                "mistake": None,
                "working": []
            }
        }

    return build_mcq(question, correct_voltage, distractors, feedback)


# =========================================================
# Question 2
# =========================================================

def generate_series_voltage_from_parallel_question(_attempt=0):

    if _attempt > 10:
        raise ValueError("Too many invalid attempts")

    rs = generate_resistance()
    rp1 = generate_resistance()
    rp2 = generate_resistance()

    parallel_voltage = random.choice([x * 0.5 for x in range(1, 11)])

    current1 = parallel_voltage / rp1
    current2 = parallel_voltage / rp2

    total_current = current1 + current2

    series_voltage = round(total_current * rs, 2)

    if parallel_voltage + series_voltage > 9:
        return generate_series_voltage_from_parallel_question(_attempt + 1)

    distractors = make_distractors(series_voltage)

    question = f"""
A circuit contains:

- Series resistor = {rs} kΩ
- Parallel resistors R1 = {rp1} kΩ, R2 = {rp2} kΩ

Voltage across R1 = {parallel_voltage} V

Find voltage across series resistor.
"""

    def feedback(correct_letter):
        return {
            correct_letter: {
                "summary": "Correct. Use Kirchhoff’s laws.",
                "mistake": None,
                "working": []
            }
        }

    return build_mcq(question, series_voltage, distractors, feedback)
