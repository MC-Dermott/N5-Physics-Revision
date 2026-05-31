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
    """Sentinel value for a wrong-unit distractor: negative, always unique."""
    return -abs(val)


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

    # multiply error guard: E × mass_kg = D when mass_kg = 1
    mult_error = round_sf(E * mass_kg)
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
        {"value": mult_error,
         "summary": "Incorrect.",
         "mistake": "You multiplied E × m instead of dividing. D = E ÷ m.",
         "working": working},
    ]

    if is_grams:
        options_data.append({
            "value": round_sf(E / mass_g),
            "summary": "Incorrect.",
            "mistake": f"You used the mass in grams ({mass_g} g) without converting to kg. "
                       f"{mass_g} g = {mass_kg} kg.",
            "working": working,
        })
    else:
        inv_error = round_sf(mass_kg / E)
        options_data.append({
            "value": inv_error,
            "summary": "Incorrect.",
            "mistake": "You divided m by E instead of E by m. D = E ÷ m.",
            "working": working,
        })

    return format_mcq(question, D, options_data, "Gy")


def _make_H_mcq(question, D, w_R, H):
    working = _H_working(D, w_R, H)

    # distractors
    wrong_wRs = [x for x in [1, 3, 20] if x != w_R]
    d_wrong_wR = round_sf(D * wrong_wRs[0])

    if w_R == 1:
        # D/w_R = D = H when w_R=1 → use a distinct wrong-w_R value instead
        div_error = d_wrong_wR
        div_mistake = f"You used a radiation weighting factor of {wrong_wRs[0]} instead of {w_R}."
    else:
        div_error = round_sf(D / w_R)
        div_mistake = "You divided D by w_R instead of multiplying. H = D × w_R."

    # second wrong-w_R distractor
    alt_wRs = [x for x in wrong_wRs if round_sf(D * x) != round_sf(div_error)]
    d_alt = round_sf(D * alt_wRs[0]) if alt_wRs else round_sf(H * 2)

    options_data = [
        {"value": H,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": _wu(H), "display": f"{round_sf(H)} Gy",
         "summary": "Incorrect.",
         "mistake": "Equivalent dose is measured in Sievert (Sv), not Gray (Gy). "
                    "Gray is used for absorbed dose.",
         "working": working},
        {"value": div_error,
         "summary": "Incorrect.", "mistake": div_mistake, "working": working},
        {"value": d_alt,
         "summary": "Incorrect.",
         "mistake": f"Check the radiation weighting factor for this radiation type.",
         "working": working},
    ]

    return format_mcq(question, H, options_data, "Sv")


def _make_Hdot_mcq(question, H, t_h, dose_rate):
    working = _Hdot_working(H, t_h, dose_rate)

    mult_error = round_sf(H * t_h)
    inv_error = round_sf(t_h / H)
    forgot_t = round_sf(H)
    # Guard 1: inv = dose_rate when H = t_h
    if round_sf(inv_error) == round_sf(dose_rate):
        inv_error = round_sf(dose_rate + H)
    # Guard 2: inv = forgot_t after guard 1
    if round_sf(inv_error) == round_sf(forgot_t):
        inv_error = round_sf(dose_rate * 2) if dose_rate > 1 else round_sf(dose_rate * 0.5)

    options_data = [
        {"value": dose_rate,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": mult_error,
         "summary": "Incorrect.",
         "mistake": "You multiplied H × t instead of dividing. Ḣ = H ÷ t.",
         "working": working},
        {"value": inv_error,
         "summary": "Incorrect.",
         "mistake": "You divided t by H instead of H by t. Ḣ = H ÷ t.",
         "working": working},
        {"value": forgot_t,
         "summary": "Incorrect.",
         "mistake": "You gave the equivalent dose (Sv) rather than the dose rate (Sv/h). "
                    "Divide H by the time to get the rate.",
         "working": working},
    ]

    return format_mcq(question, dose_rate, options_data, "Sv/h")


def _make_H_from_rate_mcq(question, dose_rate, t_h, H):
    working = _H_from_rate_working(dose_rate, t_h, H)

    div_error = round_sf(dose_rate / t_h)
    forgot_t = round_sf(dose_rate)

    options_data = [
        {"value": H,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": _wu(H), "display": f"{round_sf(H)} Gy",
         "summary": "Incorrect.",
         "mistake": "Equivalent dose is measured in Sievert (Sv), not Gray (Gy).",
         "working": working},
        {"value": div_error,
         "summary": "Incorrect.",
         "mistake": "You divided Ḣ by t instead of multiplying. H = Ḣ × t.",
         "working": working},
        {"value": forgot_t,
         "summary": "Incorrect.",
         "mistake": "You gave the dose rate rather than the total equivalent dose. "
                    "Multiply the dose rate by the time: H = Ḣ × t.",
         "working": working},
    ]

    return format_mcq(question, H, options_data, "Sv")


def _make_D_from_H_mcq(question, H, w_R, D):
    working = _D_from_H_working(H, w_R, D)

    mult_error = round_sf(H * w_R)
    if round_sf(mult_error) == round_sf(D):
        mult_error = round_sf(D * 2)

    # When w_R=1, H=D so round_sf(H) == D (correct answer) — use H/20 instead
    d4 = round_sf(H)
    d4_mistake = ("You gave the equivalent dose, not the absorbed dose. "
                  "Divide by the weighting factor: D = H ÷ w_R.")
    if round_sf(d4) == round_sf(D):
        d4 = round_sf(H / 20)
        d4_mistake = "Check the radiation weighting factor — using w_R = 20 here would give this answer."

    options_data = [
        {"value": D,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": _wu(D), "display": f"{round_sf(D)} Sv",
         "summary": "Incorrect.",
         "mistake": "Absorbed dose is measured in Gray (Gy), not Sievert (Sv).",
         "working": working},
        {"value": mult_error,
         "summary": "Incorrect.",
         "mistake": "You multiplied H × w_R instead of dividing. D = H ÷ w_R.",
         "working": working},
        {"value": d4,
         "summary": "Incorrect.", "mistake": d4_mistake, "working": working},
    ]

    return format_mcq(question, D, options_data, "Gy")


def _make_E_mcq(question, D, mass_display, mass_unit, mass_kg, is_grams, mass_g, E):
    working = _E_working(D, mass_kg, E, is_grams, mass_g)

    inv_error = round_sf(D / mass_kg)
    # When mass_kg=1, E=D so D/mass_kg=D=E (collision); use E×3 — avoids E+D=2E too
    if round_sf(inv_error) == round_sf(E):
        inv_error = round_sf(E * 3)
    div_by_D = round_sf(mass_kg / D)
    # When D == mass_kg, div_by_D = inv_error = 1; replace div_by_D
    if round_sf(div_by_D) == round_sf(inv_error):
        div_by_D = round_sf(E * 2)

    options_data = [
        {"value": E,
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": inv_error,
         "summary": "Incorrect.",
         "mistake": "You divided D by m instead of multiplying. E = D × m.",
         "working": working},
        {"value": div_by_D,
         "summary": "Incorrect.",
         "mistake": "You divided m by D. To find energy: E = D × m.",
         "working": working},
    ]

    if is_grams:
        options_data.append({
            "value": round_sf(D * mass_g),
            "summary": "Incorrect.",
            "mistake": f"You used the mass in grams ({mass_g} g) without converting to kg. "
                       f"{mass_g} g = {mass_kg} kg.",
            "working": working,
        })
    else:
        options_data.append({
            "value": round_sf(E + D),
            "summary": "Incorrect.",
            "mistake": "Check your arithmetic.",
            "working": working,
        })

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
        f"A patient is exposed to {rad_name} (radiation weighting factor = {w_R}). "
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
        f"A worker is exposed to {rad_name} (radiation weighting factor = {w_R}). "
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
