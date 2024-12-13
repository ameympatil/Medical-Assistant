import json
import requests
from config import (
    system_message_er,
    system_message_rag,
    model_name,
    temperature,
    max_tokens_rag,
    max_tokens_er,
    stream,
)


def llm_entity_extraction(patient_details):
    """
    Extracts medical entities from patient details using a language model.

    Args:
        patient_details (str): The patient details to process.

    Returns:
        str: The extracted medical entities in JSON format.

    Raises:
        Exception: If the API request fails.
    """
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_message_er},
            {"role": "user", "content": patient_details},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "medical_summary_response",
                "strict": "true",
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "gender": {"type": "string"},
                        "age": {"type": "integer"},
                        "weight": {"type": "string"},
                        "height": {"type": "string"},
                        "BMI": {"type": "number"},
                        "chief_medical_complaint": {"type": "string"},
                    },
                    "required": [
                        "name",
                        "gender",
                        "age",
                        "weight",
                        "height",
                        "BMI",
                        "chief_medical_complaint",
                    ],
                },
            },
        },
        "temperature": temperature,
        "max_tokens": max_tokens_er,
        "stream": stream,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response_data = response.json()
        final_response = response_data["choices"][0]["message"]["content"]
        return final_response
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error during API request: {e}")


def llm_rag(query, context):
    """
    Performs retrieval-augmented generation using a language model.

    Args:
        query (str): The user query.
        context (str): The context to use for generating the response.

    Returns:
        str: The generated response.

    Raises:
        Exception: If the API request fails.
    """
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_message_rag.format(context)},
            {"role": "user", "content": query},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens_rag,
        "stream": stream,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        final_response = response_data["choices"][0]["message"]["content"]
        return final_response
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error during API request: {e}")
