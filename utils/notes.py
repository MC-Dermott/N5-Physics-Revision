NOTES = {

    "speed_distance_time": """
## Speed, Distance and Time — $d = vt$

**Key equation:**
$$d = vt$$

| Symbol | Quantity | Unit |
|---|---|---|
| d | Distance | m (metres) |
| v | Speed (or average speed $\\bar{v}$) | m/s |
| t | Time | s (seconds) |

**Rearrangements:**
$$v = \\frac{d}{t} \\qquad t = \\frac{d}{v}$$

**Unit conversions:**

| To convert | Multiply by |
|---|---|
| km → m | × 1000 |
| minutes → s | × 60 |
| hours → s | × 3600 |

> **Important:** Always convert distance to metres and time to seconds before substituting.
""",

    "resistor_combinations": """
## Resistor Combinations

**Series** (resistors in a single chain):
$$R_T = R_1 + R_2 + R_3$$

**Parallel** (resistors across the same two points):
$$\\frac{1}{R_T} = \\frac{1}{R_1} + \\frac{1}{R_2} + \\frac{1}{R_3}$$

For two resistors in parallel this simplifies to:
$$R_T = \\frac{R_1 \\times R_2}{R_1 + R_2}$$

**Mixed circuits — work step by step:**
1. Identify the pair that is combined first (series or parallel)
2. Replace that pair with its equivalent resistance $R_{ab}$
3. Combine $R_{ab}$ with the remaining resistor using the appropriate formula

| Arrangement | Step 1 | Step 2 |
|---|---|---|
| $(R_1 + R_2) \\parallel R_3$ | $R_{12} = R_1 + R_2$ | $R_T = \\frac{R_{12} \\times R_3}{R_{12} + R_3}$ |
| $(R_1 \\parallel R_2) + R_3$ | $R_{12} = \\frac{R_1 R_2}{R_1 + R_2}$ | $R_T = R_{12} + R_3$ |

> **Important:** In parallel, the total resistance is always **less** than the smallest individual resistor.
""",

    "ohms_law": """
## Ohm's Law — $V = IR$

**Key equation:**
$$V = IR$$

| Symbol | Quantity | Unit |
|---|---|---|
| V | Voltage (potential difference) | V (Volts) |
| I | Current | A (Amperes) |
| R | Resistance | Ω (Ohms) |

**Rearrangements:**
$$I = \\frac{V}{R} \\qquad R = \\frac{V}{I}$$

**Prefix conversions:**

| Prefix | Symbol | Factor |
|---|---|---|
| milli | mA, mV | $\\times 10^{-3}$ |
| kilo | kΩ | $\\times 10^{3}$ |

> **Important:** Convert mA to A (÷ 1000) and kΩ to Ω (× 1000) before substituting.
""",

    "radiation_activity": """
## Activity — $A = \\frac{N}{t}$

**Key equation:**
$$A = \\frac{N}{t}$$

| Symbol | Quantity | Unit |
|---|---|---|
| A | Activity | Bq (Becquerels) |
| N | Number of nuclear decays | (none) |
| t | Time | s (seconds) |

**Rearrangements:**
$$N = At \\qquad t = \\frac{N}{A}$$

**Time conversions:**
$$1\\ \\text{minute} = 60\\ \\text{s} \\qquad 1\\ \\text{hour} = 3600\\ \\text{s}$$

> **Important:** One Becquerel = one decay per second. Always convert time to seconds.
""",

    "dynamics_newton": """
## Newton's Second Law — F = ma

**Key equation:**
$$F = ma$$

| Symbol | Quantity | Unit |
|---|---|---|
| F | Force (unbalanced/resultant) | N (Newtons) |
| m | Mass | kg (kilograms) |
| a | Acceleration | m/s² |

**Rearrangements:**
$$a = \\frac{F}{m} \\qquad m = \\frac{F}{a}$$

> **Important:** Use the *resultant* (unbalanced) force — the net force after subtracting friction from driving force.
""",

    "dynamics_weight": """
## Weight — W = mg

**Key equation:**
$$W = mg$$

| Symbol | Quantity | Unit |
|---|---|---|
| W | Weight | N (Newtons) |
| m | Mass | kg (kilograms) |
| g | Gravitational field strength | N/kg |

**Rearrangements:**
$$m = \\frac{W}{g} \\qquad g = \\frac{W}{m}$$

> **Important:** On Earth, $g = 9.81$ N/kg. Always check which planet/body you are on. Convert grams to kilograms before substituting ($\\div 1000$).
""",

    "energy_gpe": """
## Gravitational Potential Energy — $E_p = mgh$

**Key equation:**
$$E_p = mgh$$

| Symbol | Quantity | Unit |
|---|---|---|
| $E_p$ | Gravitational potential energy | J (Joules) |
| m | Mass | kg |
| g | Gravitational field strength | N/kg |
| h | Height | m |

**Rearrangements:**
$$m = \\frac{E_p}{gh} \\qquad h = \\frac{E_p}{mg}$$

> **Important:** Convert grams to kg ($\\div 1000$). Use $g = 9.8$ or $10$ N/kg as given.
""",

    "energy_ke": """
## Kinetic Energy — $E_k = \\frac{1}{2}mv^2$

**Key equation:**
$$E_k = \\frac{1}{2}mv^2$$

| Symbol | Quantity | Unit |
|---|---|---|
| $E_k$ | Kinetic energy | J (Joules) |
| m | Mass | kg |
| v | Speed/velocity | m/s |

**Rearrangements:**
$$m = \\frac{2E_k}{v^2} \\qquad v = \\sqrt{\\frac{2E_k}{m}}$$

> **Important:** Don't forget the $\\frac{1}{2}$ factor. Square root when finding $v$.
""",

    "energy_work": """
## Work Done — $E_W = Fd$

**Key equation:**
$$E_W = Fd$$

| Symbol | Quantity | Unit |
|---|---|---|
| $E_W$ | Work done (energy transferred) | J (Joules) |
| F | Force | N (Newtons) |
| d | Distance moved in direction of force | m |

**Rearrangements:**
$$F = \\frac{E_W}{d} \\qquad d = \\frac{E_W}{F}$$

> **Important:** The distance must be in the same direction as the force.
""",

    "waves_speed": """
## Wave Speed — $v = f\\lambda$

**Key equation:**
$$v = f\\lambda$$

| Symbol | Quantity | Unit |
|---|---|---|
| v | Wave speed | m/s |
| f | Frequency | Hz |
| $\\lambda$ | Wavelength | m |

**Rearrangements:**
$$f = \\frac{v}{\\lambda} \\qquad \\lambda = \\frac{v}{f}$$

**Key values:**
- Speed of light (all EM waves): $c = 3 \\times 10^8$ m/s
- Speed of sound in air: $v \\approx 340$ m/s

> **Important:** Convert all units to SI before substituting (nm → m, MHz → Hz, etc.).
""",

    "waves_period": """
## Period and Frequency — $T = \\frac{1}{f}$

**Key equation:**
$$T = \\frac{1}{f} \\qquad f = \\frac{1}{T}$$

| Symbol | Quantity | Unit |
|---|---|---|
| T | Period (time for one complete wave) | s |
| f | Frequency (waves per second) | Hz |

**Prefix conversions:**
| Prefix | Symbol | Factor |
|---|---|---|
| kilo | kHz | $\\times 10^3$ |
| mega | MHz | $\\times 10^6$ |
| giga | GHz | $\\times 10^9$ |
| milli | ms | $\\times 10^{-3}$ |
| micro | μs | $\\times 10^{-6}$ |

> **Important:** Period and frequency are reciprocals of each other. Convert to base SI units (Hz, s) before calculating.
""",

    "electricity_current": """
## Electric Current — $I = \\frac{Q}{t}$

**Key equation:**
$$I = \\frac{Q}{t}$$

| Symbol | Quantity | Unit |
|---|---|---|
| I | Current | A (Amperes) |
| Q | Charge | C (Coulombs) |
| t | Time | s (seconds) |

**Rearrangements:**
$$Q = It \\qquad t = \\frac{Q}{I}$$

> **Important:** Convert time to seconds before substituting (minutes $\\times 60$).
""",

    "electricity_power": """
## Electrical Power

**Three forms of the power equation:**

$$P = VI \\qquad P = \\frac{V^2}{R} \\qquad P = I^2 R$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Power | W (Watts) |
| V | Voltage (potential difference) | V (Volts) |
| I | Current | A (Amperes) |
| R | Resistance | Ω (Ohms) |

**Useful rearrangements:**

From $P = VI$:
$$V = \\frac{P}{I} \\qquad I = \\frac{P}{V}$$

From $P = \\frac{V^2}{R}$:
$$V = \\sqrt{PR} \\qquad R = \\frac{V^2}{P}$$

From $P = I^2 R$:
$$I = \\sqrt{\\frac{P}{R}} \\qquad R = \\frac{P}{I^2}$$

**Prefix conversions:**

| Prefix | Symbol | Factor |
|---|---|---|
| milli | mW, mV, mA | $\\times 10^{-3}$ |
| kilo | kW, kV, kΩ | $\\times 10^{3}$ |
| mega | MW | $\\times 10^{6}$ |

> **Important:** Convert all values to SI units (W, V, A, Ω) before substituting into equations.
""",

    "electricity_power_energy": """
## Power from Energy — $P = \\frac{E}{t}$

**Key equation:**
$$P = \\frac{E}{t}$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Power | W (Watts) |
| E | Energy | J (Joules) |
| t | Time | s (seconds) |

**Rearrangements:**
$$E = Pt \\qquad t = \\frac{E}{P}$$

**Prefix conversions:**

| Prefix | Symbol | Factor |
|---|---|---|
| kilo | kJ, kW | $\\times 10^{3}$ |
| mega | MJ, MW | $\\times 10^{6}$ |

**Time conversions:**
$$1\\ \\text{minute} = 60\\ \\text{s} \\qquad 1\\ \\text{hour} = 3600\\ \\text{s}$$

> **Important:** Always convert energy to Joules, time to seconds, and power to Watts before substituting.
""",

    "radiation_doses": """
## Radiation Dose Equations

**Absorbed dose:**
$$D = \\frac{E}{m} \\quad \\text{(unit: Gray, Gy = J/kg)}$$

**Equivalent dose:**
$$H = D \\times w_R \\quad \\text{(unit: Sievert, Sv)}$$

**Equivalent dose rate:**
$$\\dot{H} = \\frac{H}{t} \\quad \\text{(unit: Sv/h)}$$

| Symbol | Quantity | Unit |
|---|---|---|
| D | Absorbed dose | Gy (Gray) |
| E | Energy absorbed | J |
| m | Mass of tissue | kg |
| H | Equivalent dose | Sv (Sievert) |
| $w_R$ | Radiation weighting factor | (none) |
| $\\dot{H}$ | Equivalent dose rate | Sv/h |

**Radiation weighting factors:**

| Type of radiation | $w_R$ |
|---|---|
| Alpha particles | 20 |
| Beta particles | 1 |
| Gamma rays | 1 |
| Fast neutrons | 20 |
| Slow neutrons | 3 |
| X-rays | 1 |

> **Important:** Absorbed dose uses Gray (Gy); equivalent dose uses Sievert (Sv). Don't mix them up.
""",

    "radiation_half_life": """
## Half-Life

**Key relationships:**

Number of half-lives:
$$n = \\frac{t}{T_{1/2}}$$

Activity after $n$ half-lives:
$$A = A_0 \\times \\left(\\frac{1}{2}\\right)^n$$

| Symbol | Quantity | Unit |
|---|---|---|
| $T_{1/2}$ | Half-life | s, min, h, days, years |
| t | Total time elapsed | same as $T_{1/2}$ |
| n | Number of half-lives | (none) |
| $A_0$ | Initial activity | Bq (Becquerels) |
| A | Activity after time t | Bq |

**Activity halving rule:**
- Each half-life → divide activity by 2
- Going backwards in time → multiply activity by 2

> **Important:** Activity is measured in Becquerels (Bq). The half-life is the time for activity to halve — not fall to zero.
""",

    "gas_laws": """
## Gas Laws

**Boyle's Law** (constant temperature):
$$P_1 V_1 = P_2 V_2$$

**Charles's Law** (constant pressure):
$$\\frac{V_1}{T_1} = \\frac{V_2}{T_2}$$

**Gay-Lussac's Law** (constant volume):
$$\\frac{P_1}{T_1} = \\frac{P_2}{T_2}$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Pressure | Pa or kPa |
| V | Volume | m³, cm³, mL, L (consistent units) |
| T | Temperature | **K (Kelvin)** |

**Temperature conversion:**
$$T(K) = T(°C) + 273$$

> **Important:** Temperature MUST be in Kelvin for Charles's and Gay-Lussac's laws. Adding 273, not subtracting.
""",

    "pressure": """
## Pressure — $P = \\frac{F}{A}$

**Key equations:**
$$P = \\frac{F}{A} \\qquad W = mg$$

| Symbol | Quantity | Unit |
|---|---|---|
| P | Pressure | Pa (Pascals) |
| F | Force (weight) | N (Newtons) |
| A | Area | m² |
| W | Weight | N |
| m | Mass | kg |
| g | Gravitational field strength | 9.8 N/kg |

**Rearrangements:**
$$F = PA \\qquad A = \\frac{F}{P}$$

> **Important:** The force exerted by a stationary object on the ground equals its weight ($W = mg$). Total contact area = number of tyres × area per tyre.
""",

    "heat_shc": """
## Specific Heat Capacity & Latent Heat

**Specific heat capacity (temperature change):**
$$E_H = mc\\Delta T$$

**Latent heat (change of state):**
$$E_H = mL$$

| Symbol | Quantity | Unit |
|---|---|---|
| $E_H$ | Energy transferred | J |
| m | Mass | kg |
| c | Specific heat capacity | J/kg°C |
| $\\Delta T$ | Temperature change | °C |
| L | Specific latent heat | J/kg |

**Key values for water:**
- $c = 4200$ J/kg°C (specific heat capacity)
- $L_{fusion} = 334\\,000$ J/kg (melting/freezing)
- $L_{vaporisation} = 2\\,260\\,000$ J/kg (boiling/condensing)

> **Important:** $\\Delta T = T_2 - T_1$ (the change, not the final temperature). Convert grams to kg. During a change of state, temperature stays constant.
""",

    "vectors": """
## Vectors — Resultant & Bearing

**Magnitude of resultant** (Pythagoras):
$$R = \\sqrt{a^2 + b^2}$$

**Direction (bearing):**
$$\\theta = \\tan^{-1}\\left(\\frac{\\text{opposite}}{\\text{adjacent}}\\right)$$

**Quadrant rules for bearing:**

| Quadrant | Direction | Bearing |
|---|---|---|
| Q1 | N of E | $\\theta$ |
| Q2 | N of W | $360° - \\theta$ |
| Q3 | S of W | $180° + \\theta$ |
| Q4 | S of E | $180° - \\theta$ |

> **Important:** Don't add or subtract components — use Pythagoras. Bearings are measured clockwise from North (000° to 360°).
""",

    "projectiles": """
## Projectile Motion

A projectile has **independent** horizontal and vertical motion.

**Horizontal** (constant velocity):
$$s_H = v_H \\times t$$

**Vertical** (acceleration due to gravity, $g = 9.8$ m/s²):

Velocity at time $t$: $\\quad v_v = gt$ (initial vertical velocity = 0)

Height fallen: $\\quad s = \\frac{1}{2}gt^2$

| Symbol | Quantity | Unit |
|---|---|---|
| $v_H$ | Horizontal velocity | m/s |
| $t$ | Time of flight | s |
| $s_H$ | Horizontal range | m |
| $v_v$ | Vertical velocity | m/s |
| s | Height fallen | m |
| g | Gravitational acceleration | 9.8 m/s² |

> **Important:** Horizontal speed stays constant throughout. Vertical speed starts at 0 and increases. Use area under v-t graph (triangle) for height: $s = \\frac{1}{2} \\times t \\times v_v$.
""",
}
