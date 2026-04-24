# Contributing to Malicious URL Detection

Thank you for your interest in contributing! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs
- Check if the bug has already been reported in [Issues](../../issues)
- If not, create a new issue with:
  - Clear, descriptive title
  - Detailed description of the bug
  - Steps to reproduce
  - Expected vs actual behavior
  - Your environment (OS, Python version, etc.)

### Suggesting Features
- Check existing [Issues](../../issues) to avoid duplicates
- Provide a clear description of the feature
- Explain why it would be useful
- Show any relevant examples

### Pull Requests
1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/malicious-url-detection.git
   cd malicious-url-detection
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Make your changes**
   - Write clear, commented code
   - Follow PEP 8 style guidelines
   - Add docstrings to functions
   - Test your changes thoroughly

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure CI/CD checks pass

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused

### Testing
- Test new features locally before submitting
- Ensure existing functionality isn't broken
- Include edge cases in testing

### Documentation
- Update README.md if adding features
- Add docstrings to functions
- Comment non-obvious code

## Questions?
Feel free to open an issue or contact the maintainers.

Thank you for contributing! 🎉
