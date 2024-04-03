
from flask import Flask, jsonify
import requests

app = Flask(__name__)
PORT = 9876
WINDOW_SIZE = 10
TEST_SERVER_BASE_URL = 'http://20.244.56.144/test/'

window_numbers = []

# Headers with Authorization for accessing the test server
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzEyMTUwNjk3LCJpYXQiOjE3MTIxNTAzOTcsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6ImM0MjUwMWQyLTY1MmQtNGUwOS1iMDE5LTZkYjYxZGM1MDRiMSIsInN1YiI6Im5wNTQyN0Bzcm1pc3QuZWR1LmluIn0sImNvbXBhbnlOYW1lIjoibmVtb01hcnQiLCJjbGllbnRJRCI6ImM0MjUwMWQyLTY1MmQtNGUwOS1iMDE5LTZkYjYxZGM1MDRiMSIsImNsaWVudFNlY3JldCI6InJrZUt5QkRwcW5YdFZpbEsiLCJvd25lck5hbWUiOiJOaW1pc2giLCJvd25lckVtYWlsIjoibnA1NDI3QHNybWlzdC5lZHUuaW4iLCJyb2xsTm8iOiJSQTIxMTEwMjYwMTA0MDgifQ.s8xH2xHZcbBwWLAAmPldgIMfAk0V463GmIM2IChfYKo",
    "Content-Type": "application/json"
}
quals = {
    "e": "even",
    "p": "primes",
    "f": "fibo",
    "r": "rand"
}


# Fetch numbers from the test server
def fetch_numbers(qualifier):
    try:
        response = requests.get(TEST_SERVER_BASE_URL + quals[qualifier], headers=headers)
        return response.json().get('numbers', [])
    except Exception as e:
        print('Error fetching numbers:', e)
        return []


# Calculate average of numbers in the window
def calculate_average():
    if window_numbers:
        return sum(window_numbers) / len(window_numbers)
    else:
        return 0


# Route to handle API requests
@app.route('/numbers/<qualifier>', methods=['GET'])
def get_numbers(qualifier):
    global window_numbers

    # Fetch numbers from the test server
    numbers = fetch_numbers(qualifier)

    # update the window state
    if numbers:
        prev_window_state = window_numbers.copy()
        window_numbers = window_numbers[-(WINDOW_SIZE - len(numbers)):] + numbers
        avg = calculate_average()

        return jsonify({
            'numbers': numbers,
            'windowPrevState': prev_window_state,
            'windowCurrState': window_numbers,
            'avg': avg
        }), 200
    else:
        return jsonify({
            'numbers': [],
            'windowPrevState': window_numbers,
            'windowCurrState': window_numbers,
            'avg': calculate_average()
        }), 200


if __name__ == '__main__':
    app.run(port=PORT, use_reloader=True, debug=True)
