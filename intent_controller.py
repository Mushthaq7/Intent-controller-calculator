import re
import json
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ActionType(Enum):
    ASK_FOR_INFO = "ask_for_info"
    CALL_API = "call_api"
    ANSWER_DIRECTLY = "answer_directly"


class IntentController:
    """
    A simple controller that parses intents, checks for missing information,
    and decides on the appropriate action to take.
    """

    def __init__(self):
        self.required_fields = {
            "calculate": ["operation", "numbers"],
            "weather": ["location"],
            "book_flight": ["origin", "destination", "date"],
            "send_email": ["recipient", "subject", "message"],
            "search": ["query"],
            "schedule_meeting": ["participants", "date", "duration"]
        }

        self.api_endpoints = {
            "calculate": "calculator_api",
            "weather": "weather_api",
            "book_flight": "flight_booking_api",
            "send_email": "email_api",
            "search": "search_api",
            "schedule_meeting": "calendar_api"
        }

        # Enhanced intent patterns with more flexibility
        self.intent_patterns = {
            "calculate": [
                r"(?:calculate|compute|add|subtract|multiply|divide)\s+(.+?)\s+(?:plus|minus|times|divided by|multiply|divide)\s+(.+)",
                r"(?:what is|what's)\s+(.+?)\s+(?:plus|minus|times|divided by)\s+(.+)",
                r"(?:add|subtract|multiply|divide)\s+(.+?)\s+(?:and|to|by)\s+(.+)",
                r"(?:sum|total|result)\s+of\s+(.+?)\s+(?:and|plus)\s+(.+)",
                r"(?:calculate|compute)\s+(.+?)\s+(?:and|with)\s+(.+)",
                r"(?:math|mathematics|arithmetic)\s+(?:with|using)\s+(.+?)\s+(?:and|plus|minus|times|divided by)\s+(.+)",
                r"(?:power|exponent)\s+(.+?)\s+(?:to|raised to)\s+(.+)",
                r"(?:square root|sqrt)\s+of\s+(.+)",
                r"(?:root|radical)\s+of\s+(.+)"
            ],
            "weather": [
                r"(?:weather|temperature|forecast)\s+(?:in\s+)?(.+)",
                r"(?:what's|what is)\s+the\s+weather\s+(?:like\s+)?(?:in\s+)?(.+)",
                r"(?:how's|how is)\s+the\s+weather\s+(?:in\s+)?(.+)",
                r"(?:weather|temperature)\s+(?:for|in)\s+(.+)",
                r"(?:forecast|weather forecast)\s+(?:for|in)\s+(.+)",
                r"(?:is it|will it)\s+(?:rain|snow|sunny|cloudy)\s+(?:in\s+)?(.+)"
            ],
            "book_flight": [
                r"(?:book|reserve|schedule)\s+(?:a\s+)?flight\s+(?:from\s+)?(.+?)\s+(?:to\s+)?(.+?)(?:\s+on\s+(.+))?",
                r"(?:fly|travel|go)\s+(?:from\s+)?(.+?)\s+(?:to\s+)?(.+?)(?:\s+on\s+(.+))?",
                r"(?:flight|ticket)\s+(?:from\s+)?(.+?)\s+(?:to\s+)?(.+?)(?:\s+on\s+(.+))?",
                r"(?:i want to|i need to|can you)\s+(?:fly|travel|go)\s+(?:from\s+)?(.+?)\s+(?:to\s+)?(.+?)(?:\s+on\s+(.+))?",
                r"(?:book|reserve)\s+(?:a\s+)?(?:ticket|seat)\s+(?:from\s+)?(.+?)\s+(?:to\s+)?(.+?)(?:\s+on\s+(.+))?",
                r"(?:from\s+)?(.+?)\s+(?:to\s+)?(.+?)(?:\s+on\s+(.+))?\s+(?:flight|ticket|travel)"
            ],
            "send_email": [
                r"(?:send|write|compose)\s+(?:an\s+)?email\s+(?:to\s+)?(.+?)(?:\s+about\s+(.+))?",
                r"(?:email|mail)\s+(.+?)(?:\s+regarding\s+(.+))?",
                r"(?:send|write)\s+(?:a\s+)?message\s+(?:to\s+)?(.+?)(?:\s+about\s+(.+))?",
                r"(?:contact|reach out to)\s+(.+?)(?:\s+about\s+(.+))?",
                r"(?:i want to|i need to)\s+(?:send|write)\s+(?:an\s+)?email\s+(?:to\s+)?(.+?)(?:\s+about\s+(.+))?"
            ],
            "search": [
                r"(?:search|find|look up)\s+(.+)",
                r"(?:what is|what's)\s+(.+)",
                r"(?:tell me about|information about)\s+(.+)",
                r"(?:i want to know|i need to know)\s+(.+)",
                r"(?:can you tell me|do you know)\s+(.+)",
                r"(?:help me find|show me)\s+(.+)"
            ],
            "schedule_meeting": [
                r"(?:schedule|book|arrange)\s+(?:a\s+)?meeting\s+(?:with\s+)?(.+?)(?:\s+on\s+(.+))?",
                r"(?:meet|meeting)\s+(?:with\s+)?(.+?)(?:\s+on\s+(.+))?",
                r"(?:set up|organize)\s+(?:a\s+)?meeting\s+(?:with\s+)?(.+?)(?:\s+on\s+(.+))?",
                r"(?:i want to|i need to)\s+(?:meet|schedule)\s+(?:with\s+)?(.+?)(?:\s+on\s+(.+))?",
                r"(?:appointment|call)\s+(?:with\s+)?(.+?)(?:\s+on\s+(.+))?"
            ]
        }

        # Intent keywords for better detection
        self.intent_keywords = {
            "calculate": ["calculate", "compute", "add", "subtract", "multiply", "divide", "math", "sum", "total", "plus", "minus", "times"],
            "weather": ["weather", "temperature", "forecast", "rain", "snow", "sunny", "cloudy", "hot", "cold"],
            "book_flight": ["flight", "fly", "travel", "ticket", "airline", "airport", "from", "to", "destination", "origin"],
            "send_email": ["email", "mail", "send", "message", "contact", "recipient", "inbox"],
            "search": ["search", "find", "look", "what", "tell", "information", "know", "help"],
            "schedule_meeting": ["meeting", "schedule", "appointment", "call", "meet", "calendar", "book"]
        }

    def parse_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Parse the user input to extract intent and relevant information.

        Args:
            user_input: The user's input string

        Returns:
            Dictionary containing intent and extracted information
        """
        user_input = user_input.lower().strip()

        # First, try pattern-based matching
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_input)
                if match:
                    extracted_info = self._extract_info_from_match(
                        intent, match, user_input)
                    return {
                        "intent": intent,
                        "confidence": 0.9,  # High confidence for pattern match
                        "extracted_info": extracted_info,
                        "raw_input": user_input,
                        "detection_method": "pattern"
                    }

        # If no pattern match, try keyword-based detection
        keyword_intent = self._detect_intent_by_keywords(user_input)
        if keyword_intent:
            extracted_info = self._extract_info_by_keywords(
                keyword_intent, user_input)
            return {
                "intent": keyword_intent,
                "confidence": 0.7,  # Medium confidence for keyword match
                "extracted_info": extracted_info,
                "raw_input": user_input,
                "detection_method": "keywords"
            }

        # Default to search if no specific intent is detected
        return {
            "intent": "search",
            "confidence": 0.3,
            "extracted_info": {"query": user_input},
            "raw_input": user_input,
            "detection_method": "default"
        }

    def _detect_intent_by_keywords(self, user_input: str) -> Optional[str]:
        """Detect intent using keyword matching."""
        words = user_input.split()
        intent_scores = {}

        for intent, keywords in self.intent_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in user_input:
                    score += 1
                    # Bonus for exact word matches
                    if keyword in words:
                        score += 0.5
            intent_scores[intent] = score

        # Find the intent with the highest score
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            if intent_scores[best_intent] > 0:
                return best_intent

        return None

    def _extract_info_by_keywords(self, intent: str, user_input: str) -> Dict[str, Any]:
        """Extract information using keyword-based approach."""
        extracted = {}

        if intent == "calculate":
            # Look for numbers and operations
            numbers = re.findall(r'\d+(?:\.\d+)?', user_input)
            operation = self._detect_operation(user_input)
            extracted["operation"] = operation
            # Ensure empty list if no numbers found
            extracted["numbers"] = numbers if numbers else []

        elif intent == "weather":
            # Look for location indicators
            location_patterns = [
                r"(?:in|at|for)\s+([a-zA-Z\s]+?)(?:\s|$)",
                r"weather\s+(?:in|at|for)\s+([a-zA-Z\s]+?)(?:\s|$)"
            ]
            for pattern in location_patterns:
                match = re.search(pattern, user_input)
                if match:
                    extracted["location"] = match.group(1).strip()
                    break
            if "location" not in extracted:
                # Try to extract any capitalized words as location
                locations = re.findall(
                    r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', user_input)
                if locations:
                    extracted["location"] = locations[0]

        elif intent == "book_flight":
            # Look for "from X to Y" pattern
            from_to_pattern = r"(?:from|departing)\s+([a-zA-Z\s]+?)\s+(?:to|arriving at)\s+([a-zA-Z\s]+?)(?:\s|$)"
            match = re.search(from_to_pattern, user_input)
            if match:
                extracted["origin"] = match.group(1).strip()
                extracted["destination"] = match.group(2).strip()

            # Look for date patterns
            date_patterns = [
                r"(?:on|date|when)\s+([a-zA-Z]+\s+\d{1,2},?\s+\d{4})",
                r"(?:on|date|when)\s+(\d{1,2}/\d{1,2}/\d{4})",
                r"(?:on|date|when)\s+(\d{1,2}-\d{1,2}-\d{4})"
            ]
            for pattern in date_patterns:
                match = re.search(pattern, user_input)
                if match:
                    extracted["date"] = match.group(1).strip()
                    break

        elif intent == "send_email":
            # Look for email addresses
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, user_input)
            if emails:
                extracted["recipient"] = emails[0]

            # Look for "about" or "regarding" for subject
            subject_pattern = r"(?:about|regarding|subject)\s+([a-zA-Z\s]+?)(?:\s|$)"
            match = re.search(subject_pattern, user_input)
            if match:
                extracted["subject"] = match.group(1).strip()

        elif intent == "search":
            # Extract the search query (everything after search keywords)
            search_keywords = ["search", "find", "look",
                               "what", "tell", "information", "know", "help"]
            query = user_input
            for keyword in search_keywords:
                if keyword in user_input:
                    parts = user_input.split(keyword, 1)
                    if len(parts) > 1:
                        query = parts[1].strip()
                        break
            extracted["query"] = query

        elif intent == "schedule_meeting":
            # Look for "with X" pattern
            with_pattern = r"(?:with|meeting with)\s+([a-zA-Z\s]+?)(?:\s|$)"
            match = re.search(with_pattern, user_input)
            if match:
                extracted["participants"] = match.group(1).strip()

            # Look for date patterns
            date_patterns = [
                r"(?:on|date|when)\s+([a-zA-Z]+\s+\d{1,2},?\s+\d{4})",
                r"(?:on|date|when)\s+(\d{1,2}/\d{1,2}/\d{4})",
                r"(?:on|date|when)\s+(\d{1,2}-\d{1,2}-\d{4})"
            ]
            for pattern in date_patterns:
                match = re.search(pattern, user_input)
                if match:
                    extracted["date"] = match.group(1).strip()
                    break

        return extracted

    def _extract_info_from_match(self, intent: str, match, user_input: str) -> Dict[str, Any]:
        """Extract structured information from regex match based on intent."""
        groups = match.groups()
        extracted = {}

        if intent == "calculate":
            if len(groups) >= 2 and groups[1]:
                # Extract operation from the input text
                operation = self._detect_operation(user_input)
                # Extract numbers from both groups
                numbers = []
                for group in groups:
                    if group:
                        # Extract numbers from the group
                        nums = re.findall(r'\d+(?:\.\d+)?', group.strip())
                        numbers.extend(nums)
                extracted["operation"] = operation
                extracted["numbers"] = numbers
            else:
                # Handle single group cases (like square root)
                text = groups[0] if groups[0] else ""
                # Check if it's a square root operation
                if "square root" in user_input.lower() or "sqrt" in user_input.lower():
                    extracted["operation"] = "sqrt"
                    # Extract the number after "of"
                    numbers = re.findall(r'\d+(?:\.\d+)?', text)
                    extracted["numbers"] = numbers
                else:
                    # Try to extract operation and numbers from single group
                    extracted.update(self._parse_calculation(text))

        elif intent == "weather":
            extracted["location"] = groups[0].strip() if groups[0] else ""

        elif intent == "book_flight":
            if len(groups) >= 3:
                extracted["origin"] = groups[0].strip() if groups[0] else ""
                extracted["destination"] = groups[1].strip(
                ) if groups[1] else ""
                extracted["date"] = groups[2].strip() if groups[2] else ""
            elif len(groups) >= 2:
                extracted["origin"] = groups[0].strip() if groups[0] else ""
                extracted["destination"] = groups[1].strip(
                ) if groups[1] else ""

        elif intent == "send_email":
            extracted["recipient"] = groups[0].strip() if groups[0] else ""
            extracted["subject"] = groups[1].strip() if groups[1] else ""

        elif intent == "search":
            extracted["query"] = groups[0].strip() if groups[0] else ""

        elif intent == "schedule_meeting":
            extracted["participants"] = groups[0].strip() if groups[0] else ""
            extracted["date"] = groups[1].strip() if groups[1] else ""

        return extracted

    def _detect_operation(self, text: str) -> str:
        """Detect mathematical operation from text."""
        text = text.lower()
        if "plus" in text or "+" in text:
            return "add"
        elif "minus" in text or "-" in text:
            return "subtract"
        elif "times" in text or "*" in text or "multiply" in text:
            return "multiply"
        elif "divide" in text or "/" in text or "divided by" in text:
            return "divide"
        elif "power" in text or "exponent" in text or "raised to" in text or "^" in text:
            return "power"
        elif "square root" in text or "sqrt" in text or "root" in text or "radical" in text:
            return "sqrt"
        else:
            return "add"  # Default

    def _parse_calculation(self, text: str) -> Dict[str, Any]:
        """Parse calculation text to extract operation and numbers."""
        # Look for mathematical operations
        if "plus" in text or "+" in text:
            operation = "add"
        elif "minus" in text or "-" in text:
            operation = "subtract"
        elif "times" in text or "*" in text or "multiply" in text:
            operation = "multiply"
        elif "divide" in text or "/" in text:
            operation = "divide"
        else:
            operation = "add"  # Default

        # Extract numbers (simplified)
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        return {"operation": operation, "numbers": numbers}

    def check_missing_info(self, intent: str, extracted_info: Dict[str, Any]) -> List[str]:
        """
        Check what required information is missing for the given intent.

        Args:
            intent: The detected intent
            extracted_info: The extracted information

        Returns:
            List of missing required fields
        """
        if intent not in self.required_fields:
            return []

        required = self.required_fields[intent]
        missing = []

        for field in required:
            if field not in extracted_info or not extracted_info[field]:
                missing.append(field)
            elif isinstance(extracted_info[field], list) and not extracted_info[field]:
                missing.append(field)

        return missing

    def decide_action(self, intent: str, missing_info: List[str],
                      extracted_info: Dict[str, Any]) -> Tuple[ActionType, Dict[str, Any]]:
        """
        Decide what action to take based on intent and missing information.

        Args:
            intent: The detected intent
            missing_info: List of missing required fields
            extracted_info: The extracted information

        Returns:
            Tuple of (ActionType, action_data)
        """
        # If we have missing required information, ask for it
        if missing_info:
            return ActionType.ASK_FOR_INFO, {
                "missing_fields": missing_info,
                "intent": intent,
                "message": self._generate_missing_info_message(intent, missing_info)
            }

        # If we have all required info and it's an API-able intent, call API
        if intent in self.api_endpoints:
            return ActionType.CALL_API, {
                "endpoint": self.api_endpoints[intent],
                "intent": intent,
                "data": extracted_info
            }

        # Default to direct answer
        return ActionType.ANSWER_DIRECTLY, {
            "intent": intent,
            "data": extracted_info,
            "message": self._generate_direct_answer(intent, extracted_info)
        }

    def _generate_missing_info_message(self, intent: str, missing_fields: List[str]) -> str:
        """Generate a user-friendly message asking for missing information."""
        intent_messages = {
            "calculate": "I need to know what numbers you want to calculate with.",
            "weather": "I need to know which location you want weather information for.",
            "book_flight": "I need the origin, destination, and date for your flight.",
            "send_email": "I need the recipient and subject for your email.",
            "search": "I need to know what you want to search for.",
            "schedule_meeting": "I need to know who to meet with and when."
        }

        base_message = intent_messages.get(
            intent, "I need more information to help you.")

        if len(missing_fields) == 1:
            field_messages = {
                "operation": "What operation would you like to perform? (add, subtract, multiply, divide)",
                "numbers": "What numbers would you like to calculate with?",
                "location": "Which location would you like weather information for?",
                "origin": "Where are you departing from?",
                "destination": "Where are you traveling to?",
                "date": "What date would you like?",
                "recipient": "Who should I send the email to?",
                "subject": "What should the email subject be?",
                "message": "What message would you like to send?",
                "query": "What would you like to search for?",
                "participants": "Who should attend the meeting?",
                "duration": "How long should the meeting be?"
            }

            specific_message = field_messages.get(
                missing_fields[0], f"Please provide {missing_fields[0]}.")
            return f"{base_message} {specific_message}"

        return base_message

    def _generate_direct_answer(self, intent: str, data: Dict[str, Any]) -> str:
        """Generate a direct answer for simple intents."""
        if intent == "search":
            query = data.get("query", "")
            return f"I'll search for information about '{query}' for you."

        return f"I understand you want to {intent}. Let me help you with that."

    def execute_action(self, action_type: ActionType, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the chosen action.

        Args:
            action_type: The type of action to execute
            action_data: Data needed for the action

        Returns:
            Result of the action execution
        """
        if action_type == ActionType.ASK_FOR_INFO:
            return {
                "type": "ask_for_info",
                "response": action_data["message"],
                "missing_fields": action_data["missing_fields"],
                "intent": action_data["intent"]
            }

        elif action_type == ActionType.CALL_API:
            return self._call_api(action_data["endpoint"], action_data["data"])

        elif action_type == ActionType.ANSWER_DIRECTLY:
            return {
                "type": "direct_answer",
                "response": action_data["message"],
                "intent": action_data["intent"]
            }

    def _call_api(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate calling an API endpoint."""
        logger.info(f"Calling API endpoint: {endpoint} with data: {data}")

        # Use enhanced calculator API
        if endpoint == "calculator_api":
            return self._call_calculator_api(data)

        # Simulate other API responses
        api_responses = {
            "weather_api": {
                "type": "api_response",
                "endpoint": "weather",
                "result": f"Weather information for {data.get('location', 'unknown location')}",
                "status": "success"
            },
            "flight_booking_api": {
                "type": "api_response",
                "endpoint": "flight_booking",
                "result": f"Flight booked from {data.get('origin')} to {data.get('destination')} on {data.get('date')}",
                "status": "success"
            },
            "email_api": {
                "type": "api_response",
                "endpoint": "email",
                "result": f"Email sent to {data.get('recipient')} with subject: {data.get('subject')}",
                "status": "success"
            },
            "search_api": {
                "type": "api_response",
                "endpoint": "search",
                "result": f"Search results for: {data.get('query')}",
                "status": "success"
            },
            "calendar_api": {
                "type": "api_response",
                "endpoint": "calendar",
                "result": f"Meeting scheduled with {data.get('participants')} on {data.get('date')}",
                "status": "success"
            }
        }

        return api_responses.get(endpoint, {
            "type": "api_response",
            "endpoint": endpoint,
            "result": "API call completed",
            "status": "success"
        })

    def _call_calculator_api(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced calculator API with comprehensive error handling."""
        try:
            result = self._calculate_result(data)

            # Check if result contains an error
            if result.startswith("Error:"):
                return {
                    "type": "api_response",
                    "endpoint": "calculator",
                    "result": result,
                    "status": "error",
                    "error_type": "calculation_error",
                    "data": data
                }
            else:
                return {
                    "type": "api_response",
                    "endpoint": "calculator",
                    "result": result,
                    "status": "success",
                    "data": data
                }

        except Exception as e:
            return {
                "type": "api_response",
                "endpoint": "calculator",
                "result": f"Error: Calculator API failed - {str(e)}",
                "status": "error",
                "error_type": "api_error",
                "data": data
            }

    def _calculate_result(self, data: Dict[str, Any]) -> str:
        """Perform calculation based on extracted data with comprehensive error handling."""
        operation = data.get("operation", "add")
        numbers = data.get("numbers", [])

        # Validate input
        if not numbers:
            return "Error: No numbers provided for calculation"

        # Check minimum numbers based on operation
        if operation == "sqrt":
            if len(numbers) < 1:
                return "Error: Square root operation requires at least one number"
        else:
            if len(numbers) < 2:
                return "Error: Need at least two numbers for calculation"

        if len(numbers) > 10:
            return "Error: Too many numbers provided (maximum 10)"

        try:
            # Convert all numbers to float
            float_numbers = []
            for num_str in numbers:
                try:
                    float_numbers.append(float(num_str))
                except ValueError:
                    return f"Error: '{num_str}' is not a valid number"

            # Perform calculation based on operation
            if operation == "add":
                result = sum(float_numbers)
                operation_symbol = "+"
            elif operation == "subtract":
                result = float_numbers[0] - sum(float_numbers[1:])
                operation_symbol = "-"
            elif operation == "multiply":
                result = 1
                for num in float_numbers:
                    result *= num
                operation_symbol = "×"
            elif operation == "divide":
                if 0 in float_numbers[1:]:
                    return "Error: Cannot divide by zero"
                result = float_numbers[0]
                for num in float_numbers[1:]:
                    result /= num
                operation_symbol = "÷"
            elif operation == "power":
                if len(float_numbers) != 2:
                    return "Error: Power operation requires exactly two numbers"
                result = float_numbers[0] ** float_numbers[1]
                operation_symbol = "^"
            elif operation == "sqrt":
                if len(float_numbers) != 1:
                    return "Error: Square root operation requires exactly one number"
                if float_numbers[0] < 0:
                    return "Error: Cannot calculate square root of negative number"
                result = float_numbers[0] ** 0.5
                operation_symbol = "√"
            else:
                return f"Error: Unknown operation '{operation}'. Supported operations: add, subtract, multiply, divide, power, sqrt"

            # Format the result
            if operation == "sqrt":
                expression = f"{operation_symbol}({float_numbers[0]})"
            else:
                expression = f" {operation_symbol} ".join(
                    map(str, float_numbers))

            # Round result to avoid floating point precision issues
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 6)

            return f"{expression} = {result}"

        except OverflowError:
            return "Error: Calculation result is too large"
        except Exception as e:
            return f"Error: Calculation failed - {str(e)}"

    def process_input(self, user_input: str) -> Dict[str, Any]:
        """
        Main method to process user input through the entire pipeline.

        Args:
            user_input: The user's input string

        Returns:
            Complete response with action taken and result
        """
        logger.info(f"Processing input: {user_input}")

        # Step 1: Parse intent
        intent_result = self.parse_intent(user_input)
        logger.info(f"Parsed intent: {intent_result}")

        # Step 2: Check for missing information
        missing_info = self.check_missing_info(
            intent_result["intent"],
            intent_result["extracted_info"]
        )
        logger.info(f"Missing info: {missing_info}")

        # Step 3: Decide on action
        action_type, action_data = self.decide_action(
            intent_result["intent"],
            missing_info,
            intent_result["extracted_info"]
        )
        logger.info(f"Decided action: {action_type}")

        # Step 4: Execute action
        result = self.execute_action(action_type, action_data)
        logger.info(f"Action result: {result}")

        return {
            "input": user_input,
            "intent_analysis": intent_result,
            "missing_info": missing_info,
            "action_taken": action_type.value,
            "result": result
        }
