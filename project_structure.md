# Project Structure

```
src/
├── __init__.py
├── config/
│   ├── __init__.py
│   └── config_loader.py
├── ethics/
│   ├── __init__.py
│   ├── guidelines.py
│   └── version_control.py
├── heuristics/
│   ├── __init__.py
│   ├── principles.py
│   └── version_control.py
├── input_processing/
│   ├── __init__.py
│   └── processor.py
├── llm_pool/
│   ├── __init__.py
│   ├── llm_pool.py
│   ├── openai_api.py
│   └── pool_evolution.py
├── tests/
│   ├── __init__.py
│   ├── test_llm_pool.py
│   ├── test_openai_api.py
│   └── test_integration.py
├── moderator/
│   ├── __init__.py
│   └── moderator.py
├── principles_evolution/
│   ├── __init__.py
│   └── reflector.py
├── utils/
│   ├── __init__.py
│   ├── exceptions.py
│   └── version_control.py
├── web/
│   ├── __init__.py
│   ├── forms.py
│   ├── routes.py
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── ask_question.html
│       ├── result.html
│       └── improvement_dashboard.html
├── data_models/
│   ├── __init__.py
│   ├── experiment.py
│   ├── llm_pool.py
│   ├── expert.py
│   ├── discussion.py
│   ├── principle.py
│   └── performance_metric.py
├── database/
│   ├── __init__.py
│   ├── relational_db.py
│   └── document_store.py
├── performance_analysis/
│   ├── __init__.py
│   └── analyzer.py
├── ab_testing/
│   ├── __init__.py
│   └── test_runner.py
└── main.py
tests/
├── __init__.py
├── test_input_processing.py
├── test_llm_pool.py
├── test_moderator.py
├── test_principles_evolution.py
├── test_reflector.py
├── test_data_models.py
├── test_performance_analysis.py
└── test_ab_testing.py
config/
└── config.yaml
docs/
├── api/
├── user_guide/
├── ethical_considerations/
└── data_model/
.devcontainer/
├── devcontainer.json
└── docker-compose.yml
Dockerfile
docker-compose.yml
CONTRIBUTING.md
README.md
requirements.txt
```
