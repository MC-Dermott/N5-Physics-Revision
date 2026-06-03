import random
from utils.mcq_utils import format_mcq
from utils.notes import NOTES

L_VAPORISATION = 2_260_000  # J/kg
L_FUSION = 334_000  # J/kg
C_WATER = 4200  # J/kg°C

GIVEN_DATA = (
    "| Property | Value |\n"
    "|---|---|\n"
    "| Specific latent heat of fusion of water | 334 000 J/kg |\n"
    "| Specific latent heat of vaporisation of water | 2 260 000 J/kg |\n"
    "| Specific heat capacity of water | 4200 J/kg °C |"
)


def fmt_J(j):
    """Format a J value using SI prefixes for display."""
    j = float(j)
    if abs(j) >= 1_000_000:
        return f"{j / 1_000_000:g} MJ"
    if abs(j) >= 1000:
        return f"{j / 1000:g} kJ"
    return f"{j:g} J"


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def pick_mass():
    """Returns (display_value, display_unit, mass_kg, is_grams, mass_g).

    mass_g is always the integer gram value; used for exact integer Q arithmetic.
    """
    mass_g = random.choice(range(100, 3100, 100))
    mass_kg = mass_g / 1000
    if mass_g < 1000:
        return mass_g, "g", mass_kg, True, mass_g
    return mass_kg, "kg", mass_kg, False, mass_g


def latent_q(mass_g, L):
    """Exact integer Q = m * L, avoiding floating-point drift."""
    return mass_g * L // 1000


def shc_q(mass_g, dt):
    """Exact integer Q = m * c * ΔT, avoiding floating-point drift."""
    return mass_g * C_WATER * dt // 1000


LATENT_SITUATIONS = {
    "water_to_steam": {
        "template": "A mass of {mass} of water is completely vaporised at 100 °C.",
        "L": L_VAPORISATION,
        "L_alt": L_FUSION,
        "L_name": "specific latent heat of vaporisation",
        "L_alt_name": "specific latent heat of fusion",
    },
    "steam_to_water": {
        "template": "A mass of {mass} of steam is completely condensed to water at 100 °C.",
        "L": L_VAPORISATION,
        "L_alt": L_FUSION,
        "L_name": "specific latent heat of vaporisation",
        "L_alt_name": "specific latent heat of fusion",
    },
    "ice_to_water": {
        "template": "A mass of {mass} of ice is completely melted at 0 °C.",
        "L": L_FUSION,
        "L_alt": L_VAPORISATION,
        "L_name": "specific latent heat of fusion",
        "L_alt_name": "specific latent heat of vaporisation",
    },
    "water_to_ice": {
        "template": "A mass of {mass} of water is completely frozen at 0 °C.",
        "L": L_FUSION,
        "L_alt": L_VAPORISATION,
        "L_name": "specific latent heat of fusion",
        "L_alt_name": "specific latent heat of vaporisation",
    },
}


# =========================================================
# WORKING BUILDERS
# =========================================================

def latent_Q_working(mass_kg, L, Q):
    return [
        {"type": "text", "content": "Use the equation:"},
        {"type": "latex", "content": r"E_H = mL"},
        {"type": "latex", "content": rf"E_H = {mass_kg} \times {L:,}\ \mathrm{{J/kg}}"},
        {"type": "latex", "content": rf"E_H = {Q:,}\ \mathrm{{J}}"},
    ]


def latent_m_working(Q, L, m):
    return [
        {"type": "text", "content": "Rearrange E_H = mL to find m:"},
        {"type": "latex", "content": r"m = \frac{E_H}{L}"},
        {"type": "latex", "content": rf"m = \frac{{{Q:,}}}{{{L:,}}}"},
        {"type": "latex", "content": rf"m = {m}\ \mathrm{{kg}}"},
    ]


def shc_Q_working(mass_kg, c, T1, T2, dt, Q):
    return [
        {"type": "text", "content": "First find the temperature change:"},
        {"type": "latex", "content": rf"\Delta T = {T2} - {T1} = {dt}\ \mathrm{{°C}}"},
        {"type": "text", "content": "Then use the equation:"},
        {"type": "latex", "content": r"E_H = mc\Delta T"},
        {"type": "latex", "content": rf"E_H = {mass_kg} \times {c}\ \mathrm{{J/kg\ °C}} \times {dt}"},
        {"type": "latex", "content": rf"E_H = {Q:,}\ \mathrm{{J}}"},
    ]


def shc_m_working(Q, c, dt, m):
    return [
        {"type": "text", "content": "Rearrange E_H = mcΔT to find m:"},
        {"type": "latex", "content": r"m = \frac{E_H}{c\Delta T}"},
        {"type": "latex", "content": rf"m = \frac{{{Q:,}}}{{{c} \times {dt}}}"},
        {"type": "latex", "content": rf"m = {m}\ \mathrm{{kg}}"},
    ]


def shc_dt_working(Q, mass_kg, c, dt):
    return [
        {"type": "text", "content": "Rearrange E_H = mcΔT to find ΔT:"},
        {"type": "latex", "content": r"\Delta T = \frac{E_H}{mc}"},
        {"type": "latex", "content": rf"\Delta T = \frac{{{Q:,}}}{{{mass_kg} \times {c}}}"},
        {"type": "latex", "content": rf"\Delta T = {dt}\ \mathrm{{°C}}"},
    ]


# =========================================================
# LATENT HEAT — CALCULATE ENERGY
# =========================================================

def make_latent_Q_mcq(situation_key):
    cfg = LATENT_SITUATIONS[situation_key]
    L = cfg["L"]
    L_alt = cfg["L_alt"]

    display_val, unit, mass_kg, is_grams, mass_g = pick_mass()
    mass_text = f"{display_val} {unit}"

    correct_Q = latent_q(mass_g, L)
    wrong_L_Q = latent_q(mass_g, L_alt)
    kj_error_Q = round_sf(correct_Q / 1000)
    both_L_Q = latent_q(mass_g, L + L_alt)

    question = (
        f"{cfg['template'].format(mass=mass_text)}\n\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the energy transferred."
    )

    working = latent_Q_working(mass_kg, L, correct_Q)

    if is_grams:
        grams_Q = latent_q(mass_g * 1000, L)
        options_data = [
            {
                "value": correct_Q,
                "display": fmt_J(correct_Q),
                "summary": "Correct!",
                "mistake": None,
                "working": working,
            },
            {
                "value": wrong_L_Q,
                "display": fmt_J(wrong_L_Q),
                "summary": "Incorrect.",
                "mistake": (
                    f"You used the {cfg['L_alt_name']} ({L_alt:,} J/kg) instead of "
                    f"the {cfg['L_name']} ({L:,} J/kg). "
                    "Check which change of state is happening."
                ),
                "working": working,
            },
            {
                "value": grams_Q,
                "display": fmt_J(grams_Q),
                "summary": "Incorrect.",
                "mistake": (
                    f"You substituted {display_val} into the equation without converting to kg. "
                    f"{display_val} g = {mass_kg} kg."
                ),
                "working": working,
            },
            {
                "value": kj_error_Q,
                "display": fmt_J(kj_error_Q),
                "summary": "Incorrect.",
                "mistake": (
                    "You divided the latent heat by 1000 before substituting. "
                    f"Use the value directly: L = {L:,} J/kg."
                ),
                "working": working,
            },
        ]
    else:
        options_data = [
            {
                "value": correct_Q,
                "display": fmt_J(correct_Q),
                "summary": "Correct!",
                "mistake": None,
                "working": working,
            },
            {
                "value": wrong_L_Q,
                "display": fmt_J(wrong_L_Q),
                "summary": "Incorrect.",
                "mistake": (
                    f"You used the {cfg['L_alt_name']} ({L_alt:,} J/kg) instead of "
                    f"the {cfg['L_name']} ({L:,} J/kg). "
                    "Check which change of state is happening."
                ),
                "working": working,
            },
            {
                "value": kj_error_Q,
                "display": fmt_J(kj_error_Q),
                "summary": "Incorrect.",
                "mistake": (
                    "You divided the latent heat by 1000 before substituting. "
                    f"Use the value directly: L = {L:,} J/kg."
                ),
                "working": working,
            },
            {
                "value": both_L_Q,
                "display": fmt_J(both_L_Q),
                "summary": "Incorrect.",
                "mistake": (
                    "You added both latent heat values together. "
                    f"Only the {cfg['L_name']} applies to this change of state."
                ),
                "working": working,
            },
        ]

    return format_mcq(question, correct_Q, options_data, "J",
                      scaffold=[],
                      notes=NOTES["heat_shc"])


# =========================================================
# LATENT HEAT — CALCULATE MASS
# =========================================================

def make_latent_m_mcq(situation_key):
    cfg = LATENT_SITUATIONS[situation_key]
    L = cfg["L"]
    L_alt = cfg["L_alt"]

    _, _, seed_mass, _, seed_mass_g = pick_mass()
    Q = latent_q(seed_mass_g, L)
    correct_m = seed_mass

    wrong_L_m = round_sf(Q / L_alt)
    grams_answer = round_sf(correct_m * 1000)
    both_L_m = round_sf(Q / (L + L_alt))

    desc = {
        "water_to_steam": "Water is completely vaporised at 100 °C.",
        "steam_to_water": "Steam is completely condensed to water at 100 °C.",
        "ice_to_water": "Ice is completely melted at 0 °C.",
        "water_to_ice": "Water is completely frozen at 0 °C.",
    }[situation_key]

    question = (
        f"{desc}\n\n"
        f"Energy transferred = {fmt_J(Q)}\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the mass."
    )

    working = latent_m_working(Q, L, correct_m)

    options_data = [
        {
            "value": correct_m,
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": wrong_L_m,
            "summary": "Incorrect.",
            "mistake": (
                f"You used the {cfg['L_alt_name']} ({L_alt:,} J/kg) instead of "
                f"the {cfg['L_name']} ({L:,} J/kg)."
            ),
            "working": working,
        },
        {
            "value": grams_answer,
            "summary": "Incorrect.",
            "mistake": (
                "Your answer is in grams, not kilograms. "
                "The equation E_H = mL gives mass in kg."
            ),
            "working": working,
        },
        {
            "value": both_L_m,
            "summary": "Incorrect.",
            "mistake": (
                "You divided E_H by the sum of both latent heat values. "
                f"Only the {cfg['L_name']} applies here."
            ),
            "working": working,
        },
    ]

    return format_mcq(question, correct_m, options_data, "kg",
                      scaffold=[],
                      notes=NOTES["heat_shc"])


# =========================================================
# SPECIFIC HEAT CAPACITY — CALCULATE ENERGY
# =========================================================

def make_shc_Q_mcq():
    display_val, unit, mass_kg, is_grams, mass_g = pick_mass()
    mass_text = f"{display_val} {unit}"

    # T1 starts from 5 so T2 ≠ ΔT (avoids T2-error collapsing with correct answer)
    t_values = list(range(5, 101, 5))
    T1 = random.choice(t_values[:-2])
    T2 = random.choice([t for t in t_values if t > T1])
    dt = T2 - T1

    correct_Q = shc_q(mass_g, dt)

    question = (
        f"Water of mass {mass_text} is heated from {T1} °C to {T2} °C.\n\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the energy transferred."
    )

    working = shc_Q_working(mass_kg, C_WATER, T1, T2, dt, correct_Q)

    v_T2 = shc_q(mass_g, T2)
    v_T1 = shc_q(mass_g, T1)

    options_data = [
        {
            "value": correct_Q,
            "display": fmt_J(correct_Q),
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": v_T2,
            "display": fmt_J(v_T2),
            "summary": "Incorrect.",
            "mistake": (
                f"You used T₂ = {T2} °C directly instead of the temperature change. "
                f"ΔT = {T2} − {T1} = {dt} °C."
            ),
            "working": working,
        },
        {
            "value": v_T1,
            "display": fmt_J(v_T1),
            "summary": "Incorrect.",
            "mistake": (
                f"You used T₁ = {T1} °C directly instead of the temperature change. "
                f"ΔT = {T2} − {T1} = {dt} °C."
            ),
            "working": working,
        },
    ]

    if is_grams:
        v_g = shc_q(mass_g * 1000, dt)
        options_data.append({
            "value": v_g,
            "display": fmt_J(v_g),
            "summary": "Incorrect.",
            "mistake": (
                f"You substituted {display_val} into the equation without converting to kg. "
                f"{display_val} g = {mass_kg} kg."
            ),
            "working": working,
        })
    else:
        v_sum = shc_q(mass_g, T1 + T2)
        options_data.append({
            "value": v_sum,
            "display": fmt_J(v_sum),
            "summary": "Incorrect.",
            "mistake": (
                f"You added T₁ and T₂ instead of subtracting. "
                f"ΔT = {T2} − {T1} = {dt} °C, not {T1} + {T2} = {T1 + T2} °C."
            ),
            "working": working,
        })

    return format_mcq(question, correct_Q, options_data, "J",
                      scaffold=[
                          {"question": "Calculate the temperature change ΔT.", "answer": float(dt), "unit": "°C"},
                          {"question": "Calculate the energy transferred.", "answer": float(correct_Q), "unit": "J"},
                      ],
                      notes=NOTES["heat_shc"])


# =========================================================
# SPECIFIC HEAT CAPACITY — CALCULATE MASS
# =========================================================

def make_shc_m_mcq():
    display_val, unit, mass_kg, is_grams, mass_g = pick_mass()
    dt = random.choice(range(5, 81, 5))

    Q = shc_q(mass_g, dt)
    correct_m = mass_kg

    grams_answer = round_sf(mass_kg * 1000)
    forgot_dt = round_sf(Q / C_WATER)
    swap_dt_error = round_sf(Q * dt / C_WATER)

    question = (
        f"Water is heated through a temperature change of {dt} °C.\n\n"
        f"Energy transferred = {fmt_J(Q)}\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the mass of water."
    )

    working = shc_m_working(Q, C_WATER, dt, correct_m)

    options_data = [
        {
            "value": correct_m,
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": grams_answer,
            "summary": "Incorrect.",
            "mistake": (
                "Your answer is in grams, not kilograms. "
                "The equation E_H = mcΔT uses mass in kg."
            ),
            "working": working,
        },
        {
            "value": forgot_dt,
            "summary": "Incorrect.",
            "mistake": (
                f"You divided E_H by c only, forgetting to also divide by ΔT = {dt} °C. "
                "m = E_H ÷ (c × ΔT)."
            ),
            "working": working,
        },
        {
            "value": swap_dt_error,
            "summary": "Incorrect.",
            "mistake": (
                f"You multiplied E_H by ΔT instead of dividing by it. "
                "m = E_H ÷ (c × ΔT)."
            ),
            "working": working,
        },
    ]

    return format_mcq(question, correct_m, options_data, "kg",
                      scaffold=[],
                      notes=NOTES["heat_shc"])


# =========================================================
# SPECIFIC HEAT CAPACITY — CALCULATE TEMPERATURE CHANGE
# =========================================================

def make_shc_dt_mcq():
    display_val, unit, mass_kg, is_grams, mass_g = pick_mass()
    mass_text = f"{display_val} {unit}"

    dt = random.choice(range(5, 81, 5))
    Q = shc_q(mass_g, dt)
    correct_dt = dt

    forgot_mass = round_sf(Q / C_WATER)
    swap_m_error = round_sf(Q * mass_kg / C_WATER)

    question = (
        f"Water of mass {mass_text} is heated.\n\n"
        f"Energy transferred = {fmt_J(Q)}\n"
        f"{GIVEN_DATA}\n\n"
        f"Calculate the temperature change."
    )

    working = shc_dt_working(Q, mass_kg, C_WATER, correct_dt)

    options_data = [
        {
            "value": correct_dt,
            "summary": "Correct!",
            "mistake": None,
            "working": working,
        },
        {
            "value": forgot_mass,
            "summary": "Incorrect.",
            "mistake": (
                "You divided E_H by c only, forgetting to divide by the mass. "
                "ΔT = E_H ÷ (m × c)."
            ),
            "working": working,
        },
        {
            "value": swap_m_error,
            "summary": "Incorrect.",
            "mistake": (
                "You multiplied by m instead of dividing. "
                "ΔT = E_H ÷ (m × c)."
            ),
            "working": working,
        },
    ]

    if is_grams:
        options_data.append({
            "value": round_sf(Q / (display_val * C_WATER)),
            "summary": "Incorrect.",
            "mistake": (
                f"You substituted {display_val} into the equation without converting to kg. "
                f"{display_val} g = {mass_kg} kg."
            ),
            "working": working,
        })
    else:
        options_data.append({
            "value": round_sf(Q / (mass_kg * 1000 * C_WATER)),
            "summary": "Incorrect.",
            "mistake": (
                f"You multiplied the mass by 1000 before substituting. "
                f"The mass is already in kg: {mass_kg} kg."
            ),
            "working": working,
        })

    return format_mcq(question, correct_dt, options_data, "°C",
                      scaffold=[],
                      notes=NOTES["heat_shc"])


# =========================================================
# TOP-LEVEL GENERATOR
# =========================================================

LATENT_SITUATION_KEYS = list(LATENT_SITUATIONS.keys())


def _latent_Q():
    return make_latent_Q_mcq(random.choice(LATENT_SITUATION_KEYS))


def _latent_m():
    return make_latent_m_mcq(random.choice(LATENT_SITUATION_KEYS))


QUESTION_GENERATORS = [
    _latent_Q,
    _latent_m,
    make_shc_Q_mcq,
    make_shc_m_mcq,
    make_shc_dt_mcq,
]


def generate_specific_heat_mcqs(num=5):
    questions = []
    for _ in range(num):
        fn = random.choice(QUESTION_GENERATORS)
        questions.append(fn())
    return questions
