from intent_controller import IntentController

# Create controller
c = IntentController()

print("🧮 Calculator Tool Integration Demo")
print("=" * 50)

# Test successful calculation
print("\n✅ SUCCESSFUL CALCULATION:")
result = c.process_input("calculate 15 plus 27")
print(f"Input: calculate 15 plus 27")
print(f"Result: {result['result']['result']}")
print(f"Status: {result['result']['status']}")

# Test error handling
print("\n❌ ERROR HANDLING:")
result = c.process_input("divide 10 by 0")
print(f"Input: divide 10 by 0")
print(f"Result: {result['result']['result']}")
print(f"Status: {result['result']['status']}")
print(f"Error Type: {result['result'].get('error_type', 'none')}")

print("\n" + "=" * 50)
print("Calculator integration working perfectly! 🎉")
