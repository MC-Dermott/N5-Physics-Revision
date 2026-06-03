import random
from utils.mcq_utils import format_mcq
from utils.notes import NOTES


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


# =========================================================
# FORMAT HELPERS
# =========================================================

def fmt_power(w):
    w = float(w)
    if abs(w) >= 1_000_000:
        return f"{w / 1_000_000:g} MW"
    if abs(w) >= 1000:
        return f"{w / 1000:g} kW"
    if 0 < abs(w) < 1:
        return f"{w * 1000:g} mW"
    return f"{w:g} W"


def fmt_volt(v):
    v = float(v)
    if abs(v) >= 1000:
        return f"{v / 1000:g} kV"
    if 0 < abs(v) < 1:
        return f"{v * 1000:g} mV"
    return f"{v:g} V"


def fmt_amp(a):
    a = float(a)
    if 0 < abs(a) < 1:
        return f"{a * 1000:g} mA"
    return f"{a:g} A"


def fmt_ohm(r):
    r = float(r)
    if abs(r) >= 1000:
        return f"{r / 1000:g} kΩ"
    return f"{r:g} Ω"


# =========================================================
# PREFIX PICKERS  →  (display_val, unit_str, si_val)
# =========================================================

def _pick_voltage():
    mode = random.choice(["V", "V", "mV", "kV"])
    if mode == "mV":
        v_si = random.choice([0.1, 0.2, 0.3, 0.5])
        return v_si * 1000, "mV", v_si
    if mode == "kV":
        v_si = random.choice([1000, 2000, 3000, 5000])
        return v_si / 1000, "kV", v_si
    v_si = random.choice([1.5, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 20, 24])
    return v_si, "V", v_si


def _pick_current():
    mode = random.choice(["A", "A", "mA"])
    if mode == "mA":
        i_si = random.choice([0.05, 0.1, 0.2, 0.5])
        return i_si * 1000, "mA", i_si
    i_si = random.choice([0.5, 1, 1.5, 2, 3, 4, 5, 10])
    return i_si, "A", i_si


def _pick_resistance():
    mode = random.choice(["Ω", "Ω", "kΩ"])
    if mode == "kΩ":
        r_si = random.choice([1000, 2000, 5000, 10000])
        return r_si / 1000, "kΩ", r_si
    r_si = random.choice([5, 10, 20, 25, 50, 100, 200, 250, 500])
    return r_si, "Ω", r_si


def _pick_power():
    mode = random.choice(["W", "W", "mW", "kW"])
    if mode == "mW":
        p_si = random.choice([0.05, 0.1, 0.2, 0.5])
        return p_si * 1000, "mW", p_si
    if mode == "kW":
        p_si = random.choice([1000, 2000, 3000, 5000])
        return p_si / 1000, "kW", p_si
    p_si = random.choice([1, 2, 4, 5, 6, 8, 10, 12, 15, 20, 24, 40, 60])
    return p_si, "W", p_si


# =========================================================
# CONTEXTS
# =========================================================

_VI_CONTEXTS = [
    "A light bulb",
    "An electric motor",
    "A heating element",
    "A LED strip",
    "A phone charger",
    "An electric fan",
    "A toaster",
]

_VR_CONTEXTS = [
    "A resistor",
    "A fixed resistor",
    "A resistive component",
    "A thermistor",
]

_IR_CONTEXTS = [
    "A resistor",
    "A wire-wound resistor",
    "A resistive heating element",
    "A fixed resistor",
]


# =========================================================
# P = VI  —  FIND P
# =========================================================

def gen_pvi_find_p():
    v_disp, v_unit, v_si = _pick_voltage()
    i_disp, i_unit, i_si = _pick_current()
    correct = round_sf(v_si * i_si)

    if v_unit != "V":
        prefix_err = round_sf(v_disp * i_si)
        prefix_msg = (
            f"You used V = {v_disp} without converting from {v_unit} to V. "
            f"{v_disp} {v_unit} = {v_si} V."
        )
    elif i_unit != "A":
        prefix_err = round_sf(v_si * i_disp)
        prefix_msg = (
            f"You used I = {i_disp} without converting from {i_unit} to A. "
            f"{i_disp} {i_unit} = {i_si} A."
        )
    else:
        prefix_err = round_sf(v_si + i_si)
        prefix_msg = "You added V and I instead of multiplying. P = V × I."

    divided = round_sf(v_si / i_si)
    wrong_order = round_sf(i_si / v_si)

    steps = [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"P = VI"},
    ]
    if v_unit != "V":
        steps.append({"type": "latex", "content": rf"V = {v_disp}\ \mathrm{{{v_unit}}} = {v_si}\ \mathrm{{V}}"})
    if i_unit != "A":
        steps.append({"type": "latex", "content": rf"I = {i_disp}\ \mathrm{{{i_unit}}} = {i_si}\ \mathrm{{A}}"})
    steps += [
        {"type": "latex", "content": rf"P = {v_si} \times {i_si}"},
        {"type": "latex", "content": rf"P = {fmt_power(correct)}"},
    ]

    ctx = random.choice(_VI_CONTEXTS)
    question = (
        f"{ctx} operates at a voltage of {v_disp} {v_unit} "
        f"and draws a current of {i_disp} {i_unit}.\n\n"
        f"Calculate the power dissipated."
    )

    options_data = [
        {"value": correct,     "display": fmt_power(correct),     "summary": "Correct!",    "mistake": None,                                              "working": steps},
        {"value": divided,     "display": fmt_power(divided),     "summary": "Incorrect.", "mistake": "You divided V by I instead of multiplying. P = V × I.",   "working": steps},
        {"value": wrong_order, "display": fmt_power(wrong_order), "summary": "Incorrect.", "mistake": "You divided I by V. P = V × I.",                           "working": steps},
        {"value": prefix_err,  "display": fmt_power(prefix_err),  "summary": "Incorrect.", "mistake": prefix_msg,                                                 "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "W",
        scaffold=[{"question": "Calculate the power.", "answer": correct, "unit": "W"}],
        notes=NOTES["electricity_power"],
    )


# =========================================================
# P = VI  —  FIND V
# =========================================================

def gen_pvi_find_v():
    p_disp, p_unit, p_si = _pick_power()
    i_disp, i_unit, i_si = _pick_current()
    correct = round_sf(p_si / i_si)

    if p_unit != "W":
        prefix_err = round_sf(p_disp / i_si)
        prefix_msg = (
            f"You used P = {p_disp} without converting from {p_unit} to W. "
            f"{p_disp} {p_unit} = {p_si} W."
        )
    elif i_unit != "A":
        prefix_err = round_sf(p_si / i_disp)
        prefix_msg = (
            f"You used I = {i_disp} without converting from {i_unit} to A. "
            f"{i_disp} {i_unit} = {i_si} A."
        )
    else:
        prefix_err = round_sf(p_si * i_si)
        prefix_msg = "You multiplied P × I instead of dividing. V = P ÷ I."

    multiplied = round_sf(p_si * i_si)
    inverted = round_sf(i_si / p_si)

    steps = [
        {"type": "text", "content": "Rearrange P = VI to find V:"},
        {"type": "latex", "content": r"V = \frac{P}{I}"},
    ]
    if p_unit != "W":
        steps.append({"type": "latex", "content": rf"P = {p_disp}\ \mathrm{{{p_unit}}} = {p_si}\ \mathrm{{W}}"})
    if i_unit != "A":
        steps.append({"type": "latex", "content": rf"I = {i_disp}\ \mathrm{{{i_unit}}} = {i_si}\ \mathrm{{A}}"})
    steps += [
        {"type": "latex", "content": rf"V = \frac{{{p_si}}}{{{i_si}}}"},
        {"type": "latex", "content": rf"V = {fmt_volt(correct)}"},
    ]

    ctx = random.choice(_VI_CONTEXTS)
    question = (
        f"{ctx} dissipates {p_disp} {p_unit} when a current of {i_disp} {i_unit} flows through it.\n\n"
        f"Calculate the voltage across it."
    )

    options_data = [
        {"value": correct,    "display": fmt_volt(correct),    "summary": "Correct!",    "mistake": None,                                                    "working": steps},
        {"value": multiplied, "display": fmt_volt(multiplied), "summary": "Incorrect.", "mistake": "You multiplied P × I instead of dividing. V = P ÷ I.",        "working": steps},
        {"value": inverted,   "display": fmt_volt(inverted),   "summary": "Incorrect.", "mistake": "You divided I by P instead of P by I. V = P ÷ I.",             "working": steps},
        {"value": prefix_err, "display": fmt_volt(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                     "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "V",
        scaffold=[{"question": "Calculate the voltage.", "answer": correct, "unit": "V"}],
        notes=NOTES["electricity_power"],
    )


# =========================================================
# P = VI  —  FIND I
# =========================================================

def gen_pvi_find_i():
    p_disp, p_unit, p_si = _pick_power()
    v_disp, v_unit, v_si = _pick_voltage()
    correct = round_sf(p_si / v_si)

    if p_unit != "W":
        prefix_err = round_sf(p_disp / v_si)
        prefix_msg = (
            f"You used P = {p_disp} without converting from {p_unit} to W. "
            f"{p_disp} {p_unit} = {p_si} W."
        )
    elif v_unit != "V":
        prefix_err = round_sf(p_si / v_disp)
        prefix_msg = (
            f"You used V = {v_disp} without converting from {v_unit} to V. "
            f"{v_disp} {v_unit} = {v_si} V."
        )
    else:
        prefix_err = round_sf(p_si * v_si)
        prefix_msg = "You multiplied P × V instead of dividing. I = P ÷ V."

    multiplied = round_sf(p_si * v_si)
    inverted = round_sf(v_si / p_si)

    steps = [
        {"type": "text", "content": "Rearrange P = VI to find I:"},
        {"type": "latex", "content": r"I = \frac{P}{V}"},
    ]
    if p_unit != "W":
        steps.append({"type": "latex", "content": rf"P = {p_disp}\ \mathrm{{{p_unit}}} = {p_si}\ \mathrm{{W}}"})
    if v_unit != "V":
        steps.append({"type": "latex", "content": rf"V = {v_disp}\ \mathrm{{{v_unit}}} = {v_si}\ \mathrm{{V}}"})
    steps += [
        {"type": "latex", "content": rf"I = \frac{{{p_si}}}{{{v_si}}}"},
        {"type": "latex", "content": rf"I = {fmt_amp(correct)}"},
    ]

    ctx = random.choice(_VI_CONTEXTS)
    question = (
        f"{ctx} is rated at {p_disp} {p_unit} and operates at {v_disp} {v_unit}.\n\n"
        f"Calculate the current drawn."
    )

    options_data = [
        {"value": correct,    "display": fmt_amp(correct),    "summary": "Correct!",    "mistake": None,                                                    "working": steps},
        {"value": multiplied, "display": fmt_amp(multiplied), "summary": "Incorrect.", "mistake": "You multiplied P × V instead of dividing. I = P ÷ V.",        "working": steps},
        {"value": inverted,   "display": fmt_amp(inverted),   "summary": "Incorrect.", "mistake": "You divided V by P instead of P by V. I = P ÷ V.",             "working": steps},
        {"value": prefix_err, "display": fmt_amp(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                     "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "A",
        scaffold=[{"question": "Calculate the current.", "answer": correct, "unit": "A"}],
        notes=NOTES["electricity_power"],
    )


# =========================================================
# P = V²/R  —  FIND P
# =========================================================

def gen_pv2r_find_p():
    v_disp, v_unit, v_si = _pick_voltage()
    r_disp, r_unit, r_si = _pick_resistance()
    correct = round_sf(v_si ** 2 / r_si)

    no_square = round_sf(v_si / r_si)
    multiply  = round_sf(v_si ** 2 * r_si)

    if v_unit != "V":
        prefix_err = round_sf(v_disp ** 2 / r_si)
        prefix_msg = (
            f"You used V = {v_disp} without converting from {v_unit} to V. "
            f"{v_disp} {v_unit} = {v_si} V."
        )
    elif r_unit != "Ω":
        prefix_err = round_sf(v_si ** 2 / r_disp)
        prefix_msg = (
            f"You used R = {r_disp} without converting from {r_unit} to Ω. "
            f"{r_disp} {r_unit} = {r_si} Ω."
        )
    else:
        prefix_err = no_square
        no_square = round_sf(v_si * r_si)
        prefix_msg = "You forgot to square V. P = V² ÷ R."

    steps = [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"P = \frac{V^2}{R}"},
    ]
    if v_unit != "V":
        steps.append({"type": "latex", "content": rf"V = {v_disp}\ \mathrm{{{v_unit}}} = {v_si}\ \mathrm{{V}}"})
    if r_unit != "Ω":
        steps.append({"type": "latex", "content": rf"R = {r_disp}\ \mathrm{{{r_unit}}} = {r_si}\ \mathrm{{\Omega}}"})
    steps += [
        {"type": "latex", "content": rf"P = \frac{{{v_si}^2}}{{{r_si}}}"},
        {"type": "latex", "content": rf"P = \frac{{{round_sf(v_si**2)}}}{{{r_si}}}"},
        {"type": "latex", "content": rf"P = {fmt_power(correct)}"},
    ]

    ctx = random.choice(_VR_CONTEXTS)
    question = (
        f"{ctx} of {r_disp} {r_unit} has a potential difference of "
        f"{v_disp} {v_unit} across it.\n\n"
        f"Calculate the power dissipated."
    )

    options_data = [
        {"value": correct,   "display": fmt_power(correct),   "summary": "Correct!",    "mistake": None,                                                        "working": steps},
        {"value": no_square, "display": fmt_power(no_square), "summary": "Incorrect.", "mistake": "You forgot to square V. P = V² ÷ R, not V ÷ R.",               "working": steps},
        {"value": multiply,  "display": fmt_power(multiply),  "summary": "Incorrect.", "mistake": "You multiplied V² × R instead of dividing. P = V² ÷ R.",       "working": steps},
        {"value": prefix_err,"display": fmt_power(prefix_err),"summary": "Incorrect.", "mistake": prefix_msg,                                                      "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "W",
        scaffold=[{"question": "Calculate the power.", "answer": correct, "unit": "W"}],
        notes=NOTES["electricity_power"],
    )


# =========================================================
# P = V²/R  —  FIND V
# =========================================================

def gen_pv2r_find_v():
    p_disp, p_unit, p_si = _pick_power()
    r_disp, r_unit, r_si = _pick_resistance()
    correct = round_sf((p_si * r_si) ** 0.5)

    no_root   = round_sf(p_si * r_si)
    wrong_div = round_sf((p_si / r_si) ** 0.5)

    if p_unit != "W":
        prefix_err = round_sf((p_disp * r_si) ** 0.5)
        prefix_msg = (
            f"You used P = {p_disp} without converting from {p_unit} to W. "
            f"{p_disp} {p_unit} = {p_si} W."
        )
    elif r_unit != "Ω":
        prefix_err = round_sf((p_si * r_disp) ** 0.5)
        prefix_msg = (
            f"You used R = {r_disp} without converting from {r_unit} to Ω. "
            f"{r_disp} {r_unit} = {r_si} Ω."
        )
    else:
        prefix_err = round_sf(p_si / r_si)
        prefix_msg = "You divided P by R instead of finding √(P × R). V = √(P × R)."

    steps = [
        {"type": "text", "content": "Rearrange P = V²/R to find V:"},
        {"type": "latex", "content": r"V = \sqrt{PR}"},
    ]
    if p_unit != "W":
        steps.append({"type": "latex", "content": rf"P = {p_disp}\ \mathrm{{{p_unit}}} = {p_si}\ \mathrm{{W}}"})
    if r_unit != "Ω":
        steps.append({"type": "latex", "content": rf"R = {r_disp}\ \mathrm{{{r_unit}}} = {r_si}\ \mathrm{{\Omega}}"})
    steps += [
        {"type": "latex", "content": rf"V = \sqrt{{{p_si} \times {r_si}}}"},
        {"type": "latex", "content": rf"V = \sqrt{{{round_sf(p_si * r_si)}}}"},
        {"type": "latex", "content": rf"V = {fmt_volt(correct)}"},
    ]

    ctx = random.choice(_VR_CONTEXTS)
    question = (
        f"{ctx} of {r_disp} {r_unit} dissipates {p_disp} {p_unit}.\n\n"
        f"Calculate the voltage across it."
    )

    options_data = [
        {"value": correct,    "display": fmt_volt(correct),    "summary": "Correct!",    "mistake": None,                                                              "working": steps},
        {"value": no_root,    "display": fmt_volt(no_root),    "summary": "Incorrect.", "mistake": "You forgot to take the square root. V = √(P × R).",                  "working": steps},
        {"value": wrong_div,  "display": fmt_volt(wrong_div),  "summary": "Incorrect.", "mistake": "You divided P by R under the root. V = √(P × R), not √(P ÷ R).",    "working": steps},
        {"value": prefix_err, "display": fmt_volt(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                           "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "V",
        scaffold=[{"question": "Calculate the voltage.", "answer": correct, "unit": "V"}],
        notes=NOTES["electricity_power"],
    )


# =========================================================
# P = V²/R  —  FIND R
# =========================================================

def gen_pv2r_find_r():
    v_disp, v_unit, v_si = _pick_voltage()
    p_disp, p_unit, p_si = _pick_power()
    correct = round_sf(v_si ** 2 / p_si)

    inverted  = round_sf(p_si / v_si ** 2)
    no_square = round_sf(v_si / p_si)

    if v_unit != "V":
        prefix_err = round_sf(v_disp ** 2 / p_si)
        prefix_msg = (
            f"You used V = {v_disp} without converting from {v_unit} to V. "
            f"{v_disp} {v_unit} = {v_si} V."
        )
    elif p_unit != "W":
        prefix_err = round_sf(v_si ** 2 / p_disp)
        prefix_msg = (
            f"You used P = {p_disp} without converting from {p_unit} to W. "
            f"{p_disp} {p_unit} = {p_si} W."
        )
    else:
        prefix_err = round_sf(v_si * p_si)
        prefix_msg = "You multiplied V × P instead of using R = V² ÷ P."

    steps = [
        {"type": "text", "content": "Rearrange P = V²/R to find R:"},
        {"type": "latex", "content": r"R = \frac{V^2}{P}"},
    ]
    if v_unit != "V":
        steps.append({"type": "latex", "content": rf"V = {v_disp}\ \mathrm{{{v_unit}}} = {v_si}\ \mathrm{{V}}"})
    if p_unit != "W":
        steps.append({"type": "latex", "content": rf"P = {p_disp}\ \mathrm{{{p_unit}}} = {p_si}\ \mathrm{{W}}"})
    steps += [
        {"type": "latex", "content": rf"R = \frac{{{v_si}^2}}{{{p_si}}}"},
        {"type": "latex", "content": rf"R = \frac{{{round_sf(v_si**2)}}}{{{p_si}}}"},
        {"type": "latex", "content": rf"R = {fmt_ohm(correct)}"},
    ]

    ctx = random.choice(_VR_CONTEXTS)
    question = (
        f"{ctx} dissipates {p_disp} {p_unit} when a voltage of "
        f"{v_disp} {v_unit} is applied.\n\n"
        f"Calculate the resistance."
    )

    options_data = [
        {"value": correct,    "display": fmt_ohm(correct),    "summary": "Correct!",    "mistake": None,                                                     "working": steps},
        {"value": inverted,   "display": fmt_ohm(inverted),   "summary": "Incorrect.", "mistake": "You divided P by V² instead of V² by P. R = V² ÷ P.",      "working": steps},
        {"value": no_square,  "display": fmt_ohm(no_square),  "summary": "Incorrect.", "mistake": "You forgot to square V. R = V² ÷ P, not V ÷ P.",           "working": steps},
        {"value": prefix_err, "display": fmt_ohm(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                  "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "Ω",
        scaffold=[{"question": "Calculate the resistance.", "answer": correct, "unit": "Ω"}],
        notes=NOTES["electricity_power"],
    )


# =========================================================
# P = I²R  —  FIND P
# =========================================================

def gen_pi2r_find_p():
    i_disp, i_unit, i_si = _pick_current()
    r_disp, r_unit, r_si = _pick_resistance()
    correct = round_sf(i_si ** 2 * r_si)

    no_square = round_sf(i_si * r_si)
    divided   = round_sf(i_si ** 2 / r_si)

    if i_unit != "A":
        prefix_err = round_sf(i_disp ** 2 * r_si)
        prefix_msg = (
            f"You used I = {i_disp} without converting from {i_unit} to A. "
            f"{i_disp} {i_unit} = {i_si} A."
        )
    elif r_unit != "Ω":
        prefix_err = round_sf(i_si ** 2 * r_disp)
        prefix_msg = (
            f"You used R = {r_disp} without converting from {r_unit} to Ω. "
            f"{r_disp} {r_unit} = {r_si} Ω."
        )
    else:
        prefix_err = no_square
        no_square = round_sf(i_si * r_si * 2)
        prefix_msg = "You forgot to square I. P = I² × R, not I × R."

    steps = [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"P = I^2 R"},
    ]
    if i_unit != "A":
        steps.append({"type": "latex", "content": rf"I = {i_disp}\ \mathrm{{{i_unit}}} = {i_si}\ \mathrm{{A}}"})
    if r_unit != "Ω":
        steps.append({"type": "latex", "content": rf"R = {r_disp}\ \mathrm{{{r_unit}}} = {r_si}\ \mathrm{{\Omega}}"})
    steps += [
        {"type": "latex", "content": rf"P = {i_si}^2 \times {r_si}"},
        {"type": "latex", "content": rf"P = {round_sf(i_si**2)} \times {r_si}"},
        {"type": "latex", "content": rf"P = {fmt_power(correct)}"},
    ]

    ctx = random.choice(_IR_CONTEXTS)
    question = (
        f"{ctx} of {r_disp} {r_unit} carries a current of {i_disp} {i_unit}.\n\n"
        f"Calculate the power dissipated."
    )

    options_data = [
        {"value": correct,    "display": fmt_power(correct),    "summary": "Correct!",    "mistake": None,                                                          "working": steps},
        {"value": no_square,  "display": fmt_power(no_square),  "summary": "Incorrect.", "mistake": "You forgot to square I. P = I² × R, not I × R.",                "working": steps},
        {"value": divided,    "display": fmt_power(divided),    "summary": "Incorrect.", "mistake": "You divided I² by R instead of multiplying. P = I² × R.",        "working": steps},
        {"value": prefix_err, "display": fmt_power(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                       "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "W",
        scaffold=[{"question": "Calculate the power.", "answer": correct, "unit": "W"}],
        notes=NOTES["electricity_power"],
    )


# =========================================================
# P = I²R  —  FIND I
# =========================================================

def gen_pi2r_find_i():
    p_disp, p_unit, p_si = _pick_power()
    r_disp, r_unit, r_si = _pick_resistance()
    correct = round_sf((p_si / r_si) ** 0.5)

    no_root  = round_sf(p_si / r_si)
    multiply = round_sf((p_si * r_si) ** 0.5)

    if p_unit != "W":
        prefix_err = round_sf((p_disp / r_si) ** 0.5)
        prefix_msg = (
            f"You used P = {p_disp} without converting from {p_unit} to W. "
            f"{p_disp} {p_unit} = {p_si} W."
        )
    elif r_unit != "Ω":
        prefix_err = round_sf((p_si / r_disp) ** 0.5)
        prefix_msg = (
            f"You used R = {r_disp} without converting from {r_unit} to Ω. "
            f"{r_disp} {r_unit} = {r_si} Ω."
        )
    else:
        prefix_err = round_sf(p_si * r_si)
        prefix_msg = "You multiplied P × R instead of using I = √(P ÷ R)."

    steps = [
        {"type": "text", "content": "Rearrange P = I²R to find I:"},
        {"type": "latex", "content": r"I = \sqrt{\frac{P}{R}}"},
    ]
    if p_unit != "W":
        steps.append({"type": "latex", "content": rf"P = {p_disp}\ \mathrm{{{p_unit}}} = {p_si}\ \mathrm{{W}}"})
    if r_unit != "Ω":
        steps.append({"type": "latex", "content": rf"R = {r_disp}\ \mathrm{{{r_unit}}} = {r_si}\ \mathrm{{\Omega}}"})
    steps += [
        {"type": "latex", "content": rf"I = \sqrt{{\frac{{{p_si}}}{{{r_si}}}}}"},
        {"type": "latex", "content": rf"I = \sqrt{{{round_sf(p_si / r_si)}}}"},
        {"type": "latex", "content": rf"I = {fmt_amp(correct)}"},
    ]

    ctx = random.choice(_IR_CONTEXTS)
    question = (
        f"{ctx} of {r_disp} {r_unit} dissipates {p_disp} {p_unit}.\n\n"
        f"Calculate the current through it."
    )

    options_data = [
        {"value": correct,    "display": fmt_amp(correct),    "summary": "Correct!",    "mistake": None,                                                            "working": steps},
        {"value": no_root,    "display": fmt_amp(no_root),    "summary": "Incorrect.", "mistake": "You forgot to take the square root. I = √(P ÷ R).",               "working": steps},
        {"value": multiply,   "display": fmt_amp(multiply),   "summary": "Incorrect.", "mistake": "You multiplied P × R instead of dividing. I = √(P ÷ R).",         "working": steps},
        {"value": prefix_err, "display": fmt_amp(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                        "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "A",
        scaffold=[{"question": "Calculate the current.", "answer": correct, "unit": "A"}],
        notes=NOTES["electricity_power"],
    )


# =========================================================
# P = I²R  —  FIND R
# =========================================================

def gen_pi2r_find_r():
    p_disp, p_unit, p_si = _pick_power()
    i_disp, i_unit, i_si = _pick_current()
    correct = round_sf(p_si / i_si ** 2)

    multiply  = round_sf(p_si * i_si ** 2)
    no_square = round_sf(p_si / i_si)

    if p_unit != "W":
        prefix_err = round_sf(p_disp / i_si ** 2)
        prefix_msg = (
            f"You used P = {p_disp} without converting from {p_unit} to W. "
            f"{p_disp} {p_unit} = {p_si} W."
        )
    elif i_unit != "A":
        prefix_err = round_sf(p_si / i_disp ** 2)
        prefix_msg = (
            f"You used I = {i_disp} without converting from {i_unit} to A. "
            f"{i_disp} {i_unit} = {i_si} A."
        )
    else:
        prefix_err = multiply
        multiply = round_sf(p_si / i_si ** 3)
        prefix_msg = "You multiplied P × I² instead of dividing. R = P ÷ I²."

    steps = [
        {"type": "text", "content": "Rearrange P = I²R to find R:"},
        {"type": "latex", "content": r"R = \frac{P}{I^2}"},
    ]
    if p_unit != "W":
        steps.append({"type": "latex", "content": rf"P = {p_disp}\ \mathrm{{{p_unit}}} = {p_si}\ \mathrm{{W}}"})
    if i_unit != "A":
        steps.append({"type": "latex", "content": rf"I = {i_disp}\ \mathrm{{{i_unit}}} = {i_si}\ \mathrm{{A}}"})
    steps += [
        {"type": "latex", "content": rf"R = \frac{{{p_si}}}{{{i_si}^2}}"},
        {"type": "latex", "content": rf"R = \frac{{{p_si}}}{{{round_sf(i_si**2)}}}"},
        {"type": "latex", "content": rf"R = {fmt_ohm(correct)}"},
    ]

    ctx = random.choice(_IR_CONTEXTS)
    question = (
        f"{ctx} dissipates {p_disp} {p_unit} when a current of {i_disp} {i_unit} flows through it.\n\n"
        f"Calculate the resistance."
    )

    options_data = [
        {"value": correct,    "display": fmt_ohm(correct),    "summary": "Correct!",    "mistake": None,                                                      "working": steps},
        {"value": multiply,   "display": fmt_ohm(multiply),   "summary": "Incorrect.", "mistake": "You multiplied P × I² instead of dividing. R = P ÷ I².",    "working": steps},
        {"value": no_square,  "display": fmt_ohm(no_square),  "summary": "Incorrect.", "mistake": "You forgot to square I. R = P ÷ I², not P ÷ I.",            "working": steps},
        {"value": prefix_err, "display": fmt_ohm(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                   "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "Ω",
        scaffold=[{"question": "Calculate the resistance.", "answer": correct, "unit": "Ω"}],
        notes=NOTES["electricity_power"],
    )


# =========================================================
# QUESTION LIST  (P = VI / V²/R / I²R)
# =========================================================

_GENERATORS = [
    gen_pvi_find_p,
    gen_pvi_find_v,
    gen_pvi_find_i,
    gen_pv2r_find_p,
    gen_pv2r_find_v,
    gen_pv2r_find_r,
    gen_pi2r_find_p,
    gen_pi2r_find_i,
    gen_pi2r_find_r,
]


def generate_single_mcq_power():
    return random.choice(_GENERATORS)()


def generate_mcq_power(num=5):
    questions = []
    for _ in range(num):
        questions.append(generate_single_mcq_power())
    return questions


# =========================================================
# FORMAT HELPERS  (P = E/t)
# =========================================================

def fmt_energy(j):
    j = float(j)
    if abs(j) >= 1_000_000:
        return f"{j / 1_000_000:g} MJ"
    if abs(j) >= 1000:
        return f"{j / 1000:g} kJ"
    return f"{j:g} J"


def fmt_time(s):
    return f"{s:g} s"


# =========================================================
# PREFIX PICKERS  (P = E/t)
# =========================================================

def _pick_energy():
    mode = random.choice(["J", "J", "kJ", "MJ"])
    if mode == "kJ":
        e_si = random.choice([1000, 2000, 5000, 10000, 50000, 100000])
        return e_si / 1000, "kJ", e_si
    if mode == "MJ":
        e_si = random.choice([1_000_000, 2_000_000, 5_000_000])
        return e_si / 1_000_000, "MJ", e_si
    e_si = random.choice([100, 200, 250, 500, 750, 1000, 2000, 5000])
    return e_si, "J", e_si


def _pick_time():
    """Returns (display_val, unit_label, si_val_in_seconds)."""
    mode = random.choice(["s", "s", "minutes", "hours"])
    if mode == "minutes":
        t_min = random.choice([1, 2, 3, 4, 5, 10, 15, 20, 30])
        return t_min, "minutes", t_min * 60
    if mode == "hours":
        t_h = random.choice([1, 2, 3, 4, 5])
        return t_h, "hours", t_h * 3600
    t_si = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 120, 300])
    return t_si, "s", t_si


_PET_CONTEXTS = [
    "An electric kettle",
    "A heater",
    "An electric motor",
    "A solar panel",
    "A battery charger",
    "A microwave oven",
    "A hairdryer",
    "An immersion heater",
]


# =========================================================
# P = E/t  —  FIND P
# =========================================================

def gen_pet_find_p():
    e_disp, e_unit, e_si = _pick_energy()
    t_disp, t_unit, t_si = _pick_time()
    correct = round_sf(e_si / t_si)

    multiplied = round_sf(e_si * t_si)
    inverted   = round_sf(t_si / e_si)

    if e_unit != "J":
        prefix_err = round_sf(e_disp / t_si)
        prefix_msg = (
            f"You used E = {e_disp} without converting from {e_unit} to J. "
            f"{e_disp} {e_unit} = {e_si} J."
        )
    elif t_unit != "s":
        prefix_err = round_sf(e_si / t_disp)
        prefix_msg = (
            f"You used t = {t_disp} without converting from {t_unit} to seconds. "
            f"{t_disp} {t_unit} = {t_si} s."
        )
    else:
        prefix_err = multiplied
        multiplied = round_sf(e_si + t_si)
        prefix_msg = "You multiplied E × t instead of dividing. P = E ÷ t."

    steps = [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"P = \frac{E}{t}"},
    ]
    if e_unit != "J":
        steps.append({"type": "latex", "content": rf"E = {e_disp}\ \mathrm{{{e_unit}}} = {e_si}\ \mathrm{{J}}"})
    if t_unit != "s":
        steps.append({"type": "latex", "content": rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"P = \frac{{{e_si}}}{{{t_si}}}"},
        {"type": "latex", "content": rf"P = {fmt_power(correct)}"},
    ]

    ctx = random.choice(_PET_CONTEXTS)
    question = (
        f"{ctx} transfers {e_disp} {e_unit} of energy in {t_disp} {t_unit}.\n\n"
        f"Calculate the power output."
    )

    options_data = [
        {"value": correct,    "display": fmt_power(correct),    "summary": "Correct!",    "mistake": None,                                                    "working": steps},
        {"value": multiplied, "display": fmt_power(multiplied), "summary": "Incorrect.", "mistake": "You multiplied E × t instead of dividing. P = E ÷ t.",    "working": steps},
        {"value": inverted,   "display": fmt_power(inverted),   "summary": "Incorrect.", "mistake": "You divided t by E instead of E by t. P = E ÷ t.",         "working": steps},
        {"value": prefix_err, "display": fmt_power(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                 "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "W",
        scaffold=[{"question": "Calculate the power.", "answer": correct, "unit": "W"}],
        notes=NOTES["electricity_power_energy"],
    )


# =========================================================
# P = E/t  —  FIND E
# =========================================================

def gen_pet_find_e():
    p_disp, p_unit, p_si = _pick_power()
    t_disp, t_unit, t_si = _pick_time()
    correct = round_sf(p_si * t_si)

    divided  = round_sf(p_si / t_si)
    inverted = round_sf(t_si / p_si)

    if p_unit != "W":
        prefix_err = round_sf(p_disp * t_si)
        prefix_msg = (
            f"You used P = {p_disp} without converting from {p_unit} to W. "
            f"{p_disp} {p_unit} = {p_si} W."
        )
    elif t_unit != "s":
        prefix_err = round_sf(p_si * t_disp)
        prefix_msg = (
            f"You used t = {t_disp} without converting from {t_unit} to seconds. "
            f"{t_disp} {t_unit} = {t_si} s."
        )
    else:
        prefix_err = divided
        divided = round_sf(p_si + t_si)
        prefix_msg = "You divided P by t instead of multiplying. E = P × t."

    steps = [
        {"type": "text", "content": "Rearrange P = E/t to find E:"},
        {"type": "latex", "content": r"E = Pt"},
    ]
    if p_unit != "W":
        steps.append({"type": "latex", "content": rf"P = {p_disp}\ \mathrm{{{p_unit}}} = {p_si}\ \mathrm{{W}}"})
    if t_unit != "s":
        steps.append({"type": "latex", "content": rf"t = {t_disp}\ \mathrm{{{t_unit}}} = {t_si}\ \mathrm{{s}}"})
    steps += [
        {"type": "latex", "content": rf"E = {p_si} \times {t_si}"},
        {"type": "latex", "content": rf"E = {fmt_energy(correct)}"},
    ]

    ctx = random.choice(_PET_CONTEXTS)
    question = (
        f"{ctx} has a power output of {p_disp} {p_unit} and operates for {t_disp} {t_unit}.\n\n"
        f"Calculate the energy transferred."
    )

    options_data = [
        {"value": correct,    "display": fmt_energy(correct),    "summary": "Correct!",    "mistake": None,                                                    "working": steps},
        {"value": divided,    "display": fmt_energy(divided),    "summary": "Incorrect.", "mistake": "You divided P by t instead of multiplying. E = P × t.",   "working": steps},
        {"value": inverted,   "display": fmt_energy(inverted),   "summary": "Incorrect.", "mistake": "You divided t by P. E = P × t.",                           "working": steps},
        {"value": prefix_err, "display": fmt_energy(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                 "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "J",
        scaffold=[{"question": "Calculate the energy transferred.", "answer": correct, "unit": "J"}],
        notes=NOTES["electricity_power_energy"],
    )


# =========================================================
# P = E/t  —  FIND t
# =========================================================

def gen_pet_find_t():
    e_disp, e_unit, e_si = _pick_energy()
    p_disp, p_unit, p_si = _pick_power()
    correct = round_sf(e_si / p_si)

    multiplied = round_sf(e_si * p_si)
    inverted   = round_sf(p_si / e_si)

    if e_unit != "J":
        prefix_err = round_sf(e_disp / p_si)
        prefix_msg = (
            f"You used E = {e_disp} without converting from {e_unit} to J. "
            f"{e_disp} {e_unit} = {e_si} J."
        )
    elif p_unit != "W":
        prefix_err = round_sf(e_si / p_disp)
        prefix_msg = (
            f"You used P = {p_disp} without converting from {p_unit} to W. "
            f"{p_disp} {p_unit} = {p_si} W."
        )
    else:
        prefix_err = multiplied
        multiplied = round_sf(e_si - p_si)
        prefix_msg = "You multiplied E × P instead of dividing. t = E ÷ P."

    steps = [
        {"type": "text", "content": "Rearrange P = E/t to find t:"},
        {"type": "latex", "content": r"t = \frac{E}{P}"},
    ]
    if e_unit != "J":
        steps.append({"type": "latex", "content": rf"E = {e_disp}\ \mathrm{{{e_unit}}} = {e_si}\ \mathrm{{J}}"})
    if p_unit != "W":
        steps.append({"type": "latex", "content": rf"P = {p_disp}\ \mathrm{{{p_unit}}} = {p_si}\ \mathrm{{W}}"})
    steps += [
        {"type": "latex", "content": rf"t = \frac{{{e_si}}}{{{p_si}}}"},
        {"type": "latex", "content": rf"t = {fmt_time(correct)}"},
    ]

    ctx = random.choice(_PET_CONTEXTS)
    question = (
        f"{ctx} with a power output of {p_disp} {p_unit} transfers {e_disp} {e_unit} of energy.\n\n"
        f"Calculate the time taken."
    )

    options_data = [
        {"value": correct,    "display": fmt_time(correct),    "summary": "Correct!",    "mistake": None,                                                    "working": steps},
        {"value": multiplied, "display": fmt_time(multiplied), "summary": "Incorrect.", "mistake": "You multiplied E × P instead of dividing. t = E ÷ P.",    "working": steps},
        {"value": inverted,   "display": fmt_time(inverted),   "summary": "Incorrect.", "mistake": "You divided P by E instead of E by P. t = E ÷ P.",         "working": steps},
        {"value": prefix_err, "display": fmt_time(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                 "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "s",
        scaffold=[{"question": "Calculate the time.", "answer": correct, "unit": "s"}],
        notes=NOTES["electricity_power_energy"],
    )


# =========================================================
# QUESTION LIST  (P = E/t)
# =========================================================

_PET_GENERATORS = [
    gen_pet_find_p,
    gen_pet_find_e,
    gen_pet_find_t,
]


def generate_single_mcq_pet():
    return random.choice(_PET_GENERATORS)()


def generate_mcq_pet(num=5):
    questions = []
    for _ in range(num):
        questions.append(generate_single_mcq_pet())
    return questions
