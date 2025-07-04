#!/usr/bin/env python3
"""
Demo script for the Intent Controller
Shows how the controller processes different types of user inputs.
"""

from intent_controller import IntentController
import json


def print_result(result):
    """Pretty print the controller result."""
    print("\n" + "="*60)
    print(f"Input: {result['input']}")
    print("-" * 60)

    # Intent analysis
    intent_analysis = result['intent_analysis']
    print(f"Detected Intent: {intent_analysis['intent']}")
    print(f"Confidence: {intent_analysis['confidence']}")
    print(
        f"Extracted Info: {json.dumps(intent_analysis['extracted_info'], indent=2)}")

    # Missing information
    if result['missing_info']:
        print(f"Missing Info: {result['missing_info']}")

    # Action taken
    print(f"Action Taken: {result['action_taken']}")

    # Result
    result_data = result['result']
    print(
        f"Response: {result_data.get('response', result_data.get('result', 'No response'))}")
    print("="*60)


def main():
    """Run the demo with various example inputs."""
    controller = IntentController()

    # Example inputs to test different scenarios
    test_inputs = [
        # Complete information - should call API
        "calculate 15 plus 27",
        "what's the weather in New York",
        "book a flight from London to Paris on December 15th",

        # Missing information - should ask for more info
        "calculate something",
        "what's the weather",
        "book a flight",
        "send an email",

        # Direct answers
        "search for Python tutorials",
        "tell me about machine learning",

        # Edge cases
        "hello there",
        "calculate 10 divided by 0",
        "calculate 5 times 3",
    ]

    print("Intent Controller Demo")
    print("Testing various user inputs...\n")

    for i, user_input in enumerate(test_inputs, 1):
        print(f"\nTest {i}:")
        try:
            result = controller.process_input(user_input)
            print_result(result)
        except Exception as e:
            print(f"Error processing input: {e}")

    # Interactive mode
    print("\n" + "="*60)
    print("Interactive Mode - Enter your own inputs (type 'quit' to exit)")
    print("="*60)

    while True:
        try:
            user_input = input("\nEnter your request: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            if user_input:
                result = controller.process_input(user_input)
                print_result(result)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
