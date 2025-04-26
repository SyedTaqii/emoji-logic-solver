import yaml
import json
import os

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def save_solved_problem(problem: str, solution_steps: list, final_answer: int, evaluation: dict, filepath="outputs/solved_problems.json"):
    record = {
        "problem": problem,
        "solver_steps": solution_steps,
        "final_answer": final_answer,
        "evaluation": evaluation
    }

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
