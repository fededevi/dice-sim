import random
import math
from collections import Counter
import matplotlib.pyplot as plt

def roll_dices(n, sides):
    rolls = [random.randint(1, sides) for _ in range(n)]
    counts = Counter(rolls)
    return rolls, counts

def is_bad_bad(counts):
    return counts.get(1, 0) >= 4

def is_good_good(counts):
    return counts.get(6, 0) >= 4

def final_score_standard(counts):
    adjusted_counts = counts.copy()
    # Score calculation with floor on 4s count
    fours_score = math.floor(adjusted_counts.get(4, 0) / 2)
    score = adjusted_counts.get(5, 0) + adjusted_counts.get(6, 0) + fours_score - adjusted_counts.get(1, 0)

    # Check after adjustment
    if is_bad_bad(adjusted_counts):
        return -1
    elif is_good_good(adjusted_counts):
        return 4
    else:
        if score <= 0:
            return 0
        elif score == 1:
            return 1
        elif score == 2:
            return 2
        else:
            return 3

def final_score_balanced(counts):
    adjusted_counts = counts.copy()
    # Count all 4s fully (no floor, just add them as 1 each)
    score = adjusted_counts.get(5, 0) + adjusted_counts.get(6, 0) + adjusted_counts.get(4, 0) - adjusted_counts.get(1, 0)

    if is_bad_bad(adjusted_counts):
        return -1
    elif is_good_good(adjusted_counts):
        return 4
    else:
        if score <= 0:
            return 0
        elif score == 1:
            return 1
        elif score == 2:
            return 2
        else:
            return 3

def final_score_defensive(counts):
    adjusted_counts = counts.copy()
    if adjusted_counts.get(1, 0) > 0:
        adjusted_counts[1] -= 1
        if adjusted_counts[1] == 0:
            del adjusted_counts[1]
    # Then score as standard
    return final_score_standard(adjusted_counts)

def final_score_aggressive(counts):
    adjusted_counts = counts.copy()
    if adjusted_counts.get(6, 0) > 0:
        adjusted_counts[6] += 1
    # Then score as standard
    return final_score_standard(adjusted_counts)

# Number of simulations per dice count
NUM_SIMULATIONS = 25000

methods = {
    "standard": final_score_standard,
    "balanced": final_score_balanced,
    "defensive": final_score_defensive,
    "aggressive": final_score_aggressive,
}

results = {method: {} for method in methods}

for method_name, scoring_func in methods.items():
    print(f"Running simulations for {method_name}...")
    for n in range(1, 11):
        scores = []
        for _ in range(NUM_SIMULATIONS):
            _, counts = roll_dices(n, 6)
            score = scoring_func(counts)
            scores.append(score)
        results[method_name][n] = scores

# Plotting

fig, axs = plt.subplots(4, 10, figsize=(30, 12), sharey='row')
score_labels = [-1, 0, 1, 2, 3, 4]

for row, (method_name, method_results) in enumerate(results.items()):
    for col, n in enumerate(range(1, 11)):
        ax = axs[row, col]
        scores = method_results[n]

        freq = [scores.count(label) for label in score_labels]
        total = len(scores)
        probs = [f / total for f in freq]

        ax.bar(score_labels, probs, color='skyblue')
        if col == 0:
            ax.set_ylabel(f"{method_name}\nProbability")
        if row == 3:
            ax.set_xlabel(f"Dice: {n}")
        ax.set_xticks(score_labels)

        max_prob = max(probs)
        ax.set_ylim(0, max_prob * 1.1 if max_prob > 0 else 1)
        ax.grid(axis='y')


plt.tight_layout()
plt.savefig("output.png")  # Save the image