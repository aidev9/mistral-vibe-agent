"""
Unit tests for SDLC Expert Agent
"""

import unittest
from src.agent import SDLCExpertAgent, Requirement, TestCase, RequirementType, TestCaseType


class TestRequirementExtraction(unittest.TestCase):
    """Test requirement extraction functionality"""
    
    def setUp(self):
        self.agent = SDLCExpertAgent()
    
    def test_extract_user_stories(self):
        """Test extraction of user stories"""
        prd_text = """
        As a user, I want to login to the system so that I can access my account.
        As an admin, I want to manage users so that I can control access.
        """
        requirements = self.agent.extract_requirements(prd_text)
        
        user_stories = [r for r in requirements if r.requirement_type == RequirementType.USER_STORY]
        self.assertEqual(len(user_stories), 2)
        
        # Check first user story
        self.assertIn("user", user_stories[0].text.lower())
        self.assertIn("login", user_stories[0].text.lower())
    
    def test_extract_functional_requirements(self):
        """Test extraction of functional requirements"""
        prd_text = """
        The system shall authenticate users using email and password.
        The system must validate input data.
        """
        requirements = self.agent.extract_requirements(prd_text)
        
        functional = [r for r in requirements if r.requirement_type == RequirementType.FUNCTIONAL]
        self.assertGreaterEqual(len(functional), 2)
    
    def test_extract_acceptance_criteria(self):
        """Test extraction of acceptance criteria"""
        prd_text = """
        Acceptance Criteria:
        - User can login with valid credentials
        - System displays error for invalid login
        - Password reset email is sent within 5 minutes
        """
        requirements = self.agent.extract_requirements(prd_text)
        
        acceptance = [r for r in requirements if r.requirement_type == RequirementType.ACCEPTANCE_CRITERIA]
        self.assertGreaterEqual(len(acceptance), 3)
    
    def test_extract_business_rules(self):
        """Test extraction of business rules"""
        prd_text = """
        Business Rule: Passwords must be at least 8 characters long.
        Rule: Accounts are locked after 5 failed attempts.
        """
        requirements = self.agent.extract_requirements(prd_text)
        
        business_rules = [r for r in requirements if r.requirement_type == RequirementType.BUSINESS_RULE]
        self.assertGreaterEqual(len(business_rules), 2)
    
    def test_extract_non_functional(self):
        """Test extraction of non-functional requirements"""
        prd_text = """
        Performance: Response time shall be under 2 seconds.
        Security: All data shall be encrypted.
        """
        requirements = self.agent.extract_requirements(prd_text)
        
        non_functional = [r for r in requirements if r.requirement_type == RequirementType.NON_FUNCTIONAL]
        self.assertGreaterEqual(len(non_functional), 2)


class TestTestCaseGeneration(unittest.TestCase):
    """Test test case generation functionality"""
    
    def setUp(self):
        self.agent = SDLCExpertAgent()
    
    def test_generate_test_cases_from_user_story(self):
        """Test test case generation from user story"""
        requirement = Requirement(
            text="As a user, I want to login to the system so that I can access my account",
            requirement_type=RequirementType.USER_STORY
        )
        
        test_cases = self.agent._generate_from_user_story(requirement)
        
        self.assertGreaterEqual(len(test_cases), 2)
        
        # Check for positive and negative test cases
        positive = [tc for tc in test_cases if tc.test_case_type == TestCaseType.POSITIVE]
        negative = [tc for tc in test_cases if tc.test_case_type == TestCaseType.NEGATIVE]
        
        self.assertGreaterEqual(len(positive), 1)
        self.assertGreaterEqual(len(negative), 1)
    
    def test_generate_test_cases_from_functional(self):
        """Test test case generation from functional requirement"""
        requirement = Requirement(
            text="The system shall validate user input",
            requirement_type=RequirementType.FUNCTIONAL
        )
        
        test_cases = self.agent._generate_from_functional(requirement)
        
        self.assertGreaterEqual(len(test_cases), 2)
        
        # Should have positive, negative, and possibly edge cases
        types = set(tc.test_case_type for tc in test_cases)
        self.assertIn(TestCaseType.POSITIVE, types)
        self.assertIn(TestCaseType.NEGATIVE, types)
    
    def test_generate_test_cases_from_business_rule(self):
        """Test test case generation from business rule"""
        requirement = Requirement(
            text="Passwords must be at least 8 characters long",
            requirement_type=RequirementType.BUSINESS_RULE
        )
        
        test_cases = self.agent._generate_from_business_rule(requirement)
        
        self.assertEqual(len(test_cases), 2)
        
        # Should have positive (rule satisfied) and negative (rule violated)
        positive = [tc for tc in test_cases if tc.test_case_type == TestCaseType.POSITIVE]
        negative = [tc for tc in test_cases if tc.test_case_type == TestCaseType.NEGATIVE]
        
        self.assertEqual(len(positive), 1)
        self.assertEqual(len(negative), 1)
    
    def test_full_workflow(self):
        """Test complete workflow from PRD to test cases"""
        prd_text = """
        As a user, I want to reset my password via email so that I can regain access to my account.
        
        Acceptance Criteria:
        - User receives password reset email
        - Reset link is valid for 24 hours
        - User can set new password
        
        The system shall send password reset emails.
        Business Rule: Password reset links expire after 24 hours.
        """
        
        # Extract requirements
        requirements = self.agent.extract_requirements(prd_text)
        self.assertGreaterEqual(len(requirements), 4)
        
        # Generate test cases
        test_cases = self.agent.generate_test_cases(requirements)
        self.assertGreaterEqual(len(test_cases), 8)
        
        # Check summary
        summary = self.agent.get_summary()
        self.assertEqual(summary['total_requirements'], len(requirements))
        self.assertEqual(summary['total_test_cases'], len(test_cases))


class TestTestSuite(unittest.TestCase):
    """Test test suite functionality"""
    
    def setUp(self):
        self.agent = SDLCExpertAgent()
    
    def test_create_test_suite(self):
        """Test test suite creation"""
        prd_text = "As a user, I want to login to the system"
        
        requirements = self.agent.extract_requirements(prd_text)
        suite = self.agent.create_test_suite("Login Tests", "Test suite for login functionality")
        
        self.assertEqual(suite.name, "Login Tests")
        self.assertEqual(suite.description, "Test suite for login functionality")
        self.assertGreaterEqual(len(suite.requirements), 1)
        self.assertGreaterEqual(len(suite.test_cases), 1)
    
    def test_test_suite_coverage(self):
        """Test test suite coverage statistics"""
        prd_text = "As a user, I want to login to the system"
        
        requirements = self.agent.extract_requirements(prd_text)
        suite = self.agent.create_test_suite("Login Tests")
        
        coverage = suite.get_coverage()
        self.assertIn("Positive", coverage)
        self.assertGreaterEqual(coverage["Positive"], 1)


if __name__ == '__main__':
    unittest.main()
