import random
from utils.mcq_utils import format_mcq


# =========================================================
# WORKING HELPERS
# =========================================================
def current_working(charge, time_val, time_sec, answer):

    return [

        {
            "type": "text",
            "content": "Use the equation:"
        },

        {
            "type": "latex",
            "content": r"I = \frac{Q}{t}"
        },

        {
            "type": "latex",
            "content": rf"I = \frac{{{charge}}}{{{time_sec}}}"
        },

        {
            "type": "latex",
            "content": rf"I = {answer}\ \mathrm{{A}}"
        }
    ]


def charge_working(current, time_val, time_sec, answer):

    return [

        {
            "type": "text",
            "content": "Use the equation:"
        },

        {
            "type": "latex",
            "content": r"Q = It"
        },

        {
            "type": "latex",
            "content": rf"Q = {current} \times {time_sec}"
        },

        {
            "type": "latex",
            "content": rf"Q = {answer}\ \mathrm{{C}}"
        }
    ]


def time_working(charge, current, answer):

    return [

        {
            "type": "text",
            "content": "Rearrange the equation:"
        },

        {
            "type": "latex",
            "content": r"t = \frac{Q}{I}"
        },

        {
            "type": "latex",
            "content": rf"t = \frac{{{charge}}}{{{current}}}"
        },

        {
            "type": "latex",
            "content": rf"t = {answer}\ \mathrm{{s}}"
        }
    ]


# =========================================================
# CURRENT QUESTION
# =========================================================
def generate_current_question():

    charge = random.randint(10, 100)
    unit = "A"

    use_minutes = random.choice([True, False])

    if use_minutes:
        time_val = random.randint(1, 10)
        time_sec = time_val * 60
        time_label = "minutes"
    else:
        time_val = random.randint(5, 60)
        time_sec = time_val
        time_label = "seconds"

    correct_val = round(charge / time_sec, 2)

    conversion_distractor = round(charge / time_val, 2)

    question = (
        f"What is the current flowing if "
        f"{charge} Coulombs of charge passes in "
        f"{time_val} {time_label}?"
    )

    working = current_working(
        charge,
        time_val,
        time_sec,
        correct_val
    )

    options_data = [

        {
            "value": correct_val,
            "summary": "Correct! You used I = Q / t.",
            "mistake": None,
            "working": working
        },

        {
            "value": charge * time_sec,
            "summary": "Incorrect.",
            "mistake": "You multiplied instead of dividing.",
            "working": working
        },

        {
            "value": round(time_sec / charge, 2),
            "summary": "Incorrect.",
            "mistake": "You inverted the formula.",
            "working": working
        },

        {
            "value": conversion_distractor,
            "summary": "Incorrect.",
            "mistake": "You did not convert time into seconds.",
            "working": working
        }
    ]

    return question, correct_val, options_data, unit


# =========================================================
# CHARGE QUESTION
# =========================================================
def generate_charge_question():

    current = random.randint(1, 10)
    unit = "C"

    use_minutes = random.choice([True, False])

    if use_minutes:
        time_val = random.randint(1, 10)
        time_sec = time_val * 60
        time_label = "minutes"
    else:
        time_val = random.randint(5, 60)
        time_sec = time_val
        time_label = "seconds"

    correct_val = round(current * time_sec, 2)

    conversion_distractor = round(current * time_val, 2)

    question = (
        f"What is the total charge transferred if "
        f"a current of {current} A flows for "
        f"{time_val} {time_label}?"
    )

    working = charge_working(
        current,
        time_val,
        time_sec,
        correct_val
    )

    options_data = [

        {
            "value": correct_val,
            "summary": "Correct! You used Q = I × t.",
            "mistake": None,
            "working": working
        },

        {
            "value": round(current / time_sec, 2),
            "summary": "Incorrect.",
            "mistake": "You used division instead of multiplication.",
            "working": working
        },

        {
            "value": round(time_sec / current, 2),
            "summary": "Incorrect.",
            "mistake": "You rearranged the equation incorrectly.",
            "working": working
        },

        {
            "value": conversion_distractor,
            "summary": "Incorrect.",
            "mistake": "You forgot to convert time to seconds.",
            "working": working
        }
    ]

    return question, correct_val, options_data, unit


# =========================================================
# TIME QUESTION
# =========================================================
def generate_time_question():

    charge = random.randint(10, 100)
    current = random.randint(1, 10)

    correct_val = round(charge / current, 2)

    unit = "s"

    conversion_distractor = round((charge / current) / 60, 2)

    question = (
        f"For how long must a current of {current} A "
        f"flow to transfer {charge} Coulombs?"
    )

    working = time_working(
        charge,
        current,
        correct_val
    )

    options_data = [

        {
            "value": correct_val,
            "summary": "Correct! You used t = Q / I.",
            "mistake": None,
            "working": working
        },

        {
            "value": charge * current,
            "summary": "Incorrect.",
            "mistake": "You multiplied instead of dividing.",
            "working": working
        },

        {
            "value": round(current / charge, 2),
            "summary": "Incorrect.",
            "mistake": "You inverted the formula.",
            "working": working
        },

        {
            "value": conversion_distractor,
            "summary": "Incorrect.",
            "mistake": "You converted seconds into minutes incorrectly.",
            "working": working
        }
    ]

    return question, correct_val, options_data, unit


# =========================================================
# RANDOM QUESTION
# =========================================================
def generate_single_mcq_current():

    generators = [
        generate_time_question,
        generate_charge_question,
        generate_current_question
    ]

    return random.choice(generators)()


# =========================================================
# QUIZ GENERATOR
# =========================================================
def generate_mcq_current():

    questions = []

    for _ in range(5):

        raw_question = generate_single_mcq_current()

        formatted = format_mcq(*raw_question)

        questions.append(formatted)

    return questions
