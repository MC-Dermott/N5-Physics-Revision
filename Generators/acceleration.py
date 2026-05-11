import random

from utils.mcq_utils import format_mcq


# =========================================================
# Helper Functions
# =========================================================
def make_working_acceleration(force, mass, answer):

    return [

        {
            "type": "text",
            "content": "Use Newton's Second Law:"
        },

        {
            "type": "latex",
            "content": r"a = \frac{F}{m}"
        },

        {
            "type": "latex",
            "content": rf"a = \frac{{{force}}}{{{mass}}}"
        },

        {
            "type": "latex",
            "content": rf"a = {answer}\ \mathrm{{m/s^2}}"
        }
    ]


def make_working_mass(force, accel, answer):

    return [

        {
            "type": "text",
            "content": "Rearrange Newton's Second Law:"
        },

        {
            "type": "latex",
            "content": r"m = \frac{F}{a}"
        },

        {
            "type": "latex",
            "content": rf"m = \frac{{{force}}}{{{accel}}}"
        },

        {
            "type": "latex",
            "content": rf"m = {answer}\ \mathrm{{kg}}"
        }
    ]


def make_working_force(mass, accel, answer):

    return [

        {
            "type": "text",
            "content": "Use Newton's Second Law:"
        },

        {
            "type": "latex",
            "content": r"F = ma"
        },

        {
            "type": "latex",
            "content": rf"F = {mass} \times {accel}"
        },

        {
            "type": "latex",
            "content": rf"F = {answer}\ \mathrm{{N}}"
        }
    ]


# =========================================================
# Acceleration Question
# =========================================================
def generate_acceleration_question():

    mass = random.randint(2, 10)

    force = random.randint(10, 50)

    correct_val = round(force / mass, 2)

    unit = "m/s²"

    question = (
        f"What is the acceleration of a "
        f"{mass}kg object if {force}N "
        f"of force is applied?"
    )

    working = make_working_acceleration(
        force,
        mass,
        correct_val
    )

    options_data = [

        {
            "value": correct_val,

            "summary":
                "Correct! You used Newton's Second Law.",

            "mistake": None,

            "working": working
        },

        {
            "value": force * mass,

            "summary":
                "Incorrect.",

            "mistake":
                "You multiplied force and mass "
                "instead of dividing.",

            "working": working
        },

        {
            "value": force + mass,

            "summary":
                "Incorrect.",

            "mistake":
                "You added the values instead of "
                "using the formula.",

            "working": working
        },

        {
            "value": round(mass / force, 2),

            "summary":
                "Incorrect.",

            "mistake":
                "You inverted the formula.",

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

    accel = random.randint(2, 5)

    force = random.randint(10, 50)

    correct_val = round(force / accel, 2)

    unit = "kg"

    question = (
        f"What is the mass of an object "
        f"accelerating at {accel}m/s² "
        f"if {force}N of force is applied?"
    )

    working = make_working_mass(
        force,
        accel,
        correct_val
    )

    options_data = [

        {
            "value": correct_val,

            "summary":
                "Correct! You rearranged the formula correctly.",

            "mistake": None,

            "working": working
        },

        {
            "value": force * accel,

            "summary":
                "Incorrect.",

            "mistake":
                "You multiplied instead of dividing.",

            "working": working
        },

        {
            "value": force + accel,

            "summary":
                "Incorrect.",

            "mistake":
                "You added the values instead of "
                "using the formula.",

            "working": working
        },

        {
            "value": round(accel / force, 2),

            "summary":
                "Incorrect.",

            "mistake":
                "You inverted the formula.",

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

    mass = random.randint(2, 10)

    accel = random.randint(2, 5)

    correct_val = mass * accel

    unit = "N"

    question = (
        f"What is the force on a "
        f"{mass}kg object accelerating "
        f"at {accel}m/s²?"
    )

    working = make_working_force(
        mass,
        accel,
        correct_val
    )

    options_data = [

        {
            "value": correct_val,

            "summary":
                "Correct! You used F = ma.",

            "mistake": None,

            "working": working
        },

        {
            "value": mass + accel,

            "summary":
                "Incorrect.",

            "mistake":
                "You added the values instead "
                "of multiplying.",

            "working": working
        },

        {
            "value": mass * (accel + 1),

            "summary":
                "Incorrect.",

            "mistake":
                "You used the equation incorrectly.",

            "working": working
        },

        {
            "value": round(mass / accel, 2),

            "summary":
                "Incorrect.",

            "mistake":
                "You divided instead of multiplying.",

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
def generate_single_mcq_acc():

    generators = [

        generate_force_question,

        generate_acceleration_question,

        generate_mass_question
    ]

    question_func = random.choice(generators)

    return question_func()


# =========================================================
# Generate Quiz
# =========================================================
def generate_mcq_acc():

    questions = []

    for _ in range(5):

        raw_question = generate_single_mcq_acc()

        formatted_question = format_mcq(
            *raw_question
        )

        questions.append(
            formatted_question
        )

    return questions
