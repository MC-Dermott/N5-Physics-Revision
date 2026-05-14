import random

from utils.mcq_utils import format_mcq


# =========================================================
# Helper Function
# =========================================================
def round_sf(value, sf=3):
    """Round to significant figures."""
    return float(f"{value:.{sf}g}")


# =========================================================
# Gravitational Field Strengths
# =========================================================
GRAVITY_LOCATIONS = {
    "Mercury": 3.70,
    "Venus": 8.87,
    "Earth": 9.81,
    "Moon": 1.62,
    "Mars": 3.71,
    "Jupiter": 24.8,
    "Saturn": 10.4,
    "Uranus": 8.69,
    "Neptune": 11.2
}


def choose_location():
    """Return random location and g value."""

    location = random.choice(
        list(GRAVITY_LOCATIONS.keys())
    )

    return (
        location,
        GRAVITY_LOCATIONS[location]
    )


def choose_wrong_gravity(correct_location):
    """Choose incorrect g value."""

    other_locations = [

        loc for loc in GRAVITY_LOCATIONS

        if loc != correct_location
    ]

    wrong_location = random.choice(
        other_locations
    )

    return (
        wrong_location,
        GRAVITY_LOCATIONS[wrong_location]
    )


# =========================================================
# Working Functions
# =========================================================
def make_working_weight(
    mass_kg,
    gravity,
    answer
):

    return [

        {
            "type": "text",
            "content": "Use the equation:"
        },

        {
            "type": "latex",
            "content": r"W = mg"
        },

        {
            "type": "latex",
            "content":
                rf"W = {mass_kg} \times {gravity}"
        },

        {
            "type": "latex",
            "content":
                rf"W = {answer}\ \mathrm{{N}}"
        }
    ]


def make_working_mass(
    weight,
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
                r"m = \frac{W}{g}"
        },

        {
            "type": "latex",
            "content":
                rf"m = \frac{{{weight}}}{{{gravity}}}"
        },

        {
            "type": "latex",
            "content":
                rf"m = {answer}\ \mathrm{{kg}}"
        }
    ]


def make_working_gravity(
    weight,
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
                r"g = \frac{W}{m}"
        },

        {
            "type": "latex",
            "content":
                rf"g = \frac{{{weight}}}{{{mass}}}"
        },

        {
            "type": "latex",
            "content":
                rf"g = {answer}\ \mathrm{{N/kg}}"
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

    # kg values
    if random.choice([True, False]):

        mass = random.choice(
            range(10, 151, 10)
        )

        return mass, mass, False

    # gram values
    mass_g = random.choice(
        range(100, 5100, 100)
    )

    mass_kg = mass_g / 1000

    return mass_g, mass_kg, True


def generate_weight():

    return random.choice(
        range(10, 501, 10)
    )


# =========================================================
# Weight Question
# =========================================================
def generate_weight_question():

    display_mass, mass_kg, is_grams = (
        generate_mass()
    )

    location, gravity = choose_location()

    correct_val = round_sf(
        mass_kg * gravity
    )

    wrong_location, wrong_g = (
        choose_wrong_gravity(location)
    )

    wrong_gravity_answer = round_sf(
        mass_kg * wrong_g
    )

    rearranged_answer = round_sf(
        mass_kg / gravity
    )

    if is_grams:

        grams_error = round_sf(
            display_mass * gravity
        )

        mass_text = (
            f"{display_mass}g"
        )

    else:

        grams_error = round_sf(
            display_mass + gravity
        )

        mass_text = (
            f"{display_mass}kg"
        )

    unit = "N"

    question = (

        f"What is the weight of a "
        f"{mass_text} object on "
        f"{location}?"
    )

    working = make_working_weight(

        round_sf(mass_kg),

        round_sf(gravity),

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
            "value": wrong_gravity_answer,

            "summary":
                "Incorrect.",

            "mistake":
                f"You used the gravitational "
                f"field strength for "
                f"{wrong_location}.",

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

    weight = generate_weight()

    location, gravity = choose_location()

    correct_val = round_sf(
        weight / gravity
    )

    wrong_location, wrong_g = (
        choose_wrong_gravity(location)
    )

    wrong_gravity_answer = round_sf(
        weight / wrong_g
    )

    rearranged_answer = round_sf(
        weight * gravity
    )

    grams_error = round_sf(
        (weight / gravity) * 1000
    )

    unit = "kg"

    question = (

        f"What is the mass of an "
        f"object with weight "
        f"{weight}N on "
        f"{location}?"
    )

    working = make_working_mass(

        weight,

        round_sf(gravity),

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
            "value": wrong_gravity_answer,

            "summary":
                "Incorrect.",

            "mistake":
                f"You used the gravitational "
                f"field strength for "
                f"{wrong_location}.",

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
        }
    ]

    return (
        question,
        correct_val,
        options_data,
        unit
    )


# =========================================================
# Gravity Question
# =========================================================
def generate_gravity_question():

    display_mass, mass_kg, is_grams = (
        generate_mass()
    )

    weight = generate_weight()

    correct_val = round_sf(
        weight / mass_kg
    )

    wrong_location, wrong_g = (
        choose_wrong_gravity("")
    )

    rearranged_answer = round_sf(
        weight * mass_kg
    )

    if is_grams:

        grams_error = round_sf(
            weight / display_mass
        )

        mass_text = (
            f"{display_mass}g"
        )

    else:

        grams_error = wrong_g

        mass_text = (
            f"{display_mass}kg"
        )

    unit = "N/kg"

    question = (

        f"What is the gravitational "
        f"field strength for an object "
        f"with weight {weight}N and "
        f"mass {mass_text}?"
    )

    working = make_working_gravity(

        weight,

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
            "value": wrong_g,

            "summary":
                "Incorrect.",

            "mistake":
                f"You selected the "
                f"gravitational field "
                f"strength for "
                f"{wrong_location}.",

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
def generate_single_mcq_wmg():

    generators = [

        generate_weight_question,

        generate_mass_question,

        generate_gravity_question
    ]

    question_func = random.choice(
        generators
    )

    return question_func()


# =========================================================
# Generate Quiz
# =========================================================
def generate_mcq_wmg():

    questions = []

    for _ in range(5):

        raw_question = (
            generate_single_mcq_wmg()
        )

        formatted_question = format_mcq(
            *raw_question
        )

        questions.append(
            formatted_question
        )

    return questions
