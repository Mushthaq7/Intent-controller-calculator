from intent_controller import IntentController

c = IntentController()

print("🧮 Testing Square Root Functionality")
print("=" * 40)

# Test square root
result = c.process_input("square root of 16")
print(f"Input: square root of 16")
print(f"Operation: {result['intent_analysis']['extracted_info']['operation']}")
print(f"Numbers: {result['intent_analysis']['extracted_info']['numbers']}")
print(f"Result: {result['result']['result']}")
print(f"Status: {result['result']['status']}")

print("\n" + "=" * 40)
print("Square root test completed!")
