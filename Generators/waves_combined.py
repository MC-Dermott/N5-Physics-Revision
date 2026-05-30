"""
Two-step wave questions combining v = fλ and T = 1/f.

Three question types:
  1. Given T and λ → find v   (step 1: f = 1/T, step 2: v = fλ)
  2. Given T and v → find λ   (step 1: f = 1/T, step 2: λ = v/f)
  3. Given v and λ → find T   (step 1: f = v/λ, step 2: T = 1/f)
"""
import random
import math
from utils.mcq_utils import format_mcq

V_SOUND = 340  # m/s


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def sci_latex(val):
    exp = int(math.floor(math.log10(abs(val))))
    mantissa = round(val / 10 ** exp, 2)
    if mantissa == int(mantissa):
        mantissa = int(mantissa)
    return rf"{mantissa} \times 10^{{{exp}}}"


_SUPERSCRIPT = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _sci_plain(val):
    exp = int(math.floor(math.log10(abs(val))))
    mantissa = round(val / 10 ** exp, 2)
    if mantissa == int(mantissa):
        mantissa = int(mantissa)
    return f"{mantissa} × 10{str(exp).translate(_SUPERSCRIPT)}"


def fmt_val(val):
    if val == 0:
        return "0"
    if 0.001 <= abs(val) < 1e6:
        return str(round_sf(val))
    return _sci_plain(val)


def opt_display(val, unit):
    return f"{fmt_val(val)} {unit}"


PREFIX_POWER = {
    "ms": r"10^{-3}", "μs": r"10^{-6}", "ns": r"10^{-9}",
    "cm": r"10^{-2}", "mm": r"10^{-3}",
}

PREFIX_FACTOR = {
    "ms": 1e-3, "μs": 1e-6, "ns": 1e-9, "s": 1,
    "cm": 1e-2, "mm": 1e-3, "m": 1,
}


def best_period(T_s):
    if T_s >= 1:
        return round_sf(T_s), "s"
    elif T_s >= 1e-3:
        return round_sf(T_s * 1e3), "ms"
    elif T_s >= 1e-6:
        return round_sf(T_s * 1e6), "μs"
    else:
        return round_sf(T_s * 1e9), "ns"


# =========================================================
# COMBINED SCENARIOS
# (f_Hz, lam_m) → v = 340 m/s, T = 1/f_Hz
# f=340 excluded: f_Hz = V_SOUND causes some distractors to equal correct answer.
# =========================================================
COMBINED_SCENARIOS = [
    {"f_Hz": 100,  "lam_m": 3.4,  "lam_disp": 3.4,  "lam_unit": "m"},
    {"f_Hz": 200,  "lam_m": 1.7,  "lam_disp": 1.7,  "lam_unit": "m"},
    {"f_Hz": 680,  "lam_m": 0.5,  "lam_disp": 0.5,  "lam_unit": "m"},
    {"f_Hz": 1000, "lam_m": 0.34, "lam_disp": 34,   "lam_unit": "cm"},
    {"f_Hz": 1700, "lam_m": 0.20, "lam_disp": 20,   "lam_unit": "cm"},
    {"f_Hz": 3400, "lam_m": 0.10, "lam_disp": 10,   "lam_unit": "cm"},
]


# =========================================================
# TYPE 1: Given T and λ → find v
# =========================================================

def make_find_v_mcq():
    sc = random.choice(COMBINED_SCENARIOS)
    f_Hz = sc["f_Hz"]
    lam_m = sc["lam_m"]
    lam_disp, lam_unit = sc["lam_disp"], sc["lam_unit"]

    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)
    correct_v = V_SOUND

    # D1: used T directly as f in step 2 → v = T_s × λ (tiny number)
    d1 = round_sf(T_s * lam_m)
    # D2: no λ unit conversion (only applies when lam_unit != "m")
    #     For lam_unit="m": f/λ would equal v in some cases, so use λ×v instead
    if lam_unit != "m":
        d2 = round_sf(f_Hz * lam_disp)   # used cm/mm value without converting
        d2_mistake = (
            f"You did not convert λ to metres before step 2. "
            f"{lam_disp} {lam_unit} = {lam_m} m."
        )
    else:
        d2 = round_sf(lam_m * V_SOUND)   # v×λ instead of f×λ
        d2_mistake = "Check your substitution in v = fλ — you used v × λ instead of f × λ."
    # D3: stopped after step 1, reported f as v
    d3 = round_sf(f_Hz)

    lam_m_str = str(round_sf(lam_m))
    T_s_str = sci_latex(T_s) if T_s < 1e-3 else str(round_sf(T_s))
    T_power = PREFIX_POWER.get(T_unit, "")

    working = [{"type": "text", "content": "Step 1: find frequency from the period."},
               {"type": "latex", "content": r"f = \frac{1}{T}"}]
    if T_unit != "s":
        working.append({"type": "latex",
                        "content": rf"T = {T_disp} \times {T_power} = {T_s_str}\ \mathrm{{s}}"})
    working.append({"type": "latex",
                    "content": rf"f = \frac{{1}}{{{T_s_str}}} = {f_Hz}\ \mathrm{{Hz}}"})
    if lam_unit != "m":
        lam_power = PREFIX_POWER.get(lam_unit, "")
        working += [
            {"type": "text", "content": "Step 2: convert wavelength, then find wave speed."},
            {"type": "latex", "content": rf"\lambda = {lam_disp} \times {lam_power} = {lam_m_str}\ \mathrm{{m}}"},
        ]
    else:
        working.append({"type": "text", "content": "Step 2: find wave speed."})
    working += [
        {"type": "latex", "content": r"v = f\lambda"},
        {"type": "latex", "content": rf"v = {f_Hz} \times {lam_m_str}"},
        {"type": "latex", "content": rf"v = {correct_v}\ \mathrm{{m/s}}"},
    ]

    question = (
        f"A sound wave has a period of {T_disp} {T_unit} "
        f"and a wavelength of {lam_disp} {lam_unit}.\n\n"
        f"Calculate the wave speed."
    )

    options_data = [
        {"value": correct_v, "display": opt_display(correct_v, "m/s"),
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": d1, "display": opt_display(d1, "m/s"),
         "summary": "Incorrect.",
         "mistake": "You used T directly as f in step 2. Find f = 1/T first, then v = f × λ.",
         "working": working},
        {"value": d2, "display": opt_display(d2, "m/s"),
         "summary": "Incorrect.", "mistake": d2_mistake, "working": working},
        {"value": d3, "display": opt_display(d3, "m/s"),
         "summary": "Incorrect.",
         "mistake": "You only completed step 1 and reported f as if it were v. "
                    "You still need v = f × λ.",
         "working": working},
    ]

    return format_mcq(question, correct_v, options_data, "m/s")


# =========================================================
# TYPE 2: Given T and v → find λ
# =========================================================

def make_find_lam_mcq():
    sc = random.choice(COMBINED_SCENARIOS)
    f_Hz = sc["f_Hz"]
    lam_m = sc["lam_m"]

    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)
    correct_lam = lam_m

    # D1: no T unit conversion → f_wrong = 1/T_disp → λ = V_SOUND * T_disp
    d1 = round_sf(V_SOUND * T_disp)
    # D2: multiplied v × f instead of dividing → λ = V_SOUND × f_Hz
    d2 = round_sf(V_SOUND * f_Hz)
    # D3: reported f as λ (stopped after step 1)
    d3 = round_sf(f_Hz)

    lam_m_str = str(round_sf(lam_m))
    T_s_str = sci_latex(T_s) if T_s < 1e-3 else str(round_sf(T_s))
    T_power = PREFIX_POWER.get(T_unit, "")

    working = [{"type": "text", "content": "Step 1: find frequency from the period."},
               {"type": "latex", "content": r"f = \frac{1}{T}"}]
    if T_unit != "s":
        working.append({"type": "latex",
                        "content": rf"T = {T_disp} \times {T_power} = {T_s_str}\ \mathrm{{s}}"})
    working += [
        {"type": "latex", "content": rf"f = \frac{{1}}{{{T_s_str}}} = {f_Hz}\ \mathrm{{Hz}}"},
        {"type": "text", "content": "Step 2: find wavelength."},
        {"type": "latex", "content": r"\lambda = \frac{v}{f}"},
        {"type": "latex", "content": rf"\lambda = \frac{{{V_SOUND}}}{{{f_Hz}}}"},
        {"type": "latex", "content": rf"\lambda = {lam_m_str}\ \mathrm{{m}}"},
    ]

    question = (
        f"A sound wave has a period of {T_disp} {T_unit}.\n\n"
        f"Speed of sound = 340 m/s\n\n"
        f"Calculate the wavelength."
    )

    options_data = [
        {"value": correct_lam, "display": opt_display(correct_lam, "m"),
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": d1, "display": opt_display(d1, "m"),
         "summary": "Incorrect.",
         "mistake": (
             f"You used T = {T_disp} as if it were already in seconds. "
             f"Convert first: {T_disp} {T_unit} = {T_s_str} s, so f = 1/{T_s_str} = {f_Hz} Hz."
         ),
         "working": working},
        {"value": d2, "display": opt_display(d2, "m"),
         "summary": "Incorrect.",
         "mistake": "You multiplied v × f in step 2 instead of dividing. λ = v ÷ f.",
         "working": working},
        {"value": d3, "display": opt_display(d3, "m"),
         "summary": "Incorrect.",
         "mistake": "You only completed step 1 and reported f as the wavelength. "
                    "You still need λ = v ÷ f.",
         "working": working},
    ]

    return format_mcq(question, correct_lam, options_data, "m")


# =========================================================
# TYPE 3: Given v and λ → find T
# =========================================================

def make_find_T_mcq():
    sc = random.choice(COMBINED_SCENARIOS)
    f_Hz = sc["f_Hz"]
    lam_m = sc["lam_m"]
    lam_disp, lam_unit = sc["lam_disp"], sc["lam_unit"]

    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)
    T_factor = PREFIX_FACTOR.get(T_unit, 1)

    # D1: T = f (inverted step 2); use f/T_factor to avoid collision when f*T_factor == T_disp
    d1_raw = round_sf(f_Hz * T_factor)
    d1 = d1_raw if round_sf(d1_raw) != round_sf(T_disp) else round_sf(f_Hz / T_factor)
    # D2: student multiplied λ × v instead of dividing in step 1 → f_wrong = λ×v, T_wrong = 1/f_wrong
    f_wrong_d2 = V_SOUND * lam_m
    d2 = round_sf(1 / f_wrong_d2 / T_factor) if f_wrong_d2 > 0 else 0
    # D3: no λ unit conversion in step 1 (only for lam_unit != "m")
    if lam_unit != "m":
        f_wrong_d3 = round_sf(V_SOUND / lam_disp)  # used display value as metres
        d3_raw = round_sf(1 / f_wrong_d3 / T_factor) if f_wrong_d3 > 0 else 0
        # If d3 collides with d2 (happens when lam_disp=10 cm), use ×10 arithmetic fallback
        d3 = d3_raw if round_sf(d3_raw) != round_sf(d2) else round_sf(T_disp * 10)
        d3_mistake = (
            f"You did not convert λ to metres in step 1. "
            f"{lam_disp} {lam_unit} = {lam_m} m."
            if round_sf(d3_raw) != round_sf(d2)
            else "Check your arithmetic — your answer is 10× too large."
        )
    else:
        # λ/v always equals T exactly, so use f/v as distractor instead
        d3 = round_sf(f_Hz / V_SOUND)
        d3_mistake = "You divided f by v. To find T, use T = 1/f after finding f = v ÷ λ."

    lam_m_str = str(round_sf(lam_m))
    T_s_str = sci_latex(T_s) if T_s < 1e-3 else str(round_sf(T_s))

    working = []
    if lam_unit != "m":
        lam_power = PREFIX_POWER.get(lam_unit, "")
        working += [
            {"type": "text", "content": "Step 1: convert wavelength, then find frequency."},
            {"type": "latex", "content": rf"\lambda = {lam_disp} \times {lam_power} = {lam_m_str}\ \mathrm{{m}}"},
        ]
    else:
        working.append({"type": "text", "content": "Step 1: find frequency."})
    working += [
        {"type": "latex", "content": r"f = \frac{v}{\lambda}"},
        {"type": "latex", "content": rf"f = \frac{{{V_SOUND}}}{{{lam_m_str}}} = {f_Hz}\ \mathrm{{Hz}}"},
        {"type": "text", "content": "Step 2: find period."},
        {"type": "latex", "content": r"T = \frac{1}{f}"},
        {"type": "latex", "content": rf"T = \frac{{1}}{{{f_Hz}}} = {T_s_str}\ \mathrm{{s}} = {T_disp}\ \mathrm{{{T_unit}}}"},
    ]

    question = (
        f"A sound wave has a wavelength of {lam_disp} {lam_unit}.\n\n"
        f"Speed of sound = 340 m/s\n\n"
        f"Calculate the period of the wave."
    )

    options_data = [
        {"value": T_disp, "display": opt_display(T_disp, T_unit),
         "summary": "Correct!", "mistake": None, "working": working},
        {"value": d1, "display": opt_display(d1, T_unit),
         "summary": "Incorrect.",
         "mistake": "You used T = f in step 2 instead of T = 1/f. Period is the reciprocal of frequency.",
         "working": working},
        {"value": d2, "display": opt_display(d2, T_unit),
         "summary": "Incorrect.",
         "mistake": "You multiplied v × λ in step 1 instead of dividing. f = v ÷ λ.",
         "working": working},
        {"value": d3, "display": opt_display(d3, T_unit),
         "summary": "Incorrect.", "mistake": d3_mistake, "working": working},
    ]

    return format_mcq(question, T_disp, options_data, T_unit)


# =========================================================
# TOP-LEVEL GENERATOR
# =========================================================

def generate_waves_combined_mcqs(num=5):
    questions = []
    generators = [make_find_v_mcq, make_find_lam_mcq, make_find_T_mcq]
    for _ in range(num):
        questions.append(random.choice(generators)())
    return questions
