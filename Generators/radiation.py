import random
from utils.mcq_utils import format_mcq

# Radiation weighting factors for N5 Physics
RADIATION_TYPES = [
    {"name": "alpha radiation",  "w_R": 20},
    {"name": "beta radiation",   "w_R": 1},
    {"name": "gamma radiation",  "w_R": 1},
    {"name": "fast neutrons",    "w_R": 20},
    {"name": "slow neutrons",    "w_R": 3},
    {"name": "X-rays",           "w_R": 1},
]

D_OPTIONS = [2, 4, 5, 8, 10, 20]   # absorbed dose in Gy (integers for clean maths)
TIME_OPTIONS = [2, 4, 5, 10]        # exposure time in hours (t=1 excluded: H=dose_rate collapses distractors)

W_R_TABLE = (
    "| Type of radiation | Radiation weighting factor (w_R) |\n"
    "|---|---|\n"
    "| Alpha particles | 20 |\n"
    "| Beta particles | 1 |\n"
    "| Gamma rays | 1 |\n"
    "| Fast neutrons | 20 |\n"
    "| Slow neutrons | 3 |\n"
    "| X-rays | 1 |"
)


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def pick_mass():
    """Returns (display_val, unit, mass_kg, is_grams, mass_g)."""
    mass_g = random.choice(range(100, 5100, 100))
    mass_kg = mass_g / 1000
    if mass_g < 1000:
        return mass_g, "g", mass_kg, True, mass_g
    return mass_kg, "kg", mass_kg, False, mass_g


def _wu(val):
    """Sentinel for first wrong-unit distractor (negative, always distinct from positive correct)."""
    return -abs(val)


def _wu2(val):
    """Sentinel for second wrong-unit distractor (always distinct from _wu)."""
    return -(abs(val) * 2 + 1)


# =========================================================
# WORKING BUILDERS
# =========================================================

def _D_working(E, mass_kg, D, is_grams, mass_g):
    steps = []
    if is_grams:
        steps += [
            {"type": "text", "content": "First convert the mass to kg:"},
            {"type": "latex", "content": rf"{mass_g}\ \mathrm{{g}} = {mass_kg}\ \mathrm{{kg}}"},
        ]
    steps += [
        {"type": "text", "content": "Use the absorbed dose equation:"},
        {"type": "latex", "content": r"D = \frac{E}{m}"},
        {"type": "latex", "content": rf"D = \frac{{{E}}}{{{mass_kg}}}"},
        {"type": "latex", "content": rf"D = {round_sf(D)}\ \mathrm{{Gy}}"},
    ]
    return steps


def _H_working(D, w_R, H):
    return [
        {"type": "text", "content": "Use the equivalent dose equation:"},
        {"type": "latex", "content": r"H = D \times w_R"},
        {"type": "latex", "content": rf"H = {round_sf(D)} \times {w_R}"},
        {"type": "latex", "content": rf"H = {round_sf(H)}\ \mathrm{{Sv}}"},
    ]


def _Hdot_working(H, t_h, dose_rate):
    return [
        {"type": "text", "content": "Use the equivalent dose rate equation:"},
        {"type": "latex", "content": r"\dot{H} = \frac{H}{t}"},
        {"type": "latex", "content": rf"\dot{{H}} = \frac{{{round_sf(H)}}}{{{t_h}}}"},
        {"type": "latex", "content": rf"\dot{{H}} = {round_sf(dose_rate)}\ \mathrm{{Sv/h}}"},
    ]


def _H_from_rate_working(dose_rate, t_h, H):
    return [
        {"type": "text", "content": "Rearrange the equivalent dose rate equation to find H:"},
        {"type": "latex", "content": r"H = \dot{H} \times t"},
        {"type": "latex", "content": rf"H = {round_sf(dose_rate)} \times {t_h}"},
        {"type": "latex", "content": rf"H = {round_sf(H)}\ \mathrm{{Sv}}"},
    ]


def _D_from_H_working(H, w_R, D):
    return [
        {"type": "text", "content": "Rearrange the equivalent dose equation to find D:"},
        {"type": "latex", "content": r"D = \frac{H}{w_R}"},
        {"type": "latex", "content": rf"D = \frac{{{round_sf(H)}}}{{{w_R}}}"},
        {"type": "latex", "content": rf"D = {round_sf(D)}\ \mathrm{{Gy}}"},
    ]


def _E_working(D, mass_kg, E, is_grams, mass_g):
    steps = []
    if is_grams:
        steps += [
            {"type": "text", "content": "First convert the mass to kg:"},
            {"type": "latex", "content": rf"{mass_g}\ \mathrm{{g}} = {mass_kg}\ \mathrm{{kg}}"},
        ]
    steps += [
        {"type": "text", "content": "Rearrange D = E/m to find E:"},
        {"type": "latex", "content": r"E = D \times m"},
        {"type": "latex", "content": rf"E = {round_sf(D)} \times {mass_kg}"},
        {"type": "latex", "content": rf"E = {round_sf(E)}\ \mathrm{{J}}"},
    ]
    return steps


# =========================================================
# MCQ BUILDERS
# =========================================================

def _make_D_mcq(question, E, mass_display, mass_unit, mass_kg, is_grams, mass_g, D):
    working = _D_working(E, mass_kg, D, is_grams, mass_g)

    if is_grams:
        content_val = round_sf(E / mass_g)
        content_mistake = (f"You used the mass in grams ({mass_g} g) without converting to kg. "
                           f"{mass_g} g = {mass_kg} kg.")
    else:
        mult_error = round_sf(E * mass_kg)
        if round_sf(mult_error) == round_sf(D):
            mult_error = round_sf(D * 2)
        content_val = mult_error
        content_mistake = "You multiplied E × m instead of dividing. D = E ÷ m."

    options_data = [
        {"value": D,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": _wu(D), "display": f"{round_sf(D)} Sv",
         "summary": "Incorrect.",
         "mistake": "Absorbed dose is measured in Gray (Gy), not Sievert (Sv). "
                    "Sievert is used for equivalent dose.",
         "working": working},
        {"value": _wu2(D), "display": f"{round_sf(D)} J",
         "summary": "Incorrect.",
         "mistake": "Absorbed dose is measured in Gray (Gy), not Joules. "
                    "Joules measure energy; D = E ÷ m gives Gray.",
         "working": working},
        {"value": content_val,
         "summary": "Incorrect.", "mistake": content_mistake, "working": working},
    ]

    return format_mcq(question, D, options_data, "Gy")


def _make_H_mcq(question, D, w_R, H):
    working = _H_working(D, w_R, H)

    # Wrong-w_R content distractor
    wrong_wRs = [x for x in [1, 3, 20] if x != w_R]
    if w_R == 1:
        # D/w_R = D = H when w_R=1 — use a wrong-w_R multiply instead
        content_val = round_sf(D * wrong_wRs[0])
        content_mistake = "Check the radiation weighting factor in the table for this type of radiation."
    else:
        content_val = round_sf(D / w_R)
        content_mistake = "You divided D by w_R instead of multiplying. H = D × w_R."

    options_data = [
        {"value": H,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": _wu(H), "display": f"{round_sf(H)} Gy",
         "summary": "Incorrect.",
         "mistake": "Equivalent dose is measured in Sievert (Sv), not Gray (Gy). "
                    "Gray is used for absorbed dose.",
         "working": working},
        {"value": _wu2(H), "display": f"{round_sf(H)} Sv/h",
         "summary": "Incorrect.",
         "mistake": "Equivalent dose is measured in Sievert (Sv), not Sv/h. "
                    "Sv/h is used for dose rate.",
         "working": working},
        {"value": content_val,
         "summary": "Incorrect.", "mistake": content_mistake, "working": working},
    ]

    return format_mcq(question, H, options_data, "Sv")


def _make_Hdot_mcq(question, H, t_h, dose_rate):
    working = _Hdot_working(H, t_h, dose_rate)

    forgot_t = round_sf(H)

    options_data = [
        {"value": dose_rate,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": _wu(dose_rate), "display": f"{round_sf(dose_rate)} Sv",
         "summary": "Incorrect.",
         "mistake": "Dose rate is measured in Sv/h, not Sv. "
                    "Sv measures total equivalent dose; divide by time to get the rate.",
         "working": working},
        {"value": _wu2(dose_rate), "display": f"{round_sf(dose_rate)} Gy",
         "summary": "Incorrect.",
         "mistake": "Dose rate is measured in Sv/h, not Gy. "
                    "Gray measures absorbed dose; equivalent dose rate uses Sv/h.",
         "working": working},
        {"value": forgot_t,
         "summary": "Incorrect.",
         "mistake": "You gave the equivalent dose (Sv), not the dose rate (Sv/h). "
                    "Divide H by the time: Ḣ = H ÷ t.",
         "working": working},
    ]

    return format_mcq(question, dose_rate, options_data, "Sv/h")


def _make_H_from_rate_mcq(question, dose_rate, t_h, H):
    working = _H_from_rate_working(dose_rate, t_h, H)

    div_error = round_sf(dose_rate / t_h)

    options_data = [
        {"value": H,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": _wu(H), "display": f"{round_sf(H)} Gy",
         "summary": "Incorrect.",
         "mistake": "Equivalent dose is measured in Sievert (Sv), not Gray (Gy). "
                    "Gray is used for absorbed dose.",
         "working": working},
        {"value": _wu2(H), "display": f"{round_sf(H)} Sv/h",
         "summary": "Incorrect.",
         "mistake": "Equivalent dose is measured in Sievert (Sv), not Sv/h. "
                    "Sv/h is the unit for dose rate.",
         "working": working},
        {"value": div_error,
         "summary": "Incorrect.",
         "mistake": "You divided Ḣ by t instead of multiplying. H = Ḣ × t.",
         "working": working},
    ]

    return format_mcq(question, H, options_data, "Sv")


def _make_D_from_H_mcq(question, H, w_R, D):
    working = _D_from_H_working(H, w_R, D)

    mult_error = round_sf(H * w_R)
    if round_sf(mult_error) == round_sf(D):
        mult_error = round_sf(D * 2)

    options_data = [
        {"value": D,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": _wu(D), "display": f"{round_sf(D)} Sv",
         "summary": "Incorrect.",
         "mistake": "Absorbed dose is measured in Gray (Gy), not Sievert (Sv). "
                    "Sievert is used for equivalent dose.",
         "working": working},
        {"value": _wu2(D), "display": f"{round_sf(D)} J",
         "summary": "Incorrect.",
         "mistake": "Absorbed dose is measured in Gray (Gy), not Joules. "
                    "Gray = J/kg; the mass is already accounted for.",
         "working": working},
        {"value": mult_error,
         "summary": "Incorrect.",
         "mistake": "You multiplied H × w_R instead of dividing. D = H ÷ w_R.",
         "working": working},
    ]

    return format_mcq(question, D, options_data, "Gy")


def _make_E_mcq(question, D, mass_display, mass_unit, mass_kg, is_grams, mass_g, E):
    working = _E_working(D, mass_kg, E, is_grams, mass_g)

    if is_grams:
        content_val = round_sf(D * mass_g)
        content_mistake = (f"You used the mass in grams ({mass_g} g) without converting to kg. "
                           f"{mass_g} g = {mass_kg} kg.")
    else:
        inv_error = round_sf(D / mass_kg)
        if round_sf(inv_error) == round_sf(E):
            inv_error = round_sf(E * 3)
        content_val = inv_error
        content_mistake = "You divided D by m instead of multiplying. E = D × m."

    options_data = [
        {"value": E,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": _wu(E), "display": f"{round_sf(E)} Gy",
         "summary": "Incorrect.",
         "mistake": "Energy is measured in Joules (J), not Gray. "
                    "Gray = J/kg and is used for absorbed dose.",
         "working": working},
        {"value": _wu2(E), "display": f"{round_sf(E)} Sv",
         "summary": "Incorrect.",
         "mistake": "Energy is measured in Joules (J), not Sievert. "
                    "Sievert is used for equivalent dose.",
         "working": working},
        {"value": content_val,
         "summary": "Incorrect.", "mistake": content_mistake, "working": working},
    ]

    return format_mcq(question, E, options_data, "J")


# =========================================================
# SCENARIO GENERATORS
# =========================================================

def _pick_values():
    rad = random.choice(RADIATION_TYPES)
    mass_display, mass_unit, mass_kg, is_grams, mass_g = pick_mass()
    D = random.choice(D_OPTIONS)
    E = D * mass_kg          # exact since D is int and mass_kg is multiple of 0.001
    t_h = random.choice(TIME_OPTIONS)
    H = D * rad["w_R"]
    dose_rate = H / t_h
    return rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate


def generate_forward_scenario():
    """Absorbed dose → Equivalent dose → Equivalent dose rate."""
    rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate = _pick_values()
    mass_text = f"{mass_display} {mass_unit}"
    rad_name = rad["name"]
    w_R = rad["w_R"]

    context = (
        f"{W_R_TABLE}\n\n"
        f"A patient is exposed to {rad_name}. "
        f"A mass of {mass_text} of tissue absorbs {round_sf(E)} J of energy. "
        f"The exposure lasts {t_h} hour{'s' if t_h > 1 else ''}."
    )

    q1 = _make_D_mcq(
        f"{context}\n\nCalculate the absorbed dose.",
        E, mass_display, mass_unit, mass_kg, is_grams, mass_g, D,
    )
    q2 = _make_H_mcq(
        f"{context}\n\nUsing your answer to part 1, calculate the equivalent dose.",
        D, w_R, H,
    )
    q3 = _make_Hdot_mcq(
        f"{context}\n\nUsing your answer to part 2, calculate the equivalent dose rate.",
        H, t_h, dose_rate,
    )
    return [q1, q2, q3]


def generate_reverse_scenario():
    """Equivalent dose rate → Equivalent dose → Absorbed dose."""
    rad, mass_display, mass_unit, mass_kg, is_grams, mass_g, D, E, t_h, H, dose_rate = _pick_values()
    mass_text = f"{mass_display} {mass_unit}"
    rad_name = rad["name"]
    w_R = rad["w_R"]

    context = (
        f"{W_R_TABLE}\n\n"
        f"A worker is exposed to {rad_name}. "
        f"The equivalent dose rate is {round_sf(dose_rate)} Sv/h. "
        f"The exposure lasts {t_h} hour{'s' if t_h > 1 else ''}. "
        f"The mass of tissue exposed is {mass_text}."
    )

    q1 = _make_H_from_rate_mcq(
        f"{context}\n\nCalculate the equivalent dose.",
        dose_rate, t_h, H,
    )
    q2 = _make_D_from_H_mcq(
        f"{context}\n\nUsing your answer to part 1, calculate the absorbed dose.",
        H, w_R, D,
    )
    q3 = _make_E_mcq(
        f"{context}\n\nUsing your answer to part 2, calculate the energy absorbed by the tissue.",
        D, mass_display, mass_unit, mass_kg, is_grams, mass_g, E,
    )
    return [q1, q2, q3]


# =========================================================
# TOP-LEVEL GENERATOR
# =========================================================

def generate_radiation_scenarios(num=3):
    questions = []
    for _ in range(num):
        scenario_fn = random.choice([generate_forward_scenario, generate_reverse_scenario])
        questions.append(scenario_fn())
    return questions
