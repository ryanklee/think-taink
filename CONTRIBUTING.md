# Contributing to Multi-LLM Think Tank Simulation

We value code transparency and readability. Please follow these guidelines to ensure that the codebase remains accessible and understandable to all contributors.

## Code Style and Structure

1. Follow PEP 8 guidelines for Python code style.
2. Use meaningful and descriptive names for variables, functions, and classes.
3. Keep functions small and focused on a single task.
4. Use type hints for all function parameters and return values.

## Documentation

1. Write clear and concise docstrings for all classes and functions.
2. Include examples in docstrings where appropriate.
3. Use inline comments to explain complex logic or non-obvious decisions.
4. Update README files when adding new features or changing existing functionality.

## Code Comments

1. Use comments to explain the "why" behind the code, not just the "what".
2. Add section headers in large files to break the code into logical chunks.
3. Keep comments up-to-date when modifying code.

## Literate Programming

1. Consider using Jupyter Notebooks for exploratory coding and documentation.
2. Create markdown files explaining complex algorithms or system flows.

## Diagrams

1. Include architecture diagrams in the main README and component-specific READMEs.
2. Use sequence diagrams (e.g., using Mermaid) to explain complex interactions between components.

## Code Reviews

1. During code reviews, pay attention to code clarity and documentation.
2. Ask for clarification on any code that is not immediately understandable.

## Frontend Development

This project uses Tailwind CSS for styling. When making changes to the frontend:

1. Stick to Tailwind's utility classes as much as possible.
2. If you need to add custom styles, consider if they can be achieved through Tailwind's configuration first.
3. Keep accessibility in mind - use semantic HTML and appropriate ARIA attributes where necessary.
4. Test your changes across different browsers and screen sizes.
5. Maintain consistency with the existing design language and color scheme.
6. When adding new pages or components, extend the base.html template and follow the established patterns.

For significant design changes, please open an issue for discussion before submitting a pull request.

## Testing

1. Write unit tests for new functionality and update existing tests when modifying code.
2. Ensure all tests pass before submitting a pull request.
3. Aim for high test coverage, especially for critical components.

## Version Control

1. Use descriptive commit messages that explain the purpose of the changes.
2. Create feature branches for new features or significant changes.
3. Keep pull requests focused on a single feature or bug fix.

## API Integration

When working with the OpenAI or Claude APIs:

1. Follow best practices for API usage as outlined in their respective documentation.
2. Implement proper error handling and retries for API calls.
3. Be mindful of rate limits and implement appropriate throttling mechanisms.
4. Keep API keys and sensitive information secure and out of version control.

By following these guidelines, we can maintain a codebase that is transparent, accessible, and easy to understand for all contributors.
