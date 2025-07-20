import random
import math
from collections import Counter

def roll_dices(n, sides):
    rolls = [random.randint(1, sides) for _ in range(n)]
    counts = Counter(rolls)
    return rolls, counts

def is_bad_bad(counts):
    if counts.get(1, 0) >= 4:
        return True
    return False

def is_good_good(counts):
    if counts.get(6, 0) >= 4:
        return True
    return False

def score_standard(counts):
    fours_score = math.floor(counts.get(4, 0) / 2)
    score = counts.get(5, 0) + counts.get(6, 0) + fours_score - counts.get(1, 0)
    return score

def final_score(counts):
    if is_bad_bad(counts):
        return -1
    elif is_good_good(counts):
        return 4
    else:
        score = score_standard(counts)
        if score <= 0:
            return 0
        elif score == 1:
            return 1
        elif score == 2:
            return 2
        else:  # 3 or more
            return 3


print("\nSummary of rolls:")
for n in range(1, 11):  # from 1 to 10 dice
    print(f"\nRolling {n} dice:")
    rolls, counts = roll_dices(n, 6)

    print(f"  Rolls: {rolls}")
    for value in range(1, 7):
        print(f"  Value {value}: {counts.get(value, 0)} times")
    score = final_score(counts)
    print(f"  -> Final score: {score}")