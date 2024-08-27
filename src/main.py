import logging
import sys
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask
from src.web import create_app
from config.config_loader import load_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config = load_config()

# Create Flask app
app = create_app(config)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
from src.config.config_loader import load_config
from src.llm_pool.llm_pool import LLMPool
from src.moderator.moderator import Moderator
from src.heuristics.principles import Principles
from src.ab_testing import ABTestRunner

def main():
    config = load_config()
    llm_pool = LLMPool(config)
    principles = Principles(config['principles']['version_control_file'])
    moderator = Moderator(llm_pool, principles)

    print("Welcome to the Multi-LLM Think Tank Simulation!")
    print("1. Start a discussion")
    print("2. Run A/B test")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        input_text = input("Enter your question or topic: ")
        for response in moderator.start_discussion_stream(input_text):
            print(f"{response['expert']}: {response['response']}")
    elif choice == '2':
        input_text = input("Enter your question or topic for A/B testing: ")
        ab_runner = ABTestRunner(config)
        results = ab_runner.run_ab_test(input_text)
        analysis = ab_runner.analyze_results(results)
        print("A/B Test Results:")
        print(analysis)
    else:
        print("Invalid choice. Please run the program again and select 1 or 2.")

if __name__ == "__main__":
    main()
