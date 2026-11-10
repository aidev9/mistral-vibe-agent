"""
Test Case Templates and Patterns for SDLC Expert Agent
Provides predefined templates for common requirement patterns
"""

from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import re


class TestPatternType(Enum):
    """Types of test patterns"""
    LOGIN_AUTH = "Login & Authentication"
    DATA_VALIDATION = "Data Validation"
    API_INTEGRATION = "API Integration"
    UI_FUNCTIONALITY = "UI Functionality"
    PERFORMANCE = "Performance"
    SECURITY = "Security"
    ERROR_HANDLING = "Error Handling"
    BUSINESS_LOGIC = "Business Logic"


@dataclass
class TestPattern:
    """Represents a test pattern with templates for different scenarios"""
    name: str
    pattern_type: TestPatternType
    keywords: List[str]
    positive_template: str
    negative_template: str
    edge_template: Optional[str] = None
    priority: str = "Medium"
    tags: List[str] = field(default_factory=list)


@dataclass
class TestScenario:
    """Represents a complete test scenario with all details"""
    name: str
    description: str
    pattern: TestPattern
    variables: Dict[str, str]
    
    def generate_test_cases(self) -> List[Dict]:
        """Generate test cases from this scenario"""
        test_cases = []
        
        positive_tc = {
            "type": "Positive",
            "title": f"Verify {self.name}",
            "description": self.description,
            "steps": [self.pattern.positive_template.format(**self.variables)],
            "expected_result": f"The {self.name} works correctly",
            "priority": self.pattern.priority,
            "tags": self.pattern.tags + ["positive"]
        }
        test_cases.append(positive_tc)
        
        negative_tc = {
            "type": "Negative",
            "title": f"Verify {self.name} with invalid input",
            "description": f"Test {self.name} with invalid or missing data",
            "steps": [self.pattern.negative_template.format(**self.variables)],
            "expected_result": f"The system handles invalid input for {self.name} correctly",
            "priority": self.pattern.priority,
            "tags": self.pattern.tags + ["negative", "validation"]
        }
        test_cases.append(negative_tc)
        
        if self.pattern.edge_template:
            edge_tc = {
                "type": "Edge Case",
                "title": f"Verify edge cases for {self.name}",
                "description": f"Test edge cases for {self.name}",
                "steps": [self.pattern.edge_template.format(**self.variables)],
                "expected_result": f"The system handles edge cases for {self.name} correctly",
                "priority": "Low",
                "tags": self.pattern.tags + ["edge_case"]
            }
            test_cases.append(edge_tc)
        
        return test_cases


class TestPatternLibrary:
    """Library of common test patterns for various domains"""
    
    def __init__(self):
        self.patterns: List[TestPattern] = []
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize the pattern library"""
        self.patterns.append(TestPattern(
            name="User Login",
            pattern_type=TestPatternType.LOGIN_AUTH,
            keywords=["login", "sign in", "authenticate", "log in"],
            positive_template="1. Navigate to login page\n2. Enter valid {username} and {password}\n3. Click login button\n4. Verify user is redirected to dashboard",
            negative_template="1. Navigate to login page\n2. Enter invalid {username} or {password}\n3. Click login button\n4. Verify error message is displayed",
            edge_template="1. Navigate to login page\n2. Enter maximum length {username} and {password}\n3. Click login button\n4. Verify system handles long inputs",
            priority="High",
            tags=["authentication", "login"]
        ))
        
        self.patterns.append(TestPattern(
            name="Password Reset",
            pattern_type=TestPatternType.LOGIN_AUTH,
            keywords=["password reset", "forgot password", "reset password"],
            positive_template="1. Navigate to forgot password page\n2. Enter valid {email}\n3. Click reset button\n4. Verify reset email is sent",
            negative_template="1. Navigate to forgot password page\n2. Enter invalid {email}\n3. Click reset button\n4. Verify appropriate error is shown",
            priority="High",
            tags=["authentication", "password"]
        ))
        
        self.patterns.append(TestPattern(
            name="Form Validation",
            pattern_type=TestPatternType.DATA_VALIDATION,
            keywords=["form", "validate", "input", "submit", "required field"],
            positive_template="1. Fill {form_name} with valid data\n2. Submit the form\n3. Verify form is accepted",
            negative_template="1. Fill {form_name} with invalid data\n2. Submit the form\n3. Verify validation errors are displayed",
            edge_template="1. Fill {form_name} with boundary values\n2. Submit the form\n3. Verify boundary values are handled",
            priority="Medium",
            tags=["validation", "form"]
        ))
        
        self.patterns.append(TestPattern(
            name="Email Validation",
            pattern_type=TestPatternType.DATA_VALIDATION,
            keywords=["email", "email address", "validate email"],
            positive_template="1. Enter valid email address\n2. Submit\n3. Verify email is accepted",
            negative_template="1. Enter invalid email address\n2. Submit\n3. Verify validation error is displayed",
            edge_template="1. Enter email with maximum length\n2. Submit\n3. Verify system handles long email",
            priority="Medium",
            tags=["validation", "email"]
        ))
        
        self.patterns.append(TestPattern(
            name="API Call",
            pattern_type=TestPatternType.API_INTEGRATION,
            keywords=["API", "endpoint", "REST", "GET", "POST", "PUT", "DELETE"],
            positive_template="1. Send valid {method} request to {endpoint}\n2. Verify response status is 200\n3. Verify response data is correct",
            negative_template="1. Send invalid {method} request to {endpoint}\n2. Verify response status is 400\n3. Verify error message is returned",
            edge_template="1. Send {method} request with maximum payload to {endpoint}\n2. Verify system handles large payload",
            priority="Medium",
            tags=["api", "integration"]
        ))
        
        self.patterns.append(TestPattern(
            name="API Authentication",
            pattern_type=TestPatternType.API_INTEGRATION,
            keywords=["API key", "auth token", "bearer token", "API authentication"],
            positive_template="1. Send request with valid {auth_type} to {endpoint}\n2. Verify request is authenticated\n3. Verify response is returned",
            negative_template="1. Send request with invalid {auth_type} to {endpoint}\n2. Verify request is rejected\n3. Verify 401 status is returned",
            priority="High",
            tags=["api", "authentication"]
        ))
        
        self.patterns.append(TestPattern(
            name="Button Click",
            pattern_type=TestPatternType.UI_FUNCTIONALITY,
            keywords=["button", "click", "tap", "submit button", "action button"],
            positive_template="1. Navigate to {page}\n2. Click {button_name} button\n3. Verify expected action occurs",
            negative_template="1. Navigate to {page}\n2. Click {button_name} button with invalid state\n3. Verify appropriate error or no action",
            priority="Medium",
            tags=["ui", "button"]
        ))
        
        self.patterns.append(TestPattern(
            name="Navigation",
            pattern_type=TestPatternType.UI_FUNCTIONALITY,
            keywords=["navigate", "go to", "redirect", "navigation", "menu"],
            positive_template="1. Click {menu_item} in navigation\n2. Verify user is redirected to {target_page}",
            negative_template="1. Click {menu_item} with insufficient permissions\n2. Verify access is denied or appropriate message is shown",
            priority="Medium",
            tags=["ui", "navigation"]
        ))
        
        self.patterns.append(TestPattern(
            name="Load Time",
            pattern_type=TestPatternType.PERFORMANCE,
            keywords=["load time", "response time", "performance", "fast", "quick"],
            positive_template="1. Measure time to load {page_feature}\n2. Verify load time is under {max_time} seconds",
            negative_template="1. Simulate slow network\n2. Measure time to load {page_feature}\n3. Verify graceful degradation",
            edge_template="1. Load {page_feature} with maximum concurrent users\n2. Verify system remains responsive",
            priority="High",
            tags=["performance", "load_time"]
        ))
        
        self.patterns.append(TestPattern(
            name="Input Sanitization",
            pattern_type=TestPatternType.SECURITY,
            keywords=["sanitize", "XSS", "SQL injection", "security", "malicious input"],
            positive_template="1. Enter normal input in {field}\n2. Submit\n3. Verify input is processed correctly",
            negative_template="1. Enter malicious input (XSS/SQL) in {field}\n2. Submit\n3. Verify input is sanitized and not executed",
            priority="High",
            tags=["security", "sanitization"]
        ))
        
        self.patterns.append(TestPattern(
            name="Session Management",
            pattern_type=TestPatternType.SECURITY,
            keywords=["session", "cookie", "logout", "session timeout"],
            positive_template="1. Login and establish session\n2. Perform actions\n3. Verify session is maintained",
            negative_template="1. Login and establish session\n2. Wait for session timeout\n3. Verify session is invalidated",
            priority="High",
            tags=["security", "session"]
        ))
        
        self.patterns.append(TestPattern(
            name="Error Message",
            pattern_type=TestPatternType.ERROR_HANDLING,
            keywords=["error message", "error handling", "exception", "fail gracefully"],
            positive_template="1. Trigger error condition\n2. Verify user-friendly error message is displayed\n3. Verify system state is preserved",
            negative_template="1. Trigger unexpected error\n2. Verify system doesn't crash\n3. Verify appropriate fallback behavior",
            priority="Medium",
            tags=["error_handling", "usability"]
        ))
        
        self.patterns.append(TestPattern(
            name="Discount Calculation",
            pattern_type=TestPatternType.BUSINESS_LOGIC,
            keywords=["discount", "calculate", "price", "promotion", "offer"],
            positive_template="1. Add items to cart with valid {discount_code}\n2. Verify discount is applied correctly\n3. Verify final price is correct",
            negative_template="1. Add items to cart with invalid {discount_code}\n2. Verify discount is not applied\n3. Verify error message is shown",
            edge_template="1. Add maximum number of items with {discount_code}\n2. Verify discount is applied within limits",
            priority="High",
            tags=["business_logic", "calculation"]
        ))
        
        self.patterns.append(TestPattern(
            name="Workflow Approval",
            pattern_type=TestPatternType.BUSINESS_LOGIC,
            keywords=["approval", "workflow", "approve", "reject", "review"],
            positive_template="1. Submit {item} for approval\n2. As approver, approve the {item}\n3. Verify {item} status is updated",
            negative_template="1. Submit {item} for approval\n2. As approver, reject the {item}\n3. Verify {item} status is updated and user is notified",
            priority="Medium",
            tags=["business_logic", "workflow"]
        ))
    
    def find_matching_patterns(self, text: str) -> List[TestPattern]:
        """Find patterns that match the given text"""
        matching_patterns = []
        text_lower = text.lower()
        
        for pattern in self.patterns:
            for keyword in pattern.keywords:
                if keyword in text_lower:
                    matching_patterns.append(pattern)
                    break
        
        return matching_patterns
    
    def extract_variables(self, text: str, pattern: TestPattern) -> Dict[str, str]:
        """Extract variables from text for a given pattern"""
        variables = {}
        text_lower = text.lower()
        
        for keyword in pattern.keywords:
            if keyword in text_lower:
                start = text_lower.find(keyword)
                context = text[max(0, start - 20):min(len(text), start + 50)]
                words = re.findall(r'\b[A-Z]?[a-z]+(?:[A-Z][a-z]+)*\b', context)
                
                keyword_to_var = {
                    "login": "page",
                    "sign in": "page",
                    "form": "form_name",
                    "email": "field",
                    "API": "endpoint",
                    "GET": "method",
                    "POST": "method",
                    "PUT": "method",
                    "DELETE": "method",
                    "button": "button_name",
                    "page": "page",
                    "discount": "discount_code",
                    "approval": "item",
                }
                
                if keyword in keyword_to_var:
                    var_name = keyword_to_var[keyword]
                    if var_name not in variables:
                        variables[var_name] = keyword
        
        defaults = {
            "username": "username",
            "password": "password",
            "email": "user@example.com",
            "form_name": "form",
            "endpoint": "/api/endpoint",
            "method": "GET",
            "button_name": "Submit",
            "page": "page",
            "target_page": "target page",
            "max_time": "2",
            "field": "input field",
            "auth_type": "bearer token",
            "menu_item": "menu item",
            "discount_code": "PROMO10",
            "item": "document",
        }
        
        for var_name, default_value in defaults.items():
            if var_name not in variables:
                variables[var_name] = default_value
        
        return variables


pattern_library = TestPatternLibrary()


class EnhancedTestGenerator:
    """Enhanced test case generator using pattern matching"""
    
    def __init__(self):
        self.library = pattern_library
    
    def generate_from_text(self, text: str, requirement_id: str = "") -> List[Dict]:
        """Generate test cases from text using pattern matching"""
        test_cases = []
        patterns = self.library.find_matching_patterns(text)
        
        if not patterns:
            test_cases.append({
                "type": "Positive",
                "title": f"Verify: {text[:50]}...",
                "description": f"Test that: {text}",
                "steps": [f"1. Test the requirement: {text}"],
                "expected_result": f"The requirement '{text[:50]}...' is satisfied",
                "requirement_id": requirement_id,
                "priority": "Medium",
                "tags": ["basic"]
            })
            return test_cases
        
        for pattern in patterns:
            variables = self.library.extract_variables(text, pattern)
            scenario = TestScenario(
                name=f"{pattern.name} for {text[:30]}...",
                description=f"Test {pattern.name} functionality",
                pattern=pattern,
                variables=variables
            )
            pattern_test_cases = scenario.generate_test_cases()
            for tc in pattern_test_cases:
                tc["requirement_id"] = requirement_id
            test_cases.extend(pattern_test_cases)
        
        return test_cases


enhanced_generator = EnhancedTestGenerator()
