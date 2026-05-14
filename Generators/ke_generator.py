import random

from utils.mcq_utils import format_mcq


# =========================================================
# Helper Function
# =========================================================
def round_sf(value, sf=3):
    """Round to significant figures."""

    return float(f"{value:.{sf}g}")


# =========================================================
# Working Functions
# =========================================================
def make_working_ke(
    mass,
    velocity,
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
                r"E_k = \frac{1}{2}mv^2"
        },

        {
            "type": "latex",
            "content":
                rf"E_k = \frac{{1}}{{2}} \times {mass} \times {velocity}^2"
        },

        {
            "type": "latex",
            "content":
                rf"E_k = {answer}\ \mathrm{{J}}"
        }
    ]


def make_working_mass(
    energy,
    velocity,
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
                r"m = \frac{2E_k}{v^2}"
        },

        {
            "type": "latex",
            "content":
                rf"m = \frac{{2 \times {energy}}}{{{velocity}^2}}"
        },

        {
            "type": "latex",
            "content":
                rf"m = {answer}\ \mathrm{{kg}}"
        }
    ]


def make_working_velocity(
    energy,
    mass,
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
                r"v = \sqrt{\frac{2E_k}{m}}"
        },

        {
            "type": "latex",
            "content":
                rf"v = \sqrt{{\frac{{2 \times {energy}}}{{{mass}}}}}"
        },

        {
            "type": "latex",
            "content":
                rf"v = {answer}\ \mathrm{{m/s}}"
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


def generate_velocity():

    return random.randint(
        2,
        30
    )


def generate_energy():

    return random.choice(
        range(50, 5001, 50)
    )


# =========================================================
# Kinetic Energy Question
# =========================================================
def generate_ke_question():

    display_mass, mass_kg, is_grams = (
        generate_mass()
    )

    velocity = generate_velocity()

    correct_val = round_sf(
        0.5 * mass_kg * velocity**2
    )

    rearranged_answer = round_sf(
        (2 * correct_val) / velocity**2
    )

    if is_grams:

        grams_error = round_sf(
            0.5 * display_mass * velocity**2
        )

        mass_text = (
            f"{display_mass}g"
        )

    else:

        grams_error = round_sf(
            mass_kg + velocity
        )

        mass_text = (
            f"{display_mass}kg"
        )

    random_error = round_sf(
        mass_kg * velocity**2
    )

    unit = "J"

    question = (

        f"What is the kinetic energy "
        f"of a {mass_text} object "
        f"moving at {velocity}m/s?"
    )

    working = make_working_ke(

        round_sf(mass_kg),

        velocity,

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
                "You forgot the "
                r"\(\frac{1}{2}\) in the equation.",

            "working": working
        }
    ]

    return (
        question,
        correct_val,
        options_data,
        unit
    )


# =========================================================
# Mass Question
# =========================================================
def generate_mass_question():

    velocity = generate_velocity()

    energy = generate_energy()

    correct_val = round_sf(
        (2 * energy) / velocity**2
    )

    rearranged_answer = round_sf(
        (energy * velocity**2) / 2
    )

    grams_error = round_sf(
        correct_val * 1000
    )

    random_error = round_sf(
        energy / velocity**2
    )

    unit = "kg"

    question = (

        f"What is the mass of an "
        f"object with kinetic energy "
        f"{energy}J moving at "
        f"{velocity}m/s?"
    )

    working = make_working_mass(

        energy,

        velocity,

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
                "You forgot to multiply "
                "by 2.",

            "working": working
        }
    ]

    return (
        question,
        correct_val,
        options_data,
        unit
    )


# =========================================================
# Velocity Question
# =========================================================
def generate_velocity_question():

    display_mass, mass_kg, is_grams = (
        generate_mass()
    )

    energy = generate_energy()

    correct_val = round_sf(
        ((2 * energy) / mass_kg) ** 0.5
    )

    rearranged_answer = round_sf(
        energy / (0.5 * mass_kg)
    )

    if is_grams:

        grams_error = round_sf(
            ((2 * energy) / display_mass) ** 0.5
        )

        mass_text = (
            f"{display_mass}g"
        )

    else:

        grams_error = round_sf(
            correct_val + mass_kg
        )

        mass_text = (
            f"{display_mass}kg"
        )

    random_error = round_sf(
        (energy / mass_kg) ** 0.5
    )

    unit = "m/s"

    question = (

        f"An object with mass "
        f"{mass_text} has kinetic "
        f"energy {energy}J. "
        f"What is its velocity?"
    )

    working = make_working_velocity(

        energy,

        round_sf(mass_kg),

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
                "You forgot to multiply "
                "by 2 before square rooting.",

            "working": working
        }
    ]

    return (
        question,
        correct_val,
        options_data,
        unit
    )


# =========================================================
# Random Question
# =========================================================
def generate_single_mcq_ke():

    generators = [

        generate_ke_question,

        generate_mass_question,

        generate_velocity_question
    ]

    question_func = random.choice(
        generators
    )

    return question_func()


# =========================================================
# Generate Quiz
# =========================================================
def generate_mcq_ke():

    questions = []

    for _ in range(5):

        raw_question = (
            generate_single_mcq_ke()
        )

        formatted_question = format_mcq(
            *raw_question
        )

        questions.append(
            formatted_question
        )

    return questions
