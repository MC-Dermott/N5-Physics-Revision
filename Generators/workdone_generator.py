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
def make_working_workdone(
    force,
    distance,
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
                r"W = Fd"
        },

        {
            "type": "latex",
            "content":
                rf"W = {force} \times {distance}"
        },

        {
            "type": "latex",
            "content":
                rf"W = {answer}\ \mathrm{{J}}"
        }
    ]


def make_working_force(
    workdone,
    distance,
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
                r"F = \frac{W}{d}"
        },

        {
            "type": "latex",
            "content":
                rf"F = \frac{{{workdone}}}{{{distance}}}"
        },

        {
            "type": "latex",
            "content":
                rf"F = {answer}\ \mathrm{{N}}"
        }
    ]


def make_working_distance(
    workdone,
    force,
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
                r"d = \frac{W}{F}"
        },

        {
            "type": "latex",
            "content":
                rf"d = \frac{{{workdone}}}{{{force}}}"
        },

        {
            "type": "latex",
            "content":
                rf"d = {answer}\ \mathrm{{m}}"
        }
    ]


# =========================================================
# Value Generators
# =========================================================
def generate_force():

    return random.choice(
        range(5, 105, 5)
    )


def generate_distance():

    return random.randint(
        2,
        50
    )


def generate_workdone():

    return random.choice(
        range(50, 5001, 50)
    )


# =========================================================
# Work Done Question
# =========================================================
def generate_workdone_question():

    force = generate_force()

    distance = generate_distance()

    correct_val = round_sf(
        force * distance
    )

    rearranged_answer = round_sf(
        force / distance
    )

    random_error = round_sf(
        force + distance
    )

    missing_multiplication = round_sf(
        distance / force
    )

    unit = "J"

    question = (

        f"What is the work done when "
        f"a force of {force}N moves "
        f"an object {distance}m?"
    )

    working = make_working_workdone(

        force,

        distance,

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
            "value": random_error,

            "summary":
                "Incorrect.",

            "mistake":
                "You added instead "
                "of multiplying.",

            "working": working
        },

        {
            "value": missing_multiplication,

            "summary":
                "Incorrect.",

            "mistake":
                "You divided instead "
                "of multiplying.",

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
# Force Question
# =========================================================
def generate_force_question():

    workdone = generate_workdone()

    distance = generate_distance()

    correct_val = round_sf(
        workdone / distance
    )

    rearranged_answer = round_sf(
        workdone * distance
    )

    random_error = round_sf(
        workdone + distance
    )

    missing_division = round_sf(
        distance / workdone
    )

    unit = "N"

    question = (

        f"What force is needed to do "
        f"{workdone}J of work over "
        f"a distance of {distance}m?"
    )

    working = make_working_force(

        workdone,

        distance,

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
            "value": random_error,

            "summary":
                "Incorrect.",

            "mistake":
                "You added instead "
                "of dividing.",

            "working": working
        },

        {
            "value": missing_division,

            "summary":
                "Incorrect.",

            "mistake":
                "You divided the wrong "
                "way around.",

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
# Distance Question
# =========================================================
def generate_distance_question():

    workdone = generate_workdone()

    force = generate_force()

    correct_val = round_sf(
        workdone / force
    )

    rearranged_answer = round_sf(
        workdone * force
    )

    random_error = round_sf(
        workdone + force
    )

    missing_division = round_sf(
        force / workdone
    )

    unit = "m"

    question = (

        f"How far does an object move "
        f"if {workdone}J of work is done "
        f"using a force of {force}N?"
    )

    working = make_working_distance(

        workdone,

        force,

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
            "value": random_error,

            "summary":
                "Incorrect.",

            "mistake":
                "You added instead "
                "of dividing.",

            "working": working
        },

        {
            "value": missing_division,

            "summary":
                "Incorrect.",

            "mistake":
                "You divided the wrong "
                "way around.",

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
def generate_single_mcq_workdone():

    generators = [

        generate_workdone_question,

        generate_force_question,

        generate_distance_question
    ]

    question_func = random.choice(
        generators
    )

    return question_func()


# =========================================================
# Generate Quiz
# =========================================================
def generate_mcq_workdone():

    questions = []

    for _ in range(5):

        raw_question = (
            generate_single_mcq_workdone()
        )

        formatted_question = format_mcq(
            *raw_question
        )

        questions.append(
            formatted_question
        )

    return questions
