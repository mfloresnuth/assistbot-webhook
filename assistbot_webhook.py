from flask import Flask, request, jsonify

app = Flask(__name__)

# Example: Local resource database for Austin
resources_db = {
    "shelter": {
        "Austin": "Austin Resource Center for the Homeless (ARCH), 500 E 7th St, Austin, TX"
    },
    "food": {
        "Austin": "Caritas of Austin, 611 Neches St, Austin, TX"
    },
    "medical": {
        "Austin": "CommUnityCare Health Centers, multiple locations"
    }
}

# Dialogflow webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print("Request received:", req)  # For debugging purposes

    # Extract user intent and parameters
    intent = req.get('queryResult', {}).get('intent', {}).get('displayName')
    parameters = req.get('queryResult', {}).get('parameters', {})

    need = parameters.get('need')  # food, shelter, or medical
    city = parameters.get('city', "Austin")  # Default city is Austin

    # Look up the appropriate resource
    resource_info = resources_db.get(need, {}).get(city, "Sorry, no resources found for your request.")

    # Create a response back to Dialogflow
    response = {
        "fulfillmentText": f"For {need}, you can go to: {resource_info}"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)
