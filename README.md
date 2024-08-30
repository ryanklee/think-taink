# AI Behavioral Experiment Testbed: A Domain-Driven Design Approach to Studying Trait Bundle Interactions

This project implements a sophisticated experimental testbed for conducting complex behavioral and psychological experiments with AI agents, focusing on the interactions between different behavioral trait bundles (roles). It provides a flexible, scalable platform for researchers to design, execute, and analyze experiments in AI behavior and collaboration, grounded in established psychological theories, ethical AI practices, and Domain-Driven Design (DDD) principles.

## Domain-Driven Design and UML Approach

Our project is structured using Domain-Driven Design principles and modeled using Unified Modeling Language (UML). This approach ensures a clear separation of concerns, a rich domain model, and a shared ubiquitous language among all stakeholders. Key DDD concepts implemented in our system include:

- **Aggregates**: Experiment and Agent are our main aggregate roots, encapsulating related entities and value objects.
- **Entities**: Core domain objects with distinct identities, such as Experiment and Agent.
- **Value Objects**: Immutable objects representing descriptive aspects of the domain, like TraitBundle.
- **Domain Services**: Stateless operations that don't naturally fit within an entity or value object, such as ReasoningEngine and EthicsFramework.
- **Repositories**: Provide a way to access and persist our aggregate roots, implemented for Experiment and Agent.
- **Factories**: Encapsulate the logic of creating complex domain objects, particularly for Experiment and Agent creation.
- **Domain Events**: Capture occurrences of importance in the domain, such as ExperimentStarted or EthicalConcernRaised.

Our UML diagrams (available in the `docs/` directory) provide a visual representation of these concepts and their relationships within our system.

## Academic Foundations

Our work is informed by cutting-edge research in AI and psychology, including:

- Experimental design in AI [1][2][3]
- Trait theories in psychology [4][5]
- Ethical considerations in AI research [6][7]
- Domain-Driven Design in complex systems [8][9]
- Advanced multi-agent interaction models [10][11][12]
- Swarm intelligence and emergent behaviors [13][14]

We leverage established AI research platforms and domain-specific languages to ensure robustness and reproducibility in our experiments.

[10] Emergent Language-Based Coordination In Deep Multi-Agent Systems (2022)
[11] A Survey on Large-Population Systems and Scalable Multi-Agent Reinforcement Learning (2022)
[12] Swarm Intelligence Decentralized Decision Making In Multi-Agent System (2023)
[13] Emergence of Hierarchical Reference Systems in Multi-agent Communication (2022)
[14] A review: Swarm Robotics: Cooperative Control in Multi-Agent Systems (2022)

## Features

- Multiple AI experts with different roles (Analyst, Creative, Critic, Synthesizer, Ethicist) modeled as Agent entities
- Microservices-based architecture for scalability and flexibility, aligned with DDD principles
- Multi-API support: Seamless integration with OpenAI and Anthropic Claude APIs
- Turn-based discussion system with moderated conversation flow within the Experiment aggregate
- Heuristics and principles for idea evaluation and discussion guidance as part of the ReasoningEngine domain service
- Reflective learning to improve principles over time, implemented in the PrinciplesEvolution domain service
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

## Core Components (Domain Model)

1. Experiment Aggregate: Represents a complete behavioral study, including its lifecycle and associated agents
2. Agent Aggregate: Fundamental unit representing an AI entity with specific traits and capabilities
3. ReasoningEngine (Domain Service): Orchestrates collaborative reasoning process among agents
4. KnowledgeBase (Repository): Graph database (Neo4j) for storing concepts, relationships, and versioned configurations
5. EthicsFramework (Domain Service): Ensures adherence to predefined ethical guidelines
6. ExperimentRunner (Application Service): Facilitates complex behavioral-psychological experiments
7. TraitBundle (Value Object): Immutable collection of behavioral characteristics defining an agent's personality

## Project Structure (Aligned with DDD)

```
src/
├── domain/
│   ├── experiment/
│   ├── agent/
│   ├── trait_bundle/
│   └── ethics/
├── application/
│   ├── experiment_runner/
│   └── user_interface/
├── infrastructure/
│   ├── persistence/
│   ├── api_clients/
│   └── messaging/
├── interfaces/
│   ├── web/
│   └── cli/
└── shared/
    ├── utils/
    └── domain_events/
tests/
config/
docs/
.devcontainer/
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-behavioral-experiment-testbed.git
   cd ai-behavioral-experiment-testbed
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the necessary environment variables:
   ```
   export OPENAI_API_KEY=your_openai_api_key
   export ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

5. Initialize the database:
   ```
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Use the web interface to:
   - Design and configure experiments
   - Run experiments
   - Monitor ongoing experiments
   - Analyze results
   - Manage the LLM pool and trait bundles

4. For programmatic access, use the provided API endpoints. Refer to the API documentation for details.

## Testing

1. Ensure you're in the project root directory and your virtual environment is activated.

2. Run the test suite:
   ```
   pytest
   ```

3. For more verbose output, use:
   ```
   pytest -v
   ```

4. To run tests with coverage report:
   ```
   pytest --cov=src tests/
   ```

5. To run specific test files or classes:
   ```
   pytest tests/test_agent.py
   pytest tests/test_experiment_runner.py::TestExperimentRunner
   ```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, the process for submitting pull requests, and coding standards. We encourage contributors to familiarize themselves with DDD principles and our domain model before making significant changes.

## Documentation

For more detailed information about the project's domain model, architecture, and DDD implementation, please refer to the `docs/` directory. Key documents include:

- `domain_model.md`: Detailed explanation of our domain model and DDD concepts
- `ubiquitous_language.md`: Glossary of domain-specific terms used in the project
- `architecture.md`: Overview of the system architecture and how it aligns with DDD principles

## Deployment

This project supports deployment on Dokku. For detailed instructions, see [docs/dokku_deployment.md](docs/dokku_deployment.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI and Anthropic for providing the AI models used in this project
- The open-source community for the various libraries and tools used in this project
- Eric Evans for his work on Domain-Driven Design, which has significantly influenced our approach

## References

[1-7: Existing references]
[8] Evans, E. (2003). Domain-Driven Design: Tackling Complexity in the Heart of Software. Addison-Wesley Professional.
[9] Vernon, V. (2013). Implementing Domain-Driven Design. Addison-Wesley Professional.
