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
    mode = random.choice(["V", "V", "mV"])
    if mode == "mV":
        v_si = random.choice([0.1, 0.2, 0.3, 0.5])
        return v_si * 1000, "mV", v_si
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


_CONTEXTS = [
    "A resistor",
    "A filament lamp",
    "A component in a circuit",
    "A wire-wound resistor",
    "An LDR",
    "A thermistor",
    "A fixed resistor",
]


# =========================================================
# V = IR  —  FIND V
# =========================================================

def gen_vir_find_v():
    i_disp, i_unit, i_si = _pick_current()
    r_disp, r_unit, r_si = _pick_resistance()
    correct = round_sf(i_si * r_si)

    divided  = round_sf(i_si / r_si)
    inverted = round_sf(r_si / i_si)

    if i_unit != "A":
        prefix_err = round_sf(i_disp * r_si)
        prefix_msg = (
            f"You used I = {i_disp} without converting from {i_unit} to A. "
            f"{i_disp} {i_unit} = {i_si} A."
        )
    elif r_unit != "Ω":
        prefix_err = round_sf(i_si * r_disp)
        prefix_msg = (
            f"You used R = {r_disp} without converting from {r_unit} to Ω. "
            f"{r_disp} {r_unit} = {r_si} Ω."
        )
    else:
        prefix_err = round_sf(i_si + r_si)
        prefix_msg = "You added I and R instead of multiplying. V = I × R."

    steps = [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"V = IR"},
    ]
    if i_unit != "A":
        steps.append({"type": "latex", "content":
                       rf"I = {i_disp}\ \mathrm{{{i_unit}}} = {i_si}\ \mathrm{{A}}"})
    if r_unit != "Ω":
        steps.append({"type": "latex", "content":
                       rf"R = {r_disp}\ \mathrm{{{r_unit}}} = {r_si}\ \mathrm{{\Omega}}"})
    steps += [
        {"type": "latex", "content": rf"V = {i_si} \times {r_si}"},
        {"type": "latex", "content": rf"V = {fmt_volt(correct)}"},
    ]

    ctx = random.choice(_CONTEXTS)
    question = (
        f"{ctx} has a resistance of {r_disp} {r_unit} and carries "
        f"a current of {i_disp} {i_unit}.\n\n"
        f"Calculate the voltage across it."
    )

    options_data = [
        {"value": correct,    "display": fmt_volt(correct),    "summary": "Correct!",    "mistake": None,                                                     "working": steps},
        {"value": divided,    "display": fmt_volt(divided),    "summary": "Incorrect.", "mistake": "You divided I by R instead of multiplying. V = I × R.",    "working": steps},
        {"value": inverted,   "display": fmt_volt(inverted),   "summary": "Incorrect.", "mistake": "You divided R by I. V = I × R.",                           "working": steps},
        {"value": prefix_err, "display": fmt_volt(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                 "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "V",
        scaffold=[],
        notes=NOTES["ohms_law"],
    )


# =========================================================
# V = IR  —  FIND I
# =========================================================

def gen_vir_find_i():
    v_disp, v_unit, v_si = _pick_voltage()
    r_disp, r_unit, r_si = _pick_resistance()
    correct = round_sf(v_si / r_si)

    multiplied = round_sf(v_si * r_si)
    inverted   = round_sf(r_si / v_si)

    if v_unit != "V":
        prefix_err = round_sf(v_disp / r_si)
        prefix_msg = (
            f"You used V = {v_disp} without converting from {v_unit} to V. "
            f"{v_disp} {v_unit} = {v_si} V."
        )
    elif r_unit != "Ω":
        prefix_err = round_sf(v_si / r_disp)
        prefix_msg = (
            f"You used R = {r_disp} without converting from {r_unit} to Ω. "
            f"{r_disp} {r_unit} = {r_si} Ω."
        )
    else:
        prefix_err = round_sf(v_si * r_si)
        prefix_msg = "You multiplied V × R instead of dividing. I = V ÷ R."

    steps = [
        {"type": "text", "content": "Rearrange V = IR to find I:"},
        {"type": "latex", "content": r"I = \frac{V}{R}"},
    ]
    if v_unit != "V":
        steps.append({"type": "latex", "content":
                       rf"V = {v_disp}\ \mathrm{{{v_unit}}} = {v_si}\ \mathrm{{V}}"})
    if r_unit != "Ω":
        steps.append({"type": "latex", "content":
                       rf"R = {r_disp}\ \mathrm{{{r_unit}}} = {r_si}\ \mathrm{{\Omega}}"})
    steps += [
        {"type": "latex", "content": rf"I = \frac{{{v_si}}}{{{r_si}}}"},
        {"type": "latex", "content": rf"I = {fmt_amp(correct)}"},
    ]

    ctx = random.choice(_CONTEXTS)
    question = (
        f"{ctx} with a resistance of {r_disp} {r_unit} has a voltage of "
        f"{v_disp} {v_unit} across it.\n\n"
        f"Calculate the current through it."
    )

    options_data = [
        {"value": correct,    "display": fmt_amp(correct),    "summary": "Correct!",    "mistake": None,                                                     "working": steps},
        {"value": multiplied, "display": fmt_amp(multiplied), "summary": "Incorrect.", "mistake": "You multiplied V × R instead of dividing. I = V ÷ R.",    "working": steps},
        {"value": inverted,   "display": fmt_amp(inverted),   "summary": "Incorrect.", "mistake": "You divided R by V. I = V ÷ R.",                          "working": steps},
        {"value": prefix_err, "display": fmt_amp(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "A",
        scaffold=[],
        notes=NOTES["ohms_law"],
    )


# =========================================================
# V = IR  —  FIND R
# =========================================================

def gen_vir_find_r():
    v_disp, v_unit, v_si = _pick_voltage()
    i_disp, i_unit, i_si = _pick_current()
    correct = round_sf(v_si / i_si)

    multiplied = round_sf(v_si * i_si)
    inverted   = round_sf(i_si / v_si)

    if v_unit != "V":
        prefix_err = round_sf(v_disp / i_si)
        prefix_msg = (
            f"You used V = {v_disp} without converting from {v_unit} to V. "
            f"{v_disp} {v_unit} = {v_si} V."
        )
    elif i_unit != "A":
        prefix_err = round_sf(v_si / i_disp)
        prefix_msg = (
            f"You used I = {i_disp} without converting from {i_unit} to A. "
            f"{i_disp} {i_unit} = {i_si} A."
        )
    else:
        prefix_err = round_sf(v_si * i_si)
        prefix_msg = "You multiplied V × I instead of dividing. R = V ÷ I."

    steps = [
        {"type": "text", "content": "Rearrange V = IR to find R:"},
        {"type": "latex", "content": r"R = \frac{V}{I}"},
    ]
    if v_unit != "V":
        steps.append({"type": "latex", "content":
                       rf"V = {v_disp}\ \mathrm{{{v_unit}}} = {v_si}\ \mathrm{{V}}"})
    if i_unit != "A":
        steps.append({"type": "latex", "content":
                       rf"I = {i_disp}\ \mathrm{{{i_unit}}} = {i_si}\ \mathrm{{A}}"})
    steps += [
        {"type": "latex", "content": rf"R = \frac{{{v_si}}}{{{i_si}}}"},
        {"type": "latex", "content": rf"R = {fmt_ohm(correct)}"},
    ]

    ctx = random.choice(_CONTEXTS)
    question = (
        f"{ctx} has a current of {i_disp} {i_unit} flowing through it "
        f"when a voltage of {v_disp} {v_unit} is applied.\n\n"
        f"Calculate the resistance."
    )

    options_data = [
        {"value": correct,    "display": fmt_ohm(correct),    "summary": "Correct!",    "mistake": None,                                                     "working": steps},
        {"value": multiplied, "display": fmt_ohm(multiplied), "summary": "Incorrect.", "mistake": "You multiplied V × I instead of dividing. R = V ÷ I.",    "working": steps},
        {"value": inverted,   "display": fmt_ohm(inverted),   "summary": "Incorrect.", "mistake": "You divided I by V. R = V ÷ I.",                          "working": steps},
        {"value": prefix_err, "display": fmt_ohm(prefix_err), "summary": "Incorrect.", "mistake": prefix_msg,                                                "working": steps},
    ]

    return format_mcq(
        question, correct, options_data, "Ω",
        scaffold=[],
        notes=NOTES["ohms_law"],
    )


# =========================================================
# QUESTION LIST
# =========================================================

_GENERATORS = [
    gen_vir_find_v,
    gen_vir_find_i,
    gen_vir_find_r,
]


def generate_single_mcq_vir():
    return random.choice(_GENERATORS)()


def generate_ohms_law_mcqs(num=5):
    questions = []
    for _ in range(num):
        questions.append(generate_single_mcq_vir())
    return questions
