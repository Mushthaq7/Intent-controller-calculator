#!/usr/bin/env python3
"""
Calculator Tool Integration Demo
Shows both successful calculations and graceful error handling.
"""

from intent_controller import IntentController
import json


def print_calculation_result(result):
    """Pretty print calculator results."""
    print("\n" + "="*60)
    print(f"Input: {result['input']}")
    print("-" * 60)

    intent_analysis = result['intent_analysis']
    print(f"Detected Intent: {intent_analysis['intent']}")
    print(f"Detection Method: {intent_analysis['detection_method']}")
    print(f"Confidence: {intent_analysis['confidence']}")
    print(
        f"Extracted Info: {json.dumps(intent_analysis['extracted_info'], indent=2)}")

    print(f"Action Taken: {result['action_taken']}")

    # Show calculator-specific results
    calc_result = result['result']

    # Handle different result types
    if 'status' in calc_result:
        print(f"Status: {calc_result['status']}")
        print(f"Result: {calc_result['result']}")

        if calc_result['status'] == 'error':
            print(f"Error Type: {calc_result.get('error_type', 'unknown')}")
    else:
        # Handle ask_for_info or direct_answer cases
        print(f"Response: {calc_result.get('response', 'No response')}")
        if 'missing_fields' in calc_result:
            print(f"Missing Fields: {calc_result['missing_fields']}")

    print("="*60)


def main():
    """Demonstrate calculator functionality with various test cases."""
    controller = IntentController()

    print("🧮 Calculator Tool Integration Demo")
    print("=" * 60)

    # Test cases: Successful calculations
    print("\n✅ SUCCESSFUL CALCULATIONS:")
    successful_tests = [
        "calculate 15 plus 27",
        "what is 10 times 5",
        "add 25 and 15",
        "compute 100 divided by 4",
        "calculate 5 power 3",
        "square root of 16",
        "what's 50 minus 12",
        "multiply 2 3 4 5",
        "sum of 10 20 30 40"
    ]

    for test_input in successful_tests:
        print(f"\nTesting: {test_input}")
        result = controller.process_input(test_input)
        print_calculation_result(result)

    # Test cases: Error handling
    print("\n❌ ERROR HANDLING EXAMPLES:")
    error_tests = [
        "calculate something",  # No numbers
        "what is 5",  # Only one number
        "calculate abc plus def",  # Invalid numbers
        "divide 10 by 0",  # Division by zero
        "square root of -4",  # Negative square root
        "power 5",  # Power needs two numbers
        "calculate 1 2 3 4 5 6 7 8 9 10 11",  # Too many numbers
        "calculate 5 invalid_operation 3",  # Unknown operation
    ]

    for test_input in error_tests:
        print(f"\nTesting: {test_input}")
        result = controller.process_input(test_input)
        print_calculation_result(result)

    # Interactive calculator mode
    print("\n" + "="*60)
    print("🧮 INTERACTIVE CALCULATOR MODE")
    print("Try your own calculations! (type 'quit' to exit)")
    print("Examples:")
    print("  - calculate 10 plus 5")
    print("  - what is 20 times 3")
    print("  - square root of 25")
    print("  - power 2 8")
    print("  - divide 100 by 4")
    print("="*60)

    while True:
        try:
            user_input = input("\nEnter calculation: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break

            if user_input:
                result = controller.process_input(user_input)
                print_calculation_result(result)
        except KeyboardInterrupt:
            print("\nExiting calculator...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
