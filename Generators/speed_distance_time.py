import random
from utils.mcq_utils import format_mcq
from utils.notes import NOTES


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def fmt_speed(v):
    return f"{round_sf(float(v)):g} m/s"


def fmt_dist(d):
    d = float(d)
    if abs(d) >= 1000:
        return f"{d / 1000:g} km"
    return f"{d:g} m"


def fmt_time_s(t):
    return f"{round_sf(float(t)):g} s"


# =========================================================
# VALUE PICKERS
# =========================================================

_SPEEDS = [1, 2, 5, 10, 20, 25, 30, 50, 100, 200, 300, 340]


def _pick_speed_and_time():
    """
    Returns (v_si, t_disp, t_unit, t_si).
    Always uses a time that gives a clean distance (v × t).
    Sometimes expresses time in minutes or hours.
    """
    v_si = random.choice(_SPEEDS)
    mode  = random.choice(["s", "s", "minutes", "hours"])

    if mode == "minutes":
        t_min = random.choice([1, 2, 3, 5, 10, 15, 20])
        return v_si, t_min, "minutes", t_min * 60

    if mode == "hours":
        t_h = random.choice([1, 2, 3, 4, 5])
        return v_si, t_h, "hours", t_h * 3600

    t_si = random.choice([5, 10, 20, 25, 30, 40, 50, 60, 100, 120, 200])
    return v_si, t_si, "s", t_si


def _d_display(d_si):
    """
    Return (d_disp, d_unit) for a distance in metres.
    Randomly shows km if d_si is a clean multiple of 1000.
    """
    if d_si >= 1000 and d_si % 1000 == 0 and random.choice([True, False]):
        return int(d_si // 1000), "km"
    return d_si, "m"


_CONTEXTS = [
    "A car",
    "A train",
    "A cyclist",
    "A runner",
    "A sound wave",
    "An aeroplane",
    "A boat",
    "A sprinter",
    "A motorway vehicle",
]


# =========================================================
# d = vt  —  FIND SPEED
# =========================================================

def gen_sdt_find_v():
    v_si, t_disp, t_unit, t_si = _pick_speed_and_time()
    d_si = v_si * t_si
    d_disp, d_unit = _d_display(d_si)
    correct = float(v_si)

    multiplied = round_sf(d_si * t_si)
    inverted   = round_sf(t_si / d_si)

    if d_unit == "km":
        prefix_err = round_sf(d_disp / t_si)
        prefix_msg = (
            f"You used d = {d_disp} without converting from km to m. "
            f"{d_disp} km = {d_si} m."
        )
    elif t_unit != "s":
        prefix_err = round_sf(d_si / t_disp)
        prefix_msg = (
            f"You used t = {t_disp} without converting from {t_unit} to seconds. "
            f"{t_disp} {t_unit} = {t_si} s."
        )
    else:
        prefix_err = round_sf(d_si / t_si * 10)
        prefix_msg = "Check your arithmetic."

    steps = [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"v = \frac{d}{t}"},
    ]
    if d_unit == "km":
        steps.append({"type": "latex", "content":
                       rf"d = {d_disp}\ \mathrm{{km}} = {d_si}\ \mathrm{{m}}"})
    if t_unit != "s":
        steps.append({"type": "latex", "content":
                       rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"v = \frac{{{d_si}}}{{{t_si}}}"},
        {"type": "latex", "content": rf"v = {fmt_speed(correct)}"},
    ]

    ctx = random.choice(_CONTEXTS)
    question = (
        f"{ctx} travels {d_disp} {d_unit} in {t_disp} {t_unit}.\n\n"
        f"Calculate the average speed."
    )

    options_data = [
        {"value": correct,    "display": fmt_speed(correct),    "summary": "Correct!",    "mistake": None,                                                          "working": steps},
        {"value": multiplied, "display": fmt_speed(multiplied), "summary": "Incorrect.", "mistake": "You multiplied d × t instead of dividing. v = d ÷ t.",           "working": steps},
        {"value": inverted,   "display": fmt_speed(inverted),   "summary": "Incorrect.", "mistake": "You divided t by d instead of d by t. v = d ÷ t.",               "working": steps},
        {"value": prefix_err, "display": fmt_speed(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                       "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "m/s",
        scaffold=[{"question": "Calculate the speed.", "answer": correct, "unit": "m/s"}],
        notes=NOTES["speed_distance_time"],
    )


# =========================================================
# d = vt  —  FIND DISTANCE
# =========================================================

def gen_sdt_find_d():
    v_si, t_disp, t_unit, t_si = _pick_speed_and_time()
    d_si = v_si * t_si
    correct = float(d_si)

    divided  = round_sf(v_si / t_si)
    inverted = round_sf(t_si / v_si)

    if t_unit != "s":
        prefix_err = round_sf(v_si * t_disp)
        prefix_msg = (
            f"You used t = {t_disp} without converting from {t_unit} to seconds. "
            f"{t_disp} {t_unit} = {t_si} s."
        )
    else:
        prefix_err = round_sf(v_si + t_si)
        prefix_msg = "You added v and t instead of multiplying. d = v × t."

    steps = [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"d = vt"},
    ]
    if t_unit != "s":
        steps.append({"type": "latex", "content":
                       rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"d = {v_si} \times {t_si}"},
        {"type": "latex", "content": rf"d = {fmt_dist(correct)}"},
    ]

    ctx = random.choice(_CONTEXTS)
    question = (
        f"{ctx} travels at {v_si} m/s for {t_disp} {t_unit}.\n\n"
        f"Calculate the distance travelled."
    )

    options_data = [
        {"value": correct,    "display": fmt_dist(correct),    "summary": "Correct!",    "mistake": None,                                                    "working": steps},
        {"value": divided,    "display": fmt_dist(divided),    "summary": "Incorrect.", "mistake": "You divided v by t instead of multiplying. d = v × t.",   "working": steps},
        {"value": inverted,   "display": fmt_dist(inverted),   "summary": "Incorrect.", "mistake": "You divided t by v. d = v × t.",                          "working": steps},
        {"value": prefix_err, "display": fmt_dist(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "m",
        scaffold=[{"question": "Calculate the distance.", "answer": correct, "unit": "m"}],
        notes=NOTES["speed_distance_time"],
    )


# =========================================================
# d = vt  —  FIND TIME
# =========================================================

def gen_sdt_find_t():
    v_si = random.choice(_SPEEDS)
    t_si = random.choice([5, 10, 20, 25, 30, 40, 50, 60, 100, 120, 200, 300])
    d_si = v_si * t_si
    d_disp, d_unit = _d_display(d_si)
    correct = float(t_si)

    multiplied = round_sf(d_si * v_si)
    inverted   = round_sf(v_si / d_si)

    if d_unit == "km":
        prefix_err = round_sf(d_disp / v_si)
        prefix_msg = (
            f"You used d = {d_disp} without converting from km to m. "
            f"{d_disp} km = {d_si} m."
        )
    else:
        prefix_err = round_sf(d_si * v_si / 60)
        prefix_msg = "Check your arithmetic."

    steps = [
        {"type": "text", "content": "Rearrange d = vt to find t:"},
        {"type": "latex", "content": r"t = \frac{d}{v}"},
    ]
    if d_unit == "km":
        steps.append({"type": "latex", "content":
                       rf"d = {d_disp}\ \mathrm{{km}} = {d_si}\ \mathrm{{m}}"})
    steps += [
        {"type": "latex", "content": rf"t = \frac{{{d_si}}}{{{v_si}}}"},
        {"type": "latex", "content": rf"t = {fmt_time_s(correct)}"},
    ]

    ctx = random.choice(_CONTEXTS)
    question = (
        f"{ctx} travels {d_disp} {d_unit} at a constant speed of {v_si} m/s.\n\n"
        f"Calculate the time taken."
    )

    options_data = [
        {"value": correct,    "display": fmt_time_s(correct),    "summary": "Correct!",    "mistake": None,                                                    "working": steps},
        {"value": multiplied, "display": fmt_time_s(multiplied), "summary": "Incorrect.", "mistake": "You multiplied d × v instead of dividing. t = d ÷ v.",   "working": steps},
        {"value": inverted,   "display": fmt_time_s(inverted),   "summary": "Incorrect.", "mistake": "You divided v by d instead of d by v. t = d ÷ v.",        "working": steps},
        {"value": prefix_err, "display": fmt_time_s(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "s",
        scaffold=[{"question": "Calculate the time.", "answer": correct, "unit": "s"}],
        notes=NOTES["speed_distance_time"],
    )


# =========================================================
# QUESTION LIST
# =========================================================

_GENERATORS = [
    gen_sdt_find_v,
    gen_sdt_find_d,
    gen_sdt_find_t,
]


def generate_single_mcq_sdt():
    return random.choice(_GENERATORS)()


def generate_sdt_mcqs(num=5):
    questions = []
    for _ in range(num):
        questions.append(generate_single_mcq_sdt())
    return questions
