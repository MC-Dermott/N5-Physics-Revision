import random
from utils.mcq_utils import format_mcq

from Generators.voltage_divider import (
    generate_voltage_divider_question,
    generate_missing_voltage_question
)

from Generators.parallel_series import (
    generate_parallel_series_voltage_question,
    generate_series_voltage_from_parallel_question
)

from Generators.fixed_variable import (
    generate_fixed_variable_voltage_question,
    generate_fixed_variable_missing_voltage_question
)


VOLTAGE_GENERATORS = [
    generate_voltage_divider_question,
    generate_missing_voltage_question,
    generate_parallel_series_voltage_question,
    generate_series_voltage_from_parallel_question,
    generate_fixed_variable_voltage_question,
    generate_fixed_variable_missing_voltage_question
]


def generate_voltage_quiz(num_questions=5):

    questions = []

    for _ in range(num_questions):

        func = random.choice(VOLTAGE_GENERATORS)

        try:
            raw = func()
            questions.append(format_mcq(*raw))
        except Exception:
            continue

    return questions
