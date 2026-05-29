import random
from utils.mcq_utils import format_mcq

g = 9.8

CONTEXTS = {
    "bike": {
        "label": "bicycle and rider",
        "num_wheels": 2,
        "mass_options": list(range(70, 141, 10)),
        "area_options": [0.001, 0.002, 0.003],
    },
    "car": {
        "label": "car",
        "num_wheels": 4,
        "mass_options": list(range(1000, 2001, 100)),
        "area_options": [0.020, 0.025, 0.030, 0.040, 0.050],
    },
    "truck": {
        "label": "truck",
        "num_wheels": 6,
        "mass_options": list(range(5000, 20001, 1000)),
        "area_options": [0.050, 0.060, 0.070, 0.080, 0.100],
    },
}


# =========================================================
# WORKING BUILDERS
# =========================================================

def weight_working(mass, weight):

    return [
        {"type": "text", "content": "Use the equation for weight:"},
        {"type": "latex", "content": r"W = mg"},
        {"type": "latex", "content": rf"W = {mass} \times 9.8"},
        {"type": "latex", "content": rf"W = {weight}\ \mathrm{{N}}"},
    ]


def pressure_working(weight, num_wheels, area_per_tyre, total_area, pressure):

    return [
        {"type": "text", "content": f"Find the total contact area across all {num_wheels} tyres:"},
        {"type": "latex", "content": rf"A_{{total}} = {num_wheels} \times {area_per_tyre}"},
        {"type": "latex", "content": rf"A_{{total}} = {total_area}\ \mathrm{{m^2}}"},
        {"type": "text", "content": "Now apply the pressure equation:"},
        {"type": "latex", "content": r"P = \frac{F}{A}"},
        {"type": "latex", "content": rf"P = \frac{{{weight}}}{{{total_area}}}"},
        {"type": "latex", "content": rf"P = {pressure}\ \mathrm{{Pa}}"},
    ]


def area_working(weight, pressure, total_area):

    return [
        {"type": "text", "content": "Rearrange P = F/A to make A the subject:"},
        {"type": "latex", "content": r"A = \frac{F}{P}"},
        {"type": "latex", "content": rf"A = \frac{{{weight}}}{{{pressure}}}"},
        {"type": "latex", "content": rf"A = {total_area}\ \mathrm{{m^2}}"},
    ]


def area_per_tyre_working(weight, pressure, total_area, num_wheels, area_per_tyre):

    return [
        {"type": "text", "content": "First find the total contact area using P = F/A:"},
        {"type": "latex", "content": r"A_{total} = \frac{F}{P}"},
        {"type": "latex", "content": rf"A_{{total}} = \frac{{{weight}}}{{{pressure}}}"},
        {"type": "latex", "content": rf"A_{{total}} = {total_area}\ \mathrm{{m^2}}"},
        {"type": "text", "content": f"Now divide by the number of tyres ({num_wheels}):"},
        {"type": "latex", "content": rf"A_{{tyre}} = \frac{{{total_area}}}{{{num_wheels}}}"},
        {"type": "latex", "content": rf"A_{{tyre}} = {area_per_tyre}\ \mathrm{{m^2}}"},
    ]


def force_working(pressure, total_area, force):

    return [
        {"type": "text", "content": "Rearrange P = F/A to make F the subject:"},
        {"type": "latex", "content": r"F = P \times A"},
        {"type": "latex", "content": rf"F = {pressure} \times {total_area}"},
        {"type": "latex", "content": rf"F = {force}\ \mathrm{{N}}"},
    ]


# =========================================================
# MCQ BUILDERS
# =========================================================

def make_weight_mcq(label, mass, weight):

    working = weight_working(mass, weight)

    options_data = [
        {
            "value": weight,
            "summary": "Correct!",
            "mistake": None,
            "working": working
        },
        {
            "value": round(mass / 9.8, 1),
            "summary": "Incorrect.",
            "mistake": "You divided by g instead of multiplying. W = m × g.",
            "working": working
        },
        {
            "value": float(mass * 10),
            "summary": "Incorrect.",
            "mistake": "You used g = 10 N/kg. The correct value is g = 9.8 N/kg.",
            "working": working
        },
        {
            "value": float(mass),
            "summary": "Incorrect.",
            "mistake": "You gave the mass in kg, not the weight in N. Weight = mass × g.",
            "working": working
        },
    ]

    question = (
        f"A {label} has a total mass of {mass} kg.\n\n"
        f"g = 9.8 N/kg\n\n"
        f"Calculate the weight of the {label}."
    )

    return format_mcq(question, weight, options_data, "N")


def make_pressure_mcq(label, num_wheels, weight, area_per_tyre, total_area, pressure):

    working = pressure_working(weight, num_wheels, area_per_tyre, total_area, pressure)

    options_data = [
        {
            "value": pressure,
            "summary": "Correct!",
            "mistake": None,
            "working": working
        },
        {
            "value": round(weight / area_per_tyre),
            "summary": "Incorrect.",
            "mistake": (
                f"You used the area of one tyre, not the total. "
                f"Total contact area = {num_wheels} × {area_per_tyre} = {total_area} m²."
            ),
            "working": working
        },
        {
            "value": round(pressure / num_wheels),
            "summary": "Incorrect.",
            "mistake": f"You divided by the number of wheels ({num_wheels}) as well as the total area. P = F ÷ A_total only.",
            "working": working
        },
        {
            "value": round(weight / (total_area + area_per_tyre)),
            "summary": "Incorrect.",
            "mistake": f"Check your total contact area. The {label} has {num_wheels} tyres, each {area_per_tyre} m².",
            "working": working
        },
    ]

    question = (
        f"The {label} has {num_wheels} tyres, each with a contact area of {area_per_tyre} m² with the ground.\n\n"
        f"Using your answer to part 1, calculate the pressure exerted by the {label} on the ground."
    )

    return format_mcq(question, pressure, options_data, "Pa")


def make_total_area_mcq(label, num_wheels, weight, pressure, total_area, area_per_tyre):

    working = area_working(weight, pressure, total_area)

    options_data = [
        {
            "value": total_area,
            "summary": "Correct!",
            "mistake": None,
            "working": working
        },
        {
            "value": area_per_tyre,
            "summary": "Incorrect.",
            "mistake": (
                f"This is the contact area of one tyre. "
                f"Multiply by {num_wheels} to get the total: {total_area} m²."
            ),
            "working": working
        },
        {
            "value": round(total_area * num_wheels, 4),
            "summary": "Incorrect.",
            "mistake": f"You multiplied the total area by {num_wheels} again. A = F ÷ P gives the total contact area directly.",
            "working": working
        },
        {
            "value": round(total_area + area_per_tyre, 4),
            "summary": "Incorrect.",
            "mistake": f"Check the number of tyres. The {label} has {num_wheels} tyres, so total area = {num_wheels} × {area_per_tyre} m².",
            "working": working
        },
    ]

    question = (
        f"The {label} exerts a pressure of {pressure} Pa on the ground.\n\n"
        f"Using your answer to part 1, calculate the total contact area of the {label}'s tyres on the ground."
    )

    return format_mcq(question, total_area, options_data, "m²")


def make_per_tyre_area_mcq(label, num_wheels, weight, pressure, total_area, area_per_tyre):

    working = area_per_tyre_working(weight, pressure, total_area, num_wheels, area_per_tyre)

    options_data = [
        {
            "value": area_per_tyre,
            "summary": "Correct!",
            "mistake": None,
            "working": working
        },
        {
            "value": total_area,
            "summary": "Incorrect.",
            "mistake": f"This is the total contact area. Divide by {num_wheels} to find the area of each individual tyre.",
            "working": working
        },
        {
            "value": round(total_area * num_wheels, 4),
            "summary": "Incorrect.",
            "mistake": f"You multiplied the total area by {num_wheels} instead of dividing. Each tyre area = total area ÷ {num_wheels}.",
            "working": working
        },
        {
            "value": round(area_per_tyre / 2, 4),
            "summary": "Incorrect.",
            "mistake": "Check your arithmetic when dividing the total area by the number of tyres.",
            "working": working
        },
    ]

    question = (
        f"The {label} exerts a pressure of {pressure} Pa on the ground. "
        f"It has {num_wheels} tyres.\n\n"
        f"Using your answer to part 1, calculate the contact area of each individual tyre."
    )

    return format_mcq(question, area_per_tyre, options_data, "m²")


def make_force_mcq(label, num_wheels, pressure, total_area, force):

    working = force_working(pressure, total_area, force)

    options_data = [
        {
            "value": force,
            "summary": "Correct!",
            "mistake": None,
            "working": working
        },
        {
            "value": round(pressure * (total_area / num_wheels), 1),
            "summary": "Incorrect.",
            "mistake": f"You used the area of one tyre. The total contact area is {total_area} m² ({num_wheels} tyres combined).",
            "working": working
        },
        {
            "value": round(force * num_wheels, 1),
            "summary": "Incorrect.",
            "mistake": f"You multiplied by {num_wheels} (the number of wheels). F = P × A_total — the total area already accounts for all tyres.",
            "working": working
        },
        {
            "value": round(force / g),
            "summary": "Incorrect.",
            "mistake": "This is the mass in kg, not the weight in N. The weight is the force the object exerts due to gravity.",
            "working": working
        },
    ]

    question = (
        f"A {label} exerts a pressure of {pressure} Pa on the ground.\n\n"
        f"The total contact area of its {num_wheels} tyres is {total_area} m².\n\n"
        f"Calculate the weight of the {label}."
    )

    return format_mcq(question, force, options_data, "N")


# =========================================================
# SCENARIO / QUESTION GENERATORS
# =========================================================

def _pick_context():
    key = random.choice(list(CONTEXTS.keys()))
    ctx = CONTEXTS[key]
    mass = random.choice(ctx["mass_options"])
    area_per_tyre = random.choice(ctx["area_options"])
    num_wheels = ctx["num_wheels"]
    label = ctx["label"]
    weight = int(round(mass * g))
    total_area = round(num_wheels * area_per_tyre, 4)
    pressure = round(weight / total_area)
    return label, num_wheels, mass, weight, area_per_tyre, total_area, pressure


def generate_pressure_scenario():
    label, num_wheels, mass, weight, area_per_tyre, total_area, pressure = _pick_context()
    return [
        make_weight_mcq(label, mass, weight),
        make_pressure_mcq(label, num_wheels, weight, area_per_tyre, total_area, pressure),
    ]


def generate_area_scenario():
    label, num_wheels, mass, weight, area_per_tyre, total_area, pressure = _pick_context()
    area_mcq = random.choice([make_total_area_mcq, make_per_tyre_area_mcq])
    return [
        make_weight_mcq(label, mass, weight),
        area_mcq(label, num_wheels, weight, pressure, total_area, area_per_tyre),
    ]


def generate_force_question():
    label, num_wheels, mass, weight, area_per_tyre, total_area, pressure = _pick_context()
    return make_force_mcq(label, num_wheels, pressure, total_area, weight)


# =========================================================
# TOP-LEVEL QUIZ GENERATOR
# =========================================================

QUESTION_GENERATORS = [
    generate_pressure_scenario,
    generate_area_scenario,
    generate_force_question,
]


def generate_pressure_mcqs(num=5):

    questions = []

    for _ in range(num):
        fn = random.choice(QUESTION_GENERATORS)
        questions.append(fn())

    return questions
