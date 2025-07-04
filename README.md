# Intent Controller

A simple yet powerful controller that parses user intents, checks for missing information, and decides on the appropriate action to take.

## Features

### 🎯 Intent Parsing

- **Pattern-based recognition**: Uses regex patterns to identify user intents
- **Multiple intent types**: Supports calculation, weather, flight booking, email, search, and meeting scheduling
- **Confidence scoring**: Provides confidence levels for intent detection
- **Information extraction**: Extracts relevant data from user input

### 🔍 Missing Information Detection

- **Required field validation**: Checks if all necessary information is provided
- **Smart field mapping**: Maps different intents to their required fields
- **User-friendly prompts**: Generates helpful messages asking for missing information

### 🚀 Action Decision Engine

- **Three action types**:
  - **Ask for Info**: When required information is missing
  - **Call API**: When all info is present and an API is available
  - **Answer Directly**: For simple queries that don't need external APIs

### ⚡ Action Execution

- **API simulation**: Simulates calling external APIs (calculator, weather, etc.)
- **Direct responses**: Provides immediate answers for simple queries
- **Structured output**: Returns well-formatted results

## Supported Intents

| Intent               | Example Input                      | Required Fields              |
| -------------------- | ---------------------------------- | ---------------------------- |
| **Calculate**        | "calculate 15 plus 27"             | operation, numbers           |
| **Weather**          | "what's the weather in New York"   | location                     |
| **Book Flight**      | "book flight from London to Paris" | origin, destination, date    |
| **Send Email**       | "send email to john@example.com"   | recipient, subject, message  |
| **Search**           | "search for Python tutorials"      | query                        |
| **Schedule Meeting** | "schedule meeting with team"       | participants, date, duration |

## 🧮 Calculator Tool Integration

The calculator tool is fully integrated into the controller, providing robust arithmetic capabilities with comprehensive error handling.

### **Supported Operations**

1. **Addition** (`add`, `plus`, `+`) - `"calculate 15 plus 27"`
2. **Subtraction** (`subtract`, `minus`, `-`) - `"what's 50 minus 12"`
3. **Multiplication** (`multiply`, `times`, `*`) - `"what is 10 times 5"`
4. **Division** (`divide`, `divided by`, `/`) - `"divide 100 by 4"`
5. **Power** (`power`, `exponent`, `^`) - `"calculate 5 power 3"`
6. **Square Root** (`sqrt`, `square root`, `√`) - `"square root of 16"`

### **Features**

- **Multiple numbers support** (up to 10 numbers)
- **Natural language input** ("calculate 15 plus 27")
- **Comprehensive error handling**
- **Structured API responses**
- **Graceful failure handling**

### **Example Calculations**

```python
# Successful calculations
"calculate 15 plus 27" → 15.0 + 27.0 = 42
"what is 10 times 5" → 10.0 × 5.0 = 50
"divide 100 by 4" → 100.0 ÷ 4.0 = 25
"calculate 5 power 3" → 5.0 ^ 3.0 = 125
"square root of 16" → √(16) = 4

# Error handling
"divide 10 by 0" → Error: Cannot divide by zero
"calculate abc plus def" → Asks for valid numbers
"square root of -4" → Error: Cannot calculate square root of negative number
```

### **Error Handling**

The calculator gracefully handles:

- **Division by zero**
- **Invalid number formats**
- **Missing information** (asks for clarification)
- **Negative square roots**
- **Too many numbers** (maximum 10)
- **Mathematical overflow**

### **API Response Structure**

```json
{
  "type": "api_response",
  "endpoint": "calculator",
  "result": "15.0 + 27.0 = 42",
  "status": "success",
  "data": {
    "operation": "add",
    "numbers": ["15", "27"]
  }
}
```

## Quick Start

### Installation

1. Clone or download the files
2. Ensure you have Python 3.7+ installed
3. No external dependencies required!

### Basic Usage

```python
from intent_controller import IntentController

# Create controller instance
controller = IntentController()

# Process user input
result = controller.process_input("calculate 10 plus 5")
print(result)
```

### Running the Demo

```bash
python demo.py
```

This will run through various example inputs and then enter interactive mode where you can test your own inputs.

## Architecture

### Core Components

1. **IntentController**: Main class that orchestrates the entire process
2. **ActionType**: Enum defining the three possible actions
3. **Pattern Matching**: Regex-based intent recognition
4. **Information Extraction**: Structured data extraction from user input
5. **Decision Engine**: Logic for choosing the appropriate action
6. **Action Executor**: Handles the execution of chosen actions

### Processing Pipeline

```
User Input → Pattern Matching → Keyword Fallback → Default Search → Missing Info Check → Action Decision → Action Execution → Result
```

1. **Parse Intent**: Analyze user input to determine intent and extract information
2. **Check Missing Info**: Validate if all required fields are present
3. **Decide Action**: Choose between asking for info, calling API, or answering directly
4. **Execute Action**: Perform the chosen action and return results

## API Reference

### IntentController Class

#### `__init__()`

Initialize the controller with predefined patterns and configurations.

#### `parse_intent(user_input: str) -> Dict[str, Any]`

Parse user input to extract intent and relevant information.

**Returns:**

- `intent`: Detected intent type
- `confidence`: Confidence score (0.0-1.0)
- `extracted_info`: Dictionary of extracted information
- `raw_input`: Original user input

#### `check_missing_info(intent: str, extracted_info: Dict[str, Any]) -> List[str]`

Check what required information is missing for the given intent.

**Returns:** List of missing required field names

#### `decide_action(intent: str, missing_info: List[str], extracted_info: Dict[str, Any]) -> Tuple[ActionType, Dict[str, Any]]`

Decide what action to take based on intent and missing information.

**Returns:** Tuple of (ActionType, action_data)

#### `execute_action(action_type: ActionType, action_data: Dict[str, Any]) -> Dict[str, Any]`

Execute the chosen action.

**Returns:** Result of the action execution

#### `process_input(user_input: str) -> Dict[str, Any]`

Main method that processes user input through the entire pipeline.

**Returns:** Complete response with all processing details

## Examples

### Complete Information (API Call)

```python
result = controller.process_input("calculate 15 plus 27")
# Result: Calls calculator API and returns "15.0 + 27.0 = 42"

result = controller.process_input("what's the weather in New York")
# Result: Calls weather API and returns weather information
```

### Missing Information (Ask for Info)

```python
result = controller.process_input("calculate something")
# Result: Asks for specific numbers to calculate with

result = controller.process_input("what's the weather")
# Result: Asks for location
```

### Direct Answer

```python
result = controller.process_input("search for Python tutorials")
# Result: Direct response about searching for Python tutorials
```

### Calculator Examples

```python
# Basic operations
result = controller.process_input("calculate 15 plus 27")
# Result: 15.0 + 27.0 = 42

result = controller.process_input("what is 10 times 5")
# Result: 10.0 × 5.0 = 50

# Advanced operations
result = controller.process_input("calculate 5 power 3")
# Result: 5.0 ^ 3.0 = 125

result = controller.process_input("square root of 16")
# Result: √(16) = 4

# Error handling
result = controller.process_input("divide 10 by 0")
# Result: Error: Cannot divide by zero
```

## Extending the Controller

### Adding New Intents

1. Add intent patterns to `intent_patterns` in `__init__()`
2. Add required fields to `required_fields`
3. Add API endpoint mapping to `api_endpoints`
4. Update `_extract_info_from_match()` method
5. Add intent-specific messages to `_generate_missing_info_message()`

### Adding Real API Integration

Replace the `_call_api()` method with actual API calls:

```python
def _call_api(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    if endpoint == "weather_api":
        # Make actual weather API call
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={data['location']}")
        return response.json()
    # ... other endpoints
```

## Error Handling

The controller includes comprehensive error handling:

- Invalid input patterns
- Missing required information
- API call failures
- Calculation errors (e.g., division by zero)

## Logging

The controller uses Python's logging module to provide detailed information about:

- Input processing steps
- Intent detection results
- Missing information analysis
- Action decisions
- API call attempts

## Performance Considerations

- **Pattern Matching**: Uses compiled regex patterns for efficiency
- **Caching**: Can be extended with result caching for repeated queries
- **Async Support**: Can be modified to support async API calls
- **Memory Usage**: Minimal memory footprint, suitable for production use

## Contributing

Feel free to extend the controller with:

- New intent types
- More sophisticated NLP techniques
- Real API integrations
- Enhanced error handling
- Performance optimizations

## License

This project is open source and available under the MIT License.
