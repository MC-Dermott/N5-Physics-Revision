import random
from utils.mcq_utils import format_mcq

HALF_LIFE_OPTIONS = [
    (2,  "s"),   (5,  "s"),   (10, "s"),   (30, "s"),
    (2,  "min"), (5,  "min"), (10, "min"), (30, "min"),
    (1,  "h"),   (2,  "h"),   (6,  "h"),   (12, "h"),
    (1,  "day"), (2,  "day"), (5,  "day"), (8,  "day"), (10, "day"),
    (2,  "year"),(5,  "year"),(10, "year"),
]

# All divisible by 8 so n=1,2,3 half-lives give clean integer results
A0_OPTIONS = [800, 1600, 3200, 6400]

N_OPTIONS = [2, 3]


def round_sf(value, sf=3):
    if value == 0:
        return 0.0
    return float(f"{value:.{sf}g}")


def _time_str(val, unit):
    if val == 1:
        return f"1 {unit}"
    return f"{val} {unit}s" if unit in ("day", "year") else f"{val} {unit}"


def _pick_distractors(candidates_with_mistakes, correct_val):
    """Return up to 3 (value, mistake) pairs distinct from correct and from each other."""
    seen = {round_sf(correct_val)}
    result = []
    for val, mistake in candidates_with_mistakes:
        v = round_sf(val) if val > 0 else None
        if v and v not in seen:
            seen.add(v)
            result.append((v, mistake))
        if len(result) == 3:
            break
    return result


# =========================================================
# WORKING BUILDERS
# =========================================================

def _forward_working(A0, n, T_half, t_total, t_unit):
    # Build arrow chain: A0 → A0/2 → A0/4 → …
    values = [A0]
    current = A0
    for _ in range(n):
        current = current // 2
        values.append(current)
    arrow_chain = r" \rightarrow ".join(str(v) for v in values)

    return [
        {"type": "text", "content": "Find the number of half-lives that have passed:"},
        {"type": "latex",
         "content": rf"n = \frac{{t}}{{T_{{1/2}}}} = \frac{{{t_total}}}{{{T_half}}} = {n}"},
        {"type": "text", "content": "Halve the activity once for each half-life:"},
        {"type": "latex", "content": rf"{arrow_chain}\ \mathrm{{Bq}}"},
    ]


def _backward_working(A_now, n, T_half, t_total, t_unit):
    # Build arrow chain going backwards: A_now → 2A → 4A → …
    values = [A_now]
    current = A_now
    for _ in range(n):
        current = current * 2
        values.append(current)
    arrow_chain = r" \rightarrow ".join(str(v) for v in values)

    return [
        {"type": "text", "content": "Find the number of half-lives to go back:"},
        {"type": "latex",
         "content": rf"n = \frac{{t}}{{T_{{1/2}}}} = \frac{{{t_total}}}{{{T_half}}} = {n}"},
        {"type": "text", "content": "Double the activity once for each half-life going backwards:"},
        {"type": "latex", "content": rf"{arrow_chain}\ \mathrm{{Bq}}"},
    ]


def _half_life_working(A0, A_final, n, t_total, T_half):
    steps = [
        {"type": "text", "content": "Count the number of half-lives by halving the initial activity:"},
    ]
    current = A0
    for _ in range(n):
        nxt = current // 2
        steps.append({"type": "latex",
                       "content": rf"{current}\ \div\ 2 = {nxt}\ \mathrm{{Bq}}"})
        current = nxt
    steps += [
        {"type": "latex", "content": rf"\therefore\ n = {n}\ \text{{half-lives}}"},
        {"type": "text", "content": "Calculate the half-life:"},
        {"type": "latex", "content": r"T_{1/2} = \frac{t}{n}"},
        {"type": "latex", "content": rf"T_{{1/2}} = \frac{{{t_total}}}{{{n}}} = {T_half}"},
    ]
    return steps


# =========================================================
# TYPE 1 FORWARD — find activity after n half-lives
# =========================================================

def generate_forward_activity():
    T_half, t_unit = random.choice(HALF_LIFE_OPTIONS)
    n = random.choice(N_OPTIONS)
    A0 = random.choice(A0_OPTIONS)
    t_total = n * T_half
    A_final = A0 // (2 ** n)

    working = _forward_working(A0, n, T_half, t_total, t_unit)

    candidates = [
        (A0 * (2 ** n),
         f"Activity halves each half-life — it does not double. "
         f"After {n} half-life{'s' if n>1 else ''}: divide by 2^{n} = {2**n}."),
        (A0 // 2,
         f"{n} half-life{'s have' if n>1 else ' has'} passed, so divide by "
         f"2^{n} = {2**n}, not just 2."),
        (A0,
         "The activity must decrease. Apply the halving rule n times."),
        (A0 // 4,
         f"Check how many half-lives have passed: n = {t_total} ÷ {T_half} = {n}."),
        (A0 // 3,
         f"Divide by 2^n = {2**n}, not by 3. Each half-life halves the activity."),
        (A0 * n,
         "Activity decreases each half-life. Divide by 2 for each half-life, not multiply."),
        (A0 * 2,
         "Activity decreases each half-life. Divide by 2 for each half-life, not multiply."),
    ]
    distractors = _pick_distractors(candidates, A_final)

    question = (
        f"A radioactive source has an initial activity of {A0} Bq. "
        f"The half-life of the source is {_time_str(T_half, t_unit)}.\n\n"
        f"Calculate the activity after {_time_str(t_total, t_unit)}."
    )

    options_data = [{"value": A_final, "summary": "Correct!", "mistake": None, "working": working}]
    for val, mistake in distractors:
        options_data.append({"value": val, "summary": "Incorrect.",
                              "mistake": mistake, "working": working})

    return format_mcq(question, A_final, options_data, "Bq")


# =========================================================
# TYPE 1 BACKWARD — find original activity n half-lives ago
# =========================================================

def generate_backward_activity():
    T_half, t_unit = random.choice(HALF_LIFE_OPTIONS)
    n = random.choice(N_OPTIONS)
    A0 = random.choice(A0_OPTIONS)
    t_total = n * T_half
    A_now = A0 // (2 ** n)   # this is the *given* current activity

    working = _backward_working(A_now, n, T_half, t_total, t_unit)

    candidates = [
        (A_now // (2 ** n),
         "Going back in time, activity increases (multiply by 2^n). "
         "Dividing gives the wrong direction."),
        (A_now * n,
         f"Multiply by 2^n = {2**n}, not by n = {n}. "
         "Each half-life doubles the activity going backwards."),
        (A_now // 2,
         "Going backwards in time the activity was larger, not smaller. "
         "Multiply by 2 for each half-life."),
        (A_now * 2,
         f"{n} half-life{'s' if n>1 else ''} ago the activity was {A0} Bq. "
         f"Double {n} time{'s' if n>1 else ''} to reverse {n} half-life{'s' if n>1 else ''}."),
        (A_now,
         "The activity must have been higher in the past. Multiply by 2 for each half-life."),
        (A_now // 4,
         "Going backwards in time multiply by 2 (not divide) for each half-life."),
        (A_now * (2 ** n + 1),
         "Check your calculation — multiply by 2 exactly n times going backwards."),
    ]
    distractors = _pick_distractors(candidates, A0)

    question = (
        f"A radioactive source currently has an activity of {A_now} Bq. "
        f"The half-life of the source is {_time_str(T_half, t_unit)}.\n\n"
        f"Calculate the activity of the source {_time_str(t_total, t_unit)} ago."
    )

    options_data = [{"value": A0, "summary": "Correct!", "mistake": None, "working": working}]
    for val, mistake in distractors:
        options_data.append({"value": val, "summary": "Incorrect.",
                              "mistake": mistake, "working": working})

    return format_mcq(question, A0, options_data, "Bq")


# =========================================================
# TYPE 2 — find half-life given A0, A_final, total time
# =========================================================

def generate_half_life():
    T_half, t_unit = random.choice(HALF_LIFE_OPTIONS)
    n = random.choice(N_OPTIONS)
    A0 = random.choice(A0_OPTIONS)
    t_total = n * T_half
    A_final = A0 // (2 ** n)

    working = _half_life_working(A0, A_final, n, t_total, T_half)

    candidates = [
        (t_total,
         f"You need to count how many half-lives passed first (n = {n}), "
         f"then T½ = t ÷ n = {t_total} ÷ {n}."),
        (t_total * n,
         f"T½ = t ÷ n = {t_total} ÷ {n}. Do not multiply t by n."),
        (T_half * 2,
         f"Count the halvings carefully: {A0} → ... → {A_final} takes {n} half-life{'s' if n>1 else ''}."),
        (T_half * n,
         f"T½ = t ÷ n, not T½ × n. The half-life is {T_half} {t_unit}."),
        (T_half + 1,
         f"Count the halvings to get n = {n}, then T½ = {t_total} ÷ {n}."),
        (t_total * 2,
         f"T½ = t ÷ n = {t_total} ÷ {n}. Do not multiply."),
        (T_half * 3,
         f"The correct number of half-lives is n = {n}, giving T½ = {t_total} ÷ {n}."),
        (T_half // 2 if T_half >= 2 else T_half * 4,
         f"Count the halvings: n = {n}, so T½ = {t_total} ÷ {n} = {T_half}."),
    ]
    distractors = _pick_distractors(candidates, T_half)

    question = (
        f"A radioactive source has an initial activity of {A0} Bq. "
        f"After {_time_str(t_total, t_unit)}, the activity has fallen to {A_final} Bq.\n\n"
        f"Calculate the half-life of the source."
    )

    options_data = [{"value": T_half, "summary": "Correct!", "mistake": None, "working": working}]
    for val, mistake in distractors:
        options_data.append({"value": val, "summary": "Incorrect.",
                              "mistake": mistake, "working": working})

    return format_mcq(question, T_half, options_data, t_unit)


# =========================================================
# TOP-LEVEL GENERATOR
# =========================================================

QUESTION_GENERATORS = [
    generate_forward_activity,
    generate_backward_activity,
    generate_half_life,
]


def generate_half_life_mcqs(num=5):
    questions = []
    for _ in range(num):
        fn = random.choice(QUESTION_GENERATORS)
        questions.append(fn())
    return questions
