import random
from utils.mcq_utils import format_mcq
from utils.notes import NOTES


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def fmt_r(r, unit):
    return f"{round_sf(r):g} {unit}"


_VALUES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
_UNITS  = ["Ω", "Ω", "Ω", "kΩ", "MΩ"]   # weighted towards Ω


def _pick():
    unit = random.choice(_UNITS)
    return random.choice(_VALUES), random.choice(_VALUES), random.choice(_VALUES), unit


def _pick_parallel_pair():
    """Return (ra, rb) where ra == rb roughly half the time."""
    if random.choice([True, False]):
        r = random.choice(_VALUES)
        return r, r
    return random.choice(_VALUES), random.choice(_VALUES)


def _par(a, b):
    return a * b / (a + b)


def _par3(a, b, c):
    return 1 / (1/a + 1/b + 1/c)


# =========================================================
# WORKING BUILDERS
# =========================================================

def _work_series3(r1, r2, r3, unit, correct):
    return [
        {"type": "text",  "content": "Use the series resistance formula:"},
        {"type": "latex", "content": r"R_T = R_1 + R_2 + R_3"},
        {"type": "latex", "content": rf"R_T = {r1} + {r2} + {r3}"},
        {"type": "latex", "content": rf"R_T = {fmt_r(correct, unit)}"},
    ]


def _work_parallel3(r1, r2, r3, unit, correct):
    inv = round_sf(1/r1 + 1/r2 + 1/r3)
    return [
        {"type": "text",  "content": "Use the parallel resistance formula:"},
        {"type": "latex", "content": r"\frac{1}{R_T} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3}"},
        {"type": "latex", "content": rf"\frac{{1}}{{R_T}} = \frac{{1}}{{{r1}}} + \frac{{1}}{{{r2}}} + \frac{{1}}{{{r3}}} = {inv}"},
        {"type": "latex", "content": rf"R_T = \frac{{1}}{{{inv}}} = {fmt_r(correct, unit)}"},
    ]


def _work_series_then_parallel(na, nb, nc, ra, rb, rc, unit, r_ab, correct):
    return [
        {"type": "text",  "content": f"First combine {na} and {nb} in series:"},
        {"type": "latex", "content": rf"R_{{{na[1]}{nb[1]}}} = {ra} + {rb} = {fmt_r(r_ab, unit)}"},
        {"type": "text",  "content": f"Now combine that with {nc} in parallel:"},
        {"type": "latex", "content": r"R_T = \frac{R_{ab} \times R_c}{R_{ab} + R_c}"},
        {"type": "latex", "content":
            rf"R_T = \frac{{{round_sf(r_ab)} \times {rc}}}{{{round_sf(r_ab)} + {rc}}}"},
        {"type": "latex", "content": rf"R_T = {fmt_r(correct, unit)}"},
    ]


def _work_parallel_then_series(na, nb, nc, ra, rb, rc, unit, r_ab, correct):
    return [
        {"type": "text",  "content": f"First combine {na} and {nb} in parallel:"},
        {"type": "latex", "content":
            rf"R_{{{na[1]}{nb[1]}}} = \frac{{{ra} \times {rb}}}{{{ra} + {rb}}} = {fmt_r(r_ab, unit)}"},
        {"type": "text",  "content": f"Now add {nc} in series:"},
        {"type": "latex", "content": rf"R_T = {fmt_r(r_ab, unit)} + {rc} = {fmt_r(correct, unit)}"},
    ]


# =========================================================
# ALL IN SERIES
# =========================================================

def gen_series_3():
    r1, r2, r3, unit = _pick()
    correct = round_sf(r1 + r2 + r3)

    d_parallel  = round_sf(_par3(r1, r2, r3))
    d_two_par   = round_sf(_par(r1, r2) + r3)
    d_only_two  = round_sf(r1 + r2)

    working = _work_series3(r1, r2, r3, unit, correct)

    question = (
        f"Three resistors are connected in series:\n\n"
        f"- R1 = {r1} {unit}\n"
        f"- R2 = {r2} {unit}\n"
        f"- R3 = {r3} {unit}\n\n"
        f"Calculate the total resistance."
    )

    options_data = [
        {"value": correct,    "display": fmt_r(correct, unit),    "summary": "Correct!",    "mistake": None,                                                                                       "working": working},
        {"value": d_parallel, "display": fmt_r(d_parallel, unit), "summary": "Incorrect.", "mistake": "You used the parallel formula. For series: RT = R1 + R2 + R3.",                              "working": working},
        {"value": d_two_par,  "display": fmt_r(d_two_par, unit),  "summary": "Incorrect.", "mistake": "You combined two resistors in parallel — all three are in series here.",                      "working": working},
        {"value": d_only_two, "display": fmt_r(d_only_two, unit), "summary": "Incorrect.", "mistake": "You only added two resistors. Don't forget to include all three.",                            "working": working},
    ]

    return format_mcq(
        question, correct, options_data, unit,
        scaffold=[],
        notes=NOTES["resistor_combinations"],
    )


# =========================================================
# ALL IN PARALLEL
# =========================================================

def gen_parallel_3():
    unit = random.choice(_UNITS)
    # Force at least one matching pair about half the time
    mode = random.choice(["different", "two_equal", "all_equal"])
    if mode == "all_equal":
        r = random.choice(_VALUES)
        r1 = r2 = r3 = r
    elif mode == "two_equal":
        r = random.choice(_VALUES)
        others = [random.choice(_VALUES)]
        trio = [r, r] + others
        random.shuffle(trio)
        r1, r2, r3 = trio
    else:
        r1, r2, r3 = random.choice(_VALUES), random.choice(_VALUES), random.choice(_VALUES)
    correct  = round_sf(_par3(r1, r2, r3))

    d_series    = round_sf(r1 + r2 + r3)
    d_two_only  = round_sf(_par(r1, r2))
    d_inv_only  = round_sf(1/r1 + 1/r2 + 1/r3)   # forgot final reciprocal

    working = _work_parallel3(r1, r2, r3, unit, correct)

    question = (
        f"Three resistors are connected in parallel:\n\n"
        f"- R1 = {r1} {unit}\n"
        f"- R2 = {r2} {unit}\n"
        f"- R3 = {r3} {unit}\n\n"
        f"Calculate the total resistance."
    )

    options_data = [
        {"value": correct,    "display": fmt_r(correct, unit),    "summary": "Correct!",    "mistake": None,                                                                                       "working": working},
        {"value": d_series,   "display": fmt_r(d_series, unit),   "summary": "Incorrect.", "mistake": "You added all three — that is the series formula. For parallel: 1/RT = 1/R1 + 1/R2 + 1/R3.", "working": working},
        {"value": d_two_only, "display": fmt_r(d_two_only, unit), "summary": "Incorrect.", "mistake": "You only used two resistors. Include all three in the parallel calculation.",                 "working": working},
        {"value": d_inv_only, "display": fmt_r(d_inv_only, unit), "summary": "Incorrect.", "mistake": "You forgot to take the final reciprocal. RT = 1 ÷ (1/R1 + 1/R2 + 1/R3).",                  "working": working},
    ]

    return format_mcq(
        question, correct, options_data, unit,
        scaffold=[],
        notes=NOTES["resistor_combinations"],
    )


# =========================================================
# TWO IN SERIES, ONE IN PARALLEL WITH COMBINATION
# =========================================================

def gen_two_series_one_parallel():
    r1, r2, r3, unit = _pick()
    all_r    = [r1, r2, r3]
    all_n    = ["R1", "R2", "R3"]

    lone_i   = random.randint(0, 2)
    pair_i   = [i for i in range(3) if i != lone_i]

    ra, rb   = all_r[pair_i[0]], all_r[pair_i[1]]
    na, nb   = all_n[pair_i[0]], all_n[pair_i[1]]
    rc       = all_r[lone_i]
    nc       = all_n[lone_i]

    r_ab     = round_sf(ra + rb)
    correct  = round_sf(_par(r_ab, rc))

    d_series     = round_sf(r1 + r2 + r3)
    d_parallel   = round_sf(_par3(r1, r2, r3))
    d_par_first  = round_sf(_par(ra, rb) + rc)   # combined the pair in parallel instead

    working = _work_series_then_parallel(na, nb, nc, ra, rb, rc, unit, r_ab, correct)

    question = (
        f"{na} and {nb} are connected in series. "
        f"This combination is connected in parallel with {nc}:\n\n"
        f"- R1 = {r1} {unit}\n"
        f"- R2 = {r2} {unit}\n"
        f"- R3 = {r3} {unit}\n\n"
        f"Calculate the total resistance."
    )

    scaffold = [
        {
            "question": f"Calculate the combined resistance of {na} and {nb} in series.",
            "answer": r_ab,
            "unit": unit,
        },
        {
            "question": "Calculate the total resistance.",
            "answer": correct,
            "unit": unit,
        },
    ]

    options_data = [
        {"value": correct,      "display": fmt_r(correct, unit),      "summary": "Correct!",    "mistake": None,                                                                                           "working": working},
        {"value": d_series,     "display": fmt_r(d_series, unit),     "summary": "Incorrect.", "mistake": f"You added all three in series. {nc} is in parallel with the {na}+{nb} combination.",           "working": working},
        {"value": d_parallel,   "display": fmt_r(d_parallel, unit),   "summary": "Incorrect.", "mistake": f"You treated all three as parallel. {na} and {nb} are in series first.",                        "working": working},
        {"value": d_par_first,  "display": fmt_r(d_par_first, unit),  "summary": "Incorrect.", "mistake": f"You combined {na} and {nb} in parallel instead of series — check the circuit arrangement.",    "working": working},
    ]

    return format_mcq(
        question, correct, options_data, unit,
        scaffold=scaffold,
        notes=NOTES["resistor_combinations"],
    )


# =========================================================
# TWO IN PARALLEL, ONE IN SERIES WITH COMBINATION
# =========================================================

def gen_two_parallel_one_series():
    unit     = random.choice(_UNITS)
    lone_i   = random.randint(0, 2)
    pair_i   = [i for i in range(3) if i != lone_i]
    all_n    = ["R1", "R2", "R3"]

    ra, rb   = _pick_parallel_pair()          # equal ~50 % of the time
    rc       = random.choice(_VALUES)
    all_r    = [None, None, None]
    all_r[pair_i[0]], all_r[pair_i[1]], all_r[lone_i] = ra, rb, rc
    r1, r2, r3 = all_r
    na, nb   = all_n[pair_i[0]], all_n[pair_i[1]]
    rc       = all_r[lone_i]
    nc       = all_n[lone_i]

    r_ab     = round_sf(_par(ra, rb))
    correct  = round_sf(r_ab + rc)

    d_series     = round_sf(r1 + r2 + r3)
    d_parallel   = round_sf(_par3(r1, r2, r3))
    d_ser_first  = round_sf(_par(ra + rb, rc))   # combined the pair in series instead

    working = _work_parallel_then_series(na, nb, nc, ra, rb, rc, unit, r_ab, correct)

    question = (
        f"{na} and {nb} are connected in parallel. "
        f"{nc} is connected in series with this combination:\n\n"
        f"- R1 = {r1} {unit}\n"
        f"- R2 = {r2} {unit}\n"
        f"- R3 = {r3} {unit}\n\n"
        f"Calculate the total resistance."
    )

    scaffold = [
        {
            "question": f"Calculate the combined resistance of {na} and {nb} in parallel.",
            "answer": r_ab,
            "unit": unit,
        },
        {
            "question": "Calculate the total resistance.",
            "answer": correct,
            "unit": unit,
        },
    ]

    options_data = [
        {"value": correct,     "display": fmt_r(correct, unit),     "summary": "Correct!",    "mistake": None,                                                                                          "working": working},
        {"value": d_series,    "display": fmt_r(d_series, unit),    "summary": "Incorrect.", "mistake": f"You added all three in series. {na} and {nb} are in parallel, not series.",                   "working": working},
        {"value": d_parallel,  "display": fmt_r(d_parallel, unit),  "summary": "Incorrect.", "mistake": f"You treated all three as parallel. {nc} is in series with the parallel combination.",         "working": working},
        {"value": d_ser_first, "display": fmt_r(d_ser_first, unit), "summary": "Incorrect.", "mistake": f"You combined {na} and {nb} in series instead of parallel — check the circuit arrangement.",   "working": working},
    ]

    return format_mcq(
        question, correct, options_data, unit,
        scaffold=scaffold,
        notes=NOTES["resistor_combinations"],
    )


# =========================================================
# QUESTION LIST
# =========================================================

_GENERATORS = [
    gen_series_3,
    gen_parallel_3,
    gen_two_series_one_parallel,
    gen_two_parallel_one_series,
]


def generate_single_mcq_resistors():
    return random.choice(_GENERATORS)()


def generate_resistor_combination_mcqs(num=5):
    questions = []
    for _ in range(num):
        questions.append(generate_single_mcq_resistors())
    return questions
