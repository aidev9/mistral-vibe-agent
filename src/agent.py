"""
SDLC Expert Agent - Core functionality for extracting requirements and generating test cases
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple
import uuid


class RequirementType(Enum):
    """Types of requirements that can be extracted from PRD"""
    FUNCTIONAL = "Functional"
    NON_FUNCTIONAL = "Non-Functional"
    BUSINESS_RULE = "Business Rule"
    USER_STORY = "User Story"
    ACCEPTANCE_CRITERIA = "Acceptance Criteria"
    CONSTRAINT = "Constraint"
    ASSUMPTION = "Assumption"
    DEPENDENCY = "Dependency"


class TestCaseType(Enum):
    """Types of test cases"""
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    EDGE = "Edge Case"
    PERFORMANCE = "Performance"
    SECURITY = "Security"
    USABILITY = "Usability"
    COMPATIBILITY = "Compatibility"


@dataclass
class Requirement:
    """Represents an extracted requirement"""
    text: str
    requirement_type: RequirementType = RequirementType.FUNCTIONAL
    category: str = "General"
    priority: str = "Medium"
    dependencies: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    def __str__(self):
        return f"[{self.requirement_type.value}] {self.text}"


@dataclass
class TestCase:
    """Represents a generated test case"""
    title: str
    description: str
    test_case_type: TestCaseType = TestCaseType.POSITIVE
    requirement_id: str = ""
    steps: List[str] = field(default_factory=list)
    expected_result: str = ""
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    priority: str = "Medium"
    tags: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: f"TC-{str(uuid.uuid4())[:6]}")
    
    def __str__(self):
        return f"{self.id}: {self.title} ({self.test_case_type.value})"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.test_case_type.value,
            "requirement_id": self.requirement_id,
            "steps": self.steps,
            "expected_result": self.expected_result,
            "preconditions": self.preconditions,
            "postconditions": self.postconditions,
            "priority": self.priority,
            "tags": self.tags
        }


@dataclass
class TestSuite:
    """Collection of test cases for a feature or requirement"""
    name: str
    description: str = ""
    requirements: List[Requirement] = field(default_factory=list)
    test_cases: List[TestCase] = field(default_factory=list)
    
    def add_requirement(self, requirement: Requirement):
        self.requirements.append(requirement)
    
    def add_test_case(self, test_case: TestCase):
        self.test_cases.append(test_case)
    
    def get_test_cases_by_type(self, test_type: TestCaseType) -> List[TestCase]:
        return [tc for tc in self.test_cases if tc.test_case_type == test_type]
    
    def get_coverage(self) -> Dict[str, int]:
        """Get coverage statistics"""
        coverage = {}
        for tc in self.test_cases:
            tc_type = tc.test_case_type.value
            coverage[tc_type] = coverage.get(tc_type, 0) + 1
        return coverage


class SDLCExpertAgent:
    """Main agent class that extracts requirements from PRD text and generates test cases"""
    
    def __init__(self):
        self.test_suites: Dict[str, TestSuite] = {}
        self.all_requirements: List[Requirement] = []
        self.all_test_cases: List[TestCase] = []
        
        self.patterns = {
            "user_story": [
                r"As a\s+([^\n]+),\s+I want\s+([^\n.]+)[.\s]*so that\s+([^\n.]+)",
                r"As a\s+([^\n]+),\s+I want\s+([^\n.]+)",
            ],
            "acceptance_criteria": [
                r"Acceptance Criteria:\s*([^\n]+)",
                r"AC:\s*([^\n]+)",
                r"- \[ \]\s*([^\n]+)",
                r"- \[x\]\s*([^\n]+)",
            ],
            "functional": [
                r"The system shall\s+([^\n.]+)",
                r"The system must\s+([^\n.]+)",
                r"Shall\s+([^\n.]+)",
                r"Must\s+([^\n.]+)",
                r"Should\s+([^\n.]+)",
            ],
            "non_functional": [
                r"Performance:\s*([^\n]+)",
                r"Security:\s*([^\n]+)",
                r"Scalability:\s*([^\n]+)",
                r"Response time:\s*([^\n]+)",
                r"shall respond within\s+([^\n.]+)",
            ],
            "business_rule": [
                r"Business Rule:\s*([^\n]+)",
                r"BR:\s*([^\n]+)",
                r"Rule:\s*([^\n]+)",
            ],
            "constraint": [
                r"Constraint:\s*([^\n]+)",
                r"Limitation:\s*([^\n]+)",
                r"Cannot\s+([^\n.]+)",
            ],
        }
        
        self.test_rules = {
            "user_story": self._generate_from_user_story,
            "acceptance_criteria": self._generate_from_acceptance_criteria,
            "functional": self._generate_from_functional,
            "business_rule": self._generate_from_business_rule,
        }
    
    def extract_requirements(self, prd_text: str) -> List[Requirement]:
        """Extract requirements from PRD text"""
        requirements = []
        lines = prd_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('='):
                continue
            req = self._extract_from_line(line)
            if req:
                requirements.append(req)
        
        clean_text = self._clean_text(prd_text)
        user_stories = self._extract_user_stories(clean_text)
        requirements.extend(user_stories)
        ac_requirements = self._extract_acceptance_criteria(clean_text, lines)
        requirements.extend(ac_requirements)
        
        requirements = self._deduplicate_requirements(requirements)
        requirements = [r for r in requirements if len(r.text.strip()) > 10]
        
        self.all_requirements = requirements
        return requirements
    
    def _extract_from_line(self, line: str) -> Optional[Requirement]:
        """Extract a requirement from a single line"""
        line_lower = line.lower().strip()
        
        if not line_lower or line_lower.startswith('#') or line_lower.startswith('='):
            return None
        
        if any(keyword in line_lower for keyword in ["business rule:", "rule:", "br:"]):
            text = re.sub(r'^(Business Rule|Rule|BR):\s*', '', line, flags=re.IGNORECASE).strip()
            if text:
                return Requirement(text=text, requirement_type=RequirementType.BUSINESS_RULE, category="Business Logic")
        
        if any(keyword in line_lower for keyword in ["constraint:", "limitation:", "cannot", "must not"]):
            text = re.sub(r'^(Constraint|Limitation):\s*', '', line, flags=re.IGNORECASE).strip()
            if text:
                return Requirement(text=text, requirement_type=RequirementType.CONSTRAINT, category="Constraints")
        
        if any(keyword in line_lower for keyword in ["performance:", "security:", "scalability:", "response time:"]):
            text = re.sub(r'^(Performance|Security|Scalability|Response time):\s*', '', line, flags=re.IGNORECASE).strip()
            if text:
                return Requirement(text=text, requirement_type=RequirementType.NON_FUNCTIONAL, category="Non-Functional")
        
        if any(keyword in line_lower for keyword in ["the system shall", "the system must", "shall", "must"]):
            text = line
            if "the system shall" in line_lower:
                text = re.sub(r'^.*the system shall\s+', '', line, flags=re.IGNORECASE).strip()
            elif "the system must" in line_lower:
                text = re.sub(r'^.*the system must\s+', '', line, flags=re.IGNORECASE).strip()
            elif line_lower.startswith("shall "):
                text = re.sub(r'^shall\s+', '', line, flags=re.IGNORECASE).strip()
            elif line_lower.startswith("must "):
                text = re.sub(r'^must\s+', '', line, flags=re.IGNORECASE).strip()
            
            if text:
                return Requirement(text=f"The system shall {text}", requirement_type=RequirementType.FUNCTIONAL, category="Functional")
        
        return None
    
    def generate_test_cases(self, requirements: Optional[List[Requirement]] = None) -> List[TestCase]:
        """Generate test cases from extracted requirements"""
        if requirements is None:
            requirements = self.all_requirements
        
        test_cases = []
        for req in requirements:
            generator = self.test_rules.get(req.requirement_type.value.lower(), self._generate_default_test_cases)
            req_test_cases = generator(req)
            test_cases.extend(req_test_cases)
        
        self.all_test_cases = test_cases
        return test_cases
    
    def create_test_suite(self, name: str, description: str = "", requirements: Optional[List[Requirement]] = None) -> TestSuite:
        """Create a test suite from requirements"""
        if requirements is None:
            requirements = self.all_requirements
        
        test_suite = TestSuite(name=name, description=description)
        for req in requirements:
            test_suite.add_requirement(req)
        
        test_cases = self.generate_test_cases(requirements)
        for tc in test_cases:
            test_suite.add_test_case(tc)
        
        self.test_suites[name] = test_suite
        return test_suite
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize PRD text"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\*_~`]', '', text)
        text = re.sub(r'#\s*', '', text)
        text = re.sub(r'\n\n+', '\n', text)
        return text.strip()
    
    def _extract_user_stories(self, text: str) -> List[Requirement]:
        """Extract user stories from text"""
        requirements = []
        patterns = self.patterns["user_story"]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                if len(groups) >= 2:
                    user_story = f"As a {groups[0]}, I want {groups[1]}"
                    if len(groups) >= 3:
                        user_story += f" so that {groups[2]}"
                    requirements.append(Requirement(text=user_story, requirement_type=RequirementType.USER_STORY, category="User Experience"))
        
        return requirements
    
    def _extract_acceptance_criteria(self, text: str, lines: List[str]) -> List[Requirement]:
        """Extract acceptance criteria from text"""
        requirements = []
        patterns = self.patterns["acceptance_criteria"]
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if any(header in line_lower for header in ["acceptance criteria", "ac:", "criteria:"]):
                j = i + 1
                while j < len(lines) and lines[j].strip():
                    ac_line = lines[j].strip()
                    if ac_line and not ac_line.startswith('#'):
                        ac_text = re.sub(r'^\[[ xX]?\]\s*', '', ac_line)
                        ac_text = re.sub(r'^[\-\*\d.]\s*', '', ac_text)
                        if ac_text:
                            requirements.append(Requirement(text=ac_text, requirement_type=RequirementType.ACCEPTANCE_CRITERIA, category="Acceptance"))
                    j += 1
                break
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                ac_text = match.group(1).strip()
                if ac_text:
                    requirements.append(Requirement(text=ac_text, requirement_type=RequirementType.ACCEPTANCE_CRITERIA, category="Acceptance"))
        
        return requirements
    
    def _extract_functional_requirements(self, text: str) -> List[Requirement]:
        """Extract functional requirements from text"""
        requirements = []
        patterns = self.patterns["functional"]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                req_text = match.group(1).strip()
                if req_text:
                    requirements.append(Requirement(text=f"The system shall {req_text}", requirement_type=RequirementType.FUNCTIONAL, category="Functional"))
        
        return requirements
    
    def _extract_non_functional_requirements(self, text: str) -> List[Requirement]:
        """Extract non-functional requirements from text"""
        requirements = []
        patterns = self.patterns["non_functional"]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                req_text = match.group(1).strip()
                if req_text:
                    requirements.append(Requirement(text=req_text, requirement_type=RequirementType.NON_FUNCTIONAL, category="Non-Functional"))
        
        return requirements
    
    def _extract_business_rules(self, text: str) -> List[Requirement]:
        """Extract business rules from text"""
        requirements = []
        patterns = self.patterns["business_rule"]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                rule_text = match.group(1).strip()
                if rule_text:
                    requirements.append(Requirement(text=rule_text, requirement_type=RequirementType.BUSINESS_RULE, category="Business Logic"))
        
        return requirements
    
    def _extract_constraints(self, text: str) -> List[Requirement]:
        """Extract constraints from text"""
        requirements = []
        patterns = self.patterns["constraint"]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                constraint_text = match.group(1).strip()
                if constraint_text:
                    requirements.append(Requirement(text=constraint_text, requirement_type=RequirementType.CONSTRAINT, category="Constraints"))
        
        return requirements
    
    def _deduplicate_requirements(self, requirements: List[Requirement]) -> List[Requirement]:
        """Remove duplicate requirements"""
        seen = set()
        unique_reqs = []
        for req in requirements:
            req_key = req.text.lower().strip()
            if req_key not in seen:
                seen.add(req_key)
                unique_reqs.append(req)
        return unique_reqs
    
    def _generate_from_user_story(self, requirement: Requirement) -> List[TestCase]:
        """Generate test cases from a user story"""
        test_cases = []
        pattern = r"As a\s+([^,]+),\s+I want\s+([^.]+)[.\s]*so that\s+([^.]+)"
        match = re.search(pattern, requirement.text, re.IGNORECASE)
        
        if match:
            user_role = match.group(1).strip()
            action = match.group(2).strip()
            benefit = match.group(3).strip()
        else:
            user_role = "user"
            action = requirement.text
            benefit = "achieve the goal"
        
        positive_tc = TestCase(
            title=f"Verify {user_role} can {action}",
            description=f"Test that {user_role} can successfully {action} to {benefit}",
            test_case_type=TestCaseType.POSITIVE,
            requirement_id=requirement.id,
            steps=[f"1. Navigate to the {action.split()[0]} feature", f"2. As a {user_role}, perform the action: {action}", "3. Verify the action completes successfully"],
            expected_result=f"The {user_role} can {action} and {benefit}",
            priority="High",
            tags=["user_story", "positive", user_role.lower()]
        )
        test_cases.append(positive_tc)
        
        negative_tc = TestCase(
            title=f"Verify {user_role} cannot {action} with invalid input",
            description=f"Test that {user_role} cannot {action} with invalid or missing data",
            test_case_type=TestCaseType.NEGATIVE,
            requirement_id=requirement.id,
            steps=[f"1. Navigate to the {action.split()[0]} feature", f"2. As a {user_role}, attempt to {action} with invalid input", "3. Verify appropriate error message is displayed"],
            expected_result=f"The system prevents {user_role} from {action} with invalid input",
            priority="Medium",
            tags=["user_story", "negative", "validation"]
        )
        test_cases.append(negative_tc)
        
        return test_cases
    
    def _generate_from_acceptance_criteria(self, requirement: Requirement) -> List[TestCase]:
        """Generate test cases from acceptance criteria"""
        test_cases = []
        positive_tc = TestCase(
            title=f"Verify: {requirement.text}",
            description=f"Test that the system meets the acceptance criteria: {requirement.text}",
            test_case_type=TestCaseType.POSITIVE,
            requirement_id=requirement.id,
            steps=["1. Set up the test scenario", f"2. Perform the action described in: {requirement.text}", "3. Verify the expected outcome"],
            expected_result=f"The acceptance criteria '{requirement.text}' is satisfied",
            priority="High",
            tags=["acceptance_criteria", "positive"]
        )
        test_cases.append(positive_tc)
        
        if any(word in requirement.text.lower() for word in ["must", "shall", "should", "can", "will"]):
            negative_tc = TestCase(
                title=f"Verify failure when: {requirement.text}",
                description=f"Test that the system handles failure cases for: {requirement.text}",
                test_case_type=TestCaseType.NEGATIVE,
                requirement_id=requirement.id,
                steps=["1. Set up a scenario where the acceptance criteria cannot be met", "2. Attempt to perform the action", "3. Verify appropriate error handling"],
                expected_result=f"The system properly handles cases where '{requirement.text}' cannot be satisfied",
                priority="Medium",
                tags=["acceptance_criteria", "negative", "error_handling"]
            )
            test_cases.append(negative_tc)
        
        return test_cases
    
    def _generate_from_functional(self, requirement: Requirement) -> List[TestCase]:
        """Generate test cases from functional requirements"""
        test_cases = []
        req_text = requirement.text.lower()
        action = re.sub(r"^the system (shall|must|should|will)\s+", "", req_text).strip()
        
        positive_tc = TestCase(
            title=f"Verify system {action}",
            description=f"Test that the system correctly {action}",
            test_case_type=TestCaseType.POSITIVE,
            requirement_id=requirement.id,
            steps=["1. Set up test environment", f"2. Trigger the action: {action}", "3. Verify the expected behavior"],
            expected_result=f"The system successfully {action}",
            priority="High",
            tags=["functional", "positive"]
        )
        test_cases.append(positive_tc)
        
        negative_tc = TestCase(
            title=f"Verify system handles failure for: {action}",
            description=f"Test that the system handles failures when attempting to {action}",
            test_case_type=TestCaseType.NEGATIVE,
            requirement_id=requirement.id,
            steps=["1. Set up a failure scenario", f"2. Attempt to {action} with invalid conditions", "3. Verify error handling"],
            expected_result=f"The system properly handles failures when {action}",
            priority="Medium",
            tags=["functional", "negative", "error_handling"]
        )
        test_cases.append(negative_tc)
        
        if any(word in action for word in ["calculate", "process", "handle", "validate"]):
            edge_tc = TestCase(
                title=f"Verify edge cases for: {action}",
                description=f"Test edge cases when the system {action}",
                test_case_type=TestCaseType.EDGE,
                requirement_id=requirement.id,
                steps=["1. Set up edge case scenario", f"2. Perform action: {action} with boundary values", "3. Verify correct handling"],
                expected_result=f"The system correctly handles edge cases when {action}",
                priority="Medium",
                tags=["functional", "edge_case", "boundary"]
            )
            test_cases.append(edge_tc)
        
        return test_cases
    
    def _generate_from_business_rule(self, requirement: Requirement) -> List[TestCase]:
        """Generate test cases from business rules"""
        test_cases = []
        rule_text = requirement.text
        
        satisfied_tc = TestCase(
            title=f"Verify business rule: {rule_text}",
            description=f"Test that the business rule '{rule_text}' is enforced",
            test_case_type=TestCaseType.POSITIVE,
            requirement_id=requirement.id,
            steps=["1. Set up scenario where business rule should be applied", "2. Perform the relevant action", "3. Verify the rule is enforced correctly"],
            expected_result=f"The business rule '{rule_text}' is properly enforced",
            priority="High",
            tags=["business_rule", "positive", "enforcement"]
        )
        test_cases.append(satisfied_tc)
        
        violated_tc = TestCase(
            title=f"Verify business rule violation: {rule_text}",
            description=f"Test that the system prevents violations of business rule: {rule_text}",
            test_case_type=TestCaseType.NEGATIVE,
            requirement_id=requirement.id,
            steps=["1. Set up scenario that would violate the business rule", "2. Attempt to perform the action", "3. Verify the violation is prevented"],
            expected_result=f"The system prevents violations of business rule '{rule_text}'",
            priority="High",
            tags=["business_rule", "negative", "violation", "prevention"]
        )
        test_cases.append(violated_tc)
        
        return test_cases
    
    def _generate_default_test_cases(self, requirement: Requirement) -> List[TestCase]:
        """Generate default test cases for any requirement type"""
        test_cases = []
        positive_tc = TestCase(
            title=f"Verify: {requirement.text}",
            description=f"Test that the requirement is satisfied: {requirement.text}",
            test_case_type=TestCaseType.POSITIVE,
            requirement_id=requirement.id,
            steps=["1. Set up test scenario", "2. Execute the relevant functionality", "3. Verify the requirement is met"],
            expected_result=f"The requirement '{requirement.text}' is satisfied",
            priority="Medium",
            tags=["default", "positive"]
        )
        test_cases.append(positive_tc)
        return test_cases
    
    def generate_enhanced_test_cases(self, requirement: Requirement) -> List[TestCase]:
        """Generate test cases using enhanced pattern matching"""
        try:
            from .templates import enhanced_generator
            tc_dicts = enhanced_generator.generate_from_text(requirement.text, requirement.id)
            test_cases = []
            for tc_dict in tc_dicts:
                tc_type = TestCaseType(tc_dict.get('type', 'Positive'))
                tc = TestCase(
                    id=tc_dict.get('id', f"TC-{str(uuid.uuid4())[:6]}"),
                    title=tc_dict.get('title', f"Verify: {requirement.text[:50]}"),
                    description=tc_dict.get('description', f"Test: {requirement.text}"),
                    test_case_type=tc_type,
                    requirement_id=tc_dict.get('requirement_id', requirement.id),
                    steps=tc_dict.get('steps', []),
                    expected_result=tc_dict.get('expected_result', f"Requirement satisfied: {requirement.text[:50]}"),
                    priority=tc_dict.get('priority', 'Medium'),
                    tags=tc_dict.get('tags', [])
                )
                test_cases.append(tc)
            return test_cases
        except ImportError:
            return self._generate_default_test_cases(requirement)
    
    def get_summary(self) -> Dict:
        """Get a summary of the extracted requirements and generated test cases"""
        return {
            "total_requirements": len(self.all_requirements),
            "total_test_cases": len(self.all_test_cases),
            "requirements_by_type": self._count_by_type(self.all_requirements, RequirementType),
            "test_cases_by_type": self._count_by_type(self.all_test_cases, TestCaseType),
            "test_suites": list(self.test_suites.keys())
        }
    
    def _count_by_type(self, items: List, enum_class: Enum) -> Dict:
        """Count items by their enum type"""
        counts = {}
        for item in items:
            type_name = getattr(item, 'requirement_type' if hasattr(item, 'requirement_type') else 'test_case_type').value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts
