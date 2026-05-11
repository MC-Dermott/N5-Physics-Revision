import random


def format_mcq(
    question,
    correct_val,
    options_data,
    unit
):

    # Remove duplicate values
    unique = {}

    for option in options_data:
        unique[option["value"]] = option

    options_data = list(unique.values())

    random.shuffle(options_data)

    letters = ["A", "B", "C", "D"]

    choices = {}

    choices_display = {}

    feedback = {}

    correct_letter = None

    for letter, option in zip(
        letters,
        options_data
    ):

        value = option["value"]

        display = f"{value} {unit}"

        choices[letter] = display

        choices_display[letter] = (
            f"{letter}: {display}"
        )

        feedback[letter] = {

            "summary":
                option["summary"],

            "mistake":
                option["mistake"],

            "working":
                option["working"]
        }

        if value == correct_val:
            correct_letter = letter

    return {

        "question": question,

        "choices": choices,

        "choices_display": choices_display,

        "answer": correct_letter,

        "feedback": feedback
    }
