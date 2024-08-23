# Project Structure

```
src/
├── __init__.py
├── config/
│   ├── __init__.py
│   └── config_loader.py
├── ethics/
│   ├── __init__.py
│   └── guidelines.py
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
│       └── result.html
└── main.py
tests/
├── __init__.py
├── test_input_processing.py
├── test_llm_pool.py
├── test_moderator.py
├── test_principles_evolution.py
└── test_reflector.py
config/
└── config.yaml
docs/
├── api/
├── user_guide/
└── ethical_considerations/
CONTRIBUTING.md
README.md
requirements.txt
```
