from datetime import datetime

from config import BASE_PATH
from functions import auto_save_yaml, get_ai_response, load_yaml_data
from logger_answer import log_request

# File Paths
questions_path = f"{BASE_PATH}/data/questions/questions.yaml"
output_path = f"{BASE_PATH}/data/answers/o4-mini.yaml"

# Load Data
yaml_data = load_yaml_data(questions_path)

# AI Processing
output_data = []
auto_save_interval = 1
question_counter = 0
default_model = "openai/o4-mini"  # Fallback model

# Response language
# response_language = "english"

print("Starting Numerical Linear Algebra Question Processing\n")

for question_entry in yaml_data:
    question = question_entry.get("question", "Unknown Question")
    model = question_entry.get("model", default_model)  # Use model from YAML or default
    print(f"Processing question: {question[:50]}... (Model: {model})")

    # Get AI response
    ai_answer, status_code, api_error = get_ai_response(model, question)

    # Log API call
    log_request(
        timestamp=datetime.now().isoformat(),
        # language=response_language,
        section="Numerical Linear Algebra",
        question=question[:50] + "...",
        model=model,
        status_code=status_code,
        error=api_error,
    )
    print(f"\tOutput: {ai_answer[:50]}...")

    # Save response
    question_entry = {"question": question, "answer": ai_answer}
    if status_code == 403:
        question_entry["flagged"] = True

    output_data.append(question_entry)
    question_counter += 1

    # Auto-save
    if question_counter % auto_save_interval == 0:
        auto_save_yaml(output_data, output_path)

print(f"\nAll questions processed. Responses saved to:\n{output_path}")
print("Done.\n")
