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
