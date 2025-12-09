import re

# Hashtag & phrase seeds (add/remove as you like)
UKR_POS = [
    r"#istandwithukraine", r"#standwithukraine", r"#slavaukraini", r"free ukraine",
    r"russia.(invad|occup|war crime)", r"support ukraine", r"putin.(dictator|criminal)",
    r"glory to ukraine", r"help ukraine", r"stop russia", r"#saveukraine", r"ukraine", r"ukrainian", r"kyiv", 
    r"slava ukraini", r"stand with ukraine", r"support ukraine", r"stop russia", r"russia war crimes", r"putin criminal", r"defend ukraine", r"ukraine victory"

]
RUS_POS = [
    r"#istandwithrussia", r"#supportrussia", r"#zov", r"#z", r"denazify", r"nato.*(provok|aggress)",
    r"support russia", r"russia will win", r"putin.*(strong|leader)", r"#russianspring", r"russia", r"putin", r"moscow", r"denazification", r"pro russia", 
    r"support russia", r"nato provoked", r"ukraine nazi", r"zelensky corrupt"

]

# Negation / sarcasm guards (very simple)
NEG_GUARDS = [r"not\s+sure", r"sarcasm", r"/s", r"lol", r"haha"]

def weak_label(text: str) -> str:
    """Return 'pro_ukraine' / 'pro_russia' / 'neutral' using seed rules."""
    t = (text or "").lower()

    # guard trivial non-English or empty
    if len(t) < 8:
        return "neutral"

    # remove urls/usernames
    t = re.sub(r"http\S+|@\w+", " ", t)

    # apply guards
    for g in NEG_GUARDS:
        if re.search(g, t):
            return "neutral"

    def any_match(patterns):
        return any(re.search(p, t) for p in patterns)

    ukr = any_match(UKR_POS)
    rus = any_match(RUS_POS)

    if ukr and not rus:
        return "pro_ukraine"
    if rus and not ukr:
        return "pro_russia"

    # fallback: weak cues
    if re.search(r"\b(ukraine)\b", t) and re.search(r"\b(russia|putin)\b", t):
        # neutral by default if both sides mentioned with no strong seeds
        return "neutral"

    return "neutral"