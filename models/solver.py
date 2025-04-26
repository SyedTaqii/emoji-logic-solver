from typing import Dict
from transformers import pipeline
import openai
from models.prompts import SOLVER_PROMPT_TEMPLATE

class EmojiMathSolver:
    def __init__(self, model_name: str, use_openai: bool = False):
        self.use_openai = use_openai
        if not use_openai:
            self.generator = pipeline("text-generation", model=model_name, device=0)
        else:
            self.openai_model = model_name
            openai.api_key = "api-key"

    def solve(self, problem_text: str) -> Dict:
        prompt = SOLVER_PROMPT_TEMPLATE.format(problem=problem_text)

        if self.use_openai:
            response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are a math teacher skilled in solving emoji puzzles."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )
            output_text = response['choices'][0]['message']['content']
        else:
            output = self.generator(prompt, max_length=512, do_sample=False)[0]
            output_text = output['generated_text']

        parsed_result = self._parse_output(output_text)
        return parsed_result

    def _parse_output(self, output_text: str) -> Dict:
        steps = []
        final_answer = None

        for line in output_text.splitlines():
            line = line.strip()
            if line.lower().startswith("step"):
                steps.append(line)
            if "final answer" in line.lower() or "=" in line:
                try:
                    final_answer = int(''.join(filter(str.isdigit, line)))
                except:
                    final_answer = None

        return {
            "solver_steps": steps,
            "final_answer": final_answer
        }
