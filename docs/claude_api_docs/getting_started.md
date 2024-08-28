# Getting Started with Claude API

## Authentication and Setup
- Use API key in the `x-api-key` header for all requests
- Keep API key secure, don't expose in client-side code
- Base URL: `https://api.anthropic.com`

## Key Concepts
- Messages API: Main endpoint for interacting with Claude
- Streaming: Real-time response generation
- System Prompt: Set context and behavior for Claude

## Quick Start
1. Install Anthropic Python library: `pip install anthropic`
2. Set up client:
   ```python
   from anthropic import Anthropic
   client = Anthropic(api_key="your_api_key")
   ```
3. Send a message:
   ```python
   message = client.messages.create(
       model="claude-3-sonnet-20240229",
       max_tokens=1024,
       temperature=0.7,
       system="You are a helpful AI assistant.",
       messages=[
           {"role": "user", "content": "Hello, Claude!"}
       ]
   )
   print(message.content)
   ```

## Best Practices
- Implement exponential backoff for retries on rate limit errors
- Use `Retry-After` header to adjust retry timing
- Implement proper error handling
- Use appropriate model for the task
- Optimize `max_tokens` and `temperature` for your use case
- Use streaming for real-time applications
