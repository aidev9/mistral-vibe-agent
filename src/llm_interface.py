"""
Conversational Interface for LLM-Powered SDLC Expert Agent
"""

import sys
from typing import Optional, List, Dict, Any
from .llm_agent import LLM_SDLC_Agent, Requirement, TestCase, TestSuite, RequirementType, TestCaseType


class LLM_ConversationalInterface:
    """
    Interactive CLI for the LLM-powered SDLC Expert Agent
    """
    
    def __init__(self):
        self.agent = LLM_SDLC_Agent()
        self.current_prd: Optional[str] = None
        self.current_suite: Optional[TestSuite] = None
    
    def run(self):
        """Main entry point for conversational interface"""
        print("=" * 70)
        print("  LLM SDLC Expert Agent - PRD to Test Cases")
        print("=" * 70)
        print("\nI'm your AI-powered SDLC Expert Agent.")
        print("I use LLM intelligence to extract requirements and generate test cases.")
        print("\nType 'help' for commands, 'quit' to exit.")
        print()
        
        while True:
            try:
                command = input("llm-sdlc> ").strip()
                if not command:
                    continue
                
                if not self._process_command(command):
                    break
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
    
    def _process_command(self, command: str) -> bool:
        """Process user command"""
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        commands = {
            ('quit', 'exit', 'q'): lambda: self._quit(),
            ('help', 'h', '?'): lambda: self._show_help(),
            ('load', 'read', 'open'): lambda: self._load_prd(' '.join(args)) if args else self._load_prd_interactive(),
            ('paste', 'text', 'input'): lambda: self._load_prd_interactive(),
            ('analyze', 'extract', 'parse'): lambda: self._analyze_prd(),
            ('testcases', 'tc', 'tests'): lambda: self._generate_test_cases(),
            ('show', 'display', 'list'): lambda: self._show(' '.join(args)) if args else self._show_summary(),
            ('requirements', 'req', 'reqs'): lambda: self._show_requirements(),
            ('suite', 'create', 'new'): lambda: self._create_suite(' '.join(args)) if args else self._create_suite_interactive(),
            ('export', 'save', 'write'): lambda: self._export(' '.join(args)) if args else self._export_interactive(),
            ('clear', 'reset', 'restart'): lambda: self._reset(),
            ('info', 'summary', 'stats'): lambda: self._show_summary(),
            ('llm', 'ai', 'intelligent'): lambda: self._show_llm_info(),
        }
        
        for cmd_tuple, handler in commands.items():
            if cmd in cmd_tuple:
                result = handler()
                if result is False:
                    return False
                return True
        
        # Unknown command
        if cmd == 'quit':
            return False
        
        print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")
        return True
    
    def _quit(self) -> bool:
        """Exit the application"""
        print("Goodbye!")
        return False
    
    def _show_help(self):
        """Display help information"""
        print("\n" + "=" * 70)
        print("  Available Commands - LLM SDLC Expert Agent")
        print("=" * 70)
        
        commands = {
            "PRD Input": [
                ("load <file>", "Load PRD from a file"),
                ("paste", "Paste PRD text directly"),
                ("read <file>", "Same as load"),
            ],
            "Analysis": [
                ("analyze", "Extract requirements using LLM"),
                ("extract", "Same as analyze"),
                ("testcases", "Generate AI test cases"),
                ("tc", "Same as testcases"),
            ],
            "Display": [
                ("show", "Show analysis summary"),
                ("show requirements", "Show extracted requirements"),
                ("show testcases", "Show generated test cases"),
                ("requirements", "Same as show requirements"),
                ("info", "Show summary statistics"),
            ],
            "Test Suite": [
                ("suite <name>", "Create test suite"),
                ("create <name>", "Same as suite"),
            ],
            "Export": [
                ("export <file>", "Export test cases to file"),
                ("save <file>", "Same as export"),
            ],
            "Utility": [
                ("clear", "Reset current state"),
                ("reset", "Same as clear"),
                ("help", "Show this help"),
                ("quit", "Exit application"),
                ("llm", "Show LLM information"),
            ]
        }
        
        for category, cmds in commands.items():
            print(f"\n{category}:")
            for cmd, desc in cmds:
                print(f"  {cmd:<20} - {desc}")
        
        print("\n" + "=" * 70)
    
    def _load_prd(self, filename: str):
        """Load PRD from file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.current_prd = f.read()
            print(f"✓ Loaded PRD from '{filename}' ({len(self.current_prd)} characters)")
            print("  Use 'analyze' to extract requirements with LLM intelligence.")
        except FileNotFoundError:
            print(f"✗ Error: File '{filename}' not found.")
        except Exception as e:
            print(f"✗ Error reading file: {e}")
    
    def _load_prd_interactive(self):
        """Load PRD text interactively"""
        print("\nEnter your PRD text (press Enter twice to finish):")
        lines = []
        while True:
            try:
                line = input()
                if line == '':
                    if len(lines) > 0 and lines[-1] == '':
                        break
                lines.append(line)
            except EOFError:
                break
        
        self.current_prd = '\n'.join(lines[:-1]) if lines and lines[-1] == '' else '\n'.join(lines)
        print(f"\n✓ PRD loaded ({len(self.current_prd)} characters)")
        print("  Use 'analyze' to extract requirements with LLM intelligence.")
    
    def _analyze_prd(self):
        """Analyze PRD using LLM"""
        if not self.current_prd:
            print("✗ No PRD loaded. Use 'load' or 'paste' first.")
            return
        
        print("\n🤖 Analyzing PRD with LLM intelligence...")
        print("(This may take a moment as the LLM processes your text)")
        
        try:
            requirements = self.agent.extract_requirements(self.current_prd)
            
            print(f"\n✓ Extracted {len(requirements)} requirements:")
            for i, req in enumerate(requirements, 1):
                print(f"  {i}. [{req.requirement_type.value}] {req.text[:60]}...")
            
            print(f"\n  Use 'testcases' to generate AI-powered test cases.")
            print(f"  Use 'show requirements' to see details.")
            
        except Exception as e:
            print(f"\n✗ Error analyzing PRD: {e}")
    
    def _generate_test_cases(self):
        """Generate test cases using LLM"""
        if len(self.agent.all_requirements) == 0:
            print("✗ No requirements extracted. Use 'analyze' first.")
            return
        
        print("\n🤖 Generating AI test cases...")
        print("(This may take a moment as the LLM generates test cases)")
        
        try:
            test_cases = self.agent.generate_test_cases()
            
            print(f"\n✓ Generated {len(test_cases)} test cases:")
            
            # Group by type
            by_type: Dict[str, List[TestCase]] = {}
            for tc in test_cases:
                type_name = tc.test_case_type.value
                if type_name not in by_type:
                    by_type[type_name] = []
                by_type[type_name].append(tc)
            
            for type_name, tcs in by_type.items():
                print(f"\n  {type_name} ({len(tcs)}):")
                for tc in tcs[:3]:  # Show first 3 of each type
                    print(f"    • {tc.id}: {tc.title}")
                if len(tcs) > 3:
                    print(f"    ... and {len(tcs) - 3} more")
            
            print(f"\n  Use 'show testcases' to see all test cases in detail.")
            print(f"  Use 'suite <name>' to create a test suite.")
            
        except Exception as e:
            print(f"\n✗ Error generating test cases: {e}")
    
    def _show(self, what: str):
        """Show specific information"""
        what_lower = what.lower()
        
        if what_lower in ['requirements', 'req', 'requirement']:
            self._show_requirements()
        elif what_lower in ['testcases', 'tc', 'test', 'tests']:
            self._show_test_cases()
        elif what_lower in ['suites', 'suite', 'testsuite']:
            self._show_suites()
        elif what_lower in ['summary', 'info', 'stats']:
            self._show_summary()
        else:
            print(f"Unknown item: '{what}'. Try 'requirements' or 'testcases'.")
    
    def _show_requirements(self):
        """Show all requirements in detail"""
        if len(self.agent.all_requirements) == 0:
            print("✗ No requirements extracted. Use 'analyze' first.")
            return
        
        print("\n" + "=" * 70)
        print("  Extracted Requirements (LLM Analysis)")
        print("=" * 70)
        
        # Group by type
        by_type: Dict[str, List[Requirement]] = {}
        for req in self.agent.all_requirements:
            type_name = req.requirement_type.value
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(req)
        
        for type_name, reqs in by_type.items():
            print(f"\n{type_name} ({len(reqs)}):")
            for i, req in enumerate(reqs, 1):
                print(f"\n  {i}. [{req.id}] {req.text}")
                print(f"     Type: {req.requirement_type.value}")
                print(f"     Priority: {req.priority}")
                print(f"     Category: {req.category}")
                if req.description:
                    print(f"     Description: {req.description[:100]}...")
        
        print("\n" + "=" * 70)
    
    def _show_test_cases(self):
        """Show all test cases in detail"""
        if len(self.agent.all_test_cases) == 0:
            print("✗ No test cases generated. Use 'testcases' first.")
            return
        
        print("\n" + "=" * 70)
        print("  Generated Test Cases (LLM Intelligence)")
        print("=" * 70)
        
        # Group by type
        by_type: Dict[str, List[TestCase]] = {}
        for tc in self.agent.all_test_cases:
            type_name = tc.test_case_type.value
            if type_name not in by_type:
                by_type[type_name] = []
            by_type[type_name].append(tc)
        
        for type_name, tcs in by_type.items():
            print(f"\n{type_name} ({len(tcs)}):")
            for tc in tcs:
                print(f"\n  {tc.id}: {tc.title}")
                print(f"     Type: {tc.test_case_type.value}")
                print(f"     Priority: {tc.priority}")
                print(f"     Requirement: {tc.requirement_id}")
                print(f"     Steps: {len(tc.steps)}")
                if tc.steps:
                    for j, step in enumerate(tc.steps[:3], 1):
                        print(f"       {j}. {step}")
                    if len(tc.steps) > 3:
                        print(f"       ... and {len(tc.steps) - 3} more")
                if tc.tags:
                    print(f"     Tags: {', '.join(tc.tags)}")
        
        print("\n" + "=" * 70)
    
    def _show_suites(self):
        """Show all test suites"""
        if not self.agent.test_suites:
            print("✗ No test suites created. Use 'suite <name>' to create one.")
            return
        
        print("\n" + "=" * 70)
        print("  Test Suites")
        print("=" * 70)
        
        for name, suite in self.agent.test_suites.items():
            print(f"\n{name}:")
            print(f"  Description: {suite.description}")
            print(f"  Requirements: {len(suite.requirements)}")
            print(f"  Test Cases: {len(suite.test_cases)}")
            
            coverage = suite.get_coverage()
            print(f"  Coverage: {', '.join([f'{k}: {v}' for k, v in coverage.items()])}")
        
        print("\n" + "=" * 70)
    
    def _show_summary(self):
        """Show analysis summary"""
        summary = self.agent.get_summary()
        
        print("\n" + "=" * 70)
        print("  Analysis Summary")
        print("=" * 70)
        
        print(f"\n📋 Requirements: {summary['total_requirements']}")
        for req_type, count in summary['requirements_by_type'].items():
            print(f"  • {req_type}: {count}")
        
        print(f"\n🧪 Test Cases: {summary['total_test_cases']}")
        for tc_type, count in summary['test_cases_by_type'].items():
            print(f"  • {tc_type}: {count}")
        
        if summary['test_suites']:
            print(f"\n📦 Test Suites: {len(summary['test_suites'])}")
            for suite_name in summary['test_suites']:
                suite = self.agent.test_suites[suite_name]
                print(f"  • {suite_name}: {len(suite.test_cases)} test cases")
        
        print("\n" + "=" * 70)
    
    def _show_llm_info(self):
        """Show LLM information"""
        print("\n" + "=" * 70)
        print("  LLM Information")
        print("=" * 70)
        print("\n✓ This agent uses LLM intelligence for:")
        print("  • Deep understanding of PRD text")
        print("  • Context-aware requirement extraction")
        print("  • Creative and comprehensive test case generation")
        print("  • Adaptive learning from different PRD formats")
        print("\n🎯 Benefits:")
        print("  • Understands complex requirements")
        print("  • Generates domain-specific test cases")
        print("  • Adapts to your PRD style")
        print("  • Provides intelligent suggestions")
        print("\n" + "=" * 70)
    
    def _create_suite(self, name: str):
        """Create a test suite"""
        if len(self.agent.all_requirements) == 0:
            print("✗ No requirements extracted. Use 'analyze' first.")
            return
        
        suite = self.agent.create_test_suite(name, f"LLM-generated test suite for {name}")
        print(f"\n✓ Created test suite: '{name}'")
        print(f"  Requirements: {len(suite.requirements)}")
        print(f"  Test Cases: {len(suite.test_cases)}")
        
        coverage = suite.get_coverage()
        print(f"  Coverage: {', '.join([f'{k}: {v}' for k, v in coverage.items()])}")
    
    def _create_suite_interactive(self):
        """Create test suite interactively"""
        if len(self.agent.all_requirements) == 0:
            print("✗ No requirements extracted. Use 'analyze' first.")
            return
        
        name = input("Enter suite name: ").strip()
        if name:
            description = input("Enter description (optional): ").strip()
            suite = self.agent.create_test_suite(name, description)
            print(f"\n✓ Created test suite: '{name}' with {len(suite.test_cases)} test cases")
        else:
            print("✗ Suite name cannot be empty.")
    
    def _export(self, filename: str):
        """Export test cases to file"""
        if len(self.agent.all_test_cases) == 0:
            print("✗ No test cases to export. Use 'testcases' first.")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("# LLM-Generated Test Cases\n\n")
                f.write(f"Total: {len(self.agent.all_test_cases)} test cases\n")
                f.write(f"Generated by: LLM SDLC Expert Agent\n\n")
                
                for tc in self.agent.all_test_cases:
                    f.write(f"## {tc.id}: {tc.title}\n")
                    f.write(f"**Type:** {tc.test_case_type.value}\n")
                    f.write(f"**Priority:** {tc.priority}\n")
                    f.write(f"**Requirement ID:** {tc.requirement_id}\n")
                    f.write(f"**Description:** {tc.description}\n\n")
                    
                    if tc.preconditions:
                        f.write("**Preconditions:**\n")
                        for pc in tc.preconditions:
                            f.write(f"  - {pc}\n")
                        f.write("\n")
                    
                    f.write("**Steps:**\n")
                    for i, step in enumerate(tc.steps, 1):
                        f.write(f"  {i}. {step}\n")
                    f.write("\n")
                    
                    f.write(f"**Expected Result:** {tc.expected_result}\n")
                    
                    if tc.test_data:
                        f.write("\n**Test Data:**\n")
                        for data in tc.test_data:
                            f.write(f"  - {data}\n")
                    
                    if tc.tags:
                        f.write(f"\n**Tags:** {', '.join(tc.tags)}\n")
                    
                    f.write("\n---\n\n")
            
            print(f"\n✓ Exported {len(self.agent.all_test_cases)} test cases to '{filename}'")
            
        except Exception as e:
            print(f"\n✗ Error exporting: {e}")
    
    def _export_interactive(self):
        """Export interactively"""
        if len(self.agent.all_test_cases) == 0:
            print("✗ No test cases to export.")
            return
        
        filename = input("Enter filename to export to: ").strip()
        if filename:
            self._export(filename)
        else:
            print("✗ Filename cannot be empty.")
    
    def _reset(self):
        """Reset the agent state"""
        self.current_prd = None
        self.current_suite = None
        self.agent = LLM_SDLC_Agent()
        print("\n✓ Reset complete. All data cleared.")


# Main entry point
llm_interface = LLM_ConversationalInterface()


def main():
    """Run the LLM SDLC Expert Agent"""
    llm_interface.run()


if __name__ == "__main__":
    main()
