import zmq
import time

# Initialize ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5560")  # Port for the card grading microservice

print("Card Grading Microservice running on port 5560...")


def grade_card(condition):
    """Simulate grading based on condition (1 to 10)."""
    if condition >= 9:
        return "Mint"
    elif condition >= 7:
        return "Near Mint"
    elif condition >= 5:
        return "Good"
    else:
        return "Poor"


while True:
    print("\nWaiting for card grading request...")
    request = socket.recv_json()
    card_name = request.get("card_name")
    condition = request.get("condition")  # Expected: integer between 1 and 10

    # Validate condition
    if not isinstance(condition, (int, float)) or not (1 <= condition <= 10):
        response = f"Invalid condition '{condition}'. Please provide a value between 1 and 10."
    else:
        # Simulate grading
        print(f"Grading card '{card_name}' with condition {condition}...")
        time.sleep(2)  # Simulate processing delay

        grade = grade_card(condition)
        response = f"The card '{card_name}' is graded as: {grade}."

    print(response)
    socket.send_string(response)
