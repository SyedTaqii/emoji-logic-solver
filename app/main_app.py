import streamlit as st
from app.utils import load_config, save_solved_problem
from models.solver import EmojiMathSolver
from models.evaluator import SolutionEvaluator
import os
import json

# Load config
config = load_config()

# Instantiate models
solver = EmojiMathSolver(model_name=config["solver_model_name"], use_openai=config["use_openai"])
evaluator = SolutionEvaluator(
    model_name_1=config["evaluator_model_1"],
    model_name_2=config["evaluator_model_2"],
    use_openai=config["use_openai"]
)

# --- Streamlit App ---
st.set_page_config(page_title="Emoji Math Solver 🧠✨", page_icon="🧩", layout="wide")

st.title("🧩 Emoji Math Solver + Auto Evaluation")

st.markdown("""
Enter an emoji-based math problem like "🍕 + 🍕 + 🍕 = 9" and see the step-by-step solution plus auto-evaluation from two LLM judges! 🚀
""")

problem_input = st.text_input("Enter your Emoji Math Problem:", placeholder="Example: 🍕 + 🍕 + 🍕 = 9")

if st.button("Solve Puzzle 🚀"):
    if problem_input.strip() == "":
        st.warning("Please enter a valid emoji problem!")
    else:
        with st.spinner("Solving the problem..."):
            solution_output = solver.solve(problem_input)
            solution_text = "\n".join(solution_output["solver_steps"]) + f"\nFinal Answer: {solution_output['final_answer']}"

        st.subheader("🧠 Solver's Solution")
        st.code(solution_text)

        with st.spinner("Evaluating the solution..."):
            evaluation = evaluator.evaluate(problem_input, solution_text)

        st.subheader("✅ Evaluation by Two LLMs")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Model 1 Evaluation")
            st.json(evaluation["evaluation_by_model_1"])

        with col2:
            st.markdown("### Model 2 Evaluation")
            st.json(evaluation["evaluation_by_model_2"])

        save_solved_problem(
            problem=problem_input,
            solution_steps=solution_output["solver_steps"],
            final_answer=solution_output["final_answer"],
            evaluation=evaluation,
            filepath=config["solved_output_path"]
        )

st.markdown("---")
st.subheader("📜 Solved Problems History")

if st.button("Load Solved History"):
    if os.path.exists(config["solved_output_path"]):
        with open(config["solved_output_path"], "r", encoding="utf-8") as f:
            history = json.load(f)

        for idx, item in enumerate(history[::-1][:config["max_history_display"]]):
            st.markdown(f"**{idx+1}.** {item['problem']}")
            st.markdown(f"Solution Steps: {item['solver_steps']}")
            st.markdown(f"Final Answer: {item['final_answer']}")
            st.markdown("---")
    else:
        st.info("No problems solved yet!")
