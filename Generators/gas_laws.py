import random
from utils.mcq_utils import format_mcq


# =========================================================
# HELPERS
# =========================================================
volume_units = ["cm³", "mm³", "mL", "L"]
pressure_unit = "kPa"


def c_to_k(c):
    return c + 273


def random_volume():

    unit = random.choice(volume_units)

    if unit == "L":
        value = random.randint(1, 50)

    elif unit == "mL":
        value = random.randint(50, 500)

    elif unit == "cm³":
        value = random.randint(50, 500)

    else:  # mm³
        value = random.randint(100, 500)

    return value, unit


# =========================================================
# WORKING
# =========================================================
def boyles_working(s, answer):

    return [
        {"type": "latex", "content": r"P_1V_1=P_2V_2"},

        {
            "type": "latex",
            "content": rf"{s['p1']} \times {s['v1']} = {s['p2']} \times V_2"
        },

        {
            "type": "latex",
            "content": rf"V_2 = \frac{{{s['p1']} \times {s['v1']}}}{{{s['p2']}}}"
        },

        {
            "type": "latex",
            "content": rf"V_2 = {answer}\ {s['unit']}"
        }
    ]


def charles_working(s, answer):

    return [
        {"type": "text", "content": "Convert temperatures to kelvin first."},

        {
            "type": "latex",
            "content": rf"T_1 = {s['t1_c']} + 273 = {s['t1_k']}\ \mathrm{{K}}"
        },

        {
            "type": "latex",
            "content": rf"T_2 = {s['t2_c']} + 273 = {s['t2_k']}\ \mathrm{{K}}"
        },

        {
            "type": "latex",
            "content": r"\frac{V_1}{T_1}=\frac{V_2}{T_2}"
        },

        {
            "type": "latex",
            "content": rf"\frac{{{s['v1']}}}{{{s['t1_k']}}}=\frac{{V_2}}{{{s['t2_k']}}}"
        },

        {
            "type": "latex",
            "content": rf"V_2 = {answer}\ {s['unit']}"
        }
    ]


def gaylussac_working(s, answer):

    return [
        {"type": "text", "content": "Convert temperatures to kelvin first."},

        {
            "type": "latex",
            "content": rf"T_1 = {s['t1_c']} + 273 = {s['t1_k']}\ \mathrm{{K}}"
        },

        {
            "type": "latex",
            "content": rf"T_2 = {s['t2_c']} + 273 = {s['t2_k']}\ \mathrm{{K}}"
        },

        {
            "type": "latex",
            "content": r"\frac{P_1}{T_1}=\frac{P_2}{T_2}"
        },

        {
            "type": "latex",
            "content": rf"\frac{{{s['p1']}}}{{{s['t1_k']}}}=\frac{{P_2}}{{{s['t2_k']}}}"
        },

        {
            "type": "latex",
            "content": rf"P_2 = {answer}\ \mathrm{{kPa}}"
        }
    ]


# =========================================================
# BOYLE'S LAW
# =========================================================
def generate_boyles_mcq():

    while True:

        p1 = random.randint(50, 180)

        multiplier = random.choice([2, 3, 4])

        p2 = p1 * multiplier

        if p2 <= 200:

            v1, unit = random_volume()

            v2 = int((p1 * v1) / p2)

            if 1 <= v2 <= 500:
                break

    question = (
        f"A gas has a volume of {v1} {unit} "
        f"at a pressure of {p1} kPa. "
        f"If the pressure changes to {p2} kPa "
        f"at constant temperature, what is the new volume?"
    )

    working = boyles_working(
        {
            "p1": p1,
            "v1": v1,
            "p2": p2,
            "unit": unit
        },
        v2
    )

    return format_mcq(
        question,
        v2,
        [
            {
                "value": v2,
                "summary": "Correct!",
                "mistake": None,
                "working": working
            },

            {
                "value": int(v1 * p2 / p1),
                "summary": "Incorrect.",
                "mistake": "You rearranged Boyle's Law incorrectly.",
                "working": working
            },

            {
                "value": p1,
                "summary": "Incorrect.",
                "mistake": "You used pressure as the answer.",
                "working": working
            },

            {
                "value": v1,
                "summary": "Incorrect.",
                "mistake": "The volume changes when pressure changes.",
                "working": working
            }
        ],
        unit
    )


# =========================================================
# CHARLES' LAW
# =========================================================
def generate_charles_mcq():

    while True:

        v1, unit = random_volume()

        t1_c = random.randint(0, 50)
        t2_c = random.randint(60, 200)

        t1_k = c_to_k(t1_c)
        t2_k = c_to_k(t2_c)

        v2 = int(v1 * t2_k / t1_k)

        if 1 <= v2 <= 500:
            break

    wrong_no_kelvin = (
        int(v1 * t2_c / t1_c)
        if t1_c != 0
        else v2 + 50
    )

    wrong_subtract = abs(
        int(v1 * (t2_c - 273) / (t1_c - 273))
    )

    wrong_rearrange = int(v1 * t1_k / t2_k)

    question = (
        f"A gas occupies {v1} {unit} at {t1_c}°C. "
        f"If the temperature increases to {t2_c}°C "
        f"at constant pressure, what is the new volume?"
    )

    working = charles_working(
        {
            "v1": v1,
            "t1_c": t1_c,
            "t2_c": t2_c,
            "t1_k": t1_k,
            "t2_k": t2_k,
            "unit": unit
        },
        v2
    )

    return format_mcq(
        question,
        v2,
        [
            {
                "value": v2,
                "summary": "Correct!",
                "mistake": None,
                "working": working
            },

            {
                "value": wrong_no_kelvin,
                "summary": "Incorrect.",
                "mistake": "You forgot to convert Celsius to kelvin.",
                "working": working
            },

            {
                "value": wrong_subtract,
                "summary": "Incorrect.",
                "mistake": "You subtracted 273 instead of adding it.",
                "working": working
            },

            {
                "value": wrong_rearrange,
                "summary": "Incorrect.",
                "mistake": "You rearranged Charles' Law incorrectly.",
                "working": working
            }
        ],
        unit
    )


# =========================================================
# GAY-LUSSAC'S LAW
# =========================================================
def generate_gaylussac_mcq():

    while True:

        p1 = random.randint(50, 150)

        t1_c = random.randint(0, 50)
        t2_c = random.randint(60, 200)

        t1_k = c_to_k(t1_c)
        t2_k = c_to_k(t2_c)

        p2 = int(p1 * t2_k / t1_k)

        if 1 <= p2 <= 200:
            break

    wrong_no_kelvin = (
        int(p1 * t2_c / t1_c)
        if t1_c != 0
        else p2 + 20
    )

    wrong_subtract = abs(
        int(p1 * (t2_c - 273) / (t1_c - 273))
    )

    wrong_rearrange = int(p1 * t1_k / t2_k)

    question = (
        f"A gas is at a pressure of {p1} kPa at {t1_c}°C. "
        f"If the temperature increases to {t2_c}°C "
        f"at constant volume, what is the new pressure?"
    )

    working = gaylussac_working(
        {
            "p1": p1,
            "t1_c": t1_c,
            "t2_c": t2_c,
            "t1_k": t1_k,
            "t2_k": t2_k
        },
        p2
    )

    return format_mcq(
        question,
        p2,
        [
            {
                "value": p2,
                "summary": "Correct!",
                "mistake": None,
                "working": working
            },

            {
                "value": wrong_no_kelvin,
                "summary": "Incorrect.",
                "mistake": "You forgot to convert Celsius to kelvin.",
                "working": working
            },

            {
                "value": wrong_subtract,
                "summary": "Incorrect.",
                "mistake": "You subtracted 273 instead of adding it.",
                "working": working
            },

            {
                "value": wrong_rearrange,
                "summary": "Incorrect.",
                "mistake": "You rearranged Gay-Lussac's Law incorrectly.",
                "working": working
            }
        ],
        "kPa"
    )


# =========================================================
# RANDOM MIXED QUIZ
# =========================================================
question_generators = [
    generate_boyles_mcq,
    generate_charles_mcq,
    generate_gaylussac_mcq
]


def generate_gas_law_mcqs():

    return [
        random.choice(question_generators)()
        for _ in range(5)
    ]
