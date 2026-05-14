import random

from utils.mcq_utils import format_mcq


# =========================================================
# IMPORT QUESTION GENERATORS
# =========================================================
from Generators.gpe_generator import (
    generate_gpe_question,
    generate_mass_question as generate_gpe_mass_question,
    generate_height_question
)

from Generators.ke_generator import (
    generate_ke_question,
    generate_mass_question as generate_ke_mass_question,
    generate_velocity_question
)

from Generators.workdone_generator import (
    generate_workdone_question,
    generate_force_question,
    generate_distance_question
)


# =========================================================
# QUESTION GROUPS
# =========================================================

# -------------------------
# GPE generators
# -------------------------
GPE_GENERATORS = [
    generate_gpe_question,
    generate_gpe_mass_question,
    generate_height_question
]

# -------------------------
# KE generators
# -------------------------
KE_GENERATORS = [
    generate_ke_question,
    generate_ke_mass_question,
    generate_velocity_question
]

# -------------------------
# Work Done generators
# -------------------------
WORKDONE_GENERATORS = [
    generate_workdone_question,
    generate_force_question,
    generate_distance_question
]


# =========================================================
# Generate Energy Quiz
# =========================================================
def generate_energy_quiz():

    questions = []

    # =====================================
    # Select ONE from each topic
    # =====================================
    selected_generators = [

        random.choice(GPE_GENERATORS),

        random.choice(KE_GENERATORS),

        random.choice(WORKDONE_GENERATORS)
    ]

    # Optional:
    # randomize question order
    random.shuffle(selected_generators)

    # =====================================
    # Generate formatted questions
    # =====================================
    for question_func in selected_generators:

        raw_question = question_func()

        formatted_question = format_mcq(
            *raw_question
        )

        questions.append(
            formatted_question
        )

    return questions
