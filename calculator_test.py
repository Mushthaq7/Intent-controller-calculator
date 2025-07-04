#!/usr/bin/env python3
"""
Simple Calculator Test - Shows successful calculations and error handling.
"""

from intent_controller import IntentController


def test_calculator():
    controller = IntentController()

    print("🧮 Calculator Tool Integration Test")
    print("=" * 50)

    # Test successful calculations
    print("\n✅ SUCCESSFUL CALCULATIONS:")
    success_tests = [
        "calculate 15 plus 27",
        "what is 10 times 5",
        "divide 100 by 4",
        "calculate 5 power 3"
    ]

    for test in success_tests:
        print(f"\nInput: {test}")
        result = controller.process_input(test)
        calc_result = result['result']

        # Handle different result types
        if 'status' in calc_result:
            print(f"Status: {calc_result['status']}")
            print(f"Result: {calc_result['result']}")
        else:
            # Handle ask_for_info or direct_answer cases
            print(f"Response: {calc_result.get('response', 'No response')}")
            if 'missing_fields' in calc_result:
                print(f"Missing Fields: {calc_result['missing_fields']}")

    # Test error handling
    print("\n❌ ERROR HANDLING:")
    error_tests = [
        "divide 10 by 0",
        "calculate abc plus def",
        "square root of -4"
    ]

    for test in error_tests:
        print(f"\nInput: {test}")
        result = controller.process_input(test)
        calc_result = result['result']

        # Handle different result types
        if 'status' in calc_result:
            print(f"Status: {calc_result['status']}")
            print(f"Result: {calc_result['result']}")
            print(f"Error Type: {calc_result.get('error_type', 'none')}")
        else:
            # Handle ask_for_info or direct_answer cases
            print(f"Response: {calc_result.get('response', 'No response')}")
            if 'missing_fields' in calc_result:
                print(f"Missing Fields: {calc_result['missing_fields']}")


if __name__ == "__main__":
    test_calculator()
