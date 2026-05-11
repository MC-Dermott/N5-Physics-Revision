import random
from utils.mcq_utils import format_mcq

g = 9.8


# =========================================================
# SCENARIO GENERATOR
# =========================================================
def generate_projectile_scenario():

    v = random.randint(2, 15)

    t_mult = random.choice([x for x in range(1, 16) if x != 10])
    t = round(t_mult * 0.1, 1)

    return {
        "u_x": v,
        "t": t,
        "range": round(v * t, 2),
        "v_y": round(g * t, 2),
        "height": round(0.5 * g * t**2, 2)
    }


# =========================================================
# WORKING HELPERS
# =========================================================
def range_working(v, t, answer):

    return [
        {"type": "text", "content": "Horizontal motion: velocity is constant"},
        {"type": "latex", "content": r"R = v_x t"},
        {"type": "latex", "content": rf"R = {v} \times {t}"},
        {"type": "latex", "content": rf"R = {answer}\ \mathrm{{m}}"}
    ]


def vertical_velocity_working(t, answer):

    return [
        {"type": "text", "content": "Vertical motion under gravity"},
        {"type": "latex", "content": r"v_y = gt"},
        {"type": "latex", "content": rf"v_y = 9.8 \times {t}"},
        {"type": "latex", "content": rf"v_y = {answer}\ \mathrm{{m/s}}"}
    ]


def height_working(t, answer):

    return [
        {"type": "text", "content": "Use SUVAT equation for vertical motion"},
        {"type": "latex", "content": r"s = \frac{1}{2}gt^2"},
        {"type": "latex", "content": rf"s = 0.5 \times 9.8 \times {t}^2"},
        {"type": "latex", "content": rf"s = {answer}\ \mathrm{{m}}"}
    ]


# =========================================================
# QUESTIONS
# =========================================================
def generate_mcq_range(s):

    correct = s["range"]

    question = (
        f"A projectile is fired horizontally at {s['u_x']} m/s. "
        f"It takes {s['t']} s to hit the ground. What is the range?"
    )

    working = range_working(s["u_x"], s["t"], correct)

    return format_mcq(
        question,
        correct,
        [
            {
                "value": correct,
                "summary": "Correct! You used R = vt.",
                "mistake": None,
                "working": working
            },
            {
                "value": round(s["u_x"] * g, 2),
                "summary": "Incorrect.",
                "mistake": "You used gravity instead of time.",
                "working": working
            },
            {
                "value": s["t"],
                "summary": "Incorrect.",
                "mistake": "This is time, not distance.",
                "working": working
            },
            {
                "value": round(s["u_x"] + s["t"], 2),
                "summary": "Incorrect.",
                "mistake": "You added instead of multiplying.",
                "working": working
            }
        ],
        "m"
    )


def generate_mcq_vertical_velocity(s):

    correct = s["v_y"]

    question = (
        f"What is the vertical velocity after {s['t']} s?"
    )

    working = vertical_velocity_working(s["t"], correct)

    return format_mcq(
        question,
        correct,
        [
            {
                "value": correct,
                "summary": "Correct! You used v = gt.",
                "mistake": None,
                "working": working
            },
            {
                "value": s["u_x"],
                "summary": "Incorrect.",
                "mistake": "This is horizontal velocity.",
                "working": working
            },
            {
                "value": g,
                "summary": "Incorrect.",
                "mistake": "This is acceleration, not velocity.",
                "working": working
            },
            {
                "value": s["range"],
                "summary": "Incorrect.",
                "mistake": "This is horizontal distance.",
                "working": working
            }
        ],
        "m/s"
    )


def generate_mcq_height(s):

    correct = s["height"]

    question = (
        f"What height did the projectile fall from (t = {s['t']} s)?"
    )

    working = height_working(s["t"], correct)

    return format_mcq(
        question,
        correct,
        [
            {
                "value": correct,
                "summary": "Correct! You used s = 1/2 gt².",
                "mistake": None,
                "working": working
            },
            {
                "value": round(s["v_y"] * s["t"], 2),
                "summary": "Incorrect.",
                "mistake": "You forgot the 1/2 factor.",
                "working": working
            },
            {
                "value": s["range"],
                "summary": "Incorrect.",
                "mistake": "This is horizontal motion.",
                "working": working
            },
            {
                "value": round(g * s["t"]**2, 2),
                "summary": "Incorrect.",
                "mistake": "You missed the 1/2 factor.",
                "working": working
            }
        ],
        "m"
    )


# =========================================================
# SCENARIO SET (3 QUESTIONS LINKED)
# =========================================================
def generate_projectile_mcq_set():

    scenario = generate_projectile_scenario()

    return [
        generate_mcq_range(scenario),
        generate_mcq_vertical_velocity(scenario),
        generate_mcq_height(scenario)
    ]


# =========================================================
# FINAL OUTPUT (5 SCENARIOS)
# =========================================================
def generate_projectile_mcqs():

    return [generate_projectile_mcq_set() for _ in range(5)]
