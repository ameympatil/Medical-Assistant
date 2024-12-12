import requests
import json
from config import system_message, model_name, temperature, max_tokens, stream


def llm_request(patient_deatils):
    # Define the API endpoint and request headers
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    # Define the request payload
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": patient_deatils},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check for errors
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")

    # Parse the JSON response
    response_data = response.json()
    final_response = response_data.result.choices[0].message.content
    return response_data
