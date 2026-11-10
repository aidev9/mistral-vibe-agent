"""
Conversational Interface for SDLC Expert Agent
Provides an interactive CLI for extracting requirements and generating test cases from PRD text
"""

import sys
from typing import Optional, List
from .agent import SDLCExpertAgent, Requirement, TestCase, TestSuite, RequirementType, TestCaseType


class ConversationalInterface:
    """
    Interactive command-line interface for the SDLC Expert Agent
    """
    
    def __init__(self):
        self.agent = SDLCExpertAgent()
        self.current_prd: Optional[str] = None
        self.current_suite: Optional[TestSuite] = None
    
    def run(self):
        """Main entry point for the conversational interface"""
        print("=" * 60)
        print("  SDLC Expert Agent - PRD to Test Cases")
        print("=" * 60)
        print("\nI'm your SDLC Expert Agent. I can extract business requirements")
        print("from your PRD text and generate comprehensive test cases.")
        print("\nType 'help' for available commands, 'quit' to exit.")
        print()
        
        while True:
            try:
                command = input("sdlc> ").strip()
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
        """Process a user command"""
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == 'quit' or cmd == 'exit' or cmd == 'q':
            print("Goodbye!")
            return False
        
        elif cmd == 'help' or cmd == 'h':
            self._show_help()
        
        elif cmd == 'load' or cmd == 'read':
            if len(args) > 0:
                self._load_prd_from_file(args[0])
            else:
                self._load_prd_interactive()
        
        elif cmd == 'paste' or cmd == 'text':
            self._load_prd_interactive()
        
        elif cmd == 'analyze' or cmd == 'extract':
            self._analyze_prd()
        
        elif cmd == 'testcases' or cmd == 'tc':
            self._generate_test_cases()
        
        elif cmd == 'show' or cmd == 'display':
            if len(args) > 0:
                self._show_specific(args)
            else:
                self._show_summary()
        
        elif cmd == 'requirements' or cmd == 'req':
            self._show_requirements()
        
        elif cmd == 'suite' or cmd == 'create':
            if len(args) > 0:
                self._create_suite(' '.join(args))
            else:
                self._create_suite_interactive()
        
        elif cmd == 'export':
            if len(args) > 0:
                self._export(args[0] if len(args) > 0 else None)
            else:
                self._export_interactive()
        
        elif cmd == 'clear' or cmd == 'reset':
            self._reset()
        
        elif cmd == 'info' or cmd == 'summary':
            self._show_summary()
        
        else:
            print(f"Unknown command: '{cmd}'. Type 'help' for available commands.")
        
        return True
    
    def _show_help(self):
        """Display help information"""
        print("\n" + "=" * 60)
        print("  Available Commands")
        print("=" * 60)
        print("\nPRD Input:")
        print("  load <file>     - Load PRD from a file")
        print("  paste           - Paste PRD text directly")
        print("  read <file>     - Same as load")
        print("  text            - Same as paste")
        print("\nAnalysis:")
        print("  analyze         - Extract requirements from current PRD")
        print("  extract         - Same as analyze")
        print("  testcases       - Generate test cases from extracted requirements")
        print("  tc              - Same as testcases")
        print("\nDisplay:")
        print("  show            - Show summary of current analysis")
        print("  show <type>     - Show specific items (requirements, testcases)")
        print("  requirements    - Show extracted requirements")
        print("  req             - Same as requirements")
        print("  info            - Show summary")
        print("  summary         - Show summary")
        print("\nTest Suite:")
        print("  suite <name>    - Create a test suite from current requirements")
        print("  create <name>   - Same as suite")
        print("\nExport:")
        print("  export <file>   - Export test cases to file")
        print("  export          - Interactive export")
        print("\nUtility:")
        print("  clear           - Clear current PRD and analysis")
        print("  reset           - Same as clear")
        print("  help            - Show this help")
        print("  quit            - Exit the application")
        print("=" * 60)
