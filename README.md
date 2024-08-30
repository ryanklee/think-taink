# AI Behavioral Experiment Testbed: A Platform for Studying Trait Bundle Interactions

This project implements a sophisticated experimental testbed for conducting complex behavioral and psychological experiments with AI agents, focusing on the interactions between different behavioral trait bundles (roles). It provides a flexible, scalable platform for researchers to design, execute, and analyze experiments in AI behavior and collaboration, grounded in established psychological theories and ethical AI practices.

## Academic Foundations

Our work is informed by cutting-edge research in AI and psychology, including:

- Experimental design in AI [1][2][3]
- Trait theories in psychology [4][5]
- Ethical considerations in AI research [6][7]

We leverage established AI research platforms and domain-specific languages to ensure robustness and reproducibility in our experiments.

## Features

- Multiple AI experts with different roles (Analyst, Creative, Critic, Synthesizer, Ethicist)
- Microservices-based architecture for scalability and flexibility
- Multi-API support: Seamless integration with OpenAI and Anthropic Claude APIs
- Turn-based discussion system with moderated conversation flow
- Heuristics and principles for idea evaluation and discussion guidance
- Reflective learning to improve principles over time
- Dynamic expert pool evolution based on discussion performance
- Summarized output generation for concise results
- Web-based interface for easy interaction and experiment configuration
- Robust error handling and logging system
- Version control for principles, heuristics, and expert configurations
- Experimental control panel for fine-tuning and observing system behavior
- Real-time monitoring and visualization of discussions and system performance
- Comparative analysis tools for different experimental configurations
- A/B testing functionality to compare different AI models and configurations
- Comprehensive experiment runner for behavioral-psychological tests

## Core Components

1. Agent Abstraction: Fundamental unit representing an AI entity
2. Reasoning Engine: Orchestrates collaborative reasoning process
3. Knowledge Base: Graph database (Neo4j) for storing concepts, relationships, and versioned configurations
4. Ethics Framework: Ensures adherence to predefined ethical guidelines
5. User Interface: Real-time, interactive web interface
6. Experiment Runner: Facilitates complex behavioral-psychological experiments

## Project Structure

```
src/
├── agent/
├── reasoning_engine/
├── knowledge_base/
├── ethics_framework/
├── ui/
├── experiment_runner/
├── llm_pool/
├── moderator/
├── principles_evolution/
├── utils/
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
   git clone https://github.com/yourusername/collaborative-ai-reasoning.git
   cd collaborative-ai-reasoning
   ```

2. Install Docker and Docker Compose on your system.

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

5. If you're using VS Code with the Remote - Containers extension:
   - Open the project folder in VS Code
   - When prompted, choose "Reopen in Container" or use the command palette to select "Remote-Containers: Reopen in Container"

6. The application should now be running and accessible at `http://localhost:8000`

## Usage

1. Open your web browser and navigate to `http://localhost:8000`.
2. Use the web interface to:
   - Start a new discussion or experiment
   - Configure AI experts and reasoning parameters
   - Monitor ongoing discussions and experiments
   - Analyze results and compare different configurations

## Testing

To run the unit and integration test suite:

```
pytest
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, the process for submitting pull requests, and coding standards.

## Documentation

For more detailed information about the project's components and architecture, please refer to the `docs/` directory.

## Deployment

This project supports deployment on Dokku. For detailed instructions, see [docs/dokku_deployment.md](docs/dokku_deployment.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI and Anthropic for providing the AI models used in this project
- The open-source community for the various libraries and tools used in this project
