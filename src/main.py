#!/usr/bin/env python3
"""
SDLC Expert Agent - Main entry point
"""

import argparse
from .agent import SDLCExpertAgent
from .interface import ConversationalInterface


def main():
    """Main entry point for the SDLC Expert Agent"""
    parser = argparse.ArgumentParser(
        description="SDLC Expert Agent - Extract requirements from PRD and generate test cases"
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='PRD file to analyze'
    )
    parser.add_argument(
        '--text', '-t',
        type=str,
        help='PRD text to analyze directly'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    parser.add_argument(
        '--export', '-e',
        type=str,
        help='Export test cases to file'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode (less output)'
    )
    
    args = parser.parse_args()
    
    # If no arguments, run interactive mode
    if not any(vars(args).values()):
        args.interactive = True
    
    if args.interactive:
        # Run conversational interface
        interface = ConversationalInterface()
        interface.run()
    else:
        # Run in batch mode
        agent = SDLCExpertAgent()
        
        # Load PRD
        if args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    prd_text = f.read()
            except FileNotFoundError:
                print(f"Error: File '{args.file}' not found.")
                return
        elif args.text:
            prd_text = args.text
        else:
            print("No PRD input provided. Use --file or --text, or run with -i for interactive mode.")
            return
        
        # Extract requirements
        if not args.quiet:
            print("Analyzing PRD...")
        
        requirements = agent.extract_requirements(prd_text)
        
        if not args.quiet:
            print(f"Extracted {len(requirements)} requirements")
        
        # Generate test cases
        test_cases = agent.generate_test_cases(requirements)
        
        if not args.quiet:
            print(f"Generated {len(test_cases)} test cases")
            
            # Show summary
            summary = agent.get_summary()
            print(f"\nSummary:")
            print(f"  Requirements by type:")
            for req_type, count in summary['requirements_by_type'].items():
                print(f"    {req_type}: {count}")
            print(f"  Test cases by type:")
            for tc_type, count in summary['test_cases_by_type'].items():
                print(f"    {tc_type}: {count}")
        
        # Export if requested
        if args.export:
            try:
                with open(args.export, 'w', encoding='utf-8') as f:
                    f.write("# Generated Test Cases\n\n")
                    f.write(f"Total: {len(test_cases)} test cases\n\n")
                    
                    for tc in test_cases:
                        f.write(f"## {tc.id}: {tc.title}\n")
                        f.write(f"**Type:** {tc.test_case_type.value}\n")
                        f.write(f"**Priority:** {tc.priority}\n")
                        f.write(f"**Description:** {tc.description}\n\n")
                        
                        f.write("**Steps:**\n")
                        for i, step in enumerate(tc.steps, 1):
                            f.write(f"  {i}. {step}\n")
                        f.write("\n")
                        
                        f.write(f"**Expected Result:** {tc.expected_result}\n")
                        f.write(f"**Tags:** {', '.join(tc.tags)}\n\n")
                        f.write("---\n\n")
                
                if not args.quiet:
                    print(f"\nExported test cases to '{args.export}'")
            except Exception as e:
                print(f"Error exporting: {e}")


if __name__ == "__main__":
    main()
