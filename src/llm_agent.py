"""
LLM-Powered SDLC Expert Agent
Uses LLM intelligence to extract requirements and generate test cases from PRD text
"""

import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import uuid


class RequirementType(Enum):
    """Types of requirements"""
    USER_STORY = "User Story"
    FUNCTIONAL = "Functional"
    NON_FUNCTIONAL = "Non-Functional"
    BUSINESS_RULE = "Business Rule"
    ACCEPTANCE_CRITERIA = "Acceptance Criteria"
    CONSTRAINT = "Constraint"
    ASSUMPTION = "Assumption"
    DEPENDENCY = "Dependency"
    SECURITY = "Security"
    PERFORMANCE = "Performance"


class TestCaseType(Enum):
    """Types of test cases"""
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    EDGE_CASE = "Edge Case"
    PERFORMANCE = "Performance"
    SECURITY = "Security"
    USABILITY = "Usability"
    INTEGRATION = "Integration"
    REGRESSION = "Regression"


@dataclass
class Requirement:
    """Extracted requirement with LLM intelligence"""
    text: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    requirement_type: RequirementType = RequirementType.FUNCTIONAL
    description: str = ""
    priority: str = "Medium"
    category: str = "General"
    dependencies: List[str] = field(default_factory=list)
    
    def __str__(self):
        return f"[{self.requirement_type.value}] {self.text}"


@dataclass
class TestCase:
    """Generated test case with LLM intelligence"""
    title: str
    description: str
    id: str = field(default_factory=lambda: f"TC-{str(uuid.uuid4())[:6]}")
    test_case_type: TestCaseType = TestCaseType.POSITIVE
    requirement_id: str = ""
    steps: List[str] = field(default_factory=list)
    expected_result: str = ""
    preconditions: List[str] = field(default_factory=list)
    test_data: List[Dict] = field(default_factory=list)
    priority: str = "Medium"
    tags: List[str] = field(default_factory=list)
    
    def __str__(self):
        return f"{self.id}: {self.title} ({self.test_case_type.value})"


@dataclass
class TestSuite:
    """Collection of test cases"""
    name: str
    description: str = ""
    requirements: List[Requirement] = field(default_factory=list)
    test_cases: List[TestCase] = field(default_factory=list)
    
    def add_requirement(self, req: Requirement):
        self.requirements.append(req)
    
    def add_test_case(self, tc: TestCase):
        self.test_cases.append(tc)
    
    def get_coverage(self) -> Dict[str, int]:
        coverage = {}
        for tc in self.test_cases:
            tc_type = tc.test_case_type.value
            coverage[tc_type] = coverage.get(tc_type, 0) + 1
        return coverage


class LLM_SDLC_Agent:
    """
    Full LLM-powered SDLC Expert Agent
    Uses LLM to understand PRD and generate intelligent test cases
    """
    
    def __init__(self):
        self.all_requirements: List[Requirement] = []
        self.all_test_cases: List[TestCase] = []
        self.test_suites: Dict[str, TestSuite] = {}
        self.conversation_history: List[Dict] = []
    
    def extract_requirements(self, prd_text: str) -> List[Requirement]:
        """
        Use LLM to intelligently extract requirements from PRD text
        """
        system_prompt = """You are an expert SDLC analyst. Your task is to extract all requirements from the given PRD text.
        
For each requirement found, provide it in JSON format with these fields:
- text: The exact requirement text
- type: One of: User Story, Functional, Non-Functional, Business Rule, Acceptance Criteria, Constraint, Assumption, Dependency, Security, Performance
- description: Brief explanation of what this requirement means
- priority: High, Medium, or Low
- category: Grouping category (e.g., Authentication, Data, UI, API)

Return ONLY a JSON array of requirement objects. Do not add any other text.

Example output:
[
  {"text": "As a user, I want to login...", "type": "User Story", "description": "User authentication need", "priority": "High", "category": "Authentication"},
  {"text": "The system shall validate input", "type": "Functional", "description": "Input validation requirement", "priority": "High", "category": "Data"}
]

Now analyze this PRD text and extract all requirements:"""
        
        user_message = prd_text
        
        # Call LLM to extract requirements
        llm_response = self._call_llm(system_prompt, user_message)
        
        # Parse JSON response
        requirements = self._parse_requirements(llm_response)
        self.all_requirements = requirements
        return requirements
    
    def generate_test_cases(self, requirements: Optional[List[Requirement]] = None) -> List[TestCase]:
        """
        Use LLM to generate intelligent test cases for each requirement
        """
        if requirements is None:
            requirements = self.all_requirements
        
        if not requirements:
            return []
        
        test_cases = []
        
        # Process requirements in batches for LLM
        for req in requirements:
            req_test_cases = self._generate_test_cases_for_requirement(req)
            test_cases.extend(req_test_cases)
        
        self.all_test_cases = test_cases
        return test_cases
    
    def _generate_test_cases_for_requirement(self, requirement: Requirement) -> List[TestCase]:
        """Generate test cases for a single requirement using LLM"""
        example_json = '[' + '\n  {' + '\n    "title": "Verify user can login with valid credentials",' + '\n    "description": "Test successful authentication",' + '\n    "type": "Positive",' + '\n    "steps": ["Navigate to login page", "Enter valid username and password", "Click login"],' + '\n    "expected_result": "User is authenticated and redirected to dashboard",' + '\n    "preconditions": ["User account exists"],' + '\n    "test_data": [{"username": "testuser", "password": "ValidPass123"}],' + '\n    "priority": "High",' + '\n    "tags": ["authentication", "login", "positive"]' + '\n  }' + '\n]'
        
        system_prompt = """You are an expert QA engineer. Generate comprehensive test cases for this requirement:

Requirement: {}
Type: {}
Description: {}

Generate test cases that cover:
1. Positive scenarios (normal operation)
2. Negative scenarios (error cases, invalid inputs)
3. Edge cases (boundary conditions, extreme values)
4. If applicable: Performance, Security, Usability aspects

For each test case, provide JSON with these fields:
- title: Clear test case title
- description: What this test verifies
- type: Positive, Negative, or Edge Case
- steps: Array of step-by-step instructions
- expected_result: What should happen
- preconditions: Any setup needed (array)
- test_data: Sample data to use (array of objects)
- priority: High, Medium, or Low
- tags: Array of categorization tags

Return ONLY a JSON array of test case objects. Do not add any other text.

Example output:
{}

Now generate test cases for the requirement above:""".format(
            requirement.text,
            requirement.requirement_type.value,
            requirement.description,
            example_json
        )
        
        user_message = requirement.text
        llm_response = self._call_llm(system_prompt, user_message)
        
        return self._parse_test_cases(llm_response, requirement.id)
    
    def create_test_suite(self, name: str, description: str = "", 
                          requirements: Optional[List[Requirement]] = None) -> TestSuite:
        """Create a test suite from requirements"""
        if requirements is None:
            requirements = self.all_requirements
        
        suite = TestSuite(name=name, description=description)
        
        for req in requirements:
            suite.add_requirement(req)
        
        test_cases = self.generate_test_cases(requirements)
        for tc in test_cases:
            suite.add_test_case(tc)
        
        self.test_suites[name] = suite
        return suite
    
    def analyze_prd(self, prd_text: str) -> Dict[str, Any]:
        """
        Complete PRD analysis: extract requirements and generate test cases
        """
        requirements = self.extract_requirements(prd_text)
        test_cases = self.generate_test_cases(requirements)
        
        return {
            "requirements": [r.to_dict() for r in requirements],
            "test_cases": [tc.to_dict() for tc in test_cases],
            "summary": self.get_summary()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get analysis summary"""
        req_by_type = {}
        for r in self.all_requirements:
            req_type = r.requirement_type.value
            req_by_type[req_type] = req_by_type.get(req_type, 0) + 1
        
        tc_by_type = {}
        for tc in self.all_test_cases:
            tc_type = tc.test_case_type.value
            tc_by_type[tc_type] = tc_by_type.get(tc_type, 0) + 1
        
        return {
            "total_requirements": len(self.all_requirements),
            "total_test_cases": len(self.all_test_cases),
            "requirements_by_type": req_by_type,
            "test_cases_by_type": tc_by_type,
            "test_suites": list(self.test_suites.keys())
        }
    
    def to_dict(self, requirement: Requirement) -> Dict:
        """Convert requirement to dictionary"""
        return {
            "id": requirement.id,
            "text": requirement.text,
            "type": requirement.requirement_type.value,
            "description": requirement.description,
            "priority": requirement.priority,
            "category": requirement.category,
            "dependencies": requirement.dependencies
        }
    
    def to_dict(self, test_case: TestCase) -> Dict:
        """Convert test case to dictionary"""
        return {
            "id": test_case.id,
            "title": test_case.title,
            "description": test_case.description,
            "type": test_case.test_case_type.value,
            "requirement_id": test_case.requirement_id,
            "steps": test_case.steps,
            "expected_result": test_case.expected_result,
            "preconditions": test_case.preconditions,
            "test_data": test_case.test_data,
            "priority": test_case.priority,
            "tags": test_case.tags
        }
    
    def _call_llm(self, system_prompt: str, user_message: str) -> str:
        """
        Call the LLM with structured prompt
        This is a placeholder - in actual implementation, this would call the real LLM
        """
        # For now, we'll use a mock implementation
        # In production, this would call the actual LLM API
        
        # Try to use the actual LLM if available
        try:
            from mistralai.client import MistralClient
            from mistralai.models.chat_completion import ChatMessage
            
            client = MistralClient()
            messages = [
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=user_message)
            ]
            
            response = client.chat(
                model="mistral-tiny",
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Fallback to mock for testing
            return self._mock_llm_call(system_prompt, user_message)
    
    def _mock_llm_call(self, system_prompt: str, user_message: str) -> str:
        """
        Mock LLM call for testing without actual LLM
        This generates realistic responses based on the prompt
        """
        # Simple mock that returns structured JSON based on prompt type
        if "extract all requirements" in system_prompt.lower():
            return self._mock_extract_requirements(user_message)
        elif "generate comprehensive test cases" in system_prompt.lower():
            # Extract requirement from the prompt
            req_text = user_message
            return self._mock_generate_test_cases(req_text)
        else:
            return json.dumps([])
    
    def _mock_extract_requirements(self, prd_text: str) -> str:
        """Mock requirement extraction"""
        # This is a simplified mock - real LLM would be much better
        import re
        
        requirements = []
        
        # Extract user stories
        user_story_pattern = r"As a\s+([^,]+),\s+I want\s+([^.]+)[.\s]*so that\s+([^.]+)"
        for match in re.finditer(user_story_pattern, prd_text, re.IGNORECASE):
            req_text = f"As a {match.group(1)}, I want {match.group(2)} so that {match.group(3)}"
            requirements.append({
                "text": req_text,
                "type": "User Story",
                "description": f"User need: {match.group(1)} wants to {match.group(2)}",
                "priority": "High",
                "category": "User Experience"
            })
        
        # Extract functional requirements
        functional_pattern = r"The system (shall|must|should|will)\s+([^.\n]+)"
        for match in re.finditer(functional_pattern, prd_text, re.IGNORECASE):
            req_text = f"The system {match.group(1)} {match.group(2)}"
            requirements.append({
                "text": req_text,
                "type": "Functional",
                "description": f"System requirement: {match.group(2)}",
                "priority": "High",
                "category": "Functional"
            })
        
        # Extract business rules
        br_pattern = r"(?:Business Rule|Rule|BR):\s*([^.\n]+)"
        for match in re.finditer(br_pattern, prd_text, re.IGNORECASE):
            requirements.append({
                "text": match.group(1).strip(),
                "type": "Business Rule",
                "description": f"Business logic: {match.group(1).strip()}",
                "priority": "High",
                "category": "Business Logic"
            })
        
        # Extract acceptance criteria
        ac_pattern = r"- \[(?: |x)\]\s*([^.\n]+)"
        for match in re.finditer(ac_pattern, prd_text, re.IGNORECASE):
            requirements.append({
                "text": match.group(1).strip(),
                "type": "Acceptance Criteria",
                "description": f"Acceptance: {match.group(1).strip()}",
                "priority": "High",
                "category": "Acceptance"
            })
        
        return json.dumps(requirements, indent=2)
    
    def _mock_generate_test_cases(self, requirement_text: str) -> str:
        """Mock test case generation"""
        # Generate realistic test cases based on requirement type
        test_cases = []
        
        # Positive test case
        test_cases.append({
            "title": f"Verify: {requirement_text[:50]}...",
            "description": f"Test that the system satisfies: {requirement_text[:100]}...",
            "type": "Positive",
            "steps": [
                "1. Set up test environment",
                "2. Execute the functionality related to this requirement",
                "3. Verify the expected behavior"
            ],
            "expected_result": f"The requirement '{requirement_text[:50]}...' is satisfied",
            "preconditions": ["System is in valid state"],
            "test_data": [],
            "priority": "High",
            "tags": ["positive", "requirement"]
        })
        
        # Negative test case
        test_cases.append({
            "title": f"Verify error handling for: {requirement_text[:50]}...",
            "description": f"Test that the system handles failures for: {requirement_text[:100]}...",
            "type": "Negative",
            "steps": [
                "1. Set up invalid scenario",
                "2. Attempt to execute the functionality",
                "3. Verify appropriate error is displayed"
            ],
            "expected_result": f"The system properly handles invalid cases for '{requirement_text[:50]}...'",
            "preconditions": ["Invalid input data"],
            "test_data": [{"invalid": "data"}],
            "priority": "Medium",
            "tags": ["negative", "error_handling"]
        })
        
        return json.dumps(test_cases, indent=2)
    
    def _parse_requirements(self, llm_output: str) -> List[Requirement]:
        """Parse LLM output into Requirement objects"""
        try:
            data = json.loads(llm_output)
            if not isinstance(data, list):
                return []
            
            requirements = []
            for item in data:
                req_type = getattr(RequirementType, item.get("type", "FUNCTIONAL"), RequirementType.FUNCTIONAL)
                req = Requirement(
                    text=item.get("text", ""),
                    requirement_type=req_type,
                    description=item.get("description", ""),
                    priority=item.get("priority", "Medium"),
                    category=item.get("category", "General"),
                    dependencies=item.get("dependencies", [])
                )
                requirements.append(req)
            return requirements
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing requirements: {e}")
            return []
    
    def _parse_test_cases(self, llm_output: str, requirement_id: str = "") -> List[TestCase]:
        """Parse LLM output into TestCase objects"""
        try:
            data = json.loads(llm_output)
            if not isinstance(data, list):
                return []
            
            test_cases = []
            for item in data:
                tc_type = getattr(TestCaseType, item.get("type", "POSITIVE"), TestCaseType.POSITIVE)
                tc = TestCase(
                    title=item.get("title", "Untitled Test Case"),
                    description=item.get("description", ""),
                    test_case_type=tc_type,
                    requirement_id=requirement_id,
                    steps=item.get("steps", []),
                    expected_result=item.get("expected_result", ""),
                    preconditions=item.get("preconditions", []),
                    test_data=item.get("test_data", []),
                    priority=item.get("priority", "Medium"),
                    tags=item.get("tags", [])
                )
                test_cases.append(tc)
            return test_cases
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing test cases: {e}")
            return []


# Global agent instance
llm_agent = LLM_SDLC_Agent()
