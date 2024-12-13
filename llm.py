import requests
import json
from config import (
    system_message_er,
    system_message_rag,
    model_name,
    temperature,
    max_tokens_rag,
    max_tokens_er,
    stream,
)


def llm_entity_extraction(patient_deatils):
    # Define the API endpoint and request headers
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    # Define the request payload
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_message_er},
            {"role": "user", "content": patient_deatils},
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

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check for errors
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")

    # Parse the JSON response
    response_data = response.json()
    final_response = response_data["choices"][0]["message"]["content"]
    return final_response


def llm_rag(query, context):
    # Define the API endpoint and request headers
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    # Define the request payload
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

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check for errors
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")

    # Parse the JSON response
    response_data = response.json()
    final_response = response_data["choices"][0]["message"]["content"]
    return final_response
