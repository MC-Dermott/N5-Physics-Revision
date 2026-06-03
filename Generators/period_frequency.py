import random
import math
from utils.mcq_utils import format_mcq
from utils.notes import NOTES


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


def sci_plain(val):
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
    return sci_plain(val)


def opt_display(val, unit):
    return f"{fmt_val(val)} {unit}"


PREFIX_POWER = {
    "kHz": r"10^{3}",
    "MHz": r"10^{6}",
    "GHz": r"10^{9}",
    "ms":  r"10^{-3}",
    "μs":  r"10^{-6}",
    "ns":  r"10^{-9}",
}

PREFIX_FACTOR = {
    "kHz": 1e3,
    "MHz": 1e6,
    "GHz": 1e9,
    "ms":  1e-3,
    "μs":  1e-6,
    "ns":  1e-9,
    "Hz":  1,
    "s":   1,
}


def best_period(T_s):
    """Return (T_display, unit) for the cleanest representation of T in seconds."""
    if T_s >= 1:
        return round_sf(T_s), "s"
    elif T_s >= 1e-3:
        return round_sf(T_s * 1e3), "ms"
    elif T_s >= 1e-6:
        return round_sf(T_s * 1e6), "μs"
    else:
        return round_sf(T_s * 1e9), "ns"


def best_freq(f_Hz):
    """Return (f_display, unit) for the cleanest representation of f in Hz."""
    if f_Hz >= 1e9:
        return round_sf(f_Hz / 1e9), "GHz"
    elif f_Hz >= 1e6:
        return round_sf(f_Hz / 1e6), "MHz"
    elif f_Hz >= 1e3:
        return round_sf(f_Hz / 1e3), "kHz"
    else:
        return round_sf(f_Hz), "Hz"


# =========================================================
# SCENARIOS
# (f_disp, f_unit, f_Hz)  — T_s = 1 / f_Hz
# =========================================================
SCENARIOS = [
    (100,   "Hz",  100),
    (200,   "Hz",  200),
    (500,   "Hz",  500),
    (1000,  "Hz",  1000),
    (2000,  "Hz",  2000),
    (5,     "kHz", 5e3),
    (10,    "kHz", 10e3),
    (50,    "kHz", 50e3),
    (100,   "kHz", 100e3),
    (1,     "MHz", 1e6),
    (5,     "MHz", 5e6),
    (10,    "MHz", 10e6),
    (100,   "MHz", 100e6),
    (1,     "GHz", 1e9),
    (2,     "GHz", 2e9),
    (5,     "GHz", 5e9),
    (10,    "GHz", 10e9),
]


# =========================================================
# WORKING BUILDERS
# =========================================================

def _find_T_working(f_disp, f_unit, f_Hz, T_disp, T_unit):
    f_Hz_str = sci_latex(f_Hz) if f_Hz >= 1e6 else str(f_Hz)
    T_str = fmt_val(T_disp)
    steps = []
    if f_unit != "Hz":
        power = PREFIX_POWER.get(f_unit, "")
        steps += [
            {"type": "text", "content": "First convert the frequency to Hz:"},
            {"type": "latex", "content": rf"f = {f_disp} \times {power} = {f_Hz_str}\ \mathrm{{Hz}}"},
        ]
    steps += [
        {"type": "text", "content": "Use the period equation:"},
        {"type": "latex", "content": r"T = \frac{1}{f}"},
        {"type": "latex", "content": rf"T = \frac{{1}}{{{f_Hz_str}}}"},
        {"type": "latex", "content": rf"T = {T_str}\ \mathrm{{{T_unit}}}"},
    ]
    return steps


def _find_f_working(T_disp, T_unit, T_s, f_disp, f_unit):
    T_s_str = sci_latex(T_s) if T_s < 1e-3 else str(round_sf(T_s))
    f_str = sci_latex(1 / T_s) if (1 / T_s) >= 1e6 else str(round_sf(1 / T_s))
    steps = []
    if T_unit != "s":
        power = PREFIX_POWER.get(T_unit, "")
        steps += [
            {"type": "text", "content": "First convert the period to seconds:"},
            {"type": "latex", "content": rf"T = {T_disp} \times {power} = {T_s_str}\ \mathrm{{s}}"},
        ]
    steps += [
        {"type": "text", "content": "Rearrange T = 1/f to find f:"},
        {"type": "latex", "content": r"f = \frac{1}{T}"},
        {"type": "latex", "content": rf"f = \frac{{1}}{{{T_s_str}}}"},
        {"type": "latex", "content": rf"f = {f_str}\ \mathrm{{Hz}}"},
    ]
    return steps


# =========================================================
# MCQ BUILDERS
# =========================================================

def make_find_T_mcq():
    f_disp, f_unit, f_Hz = random.choice(SCENARIOS)
    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)

    # Distractors (values expressed in same T_unit for consistency)
    T_factor = PREFIX_FACTOR.get(T_unit, 1)

    # 1. Inverted: T = f (i.e. T_s = f_Hz seconds, then converted to T_unit)
    # Using f_Hz/T_factor avoids collision when f_Hz*T_factor == T_disp (e.g. f=1MHz, T=1μs)
    inv_val = round_sf(f_Hz / T_factor)

    # 2. No unit conversion: T = 1 / f_disp (in T_unit)
    no_conv_T_s = 1 / f_disp if f_unit != "Hz" else None
    no_conv_val = (no_conv_T_s / T_factor) if no_conv_T_s else None

    # 3. T = f_Hz² (arbitrary wrong formula)
    sq_val = round_sf(1 / (f_Hz ** 2) / T_factor)

    working = _find_T_working(f_disp, f_unit, f_Hz, T_disp, T_unit)

    question = (
        f"A signal has a frequency of {f_disp} {f_unit}.\n\n"
        f"Calculate the period."
    )

    options_data = [
        {
            "value": T_disp,
            "display": opt_display(T_disp, T_unit),
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": inv_val,
            "display": opt_display(inv_val, T_unit),
            "summary": "Incorrect.",
            "mistake": "You used T = f instead of T = 1/f. Period is the reciprocal of frequency.",
            "working": working,
        },
        {
            "value": sq_val,
            "display": opt_display(sq_val, T_unit),
            "summary": "Incorrect.",
            "mistake": "Check your equation. T = 1 ÷ f.",
            "working": working,
        },
    ]

    if f_unit != "Hz" and no_conv_val is not None:
        options_data.append({
            "value": round_sf(no_conv_val),
            "display": opt_display(round_sf(no_conv_val), T_unit),
            "summary": "Incorrect.",
            "mistake": (
                f"You used f = {f_disp} without converting to Hz. "
                f"{f_disp} {f_unit} = {sci_latex(f_Hz) if f_Hz >= 1e6 else f_Hz} Hz."
            ),
            "working": working,
        })
    else:
        options_data.append({
            "value": round_sf(T_disp * 10),
            "display": opt_display(round_sf(T_disp * 10), T_unit),
            "summary": "Incorrect.",
            "mistake": "Check your arithmetic — your answer is 10× too large.",
            "working": working,
        })

    return format_mcq(question, T_disp, options_data, T_unit,
                      scaffold=[{"question": "Calculate the period.", "answer": T_disp, "unit": T_unit}],
                      notes=NOTES["waves_period"])


def make_find_f_mcq():
    f_disp_orig, f_unit_orig, f_Hz = random.choice(SCENARIOS)
    T_s = 1 / f_Hz
    T_disp, T_unit = best_period(T_s)
    f_disp, f_unit = best_freq(f_Hz)

    T_factor = PREFIX_FACTOR.get(T_unit, 1)

    # Distractors (in Hz then converted to best display unit)
    inv_f_Hz = T_s         # T instead of 1/T
    no_conv_f_Hz = 1 / T_disp if T_unit != "s" else None
    sq_f_Hz = f_Hz ** 2

    working = _find_f_working(T_disp, T_unit, T_s, f_disp, f_unit)

    question = (
        f"A signal has a period of {T_disp} {T_unit}.\n\n"
        f"Calculate the frequency."
    )

    options_data = [
        {
            "value": f_Hz,
            "display": opt_display(f_disp, f_unit),
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": inv_f_Hz,
            "display": opt_display(*best_freq(inv_f_Hz)) if inv_f_Hz > 0 else opt_display(inv_f_Hz, "Hz"),
            "summary": "Incorrect.",
            "mistake": "You used f = T instead of f = 1/T. Frequency is the reciprocal of period.",
            "working": working,
        },
    ]

    if T_unit != "s" and no_conv_f_Hz is not None:
        options_data.append({
            "value": no_conv_f_Hz,
            "display": opt_display(*best_freq(no_conv_f_Hz)),
            "summary": "Incorrect.",
            "mistake": (
                f"You used T = {T_disp} without converting to seconds. "
                f"{T_disp} {T_unit} = {sci_latex(T_s) if T_s < 1e-3 else round_sf(T_s)} s."
            ),
            "working": working,
        })
    else:
        options_data.append({
            "value": f_Hz * 10,
            "display": opt_display(*best_freq(f_Hz * 10)),
            "summary": "Incorrect.",
            "mistake": "Check your arithmetic — your answer is 10× too large.",
            "working": working,
        })

    options_data.append({
        "value": round_sf(f_Hz / 10),
        "display": opt_display(*best_freq(round_sf(f_Hz / 10))),
        "summary": "Incorrect.",
        "mistake": "Check your arithmetic — your answer is 10× too small.",
        "working": working,
    })

    return format_mcq(question, f_Hz, options_data, f_unit,
                      scaffold=[{"question": "Calculate the frequency.", "answer": f_Hz, "unit": f_unit}],
                      notes=NOTES["waves_period"])


# =========================================================
# f = N/t  —  FIND f
# =========================================================

_COUNT_SCENARIOS = [
    # (N, t_disp, t_unit, t_si)
    (20,   10,  "s",       10),
    (50,   5,   "s",       5),
    (100,  20,  "s",       20),
    (200,  40,  "s",       40),
    (300,  60,  "s",       60),
    (500,  100, "s",       100),
    (60,   1,   "minutes", 60),
    (120,  2,   "minutes", 120),
    (300,  5,   "minutes", 300),
    (600,  10,  "minutes", 600),
    (1200, 20,  "minutes", 1200),
    (30,   10,  "s",       10),
    (80,   20,  "s",       20),
    (250,  50,  "s",       50),
]


def make_find_f_from_count_mcq():
    sc = random.choice(_COUNT_SCENARIOS)
    N, t_disp, t_unit, t_si = sc
    correct_f = N / t_si

    multiplied = round_sf(N * t_si)
    inverted   = round_sf(t_si / N)

    if t_unit != "s":
        no_conv = round_sf(N / t_disp)
        no_conv_msg = (
            f"You used t = {t_disp} without converting from {t_unit} to seconds. "
            f"{t_disp} {t_unit} = {t_si} s."
        )
    else:
        no_conv = round_sf(N + t_si)
        no_conv_msg = "You added N and t instead of dividing. f = N ÷ t."

    steps = [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"f = \frac{N}{t}"},
    ]
    if t_unit != "s":
        steps.append({"type": "latex", "content":
                       rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"f = \frac{{{N}}}{{{t_si}}}"},
        {"type": "latex", "content": rf"f = {round_sf(correct_f)}\ \mathrm{{Hz}}"},
    ]

    question = (
        f"{N} complete waves pass a point in {t_disp} {t_unit}.\n\n"
        f"Calculate the frequency."
    )

    options_data = [
        {"value": correct_f, "display": opt_display(correct_f, "Hz"), "summary": "Correct!",    "mistake": None,                                                            "working": steps},
        {"value": multiplied,"display": opt_display(multiplied, "Hz"),"summary": "Incorrect.", "mistake": "You multiplied N × t instead of dividing. f = N ÷ t.",             "working": steps},
        {"value": inverted,  "display": opt_display(inverted, "Hz"),  "summary": "Incorrect.", "mistake": "You divided t by N instead of N by t. f = N ÷ t.",                 "working": steps},
        {"value": no_conv,   "display": opt_display(no_conv, "Hz"),   "summary": "Incorrect.", "mistake": no_conv_msg,                                                        "working": steps},
    ]

    return format_mcq(question, correct_f, options_data, "Hz",
                      scaffold=[{"question": "Calculate the frequency.", "answer": correct_f, "unit": "Hz"}],
                      notes=NOTES["waves_period"])


def make_find_N_mcq():
    sc = random.choice(_COUNT_SCENARIOS)
    N, t_disp, t_unit, t_si = sc
    f = N / t_si
    f_disp, f_unit = best_freq(f)
    correct = float(N)

    divided  = round_sf(f / t_si)
    inverted = round_sf(t_si / f)

    if f_unit != "Hz":
        no_conv = round_sf(f_disp * t_si)
        no_conv_msg = (
            f"You used f = {f_disp} without converting from {f_unit} to Hz. "
            f"{f_disp} {f_unit} = {f} Hz."
        )
    elif t_unit != "s":
        no_conv = round_sf(f * t_disp)
        no_conv_msg = (
            f"You used t = {t_disp} without converting from {t_unit} to seconds. "
            f"{t_disp} {t_unit} = {t_si} s."
        )
    else:
        no_conv = round_sf(f + t_si)
        no_conv_msg = "You added f and t instead of multiplying. N = f × t."

    steps = [
        {"type": "text", "content": "Rearrange f = N/t to find N:"},
        {"type": "latex", "content": r"N = ft"},
    ]
    if t_unit != "s":
        steps.append({"type": "latex", "content":
                       rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"N = {f} \times {t_si}"},
        {"type": "latex", "content": rf"N = {int(correct)}\ \mathrm{{waves}}"},
    ]

    question = (
        f"A wave has a frequency of {f_disp} {f_unit}.\n\n"
        f"How many complete waves pass a point in {t_disp} {t_unit}?"
    )

    options_data = [
        {"value": correct,  "display": str(int(correct)),       "summary": "Correct!",    "mistake": None,                                                           "working": steps},
        {"value": divided,  "display": opt_display(divided, ""),"summary": "Incorrect.", "mistake": "You divided f by t instead of multiplying. N = f × t.",           "working": steps},
        {"value": inverted, "display": opt_display(inverted, ""),"summary": "Incorrect.","mistake": "You divided t by f. N = f × t.",                                  "working": steps},
        {"value": no_conv,  "display": opt_display(no_conv, ""),"summary": "Incorrect.", "mistake": no_conv_msg,                                                       "working": steps},
    ]

    return format_mcq(question, correct, options_data, "waves",
                      scaffold=[{"question": "Calculate the number of waves.", "answer": correct, "unit": "waves"}],
                      notes=NOTES["waves_period"])


# =========================================================
# TOP-LEVEL GENERATOR
# =========================================================

def generate_period_frequency_mcqs(num=5):
    questions = []
    generators = [make_find_T_mcq, make_find_f_mcq, make_find_f_from_count_mcq, make_find_N_mcq]
    for _ in range(num):
        questions.append(random.choice(generators)())
    return questions
