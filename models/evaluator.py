from typing import Dict
from transformers import pipeline
import openai
from models.prompts import EVALUATOR_PROMPT_TEMPLATE

class SolutionEvaluator:
    def __init__(self, model_name_1: str, model_name_2: str, use_openai: bool = False):
        self.use_openai = use_openai
        if not use_openai:
            self.evaluator_1 = pipeline("text-generation", model=model_name_1, device=0)
            self.evaluator_2 = pipeline("text-generation", model=model_name_2, device=0)
        else:
            self.openai_model_1 = model_name_1
            self.openai_model_2 = model_name_2
            openai.api_key = "your-openai-api-key"

    def evaluate(self, problem: str, solution: str) -> Dict:
        prompt = EVALUATOR_PROMPT_TEMPLATE.format(problem=problem, solution=solution)

        eval1 = self._evaluate_single(prompt, evaluator_id=1)
        eval2 = self._evaluate_single(prompt, evaluator_id=2)

        return {
            "evaluation_by_model_1": eval1,
            "evaluation_by_model_2": eval2
        }

    def _evaluate_single(self, prompt: str, evaluator_id: int) -> Dict:
        if self.use_openai:
            model = self.openai_model_1 if evaluator_id == 1 else self.openai_model_2
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a strict math evaluator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=300
            )
            output_text = response['choices'][0]['message']['content']
        else:
            model = self.evaluator_1 if evaluator_id == 1 else self.evaluator_2
            output = model(prompt, max_length=512, do_sample=False)[0]
            output_text = output['generated_text']

        try:
            parsed = eval(output_text.strip())
        except Exception:
            parsed = {
                "correctness": "Unknown",
                "reasoning_score": 0.0,
                "explanation_clarity": 0.0
            }

        return parsed
