import random

from utils.mcq_utils import format_mcq
from utils.notes import NOTES


# =========================================================
# IMPORT QUESTION GENERATORS
# =========================================================

from Generators.potential_divider_generator import (
    generate_type1_question as generate_pd_type1,
    generate_type2_question as generate_pd_type2
)

from Generators.transistor_generator import (
    generate_type1 as generate_fixed5v_type1,
    generate_type2 as generate_fixed5v_type2
)

from Generators.complex_circuit_generator import (
    generate_type1 as generate_parallel_series_type1,
    generate_type2 as generate_parallel_series_type2
)


# =========================================================
# QUESTION GROUPS
# =========================================================

POTENTIAL_DIVIDER_GENERATORS = [
    generate_pd_type1,
    generate_pd_type2
]

FIXED_5V_GENERATORS = [
    generate_fixed5v_type1,
    generate_fixed5v_type2
]

PARALLEL_SERIES_GENERATORS = [
    generate_parallel_series_type1,
    generate_parallel_series_type2
]


# =========================================================
# Generate Combined Circuit Quiz
# =========================================================

def generate_circuit_quiz():

    questions = []

    selected_generators = [

        random.choice(POTENTIAL_DIVIDER_GENERATORS),
        random.choice(FIXED_5V_GENERATORS),
        random.choice(PARALLEL_SERIES_GENERATORS)
    ]

    random.shuffle(selected_generators)

    for question_func in selected_generators:

        raw = question_func()

        question, correct, options_data, unit, diagram, *rest = raw
        scaffold = rest[0] if rest else []

        formatted = format_mcq(
            question,
            correct,
            options_data,
            unit,
            scaffold=scaffold,
            notes=NOTES["electricity_current"]
        )

        # attach diagram so Streamlit can render it
        formatted["diagram"] = diagram

        questions.append(formatted)

    return questions
