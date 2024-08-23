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
- Experimental control panel for fine-tuning and observing system behavior
- Real-time monitoring and visualization of discussions and system performance
- Comparative analysis tools for different experimental configurations

## Recent Updates

- Improved error handling across all components
- Implemented custom exceptions for better error management
- Enhanced logging system with rotation
- Added version control for principles and heuristics
- Expanded unit test coverage, especially for the Moderator class
- Improved inline documentation for complex methods

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
└── web/
tests/
config/
docs/
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/multi-llm-think-tank.git
   cd multi-llm-think-tank
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

6. Run the application:
   ```
   python src/main.py
   ```

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

For more detailed information about the project's components and architecture, please refer to the `docs/` directory.

## Error Handling and Logging

The project now includes a robust error handling system with custom exceptions. Logs are automatically rotated to prevent excessive file sizes. Check the `logs/` directory for detailed application logs.

## Version Control for Principles and Heuristics

The system now includes version control for principles and heuristics, allowing for tracking of changes over time. This feature enhances the system's ability to learn and adapt.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT models used in this project
- The open-source community for the various libraries and tools used in this project
