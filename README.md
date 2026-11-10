# SDLC Expert Agent - PRD to Test Cases

A conversational software development lifecycle expert agent that extracts business requirements from Product Requirements Documents (PRD) and generates comprehensive test cases.

## Features

- **Requirement Extraction**: Automatically extracts user stories, functional requirements, non-functional requirements, business rules, acceptance criteria, and constraints from PRD text
- **Test Case Generation**: Generates positive, negative, and edge case test cases for each extracted requirement
- **Pattern Matching**: Uses intelligent pattern matching to identify common requirement types and generate appropriate test cases
- **Conversational Interface**: Interactive CLI for easy exploration and refinement of requirements and test cases
- **Test Suite Creation**: Organize test cases into suites with coverage statistics
- **Export Functionality**: Export generated test cases to markdown or other formats

## Installation

```bash
# Clone or download the repository
cd mistral-vibe-agent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Interactive Mode

```bash
# Run the conversational interface
python -m src.main -i

# Or simply
python -m src.main
```

Once in interactive mode, use commands like:
- `load <file>` - Load PRD from a file
- `paste` - Paste PRD text directly
- `analyze` - Extract requirements from the loaded PRD
- `testcases` - Generate test cases from extracted requirements
- `show` - Show analysis summary
- `requirements` - Show extracted requirements in detail
- `suite <name>` - Create a test suite
- `export <file>` - Export test cases to a file
- `help` - Show all available commands
- `quit` - Exit the application

### Batch Mode

```bash
# Analyze a PRD file and display results
python -m src.main --file examples/ecommerce_prd.md

# Analyze PRD text directly
python -m src.main --text "As a user, I want to login..."

# Analyze and export test cases
python -m src.main --file examples/simple_prd.txt --export test_cases.md

# Quiet mode (less output)
python -m src.main --file examples/simple_prd.txt --quiet
```

## Examples

### Example 1: Analyze a PRD file

```bash
python -m src.main --file examples/ecommerce_prd.md
```

This will:
1. Load the e-commerce PRD
2. Extract all requirements (user stories, functional requirements, business rules, etc.)
3. Generate test cases for each requirement
4. Display a summary with counts by requirement and test case types

### Example 2: Interactive analysis

```bash
python -m src.main
sdlc> load examples/simple_prd.txt
sdlc> analyze
sdlc> show requirements
sdlc> testcases
sdlc> show testcases
sdlc> suite login_tests
sdlc> export login_test_cases.md
```

### Example 3: Quick analysis of text

```bash
python -m src.main --text "As a user, I want to reset my password via email so that I can regain access to my account. The system must send a reset link to the user's email address."
```

## Output Format

Generated test cases include:
- **Test Case ID**: Unique identifier (e.g., TC-abc123)
- **Title**: Descriptive title of the test case
- **Description**: Detailed description of what's being tested
- **Type**: Positive, Negative, Edge Case, Performance, Security, etc.
- **Steps**: Step-by-step instructions to execute the test
- **Expected Result**: What should happen when the test is executed
- **Priority**: High, Medium, or Low
- **Tags**: Categorization tags for filtering and organization
- **Requirement ID**: Link back to the original requirement

## Test Case Types

The agent generates different types of test cases:

1. **Positive Test Cases**: Verify that the system works as expected under normal conditions
2. **Negative Test Cases**: Verify that the system handles invalid inputs and edge cases gracefully
3. **Edge Cases**: Test boundary conditions and extreme scenarios
4. **Performance Test Cases**: Verify system performance under load
5. **Security Test Cases**: Verify security requirements and protections
6. **Usability Test Cases**: Verify user experience and interface behavior
7. **Compatibility Test Cases**: Verify cross-browser and cross-device compatibility

## Requirement Types

The agent can extract and process various requirement types:

- **User Stories**: "As a [role], I want [feature] so that [benefit]"
- **Acceptance Criteria**: Specific conditions that must be met
- **Functional Requirements**: What the system should do
- **Non-Functional Requirements**: How the system should perform (performance, security, etc.)
- **Business Rules**: Rules that govern business logic
- **Constraints**: Limitations and restrictions
- **Assumptions**: Assumptions made during requirements gathering
- **Dependencies**: External systems or services required

## Pattern Matching

The agent uses intelligent pattern matching to identify common requirement types and generate appropriate test cases. For example:

- **Login/Authentication**: Generates test cases for login, logout, password reset
- **Form Validation**: Generates test cases for input validation, required fields
- **API Integration**: Generates test cases for API endpoints, authentication, error handling
- **Data Processing**: Generates test cases for calculations, transformations, validations
- **Business Logic**: Generates test cases for rules, workflows, conditions

## Extending the Agent

You can extend the agent by:

1. **Adding New Patterns**: Add new test patterns to the `templates.py` file
2. **Custom Extraction Rules**: Modify the pattern matching in `agent.py`
3. **New Output Formats**: Add new export formats in the interface
4. **Integration**: Integrate with test management tools or CI/CD pipelines

## Project Structure

```
mistral-vibe-agent/
├── src/
│   ├── __init__.py
│   ├── agent.py           # Core agent functionality
│   ├── interface.py       # Conversational CLI interface
│   ├── main.py            # Main entry point
│   └── templates.py       # Test case templates and patterns
├── examples/
│   ├── ecommerce_prd.md   # Example e-commerce PRD
│   └── simple_prd.txt     # Simple example PRD
├── tests/
│   ├── __init__.py
│   └── test_agent.py      # Unit tests
├── demo.py                # Demonstration script
├── setup.py               # Setup script
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - Feel free to use, modify, and distribute.

## Support

For issues, questions, or feature requests, please open an issue on the project repository.
