# Prompt Engineering

## Key Principles and Best Practices
1. Be clear and specific
2. Provide context and examples
3. Use structured formats (e.g., XML tags)
4. Leverage system prompts for consistent behavior
5. Start with a clear task description
6. Break complex tasks into steps
7. Specify output format explicitly
8. Encourage Claude to ask for clarification when needed

## Techniques
1. Multi-shot prompting: Provide multiple examples
2. Chain-of-thought: Break down complex tasks
3. XML tags: Structure input and desired output
4. System prompts: Set overall context and behavior
5. Prompt templates: Create reusable templates for common tasks

## Handling Long Contexts
1. Summarize key information
2. Use hierarchical structuring
3. Prioritize most relevant information
4. Leverage Claude's ability to reference earlier parts of the conversation

## Using XML Tags
XML tags are a powerful tool for structuring prompts and guiding Claude's responses. They help create clear boundaries between different parts of the input and output.

### Benefits and Best Practices
- Clearly define input and output sections
- Structure complex prompts
- Guide Claude to produce specific output formats
- Improve consistency in responses
- Use descriptive tag names
- Nest tags logically for hierarchical structure
- Close all tags properly
- Use consistent capitalization for tag names

### Examples of XML Tag Usage

1. Structuring input:
   ```
   <input>
     <question>What is the capital of France?</question>
     <context>We are discussing European geography.</context>
   </input>
   ```

2. Specifying output format:
   ```
   Please provide your answer in the following format:
   <answer>
     <capital>Name of the capital</capital>
     <country>Name of the country</country>
     <population>Population of the capital</population>
   </answer>
   ```

3. Multi-part tasks:
   ```
   <task1>Summarize the main points of the given text.</task1>
   <task2>Identify any biases in the author's argument.</task2>
   <task3>Suggest counterarguments to the main thesis.</task3>
   ```

4. Roleplay scenarios:
   ```
   <scenario>
     <setting>A busy emergency room in a large city hospital</setting>
     <your_role>You are the head nurse on duty</your_role>
     <situation>A patient has just arrived with severe chest pain</situation>
   </scenario>
   What actions do you take? Provide your response in the following format:
   <response>
     <immediate_actions>List immediate steps</immediate_actions>
     <communication>Describe how you communicate with the patient and other staff</communication>
     <next_steps>Outline the next steps in patient care</next_steps>
   </response>
   ```

Remember to close all XML tags and use them consistently throughout your prompts to maximize their effectiveness in guiding Claude's responses.
