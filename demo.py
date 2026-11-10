#!/usr/bin/env python3
"""
Demonstration script for SDLC Expert Agent
Shows how to use the agent to extract requirements and generate test cases from PRD text
"""

from src.agent import SDLCExpertAgent
from src.templates import enhanced_generator


def demo_basic_usage():
    """Demonstrate basic usage of the SDLC Expert Agent"""
    print("=" * 60)
    print("SDLC Expert Agent - Basic Usage Demo")
    print("=" * 60)
    
    prd_text = """
    As a user, I want to reset my password via email so that I can regain access to my account.
    
    Acceptance Criteria:
    - User receives password reset email within 5 minutes
    - Reset link is valid for 24 hours
    - User can set new password using the link
    - System validates new password strength
    
    The system shall send password reset emails to registered users.
    The system must validate that the email address exists in the system.
    
    Business Rule: Password reset links expire after 24 hours.
    Business Rule: Users cannot reuse their last 5 passwords.
    
    Constraint: Cannot send more than 3 reset emails per hour to the same address.
    """
    
    print("\nPRD Text:")
    print("-" * 40)
    print(prd_text)
    print("-" * 40)
    
    agent = SDLCExpertAgent()
    requirements = agent.extract_requirements(prd_text)
    
    print(f"\nExtracted {len(requirements)} requirements:")
    for i, req in enumerate(requirements, 1):
        print(f"  {i}. [{req.requirement_type.value}] {req.text}")
    
    test_cases = agent.generate_test_cases(requirements)
    
    print(f"\nGenerated {len(test_cases)} test cases:")
    for i, tc in enumerate(test_cases, 1):
        print(f"  {i}. {tc.id}: {tc.title} ({tc.test_case_type.value})")
        if i <= 3:
            print(f"     Description: {tc.description}")
            print(f"     Steps: {len(tc.steps)}")
            print(f"     Expected: {tc.expected_result}")
            print()
    
    summary = agent.get_summary()
    print(f"\nSummary:")
    print(f"  Total requirements: {summary['total_requirements']}")
    print(f"  Total test cases: {summary['total_test_cases']}")
    print(f"  Requirements by type: {summary['requirements_by_type']}")
    print(f"  Test cases by type: {summary['test_cases_by_type']}")


def demo_enhanced_patterns():
    """Demonstrate enhanced pattern matching"""
    print("\n" + "=" * 60)
    print("Enhanced Pattern Matching Demo")
    print("=" * 60)
    
    login_prd = """
    As a user, I want to login to the system with my username and password.
    
    The system shall authenticate users using email and password.
    The system must validate that both username and password are provided.
    
    Business Rule: Accounts are locked after 5 failed login attempts.
    Constraint: Passwords must be at least 8 characters long.
    """
    
    print("\nLogin Feature PRD:")
    print("-" * 40)
    print(login_prd)
    print("-" * 40)
    
    agent = SDLCExpertAgent()
    requirements = agent.extract_requirements(login_prd)
    
    print(f"\nExtracted {len(requirements)} requirements")
    
    for req in requirements:
        print(f"\nRequirement: {req.text}")
        enhanced_tcs = agent.generate_enhanced_test_cases(req)
        print(f"  Enhanced test cases: {len(enhanced_tcs)}")
        for tc in enhanced_tcs:
            print(f"    - {tc.title} ({tc.test_case_type.value})")


def demo_test_suite():
    """Demonstrate test suite creation"""
    print("\n" + "=" * 60)
    print("Test Suite Creation Demo")
    print("=" * 60)
    
    prd_text = """
    As a shopper, I want to add products to my cart so that I can purchase them later.
    As a shopper, I want to view my cart contents so that I can see what I've added.
    As a shopper, I want to remove items from my cart so that I can correct mistakes.
    
    Acceptance Criteria:
    - User can add products to cart
    - Cart contents persist across sessions
    - User can update item quantities
    - User can remove items from cart
    
    The system shall maintain cart contents for logged-in users.
    The system must validate that requested quantities do not exceed available stock.
    """
    
    agent = SDLCExpertAgent()
    requirements = agent.extract_requirements(prd_text)
    
    suite = agent.create_test_suite("Shopping Cart Tests", "Test suite for shopping cart functionality")
    
    print(f"Created test suite: {suite.name}")
    print(f"Description: {suite.description}")
    print(f"Requirements: {len(suite.requirements)}")
    print(f"Test cases: {len(suite.test_cases)}")
    
    coverage = suite.get_coverage()
    print(f"\nTest case coverage:")
    for tc_type, count in coverage.items():
        print(f"  {tc_type}: {count}")
    
    print(f"\nSample test cases:")
    for i, tc in enumerate(suite.test_cases[:5], 1):
        print(f"  {i}. {tc.id}: {tc.title}")


def demo_export():
    """Demonstrate export functionality"""
    print("\n" + "=" * 60)
    print("Export Functionality Demo")
    print("=" * 60)
    
    prd_text = """
    As a user, I want to search for products so that I can find what I need.
    
    Acceptance Criteria:
    - User can search by product name
    - User can search by product description
    - Search results show matching products
    - Search is case-insensitive
    
    The system shall return search results within 2 seconds.
    Business Rule: Search results are limited to 100 items per page.
    """
    
    agent = SDLCExpertAgent()
    requirements = agent.extract_requirements(prd_text)
    test_cases = agent.generate_test_cases(requirements)
    
    print("Exported test cases (Markdown format):")
    print("-" * 40)
    
    for tc in test_cases[:3]:
        print(f"## {tc.id}: {tc.title}")
        print(f"**Type:** {tc.test_case_type.value}")
        print(f"**Priority:** {tc.priority}")
        print(f"**Description:** {tc.description}")
        print("\n**Steps:**")
        for i, step in enumerate(tc.steps, 1):
            print(f"  {i}. {step}")
        print(f"\n**Expected Result:** {tc.expected_result}")
        print(f"**Tags:** {', '.join(tc.tags)}")
        print("\n---")


def main():
    """Run all demonstrations"""
    print("SDLC Expert Agent - Full Demonstration")
    print("=" * 60)
    
    demo_basic_usage()
    demo_enhanced_patterns()
    demo_test_suite()
    demo_export()
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("To try the interactive interface, run: python -m src.main")
    print("=" * 60)


if __name__ == "__main__":
    main()
