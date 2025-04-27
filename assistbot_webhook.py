from flask import Flask, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

# Load resources from Excel file
try:
    df = pd.read_excel('FindHelpOrg Data.xlsx')

    # Building a resources database from the Excel data
    resources_db = {
        "shelter": df[df['Type'].str.lower() == 'shelter']['Providor'].dropna().tolist(),
        "food": df[df['Type'].str.lower() == 'food']['Providor'].dropna().tolist(),
        "medical": df[df['Type'].str.lower() == 'medical']['Providor'].dropna().tolist()
    }
except Exception as e:
    print(f"Error loading resources: {e}")
    resources_db = {
        "shelter": ["Default Shelter - No data loaded"],
        "food": ["Default Food - No data loaded"],
        "medical": ["Default Medical - No data loaded"]
    }

# Caring messages for responses
caring_messages = {
    "shelter": [
        "I'm here to help you find a safe place. Here's a nearby shelter:",
        "Finding a shelter is important. Please consider visiting this place:"
    ],
    "food": [
        "You deserve to have a meal. Here's a food service that can assist:",
        "I found a place nearby where you can get food and support:"
    ],
    "medical": [
        "Taking care of your health is important. Here's a clinic that can help:",
        "There’s medical help nearby for you. Here’s where you can go:"
    ]
}

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print("Request received:", req)

    intent = req.get('queryResult', {}).get('intent', {}).get('displayName')
    parameters = req.get('queryResult', {}).get('parameters', {})

    need = parameters.get('need')  # food, shelter, medical
    city = parameters.get('city', "Austin")  # Default to Austin

    # Pick a caring message
    caring_message = random.choice(caring_messages.get(need, ["Here's a resource for you:"]))

    # Pick a random resource from the loaded list
    resource_list = resources_db.get(need, [])
    if resource_list:
        resource_info = random.choice(resource_list)
    else:
        resource_info = "Sorry, no resource found for your need."

    # Build the full caring response
    full_response = f"{caring_message} {resource_info}"

    response = {
        "fulfillmentText": full_response
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)

