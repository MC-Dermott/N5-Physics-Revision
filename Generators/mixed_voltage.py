import random

from utils.mcq_utils import format_mcq


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

        # =================================================
        # FIX: unpack diagram separately if present
        # =================================================
        if len(raw) == 5:
            question, correct, options_data, unit, diagram = raw
        else:
            question, correct, options_data, unit = raw
            diagram = None

        formatted = format_mcq(
            question,
            correct,
            options_data,
            unit
        )

        # attach diagram so Streamlit can render it
        formatted["diagram"] = diagram

        questions.append(formatted)

    return questions
