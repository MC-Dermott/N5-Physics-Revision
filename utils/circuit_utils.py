import random


def generate_resistance():
    """
    Resistance values:
    0.5 Ω to 5.0 Ω
    """
    return random.randint(1, 10) * 0.5


def generate_voltage():
    """
    Supply voltages:
    1V to 9V
    """
    return random.randint(1, 9)


def make_distractors(correct):
    """
    Generate 3 plausible incorrect answers
    """
    distractors = set()

    while len(distractors) < 3:
        variation = random.choice([-2, -1, -0.5, 0.5, 1, 2])
        value = round(correct + variation, 2)

        if value > 0 and value != correct:
            distractors.add(value)

    return list(distractors)
