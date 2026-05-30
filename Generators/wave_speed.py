import random
import math
from utils.mcq_utils import format_mcq

C = 3e8        # speed of light, m/s
V_SOUND = 340  # speed of sound in air, m/s


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def sci_latex(val):
    """e.g. 6e14 → r'6 \times 10^{14}'"""
    exp = int(math.floor(math.log10(abs(val))))
    mantissa = round(val / 10 ** exp, 2)
    if mantissa == int(mantissa):
        mantissa = int(mantissa)
    return rf"{mantissa} \times 10^{{{exp}}}"


_SUPERSCRIPT = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sci_plain(val):
    """Plain-text scientific notation with Unicode superscripts, e.g. '6 × 10⁹'."""
    exp = int(math.floor(math.log10(abs(val))))
    mantissa = round(val / 10 ** exp, 2)
    if mantissa == int(mantissa):
        mantissa = int(mantissa)
    return f"{mantissa} × 10{str(exp).translate(_SUPERSCRIPT)}"


def fmt_val(val):
    """Plain string for reasonable numbers, plain sci notation for very large/small."""
    if val == 0:
        return "0"
    if 0.001 <= abs(val) < 1e6:
        return str(round_sf(val))
    return sci_plain(val)


def opt_display(val, unit):
    return f"{fmt_val(val)} {unit}"


# Conversion LaTeX for common prefixes
PREFIX_POWER = {
    "nm": r"10^{-9}",
    "μm": r"10^{-6}",
    "mm": r"10^{-3}",
    "cm": r"10^{-2}",
    "MHz": r"10^{6}",
    "GHz": r"10^{9}",
}


def convert_latex(disp, unit, si_val):
    """LaTeX showing unit → SI, e.g. '500 \times 10^{-9} = 5 \times 10^{-7}'"""
    si_str = sci_latex(si_val) if abs(si_val) < 0.001 or abs(si_val) >= 1e6 else str(round_sf(si_val))
    power = PREFIX_POWER.get(unit)
    if power:
        return rf"{disp} \times {power} = {si_str}"
    return si_str


# =========================================================
# SCENARIOS
# =========================================================

# EM scenarios where λ is in a prefix unit (not metres) — used for "find f" questions
EM_FIND_F = [
    {"type": "radio wave",    "lam_disp": 30,    "lam_unit": "cm", "lam_m": 0.30},
    {"type": "microwave",     "lam_disp": 10,    "lam_unit": "cm", "lam_m": 0.10},
    {"type": "microwave",     "lam_disp": 6,     "lam_unit": "cm", "lam_m": 0.06},
    {"type": "microwave",     "lam_disp": 5,     "lam_unit": "cm", "lam_m": 0.05},
    {"type": "microwave",     "lam_disp": 3,     "lam_unit": "cm", "lam_m": 0.03},
    {"type": "infrared",      "lam_disp": 10,    "lam_unit": "μm", "lam_m": 10e-6},
    {"type": "infrared",      "lam_disp": 5,     "lam_unit": "μm", "lam_m": 5e-6},
    {"type": "infrared",      "lam_disp": 2,     "lam_unit": "μm", "lam_m": 2e-6},
    {"type": "visible light", "lam_disp": 700,   "lam_unit": "nm", "lam_m": 700e-9},
    {"type": "visible light", "lam_disp": 600,   "lam_unit": "nm", "lam_m": 600e-9},
    {"type": "visible light", "lam_disp": 500,   "lam_unit": "nm", "lam_m": 500e-9},
    {"type": "visible light", "lam_disp": 400,   "lam_unit": "nm", "lam_m": 400e-9},
    {"type": "ultraviolet",   "lam_disp": 300,   "lam_unit": "nm", "lam_m": 300e-9},
    {"type": "ultraviolet",   "lam_disp": 200,   "lam_unit": "nm", "lam_m": 200e-9},
    {"type": "ultraviolet",   "lam_disp": 100,   "lam_unit": "nm", "lam_m": 100e-9},
    {"type": "X-ray",         "lam_disp": 1,     "lam_unit": "nm", "lam_m": 1e-9},
    {"type": "X-ray",         "lam_disp": 0.1,   "lam_unit": "nm", "lam_m": 0.1e-9},
    {"type": "gamma ray",     "lam_disp": 0.01,  "lam_unit": "nm", "lam_m": 0.01e-9},
]

# EM scenarios where f is given in MHz/GHz — used for "find λ" questions
EM_FIND_LAM = [
    {"type": "radio wave",  "f_disp": 100,  "f_unit": "MHz", "f_Hz": 100e6},
    {"type": "radio wave",  "f_disp": 150,  "f_unit": "MHz", "f_Hz": 150e6},
    {"type": "radio wave",  "f_disp": 300,  "f_unit": "MHz", "f_Hz": 300e6},
    {"type": "radio wave",  "f_disp": 500,  "f_unit": "MHz", "f_Hz": 500e6},
    {"type": "radio wave",  "f_disp": 600,  "f_unit": "MHz", "f_Hz": 600e6},
    {"type": "radio wave",  "f_disp": 1,    "f_unit": "GHz", "f_Hz": 1e9},
    {"type": "radio wave",  "f_disp": 2,    "f_unit": "GHz", "f_Hz": 2e9},
    {"type": "microwave",   "f_disp": 3,    "f_unit": "GHz", "f_Hz": 3e9},
    {"type": "microwave",   "f_disp": 5,    "f_unit": "GHz", "f_Hz": 5e9},
    {"type": "microwave",   "f_disp": 6,    "f_unit": "GHz", "f_Hz": 6e9},
    {"type": "microwave",   "f_disp": 10,   "f_unit": "GHz", "f_Hz": 10e9},
]

# Sound scenarios: all satisfy v = f_Hz × lam_m = 340 m/s
SOUND = [
    {"f_Hz": 100,   "f_disp": 100,  "f_unit": "Hz",  "lam_disp": 3.4,  "lam_unit": "m",  "lam_m": 3.4},
    {"f_Hz": 200,   "f_disp": 200,  "f_unit": "Hz",  "lam_disp": 1.7,  "lam_unit": "m",  "lam_m": 1.7},
    {"f_Hz": 680,   "f_disp": 680,  "f_unit": "Hz",  "lam_disp": 0.5,  "lam_unit": "m",  "lam_m": 0.5},
    {"f_Hz": 1000,  "f_disp": 1000, "f_unit": "Hz",  "lam_disp": 34,   "lam_unit": "cm", "lam_m": 0.34},
    {"f_Hz": 1700,  "f_disp": 1700, "f_unit": "Hz",  "lam_disp": 20,   "lam_unit": "cm", "lam_m": 0.20},
    {"f_Hz": 3400,  "f_disp": 3400, "f_unit": "Hz",  "lam_disp": 10,   "lam_unit": "cm", "lam_m": 0.10},
    {"f_Hz": 17000, "f_disp": 17,   "f_unit": "kHz", "lam_disp": 2,    "lam_unit": "cm", "lam_m": 0.02},
    {"f_Hz": 20000, "f_disp": 20,   "f_unit": "kHz", "lam_disp": 17,   "lam_unit": "mm", "lam_m": 0.017},
]


# =========================================================
# WORKING BUILDERS
# =========================================================

def _find_f_working(lam_disp, lam_unit, lam_m, v, correct_f):
    lam_m_str = sci_latex(lam_m) if abs(lam_m) < 0.001 else str(round_sf(lam_m))
    v_str = sci_latex(v) if v >= 1e6 else str(round_sf(v))
    f_str = sci_latex(correct_f) if abs(correct_f) >= 1e6 else str(round_sf(correct_f))
    steps = []
    if lam_unit != "m":
        steps += [
            {"type": "text", "content": "First convert the wavelength to metres:"},
            {"type": "latex", "content": rf"\lambda = {convert_latex(lam_disp, lam_unit, lam_m)}\ \mathrm{{m}}"},
        ]
    if v == C:
        steps.append({"type": "text", "content": "All EM waves travel at the speed of light: v = 3 × 10⁸ m/s"})
    steps += [
        {"type": "text", "content": "Rearrange v = fλ to find f:"},
        {"type": "latex", "content": r"f = \frac{v}{\lambda}"},
        {"type": "latex", "content": rf"f = \frac{{{v_str}}}{{{lam_m_str}}}"},
        {"type": "latex", "content": rf"f = {f_str}\ \mathrm{{Hz}}"},
    ]
    return steps


def _find_lam_working(f_disp, f_unit, f_Hz, v, correct_lam):
    f_Hz_str = sci_latex(f_Hz) if f_Hz >= 1e6 else str(round_sf(f_Hz))
    v_str = sci_latex(v) if v >= 1e6 else str(round_sf(v))
    lam_str = sci_latex(correct_lam) if abs(correct_lam) < 0.001 else str(round_sf(correct_lam))
    steps = []
    if f_unit not in ("Hz",):
        steps += [
            {"type": "text", "content": "First convert the frequency to Hz:"},
            {"type": "latex", "content": rf"f = {convert_latex(f_disp, f_unit, f_Hz)}\ \mathrm{{Hz}}"},
        ]
    if v == C:
        steps.append({"type": "text", "content": "All EM waves travel at the speed of light: v = 3 × 10⁸ m/s"})
    steps += [
        {"type": "text", "content": "Rearrange v = fλ to find λ:"},
        {"type": "latex", "content": r"\lambda = \frac{v}{f}"},
        {"type": "latex", "content": rf"\lambda = \frac{{{v_str}}}{{{f_Hz_str}}}"},
        {"type": "latex", "content": rf"\lambda = {lam_str}\ \mathrm{{m}}"},
    ]
    return steps


def _find_v_working(f_Hz, lam_disp, lam_unit, lam_m, correct_v):
    lam_m_str = sci_latex(lam_m) if abs(lam_m) < 0.001 else str(round_sf(lam_m))
    v_str = sci_latex(correct_v) if correct_v >= 1e6 else str(round_sf(correct_v))
    steps = []
    if lam_unit != "m":
        steps += [
            {"type": "text", "content": "First convert the wavelength to metres:"},
            {"type": "latex", "content": rf"\lambda = {convert_latex(lam_disp, lam_unit, lam_m)}\ \mathrm{{m}}"},
        ]
    steps += [
        {"type": "text", "content": "Use the wave speed equation:"},
        {"type": "latex", "content": r"v = f\lambda"},
        {"type": "latex", "content": rf"v = {f_Hz} \times {lam_m_str}"},
        {"type": "latex", "content": rf"v = {v_str}\ \mathrm{{m/s}}"},
    ]
    return steps


# =========================================================
# MCQ BUILDERS
# =========================================================

def make_find_f_em_mcq():
    sc = random.choice(EM_FIND_F)
    em_type = sc["type"]
    lam_disp, lam_unit, lam_m = sc["lam_disp"], sc["lam_unit"], sc["lam_m"]

    correct_f = C / lam_m
    no_conv_f = C / lam_disp       # used display value (not converted) as metres
    wrong_v_f = V_SOUND / lam_m    # used speed of sound instead of c
    mult_f    = C * lam_m          # multiplied instead of divided
    # When no_conv_f == mult_f (e.g. lam_disp=10 cm), use off-by-1000 distractor instead
    if round_sf(no_conv_f) == round_sf(mult_f):
        mult_f = round_sf(C / (lam_m * 1000))

    working = _find_f_working(lam_disp, lam_unit, lam_m, C, correct_f)

    question = (
        f"A {em_type} has a wavelength of {lam_disp} {lam_unit}.\n\n"
        f"Speed of light = 3 × 10⁸ m/s\n\n"
        f"Calculate the frequency."
    )

    options_data = [
        {
            "value": correct_f,
            "display": opt_display(correct_f, "Hz"),
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": no_conv_f,
            "display": opt_display(no_conv_f, "Hz"),
            "summary": "Incorrect.",
            "mistake": (
                f"You used λ = {lam_disp} without converting to metres. "
                f"{lam_disp} {lam_unit} = {sci_latex(lam_m)} m."
            ),
            "working": working,
        },
        {
            "value": wrong_v_f,
            "display": opt_display(wrong_v_f, "Hz"),
            "summary": "Incorrect.",
            "mistake": (
                "You used v = 340 m/s (speed of sound) instead of the speed of light. "
                "All EM waves travel at 3 × 10⁸ m/s."
            ),
            "working": working,
        },
        {
            "value": mult_f,
            "display": opt_display(mult_f, "Hz"),
            "summary": "Incorrect.",
            "mistake": "You multiplied v × λ instead of dividing. f = v ÷ λ.",
            "working": working,
        },
    ]

    return format_mcq(question, correct_f, options_data, "Hz")


def make_find_lam_em_mcq():
    sc = random.choice(EM_FIND_LAM)
    em_type = sc["type"]
    f_disp, f_unit, f_Hz = sc["f_disp"], sc["f_unit"], sc["f_Hz"]

    correct_lam = C / f_Hz
    no_conv_lam = C / f_disp       # used display value without converting to Hz
    wrong_v_lam = V_SOUND / f_Hz   # used sound speed instead of c
    mult_lam    = C * f_Hz         # multiplied instead of divided

    working = _find_lam_working(f_disp, f_unit, f_Hz, C, correct_lam)

    question = (
        f"A {em_type} has a frequency of {f_disp} {f_unit}.\n\n"
        f"Speed of light = 3 × 10⁸ m/s\n\n"
        f"Calculate the wavelength."
    )

    options_data = [
        {
            "value": correct_lam,
            "display": opt_display(correct_lam, "m"),
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": no_conv_lam,
            "display": opt_display(no_conv_lam, "m"),
            "summary": "Incorrect.",
            "mistake": (
                f"You used f = {f_disp} without converting to Hz. "
                f"{f_disp} {f_unit} = {sci_latex(f_Hz)} Hz."
            ),
            "working": working,
        },
        {
            "value": wrong_v_lam,
            "display": opt_display(wrong_v_lam, "m"),
            "summary": "Incorrect.",
            "mistake": (
                "You used v = 340 m/s (speed of sound) instead of the speed of light. "
                "All EM waves travel at 3 × 10⁸ m/s."
            ),
            "working": working,
        },
        {
            "value": mult_lam,
            "display": opt_display(mult_lam, "m"),
            "summary": "Incorrect.",
            "mistake": "You multiplied v × f instead of dividing. λ = v ÷ f.",
            "working": working,
        },
    ]

    return format_mcq(question, correct_lam, options_data, "m")


def make_find_v_sound_mcq():
    sc = random.choice(SOUND)
    f_Hz = sc["f_Hz"]
    f_disp, f_unit = sc["f_disp"], sc["f_unit"]
    lam_disp, lam_unit, lam_m = sc["lam_disp"], sc["lam_unit"], sc["lam_m"]

    correct_v = round_sf(f_Hz * lam_m)  # should be 340
    div_error = round_sf(f_Hz / lam_m) if lam_m > 0 else 0
    lam_error = round_sf(f_Hz * lam_disp) if lam_unit != "m" else round_sf(lam_m / f_Hz)
    # If div_error and lam_error collide (e.g. lam_disp=10 cm → both = 34000), use λ/f instead
    if round_sf(div_error) == round_sf(lam_error):
        div_error = round_sf(lam_m / f_Hz)

    working = _find_v_working(f_Hz, lam_disp, lam_unit, lam_m, correct_v)

    f_str = f"{f_disp} {f_unit}"
    question = (
        f"A sound wave has a frequency of {f_str} and a wavelength of {lam_disp} {lam_unit}.\n\n"
        f"Calculate the wave speed."
    )

    options_data = [
        {
            "value": correct_v,
            "display": opt_display(correct_v, "m/s"),
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": div_error,
            "display": opt_display(div_error, "m/s"),
            "summary": "Incorrect.",
            "mistake": "You divided f by λ instead of multiplying. v = f × λ.",
            "working": working,
        },
    ]

    if lam_unit != "m":
        options_data.append({
            "value": lam_error,
            "display": opt_display(lam_error, "m/s"),
            "summary": "Incorrect.",
            "mistake": (
                f"You used λ = {lam_disp} without converting to metres. "
                f"{lam_disp} {lam_unit} = {round_sf(lam_m)} m."
            ),
            "working": working,
        })
    else:
        options_data.append({
            "value": round_sf(lam_m / f_Hz),
            "display": opt_display(round_sf(lam_m / f_Hz), "m/s"),
            "summary": "Incorrect.",
            "mistake": "You divided λ by f instead of multiplying. v = f × λ.",
            "working": working,
        })

    options_data.append({
        "value": round_sf(f_Hz + lam_m),
        "display": opt_display(round_sf(f_Hz + lam_m), "m/s"),
        "summary": "Incorrect.",
        "mistake": "You added f and λ instead of multiplying. v = f × λ.",
        "working": working,
    })

    return format_mcq(question, correct_v, options_data, "m/s")


def make_find_f_sound_mcq():
    sc = random.choice(SOUND)
    f_Hz = sc["f_Hz"]
    lam_disp, lam_unit, lam_m = sc["lam_disp"], sc["lam_unit"], sc["lam_m"]

    correct_f = round_sf(V_SOUND / lam_m)
    inv_f = round_sf(lam_m / V_SOUND)
    mult_f = round_sf(V_SOUND * lam_m)

    working = _find_f_working(lam_disp, lam_unit, lam_m, V_SOUND, correct_f)

    question = (
        f"A sound wave has a wavelength of {lam_disp} {lam_unit}.\n\n"
        f"Speed of sound = 340 m/s\n\n"
        f"Calculate the frequency."
    )

    options_data = [
        {
            "value": correct_f,
            "display": opt_display(correct_f, "Hz"),
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": inv_f,
            "display": opt_display(inv_f, "Hz"),
            "summary": "Incorrect.",
            "mistake": "You divided λ by v instead of v by λ. f = v ÷ λ.",
            "working": working,
        },
        {
            "value": mult_f,
            "display": opt_display(mult_f, "Hz"),
            "summary": "Incorrect.",
            "mistake": "You multiplied v × λ instead of dividing. f = v ÷ λ.",
            "working": working,
        },
    ]

    if lam_unit != "m":
        no_conv_f = round_sf(V_SOUND / lam_disp)
        # If no_conv_f collides with mult_f (happens when lam_disp=10 cm), use inv_f×10 instead
        if round_sf(no_conv_f) == round_sf(mult_f):
            no_conv_f = round_sf(inv_f * 0.1)
        options_data.append({
            "value": no_conv_f,
            "display": opt_display(no_conv_f, "Hz"),
            "summary": "Incorrect.",
            "mistake": (
                f"You used λ = {lam_disp} without converting to metres. "
                f"{lam_disp} {lam_unit} = {round_sf(lam_m)} m."
            ),
            "working": working,
        })
    else:
        options_data.append({
            "value": round_sf(correct_f * 10),
            "display": opt_display(round_sf(correct_f * 10), "Hz"),
            "summary": "Incorrect.",
            "mistake": "Check your arithmetic.",
            "working": working,
        })

    return format_mcq(question, correct_f, options_data, "Hz")


def make_find_lam_sound_mcq():
    sc = random.choice(SOUND)
    f_Hz = sc["f_Hz"]
    f_disp, f_unit = sc["f_disp"], sc["f_unit"]
    lam_m = sc["lam_m"]

    correct_lam = round_sf(V_SOUND / f_Hz)
    inv_lam = round_sf(f_Hz / V_SOUND)
    mult_lam = round_sf(V_SOUND * f_Hz)

    f_Hz_str = str(f_Hz)
    v_str = str(V_SOUND)
    lam_str = str(correct_lam)

    working = [
        {"type": "text", "content": "Rearrange v = fλ to find λ:"},
        {"type": "latex", "content": r"\lambda = \frac{v}{f}"},
        {"type": "latex", "content": rf"\lambda = \frac{{{v_str}}}{{{f_Hz_str}}}"},
        {"type": "latex", "content": rf"\lambda = {lam_str}\ \mathrm{{m}}"},
    ]

    question = (
        f"A sound wave has a frequency of {f_disp} {f_unit}.\n\n"
        f"Speed of sound = 340 m/s\n\n"
        f"Calculate the wavelength."
    )

    options_data = [
        {
            "value": correct_lam,
            "display": opt_display(correct_lam, "m"),
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": inv_lam,
            "display": opt_display(inv_lam, "m"),
            "summary": "Incorrect.",
            "mistake": "You divided f by v instead of v by f. λ = v ÷ f.",
            "working": working,
        },
        {
            "value": mult_lam,
            "display": opt_display(mult_lam, "m"),
            "summary": "Incorrect.",
            "mistake": "You multiplied v × f instead of dividing. λ = v ÷ f.",
            "working": working,
        },
    ]

    if f_unit != "Hz":
        no_conv_lam = round_sf(V_SOUND / f_disp)
        options_data.append({
            "value": no_conv_lam,
            "display": opt_display(no_conv_lam, "m"),
            "summary": "Incorrect.",
            "mistake": (
                f"You used f = {f_disp} without converting to Hz. "
                f"{f_disp} {f_unit} = {f_Hz} Hz."
            ),
            "working": working,
        })
    else:
        # × 100 collides with inv_lam when f_Hz = V_SOUND × 10 (e.g. 3400 Hz); use ÷ 10 instead
        fallback = round_sf(correct_lam * 100)
        if round_sf(fallback) == round_sf(inv_lam):
            fallback = round_sf(correct_lam / 10)
        options_data.append({
            "value": fallback,
            "display": opt_display(fallback, "m"),
            "summary": "Incorrect.",
            "mistake": "Check your arithmetic.",
            "working": working,
        })

    return format_mcq(question, correct_lam, options_data, "m")


# =========================================================
# TOP-LEVEL GENERATOR
# =========================================================

QUESTION_GENERATORS = [
    make_find_f_em_mcq,
    make_find_lam_em_mcq,
    make_find_v_sound_mcq,
    make_find_f_sound_mcq,
    make_find_lam_sound_mcq,
]


def generate_wave_speed_mcqs(num=5):
    questions = []
    for _ in range(num):
        fn = random.choice(QUESTION_GENERATORS)
        questions.append(fn())
    return questions
