import os

import requests
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError(
        "API key not found. Please set OPENROUTER_API_KEY in your .env file."
    )


def load_yaml_data(file_path):
    """Loads YAML data from the given file path."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or []
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return []
    except yaml.YAMLError as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return []


def get_ai_response(model, question) -> tuple[str, int | None, Exception | None]:
    """Sends a request to OpenRouter API and retrieves AI response.

    Args:
        model (str): The OpenRouter model ID.
        question (str): The question to fetch the answer for.

    Returns:
        tuple[str, int | None, Exception | None]: The response, status code, and exception if any.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    system_prompt = """You are an expert in numerical linear algebra, specializing in computational methods.

For each question, provide a clear, step-by-step answer in plain text (no JSON, no LaTeX). Use numbered steps (e.g., 1., 2.) for clarity. Focus on computational algorithms, numerical stability, and complexity, drawing from Trefethen and Bau's 'Numerical Linear Algebra' and Golub and Van Loan's 'Matrix Computations'. Keep answers concise (<100 words), precise, and professional, using consistent notation (e.g., A for matrices, ||x||_2 for Euclidean norm). Avoid extra text outside the steps."""

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if response.status_code == 200:
            return (
                result["choices"][0]["message"]["content"].strip(),
                response.status_code,
                None,
            )
        return "Null", response.status_code, None
    except requests.RequestException as e:
        return "Null", getattr(response, "status_code", None), e
    except Exception as e:
        return "Null", getattr(response, "status_code", None), e


def save_to_yaml(data, output_path):
    """Save in plain format: question followed by answer in single-line block with internal newlines."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as file:
            for item in data:
                file.write(f"- question: {item['question'].strip()}\n")
                answer_lines = item["answer"].strip().splitlines()
                file.write(f"  answer: {answer_lines[0]}\n")
                for line in answer_lines[1:]:
                    file.write(f"    {line}\n")
        print(f"Data successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving data to YAML file: {e}")


def auto_save_yaml(data, output_path):
    """Auto-saves the data into a YAML file at intervals."""
    try:
        save_to_yaml(data, output_path)
        print(f"Auto-saved progress to {output_path}")
    except Exception as e:
        print(f"Error auto-saving to YAML: {e}")
