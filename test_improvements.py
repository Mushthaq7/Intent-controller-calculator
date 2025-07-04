#!/usr/bin/env python3
"""
Test script to demonstrate the improved intent detection.
"""

from intent_controller import IntentController


def test_improved_detection():
    controller = IntentController()

    # Test cases that should now work better
    test_cases = [
        "from kualalumpur to kochi on july 1 2025",
        "what is 15 plus 27",
        "weather in new york",
        "send email to john@example.com about meeting",
        "search for python tutorials",
        "calculate 10 times 5",
        "book flight from london to paris",
        "schedule meeting with team on friday"
    ]

    print("Improved Intent Detection Test")
    print("=" * 50)

    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{i}. Input: '{test_input}'")
        result = controller.process_input(test_input)

        intent_analysis = result['intent_analysis']
        print(f"   Intent: {intent_analysis['intent']}")
        print(f"   Method: {intent_analysis['detection_method']}")
        print(f"   Confidence: {intent_analysis['confidence']}")
        print(f"   Extracted: {intent_analysis['extracted_info']}")
        print(f"   Action: {result['action_taken']}")

        # Show the response
        response = result['result'].get(
            'response', result['result'].get('result', 'No response'))
        print(f"   Response: {response}")
        print("-" * 30)


if __name__ == "__main__":
    test_improved_detection()
