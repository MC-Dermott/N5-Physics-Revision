import random
import math
from utils.mcq_utils import format_mcq


# =========================================================
# VECTOR GENERATION (N/S + E/W COMBINATIONS)
# =========================================================
def generate_vector_components():

    vertical_dir = random.choice(["N", "S"])
    horizontal_dir = random.choice(["E", "W"])

    north_mag = random.randint(3, 20)
    east_mag = random.randint(3, 20)

    north = north_mag if vertical_dir == "N" else -north_mag
    east = east_mag if horizontal_dir == "E" else -east_mag

    return east, north, vertical_dir, horizontal_dir


# =========================================================
# MAGNITUDE WORKING
# =========================================================
def magnitude_working(east, north, answer):

    return [
        {"type": "text", "content": "Use Pythagoras' theorem:"},
        {"type": "latex", "content": r"R = \sqrt{x^2 + y^2}"},
        {"type": "latex", "content": rf"R = \sqrt{{{east}^2 + {north}^2}}"},
        {"type": "latex", "content": rf"R = {answer}\ \mathrm{{km}}"}
    ]


# =========================================================
# BEARING WORKING (NO INTRO LINE)
# =========================================================
def bearing_working(east, north, angle, bearing):

    return [

        {
            "type": "latex",
            "content": rf"\theta = \tan^{{-1}}\left(\frac{{{abs(east)}}}{{{abs(north)}}}\right)"
        },

        {
            "type": "latex",
            "content": rf"\theta = {angle}^\circ"
        },

        {
            "type": "text",
            "content": "Apply quadrant rule:"
        },

        {
            "type": "text",
            "content": "Q1: θ, Q2: 180 − θ, Q3: 180 + θ, Q4: 360 − θ"
        },

        {
            "type": "latex",
            "content": rf"\text{{Bearing}} = {bearing}"
        }
    ]

# =========================================================
# MAGNITUDE QUESTION
# =========================================================
def generate_magnitude_question(east, north):

    correct_val = round(math.sqrt(east**2 + north**2), 2)

    question = (
        f"A boat travels {abs(north)} km "
        f"{'north' if north > 0 else 'south'} and "
        f"{abs(east)} km "
        f"{'east' if east > 0 else 'west'}.\n\n"
        "What is the magnitude of the resultant displacement?"
    )

    working = magnitude_working(east, north, correct_val)

    options_data = [

        {
            "value": correct_val,
            "summary": "Correct! You used Pythagoras' theorem.",
            "mistake": None,
            "working": working
        },

        {
            "value": abs(east + north),
            "summary": "Incorrect.",
            "mistake": "You added components instead of using Pythagoras.",
            "working": working
        },

        {
            "value": abs(east - north),
            "summary": "Incorrect.",
            "mistake": "You subtracted components instead of using Pythagoras.",
            "working": working
        },

        {
            "value": round(east**2 + north**2, 2),
            "summary": "Incorrect.",
            "mistake": "You forgot to square root the result.",
            "working": working
        }
    ]

    return question, correct_val, options_data, "km"


# =========================================================
# BEARING QUESTION
# =========================================================
def generate_bearing_question(east, north):

    angle = round(math.degrees(math.atan(abs(east) / abs(north))), 1)

    # Determine quadrant and apply rule
    if north > 0 and east > 0:
        bearing = angle
    elif north > 0 and east < 0:
        bearing = 360 - angle
    elif north < 0 and east < 0:
        bearing = 180 + angle
    else:
        bearing = 180 - angle

    bearing = round(bearing, 0)

    # format with leading zero if needed
    bearing_display = f"{int(bearing):03d}"

    question = (
        f"A boat travels {abs(north)} km "
        f"{'north' if north > 0 else 'south'} and "
        f"{abs(east)} km "
        f"{'east' if east > 0 else 'west'}.\n\n"
        "What is the bearing of the resultant displacement?"
    )

    working = bearing_working(east, north, angle, bearing_display)

    # =====================================================
    # DISTRACTORS (OTHER QUADRANT RULES)
    # =====================================================
    distractors = [
        round(angle, 0),
        round(180 - angle, 0),
        round(180 + angle, 0),
        round(360 - angle, 0)
    ]

    distractors = [d for d in distractors if d != round(bearing, 0)]
    distractors = distractors[:3]

    options_data = [

        {
            "value": bearing,
            "summary": "Correct bearing using correct quadrant rule.",
            "mistake": None,
            "working": working
        }
    ]

    for d in distractors:

        options_data.append({

            "value": d,
            "summary": "Incorrect.",
            "mistake": "Wrong quadrant rule applied.",
            "working": working
        })

    return question, bearing, options_data, "°"


# =========================================================
# VECTOR SCENARIO (PAIRED QUESTIONS)
# =========================================================
def generate_vector_scenario():

    east, north, v_dir, h_dir = generate_vector_components()

    magnitude_q = format_mcq(
        *generate_magnitude_question(east, north)
    )

    bearing_q = format_mcq(
        *generate_bearing_question(east, north)
    )

    return [
        magnitude_q,
        bearing_q
    ]


# =========================================================
# QUIZ GENERATOR
# =========================================================
def generate_mcq_vectors():

    return [
        generate_vector_scenario()
        for _ in range(5)
    ]
