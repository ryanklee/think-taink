# Multi-LLM Think Tank Simulation

## 1. Design Space

### a) LLM Pool
- Number of LLMs: 3
- Using GPT-3.5-turbo model with different prompts/personalities to simulate different experts

### b) Question/Objective Input
- Simple text input system for questions or intellectual objectives
- (Future improvement: Mechanism to break down complex objectives into smaller tasks)

### c) Processing Mechanism
- Turn-based system for LLM contributions
- Separate moderator/coordinator module to manage discussion flow

### d) Heuristics and Principles
- Guiding principles: intellectual honesty, critical thinking, creativity
- Simple scoring system for ideas based on relevance and originality

### e) Criteria for Completion
- Time limit: maximum number of turns
- Idea saturation: no new significant ideas in the last N turns

### f) Output Generation
- Summary generation system combining most relevant and highly-scored ideas

## 2. Documentation

- Project overview and goals
- System architecture
- LLM pool configuration
- Input processing
- Discussion flow and moderation
- Heuristics and principles
- Completion criteria
- Output generation
- Tech stack and dependencies

## 3. Implementation Plan

a) Set up development environment
b) Implement input processing system
c) Develop LLM pool and integration
d) Create moderator/coordinator
e) Implement discussion flow mechanism
f) Develop heuristics and principles
g) Implement completion criteria
h) Create output generation system
i) Develop user interface (if required)
j) Test and refine the system

## 4. Tech Stack

### a) Programming Language
- Python

### b) LLM Integration
- OpenAI API (for GPT models)
- Hugging Face Transformers (for open-source models)

### c) Backend Framework
- FastAPI or Flask

### d) Frontend (if needed)
- React or Vue.js

### e) Database
- PostgreSQL or MongoDB

### f) Message Queue
- RabbitMQ or Redis

### g) Containerization
- Docker

## 5. Implementation Steps

a) Set up development environment:
   - Install Python, libraries, and frameworks
   - Set up version control (Git)

b) Implement input processing:
   - Functions to accept and preprocess questions/objectives

c) Develop LLM pool:
   - Classes for each LLM, including API calls and response handling

d) Create moderator/coordinator:
   - Class to manage discussion flow and LLM interactions

e) Implement discussion flow:
   - Turn-based system for LLM contributions
   - Message passing between LLMs and moderator

f) Develop heuristics and principles:
   - Functions to evaluate and guide LLM responses
   - System to enforce guiding principles

g) Implement completion criteria:
   - Functions to check for consensus, time limits, or idea saturation

h) Create output generation:
   - System to synthesize final output from LLM contributions

i) Develop user interface (if required):
   - Web-based interface for input and output display

j) Test and refine:
   - Develop unit tests and integration tests
   - Refine system based on test results and performance
