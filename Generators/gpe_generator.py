import random

from utils.mcq_utils import format_mcq
from utils.notes import NOTES


# =========================================================
# Helper Function
# =========================================================
def round_sf(value, sf=3):
    """Round to significant figures."""

    return float(f"{value:.{sf}g}")


def fmt_J(j):
    """Format a J value using SI prefixes for display."""
    j = float(j)
    if abs(j) >= 1_000_000:
        return f"{j / 1_000_000:g} MJ"
    if abs(j) >= 1000:
        return f"{j / 1000:g} kJ"
    return f"{j:g} J"


def g_table(gravity):
    return f"| Constant | Value |\n|---|---|\n| g | {gravity} N/kg |"


# =========================================================
# Working Functions
# =========================================================
def make_working_gpe(
    mass,
    gravity,
    height,
    answer
):

    return [

        {
            "type": "text",
            "content":
                "Use the equation:"
        },

        {
            "type": "latex",
            "content":
                r"E_p = mgh"
        },

        {
            "type": "latex",
            "content":
                rf"E_p = {mass} \times {gravity} \times {height}"
        },

        {
            "type": "latex",
            "content":
                rf"E_p = {fmt_J(answer)}"
        }
    ]


def make_working_mass(
    energy,
    gravity,
    height,
    answer
):

    return [

        {
            "type": "text",
            "content":
                "Rearrange the equation:"
        },

        {
            "type": "latex",
            "content":
                r"m = \frac{E_p}{gh}"
        },

        {
            "type": "latex",
            "content":
                rf"m = \frac{{{fmt_J(energy)}}}{{{gravity} \times {height}}}"
        },

        {
            "type": "latex",
            "content":
                rf"m = {answer}\ \mathrm{{kg}}"
        }
    ]


def make_working_height(
    energy,
    mass,
    gravity,
    answer
):

    return [

        {
            "type": "text",
            "content":
                "Rearrange the equation:"
        },

        {
            "type": "latex",
            "content":
                r"h = \frac{E_p}{mg}"
        },

        {
            "type": "latex",
            "content":
                rf"h = \frac{{{fmt_J(energy)}}}{{{mass} \times {gravity}}}"
        },

        {
            "type": "latex",
            "content":
                rf"h = {answer}\ \mathrm{{m}}"
        }
    ]


# =========================================================
# Value Generators
# =========================================================
def generate_mass():
    """
    Returns:
        display_mass
        actual_mass_kg
        is_grams
    """

    # kg masses
    if random.choice([True, False]):

        mass = random.choice(
            range(5, 105, 5)
        )

        return (
            mass,
            mass,
            False
        )

    # gram masses
    mass_g = random.choice(
        range(100, 1000, 100)
    )

    mass_kg = mass_g / 1000

    return (
        mass_g,
        mass_kg,
        True
    )


def generate_gravity():

    return random.choice([
        9.8,
        10
    ])


def generate_height():

    return random.randint(
        2,
        50
    )


def generate_energy():

    return random.choice(
        range(50, 5001, 50)
    )


# =========================================================
# GPE Question
# =========================================================
def generate_gpe_question():

    display_mass, mass_kg, is_grams = (
        generate_mass()
    )

    gravity = generate_gravity()

    height = generate_height()

    correct_val = round_sf(
        mass_kg * gravity * height
    )

    rearranged_answer = round_sf(
        mass_kg / (gravity * height)
    )

    if is_grams:

        grams_error = round_sf(
            display_mass * gravity * height
        )

        mass_text = (
            f"{display_mass}g"
        )

    else:

        grams_error = round_sf(
            mass_kg + gravity + height
        )

        mass_text = (
            f"{display_mass}kg"
        )

    random_error = round_sf(
        mass_kg * gravity + height
    )

    unit = "J"

    question = (

        f"What is the gravitational "
        f"potential energy of a "
        f"{mass_text} object raised "
        f"{height} m?\n\n"
        f"{g_table(gravity)}"
    )

    working = make_working_gpe(

        round_sf(mass_kg),

        gravity,

        height,

        correct_val
    )

    options_data = [

        {
            "value": correct_val,
            "display": fmt_J(correct_val),
            "summary":
                "Correct!",

            "mistake": None,

            "working": working
        },

        {
            "value": rearranged_answer,
            "display": fmt_J(rearranged_answer),
            "summary":
                "Incorrect.",

            "mistake":
                "You rearranged the "
                "equation incorrectly.",

            "working": working
        },

        {
            "value": grams_error,
            "display": fmt_J(grams_error),
            "summary":
                "Incorrect.",

            "mistake":
                "You did not convert "
                "grams into kilograms.",

            "working": working
        },

        {
            "value": random_error,
            "display": fmt_J(random_error),
            "summary":
                "Incorrect.",

            "mistake":
                "You used the equation "
                "incorrectly.",

            "working": working
        }
    ]

    return format_mcq(
        question,
        correct_val,
        options_data,
        unit,
        scaffold=[],
        notes=NOTES["energy_gpe"]
    )


# =========================================================
# Mass Question
# =========================================================
def generate_mass_question():

    gravity = generate_gravity()

    height = generate_height()

    energy = generate_energy()

    correct_val = round_sf(
        energy / (gravity * height)
    )

    rearranged_answer = round_sf(
        energy * gravity * height
    )

    grams_error = round_sf(
        correct_val * 1000
    )

    random_error = round_sf(
        energy / gravity
    )

    unit = "kg"

    question = (

        f"What is the mass of an object "
        f"with gravitational potential "
        f"energy {fmt_J(energy)} raised "
        f"{height} m?\n\n"
        f"{g_table(gravity)}"
    )

    working = make_working_mass(

        energy,

        gravity,

        height,

        correct_val
    )

    options_data = [

        {
            "value": correct_val,

            "summary":
                "Correct!",

            "mistake": None,

            "working": working
        },

        {
            "value": rearranged_answer,

            "summary":
                "Incorrect.",

            "mistake":
                "You rearranged the "
                "equation incorrectly.",

            "working": working
        },

        {
            "value": grams_error,

            "summary":
                "Incorrect.",

            "mistake":
                "You converted kilograms "
                "into grams incorrectly.",

            "working": working
        },

        {
            "value": random_error,

            "summary":
                "Incorrect.",

            "mistake":
                "You used the equation "
                "incorrectly.",

            "working": working
        }
    ]

    return format_mcq(
        question,
        correct_val,
        options_data,
        unit,
        scaffold=[],
        notes=NOTES["energy_gpe"]
    )


# =========================================================
# Height Question
# =========================================================
def generate_height_question():

    display_mass, mass_kg, is_grams = (
        generate_mass()
    )

    gravity = generate_gravity()

    energy = generate_energy()

    correct_val = round_sf(
        energy / (mass_kg * gravity)
    )

    rearranged_answer = round_sf(
        energy * mass_kg * gravity
    )

    if is_grams:

        grams_error = round_sf(
            energy / (display_mass * gravity)
        )

        mass_text = (
            f"{display_mass}g"
        )

    else:

        grams_error = round_sf(
            correct_val + gravity
        )

        mass_text = (
            f"{display_mass}kg"
        )

    random_error = round_sf(
        energy / mass_kg
    )

    unit = "m"

    question = (

        f"An object with mass "
        f"{mass_text} has "
        f"gravitational potential "
        f"energy {fmt_J(energy)}. "
        f"What height was it raised?\n\n"
        f"{g_table(gravity)}"
    )

    working = make_working_height(

        energy,

        round_sf(mass_kg),

        gravity,

        correct_val
    )

    options_data = [

        {
            "value": correct_val,

            "summary":
                "Correct!",

            "mistake": None,

            "working": working
        },

        {
            "value": rearranged_answer,

            "summary":
                "Incorrect.",

            "mistake":
                "You rearranged the "
                "equation incorrectly.",

            "working": working
        },

        {
            "value": grams_error,

            "summary":
                "Incorrect.",

            "mistake":
                "You did not convert "
                "grams into kilograms.",

            "working": working
        },

        {
            "value": random_error,

            "summary":
                "Incorrect.",

            "mistake":
                "You used the equation "
                "incorrectly.",

            "working": working
        }
    ]

    return format_mcq(
        question,
        correct_val,
        options_data,
        unit,
        scaffold=[],
        notes=NOTES["energy_gpe"]
    )


# =========================================================
# Random Question
# =========================================================
def generate_single_mcq_gpe():

    generators = [

        generate_gpe_question,

        generate_mass_question,

        generate_height_question
    ]

    question_func = random.choice(
        generators
    )

    return question_func()


# =========================================================
# Generate Quiz
# =========================================================
def generate_mcq_gpe():

    questions = []

    for _ in range(5):

        formatted_question = (
            generate_single_mcq_gpe()
        )

        questions.append(
            formatted_question
        )

    return questions
