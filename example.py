#!/usr/bin/env python3
"""
Simple example demonstrating the Intent Controller's three decision paths:
1. Ask for more info (when information is missing)
2. Call API/tool (when all info is present)
3. Answer directly (for simple queries)
"""

from intent_controller import IntentController


def main():
    controller = IntentController()

    print("Intent Controller Example")
    print("=" * 50)

    # Example 1: Missing information - should ask for more info
    print("\n1. MISSING INFORMATION EXAMPLE:")
    print("Input: 'calculate'")
    result = controller.process_input("calculate")
    print(f"Action: {result['action_taken']}")
    response = result['result'].get(
        'response', result['result'].get('result', 'No response'))
    print(f"Response: {response}")

    # Example 2: Complete information - should call API
    print("\n2. COMPLETE INFORMATION EXAMPLE:")
    print("Input: 'calculate 15 plus 27'")
    result = controller.process_input("calculate 15 plus 27")
    print(f"Action: {result['action_taken']}")
    response = result['result'].get(
        'response', result['result'].get('result', 'No response'))
    print(f"Response: {response}")

    # Example 3: Direct answer - should answer directly
    print("\n3. DIRECT ANSWER EXAMPLE:")
    print("Input: 'search for Python tutorials'")
    result = controller.process_input("search for Python tutorials")
    print(f"Action: {result['action_taken']}")
    response = result['result'].get(
        'response', result['result'].get('result', 'No response'))
    print(f"Response: {response}")

    # Example 4: Weather with missing location
    print("\n4. WEATHER MISSING LOCATION:")
    print("Input: 'what's the weather'")
    result = controller.process_input("what's the weather")
    print(f"Action: {result['action_taken']}")
    response = result['result'].get(
        'response', result['result'].get('result', 'No response'))
    print(f"Response: {response}")

    # Example 5: Weather with location
    print("\n5. WEATHER WITH LOCATION:")
    print("Input: 'what's the weather in New York'")
    result = controller.process_input("what's the weather in New York")
    print(f"Action: {result['action_taken']}")
    response = result['result'].get(
        'response', result['result'].get('result', 'No response'))
    print(f"Response: {response}")

    print("\n" + "=" * 50)
    print("The controller successfully demonstrates all three decision paths!")
    print("=" * 50)


if __name__ == "__main__":
    main()
