import random
from utils.mcq_utils import format_mcq


# =========================================================
# WORKING BUILDERS
# =========================================================
def friction_working(mass, driving_force, accel, answer):

    resultant = mass * accel

    return [
        {
            "type": "text",
            "content": "Step 1: Find the resultant (unbalanced) force using Newton's Second Law"
        },
        {
            "type": "latex",
            "content": r"F_{\text{resultant}} = ma"
        },
        {
            "type": "latex",
            "content": rf"F_{{resultant}} = {mass} \times {accel}"
        },
        {
            "type": "latex",
            "content": rf"F_{{resultant}} = {resultant}\ \mathrm{{N}}"
        },
        {
            "type": "text",
            "content": "Step 2: Use driving force minus resultant force"
        },
        {
            "type": "latex",
            "content": r"F_{\text{friction}} = F_{\text{driving}} - F_{\text{resultant}}"
        },
        {
            "type": "latex",
            "content": rf"F_{{friction}} = {driving_force} - {resultant}"
        },
        {
            "type": "latex",
            "content": rf"F_{{friction}} = {answer}\ \mathrm{{N}}"
        }
    ]


def driving_working(mass, accel, friction_force, answer):

    resultant = mass * accel

    return [
        {
            "type": "text",
            "content": "Step 1: Find resultant force using Newton's Second Law"
        },
        {
            "type": "latex",
            "content": r"F_{\text{resultant}} = ma"
        },
        {
            "type": "latex",
            "content": rf"F_{{resultant}} = {mass} \times {accel}"
        },
        {
            "type": "latex",
            "content": rf"F_{{resultant}} = {resultant}\ \mathrm{{N}}"
        },
        {
            "type": "text",
            "content": "Step 2: Add friction to get driving force"
        },
        {
            "type": "latex",
            "content": r"F_{\text{driving}} = F_{\text{resultant}} + F_{\text{friction}}"
        },
        {
            "type": "latex",
            "content": rf"F_{{driving}} = {resultant} + {friction_force}"
        },
        {
            "type": "latex",
            "content": rf"F_{{driving}} = {answer}\ \mathrm{{N}}"
        }
    ]


def acceleration_working(mass, driving_force, friction_force, answer):

    resultant = driving_force - friction_force

    return [
        {
            "type": "text",
            "content": "Step 1: Find resultant force"
        },
        {
            "type": "latex",
            "content": r"F_{\text{resultant}} = F_{\text{driving}} - F_{\text{friction}}"
        },
        {
            "type": "latex",
            "content": rf"F_{{resultant}} = {driving_force} - {friction_force}"
        },
        {
            "type": "latex",
            "content": rf"F_{{resultant}} = {resultant}\ \mathrm{{N}}"
        },
        {
            "type": "text",
            "content": "Step 2: Apply Newton's Second Law"
        },
        {
            "type": "latex",
            "content": r"a = \frac{F}{m}"
        },
        {
            "type": "latex",
            "content": rf"a = \frac{{{resultant}}}{{{mass}}}"
        },
        {
            "type": "latex",
            "content": rf"a = {answer}\ \mathrm{{m/s^2}}"
        }
    ]


# =========================================================
# QUESTION GENERATORS
# =========================================================
def generate_missing_friction():

    mass = random.randint(2, 10)
    driving_force = random.randint(10, 50)
    acceleration = random.randint(2, 5)

    resultant = mass * acceleration
    correct_val = driving_force - resultant

    unit = "N"

    question = (
        f"What is the frictional force acting on an object of mass "
        f"{mass}kg if the acceleration is {acceleration} m/s² "
        f"and the driving force is {driving_force}N?"
    )

    working = friction_working(
        mass,
        driving_force,
        acceleration,
        correct_val
    )

    options_data = [
        {
            "value": correct_val,
            "summary": "Correct!",
            "mistake": None,
            "working": working
        },
        {
            "value": resultant,
            "summary": "Incorrect.",
            "mistake": "You've calculated the unbalanced force, not the friction.",
            "working": working
        },
        {
            "value": driving_force + resultant,
            "summary": "Incorrect.",
            "mistake": "You used the unbalanced force incorrectly. Remember, friction is equal to the unabalanced force take away the driving force.",
            "working": working
        },
        {
            "value": resultant - driving_force,
            "summary": "Incorrect.",
            "mistake": "You used the unbalanced force incorrectly. Remember, friction is equal to the unabalanced force take away the driving force.",
            "working": working
        }
    ]

    return question, correct_val, options_data, unit


def generate_missing_driving():

    mass = random.randint(2, 10)
    friction_force = random.randint(2, 50)
    acceleration = random.randint(2, 5)

    resultant = mass * acceleration
    correct_val = resultant + friction_force

    unit = "N"

    question = (
        f"What is the driving force acting on an object of mass "
        f"{mass}kg if the acceleration is {acceleration} m/s² "
        f"and the frictional force is {friction_force}N?"
    )

    working = driving_working(
        mass,
        acceleration,
        friction_force,
        correct_val
    )

    options_data = [
        {
            "value": correct_val,
            "summary": "Correct!",
            "mistake": None,
            "working": working
        },
        {
            "value": resultant,
            "summary": "Incorrect.",
            "mistake": "Remember, the driving force is the unbalanced force PLUS friction.",
            "working": working
        },
        {
            "value": friction_force - resultant,
            "summary": "Incorrect.",
            "mistake": "Remember, the driving force is the unbalanced force PLUS friction.",
            "working": working
        },
        {
            "value": friction_force,
            "summary": "Incorrect.",
            "mistake": "This is only friction, not driving force.",
            "working": working
        }
    ]

    return question, correct_val, options_data, unit


def generate_missing_acceleration():

    mass = random.randint(2, 10)
    driving_force = random.randint(10, 50)
    friction_force = random.randint(2, driving_force - 1)

    resultant = driving_force - friction_force
    correct_val = round(resultant / mass, 2)

    unit = "m/s²"

    question = (
        f"What is the acceleration of an object of mass {mass}kg "
        f"with driving force {driving_force}N and friction "
        f"{friction_force}N?"
    )

    working = acceleration_working(
        mass,
        driving_force,
        friction_force,
        correct_val
    )

    options_data = [
        {
            "value": correct_val,
            "summary": "Correct!",
            "mistake": None,
            "working": working
        },
        {
            "value": round(driving_force / mass, 2),
            "summary": "Incorrect.",
            "mistake": "Remember, you need to work out the unbalanced force first!",
            "working": working
        },
        {
            "value": round(friction_force / mass, 2),
            "summary": "Incorrect.",
            "mistake": "YRemember, you need to work out the unbalanced force first!",
            "working": working
        },
        {
            "value": round((driving_force + friction_force) / mass, 2),
            "summary": "Incorrect.",
            "mistake": "Remember, the unbalanced force is the DIFFERENCE between the driving force and friction.",
            "working": working
        }
    ]

    return question, correct_val, options_data, unit


# =========================================================
# MAIN GENERATOR
# =========================================================
def generate_single_mcq_forces():

    generators = [
        generate_missing_friction,
        generate_missing_driving,
        generate_missing_acceleration
    ]

    return random.choice(generators)()


def generate_mcq_forces():

    questions = []

    for _ in range(5):
        raw = generate_single_mcq_forces()
        formatted = format_mcq(*raw)
        questions.append(formatted)

    return questions
