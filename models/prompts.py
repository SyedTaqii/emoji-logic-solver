SOLVER_PROMPT_TEMPLATE = """
You are a skilled math teacher. Solve the following emoji-based math problem step-by-step:

Problem: {problem}

Instructions:
- Clearly write each step (e.g., Step 1, Step 2, etc.)
- Show substitutions and simplifications.
- Give the final numeric answer clearly at the end, like: "Final Answer: X".

Begin solving:
"""

EVALUATOR_PROMPT_TEMPLATE = """
You are a strict math examiner.

Please evaluate the following emoji math solution.

Problem: {problem}
Model's Solution:
{solution}

Evaluate:
1. Correctness (Is the final answer right?): Yes / No
2. Reasoning Score (Rate from 1.0 to 5.0)
3. Explanation Clarity (Rate from 1.0 to 5.0)

Respond in JSON format like:
{
  "correctness": "Yes",
  "reasoning_score": 4.5,
  "explanation_clarity": 5.0
}
"""
