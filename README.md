# Multi-LLM Think Tank Simulation

This project simulates a think tank using multiple Language Learning Models (LLMs) to generate, discuss, and refine ideas on given topics or questions. It leverages the power of various AI models to create a dynamic, collaborative environment for idea generation and problem-solving.

## Features

- Multiple LLM experts with different personas (Analyst, Creative, Critic, Synthesizer, Ethicist)
- Turn-based discussion system with moderated conversation flow
- Heuristics and principles for idea evaluation and discussion guidance
- Reflective learning to improve principles over time
- Dynamic expert pool evolution based on discussion performance
- Summarized output generation for concise results
- Web-based interface for easy interaction
- Robust error handling and logging system
- Version control for principles and heuristics
- Experimental control panel for fine-tuning and observing system behavior (in progress)
- Real-time monitoring and visualization of discussions and system performance (in progress)
- Comparative analysis tools for different experimental configurations (in progress)

## Recent Updates

- Initiated migration to support Claude API alongside OpenAI API
- Created AnthropicAPI class for Claude API integration
- Enhanced LLMPool to support multiple API providers
- Updated configuration to include Anthropic API settings
- Implemented streaming response generation for Claude API
- Updated integration tests to accommodate Claude API
- Improved error handling and logging for both APIs
- Enhanced documentation and inline comments for better code readability
- Added migration guide for users switching to or adding Claude API support

## Upcoming Changes

- Complete Claude API integration and testing
- Implement A/B testing between OpenAI and Claude APIs
- Update performance analysis tools for multi-API support
- Enhance prompt engineering to leverage Claude's XML tag capabilities

## Project Structure

```
src/
├── config/
├── ethics/
├── heuristics/
├── input_processing/
├── llm_pool/
├── moderator/
├── output_generation/
├── principles_evolution/
├── utils/
├── web/
├── data_models/
├── database/
├── performance_analysis/
└── ab_testing/
tests/
config/
docs/
.devcontainer/
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/multi-llm-think-tank.git
   cd multi-llm-think-tank
   ```

2. Install Docker and Docker Compose on your system.

3. Build and run the Docker container:
   ```
   docker-compose up --build
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

5. If you're using VS Code with the Remote - Containers extension:
   - Open the project folder in VS Code
   - When prompted, choose "Reopen in Container" or use the command palette to select "Remote-Containers: Reopen in Container"

6. The application should now be running and accessible at `http://localhost:5000`

## Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Enter your question or topic in the provided form.
3. Submit the form to start the think tank simulation.
4. Review the generated discussion and final output.

## Testing

To run the test suite:

```
pytest
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, the process for submitting pull requests, and coding standards.

## Documentation

For more detailed information about the project's components and architecture, please refer to the `docs/` directory. This includes a summary of the Claude API documentation (`claude_api_summary.md`) for quick reference when working with the API.

## Error Handling and Logging

The project now includes a robust error handling system with custom exceptions. Logs are automatically rotated to prevent excessive file sizes. Check the `logs/` directory for detailed application logs.

## Version Control for Principles and Heuristics

The system now includes version control for principles and heuristics, allowing for tracking of changes over time. This feature enhances the system's ability to learn and adapt.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT models used in this project
- The open-source community for the various libraries and tools used in this project
