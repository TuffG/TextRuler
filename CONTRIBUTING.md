# Contributing to TextRuler

Thank you for your interest in contributing to TextRuler! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Be open to different viewpoints and experiences

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Your system information (Windows version, Python version)
- Any relevant error messages or logs

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:
- A clear description of the feature
- Use cases and examples
- Any potential implementation ideas (optional)

### Pull Requests

1. **Fork the repository** and create a new branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Test your changes** thoroughly

4. **Commit your changes** with clear, descriptive commit messages
   ```bash
   git commit -m "Add feature: description of what you did"
   ```

5. **Push to your fork** and open a Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Wait for review** and address any feedback

## Coding Standards

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Keep functions focused on a single responsibility
- Add docstrings to classes and functions
- Comment complex logic

### Code Organization

- Functions should be organized by abstraction level:
  - **Zone 1**: High-level operations (e.g., `processFormSubmission()`)
  - **Zone 2**: Mid-level operations (e.g., `validateInput()`, `saveToDatabase()`)
  - **Zone 3**: Low-level operations (e.g., `getTimestamp()`, `parseData()`)

### Example

```python
def process_user_input(self, input_data):
    """Process user input and save to database."""
    # Zone 1: High-level
    validated = self.validate_input(input_data)
    transformed = self.transform_data(validated)
    self.save_to_database(transformed)

def validate_input(self, data):
    """Validate input data."""
    # Zone 2: Mid-level
    if not self.check_required_fields(data):
        raise ValueError("Missing required fields")
    return self.sanitize_data(data)

def check_required_fields(self, data):
    """Check if all required fields are present."""
    # Zone 3: Low-level
    required = ['name', 'email']
    return all(field in data for field in required)
```

## Testing

- Test your changes manually before submitting
- Ensure the application starts without errors
- Test on different screen configurations if possible
- Verify settings persistence works correctly

## Documentation

- Update README.md if you add new features
- Add comments for complex code sections
- Update QUICKSTART.md if usage changes
- Keep docstrings up to date

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/TextRuler.git
   cd TextRuler
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make your changes and test:
   ```bash
   python main.py
   ```

## Commit Message Guidelines

Use clear, descriptive commit messages:

- **Good**: `Add support for custom hotkey configuration`
- **Good**: `Fix ruler position not saving on multi-monitor setup`
- **Bad**: `fix bug`
- **Bad**: `update code`

## Questions?

If you have questions, feel free to:
- Open an issue with the `question` label
- Check existing issues and discussions

Thank you for contributing to TextRuler! 🎉

