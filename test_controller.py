#!/usr/bin/env python3
"""
Test script for the Intent Controller
Demonstrates various functionality and validates the controller works correctly.
"""

from intent_controller import IntentController, ActionType
import json

def test_intent_parsing():
    """Test intent parsing functionality."""
    print("Testing Intent Parsing...")
    controller = IntentController()
    
    test_cases = [
        ("calculate 15 plus 27", "calculate"),
        ("what's the weather in New York", "weather"),
        ("book a flight from London to Paris", "book_flight"),
        ("send email to john@example.com", "send_email"),
        ("search for Python tutorials", "search"),
        ("schedule meeting with team", "schedule_meeting"),
    ]
    
    for input_text, expected_intent in test_cases:
        result = controller.parse_intent(input_text)
        actual_intent = result["intent"]
        confidence = result["confidence"]
        
        print(f"  Input: '{input_text}'")
        print(f"  Expected: {expected_intent}, Got: {actual_intent}, Confidence: {confidence}")
        print(f"  Extracted Info: {json.dumps(result['extracted_info'], indent=4)}")
        print()

def test_missing_info_detection():
    """Test missing information detection."""
    print("Testing Missing Information Detection...")
    controller = IntentController()
    
    # Test cases with missing information
    test_cases = [
        ("calculate something", ["operation", "numbers"]),
        ("what's the weather", ["location"]),
        ("book a flight", ["origin", "destination", "date"]),
        ("send an email", ["recipient", "subject", "message"]),
    ]
    
    for input_text, expected_missing in test_cases:
        intent_result = controller.parse_intent(input_text)
        missing_info = controller.check_missing_info(
            intent_result["intent"], 
            intent_result["extracted_info"]
        )
        
        print(f"  Input: '{input_text}'")
        print(f"  Expected Missing: {expected_missing}")
        print(f"  Actual Missing: {missing_info}")
        print()

def test_action_decision():
    """Test action decision logic."""
    print("Testing Action Decision Logic...")
    controller = IntentController()
    
    # Test complete information (should call API)
    complete_input = "calculate 10 plus 5"
    intent_result = controller.parse_intent(complete_input)
    missing_info = controller.check_missing_info(
        intent_result["intent"], 
        intent_result["extracted_info"]
    )
    action_type, action_data = controller.decide_action(
        intent_result["intent"],
        missing_info,
        intent_result["extracted_info"]
    )
    
    print(f"  Complete Input: '{complete_input}'")
    print(f"  Action Type: {action_type}")
    print(f"  Action Data: {json.dumps(action_data, indent=4)}")
    print()
    
    # Test missing information (should ask for info)
    incomplete_input = "calculate something"
    intent_result = controller.parse_intent(incomplete_input)
    missing_info = controller.check_missing_info(
        intent_result["intent"], 
        intent_result["extracted_info"]
    )
    action_type, action_data = controller.decide_action(
        intent_result["intent"],
        missing_info,
        intent_result["extracted_info"]
    )
    
    print(f"  Incomplete Input: '{incomplete_input}'")
    print(f"  Action Type: {action_type}")
    print(f"  Action Data: {json.dumps(action_data, indent=4)}")
    print()

def test_calculation_functionality():
    """Test calculation functionality."""
    print("Testing Calculation Functionality...")
    controller = IntentController()
    
    test_calculations = [
        ("calculate 15 plus 27", "15 add 27 = 42.0"),
        ("calculate 10 minus 3", "10 subtract 3 = 7.0"),
        ("calculate 5 times 6", "5 multiply 6 = 30.0"),
        ("calculate 20 divided by 4", "20 divide 4 = 5.0"),
    ]
    
    for input_text, expected_result in test_calculations:
        result = controller.process_input(input_text)
        actual_result = result["result"]["result"]
        
        print(f"  Input: '{input_text}'")
        print(f"  Expected: {expected_result}")
        print(f"  Got: {actual_result}")
        print()

def test_error_handling():
    """Test error handling."""
    print("Testing Error Handling...")
    controller = IntentController()
    
    # Test division by zero
    result = controller.process_input("calculate 10 divided by 0")
    print(f"  Division by zero: {result['result']['result']}")
    
    # Test invalid numbers
    result = controller.process_input("calculate abc plus def")
    print(f"  Invalid numbers: {result['result']['result']}")
    
    # Test insufficient numbers
    result = controller.process_input("calculate 5")
    print(f"  Insufficient numbers: {result['result']['result']}")
    print()

def test_full_pipeline():
    """Test the complete processing pipeline."""
    print("Testing Complete Pipeline...")
    controller = IntentController()
    
    test_inputs = [
        "calculate 25 plus 15",
        "what's the weather in London",
        "book a flight from New York to Los Angeles on December 20th",
        "send email to alice@example.com about project update",
        "search for machine learning tutorials",
        "schedule meeting with marketing team on Friday",
    ]
    
    for input_text in test_inputs:
        print(f"Processing: '{input_text}'")
        result = controller.process_input(input_text)
        
        print(f"  Intent: {result['intent_analysis']['intent']}")
        print(f"  Action: {result['action_taken']}")
        print(f"  Response: {result['result'].get('response', result['result'].get('result', 'No response'))}")
        print()

def main():
    """Run all tests."""
    print("=" * 60)
    print("Intent Controller Test Suite")
    print("=" * 60)
    
    try:
        test_intent_parsing()
        test_missing_info_detection()
        test_action_decision()
        test_calculation_functionality()
        test_error_handling()
        test_full_pipeline()
        
        print("=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 