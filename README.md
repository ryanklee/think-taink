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

5. Copy `config/config.yaml.example` to `config/config.yaml` and update with your settings:
   ```
   cp config/config.yaml.example config/config.yaml
   ```
   Edit `config/config.yaml` with your preferred text editor and update the necessary settings.

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT models used in this project
- The open-source community for the various libraries and tools used in this project
