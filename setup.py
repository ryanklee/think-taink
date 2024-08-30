from setuptools import setup, find_packages

setup(
    name="multi-llm-think-tank",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.68.0",
        "uvicorn==0.15.0",
        "openai==0.27.0",
        "pyyaml==5.4.1",
        "pytest==8.3.2",
        "Flask==2.0.1",
        "WTForms==2.3.3",
        "Werkzeug==2.0.1",
        "flask-wtf==0.15.1",
        "python-dotenv==0.19.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A multi-LLM think tank simulation project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/multi-llm-think-tank",
)

# Download required NLTK data
import nltk
nltk.download('punkt')
