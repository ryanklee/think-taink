# API Reference

## Messages API

### Create a message
- POST `/v1/messages`
- Required parameters:
  - `model`: e.g., "claude-3-sonnet-20240229"
  - `max_tokens`: int, maximum number of tokens to generate
  - `messages`: list of message objects with `role` and `content`
- Optional parameters:
  - `system`: string, system prompt
  - `temperature`: float, 0-1, controls randomness
  - `top_p`, `top_k`: control sampling diversity
  - `metadata`: object for your own use

### Streaming
- Same endpoint with `stream=true`
- Yields chunks of the response as they're generated

## Content Moderation
- Automatic content filtering
- Override with `anthropic-version` header set to `2023-06-01`

## Embeddings (Beta)
- POST `/v1/embeddings`
- Get vector representations of text

## Versioning
- Use `anthropic-version` header to specify API version
- Latest stable: `2023-06-01`

## Error Handling
- HTTP status codes:
  - 200: Successful request
  - 400: Bad request (invalid parameters)
  - 401: Unauthorized (invalid API key)
  - 403: Forbidden (exceeded quota or content policy violation)
  - 404: Not found
  - 429: Too many requests (rate limit exceeded)
  - 500: Internal server error
- Error response format:
  ```json
  {
    "error": {
      "type": "invalid_request_error",
      "message": "Detailed error message"
    }
  }
  ```
- Common error types:
  - `invalid_request_error`: Malformed request or invalid parameters
  - `authentication_error`: Invalid API key
  - `permission_error`: Lack necessary permissions
  - `not_found_error`: Requested resource doesn't exist
  - `rate_limit_error`: Exceeded rate limits
  - `api_error`: Unexpected API error

## Best Practices
- Implement proper error handling in your code
- Use exponential backoff for retries on 429 errors
- Log errors for debugging and monitoring
- Handle different error types appropriately in your application
