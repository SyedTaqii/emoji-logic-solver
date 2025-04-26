import random
import json

emoji_pool = ["🍕", "🍔", "🍟", "🌮", "🍎", "🍌", "🚗", "🚲", "🐶", "🐱", "🏀", "🎸", "🎈", "🎯", "🏡", "🛒"]

def generate_simple_equation():
    emoji1 = random.choice(emoji_pool)
    emoji2 = random.choice(emoji_pool)
    while emoji2 == emoji1:
        emoji2 = random.choice(emoji_pool)

    value1 = random.randint(1, 10)
    value2 = random.randint(1, 10)
    total = value1 + value2

    problem = f"{emoji1} + {emoji2} = {total}, {emoji2} = {value2}"
    solution_steps = [
        f"Step 1: {emoji2} = {value2}",
        f"Step 2: {emoji1} + {value2} = {total}",
        f"Step 3: {emoji1} = {total - value2}"
    ]
    final_answer = total - value2

    return {
        "problem": problem,
        "solver_steps": solution_steps,
        "final_answer": final_answer
    }

def generate_dataset(n_samples: int = 300):
    dataset = []
    for _ in range(n_samples):
        dataset.append(generate_simple_equation())
    return dataset

if __name__ == "__main__":
    dataset = generate_dataset(300)
    with open("data/raw_problems.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully generated {len(dataset)} emoji math puzzles!")
