# Error Handling

## HTTP Status Codes
- 200: Successful request
- 400: Bad request (invalid parameters)
- 401: Unauthorized (invalid API key)
- 403: Forbidden (exceeded quota or content policy violation)
- 404: Not found
- 429: Too many requests (rate limit exceeded)
- 500: Internal server error

## Error Response Format
```json
{
  "error": {
    "type": "invalid_request_error",
    "message": "Detailed error message"
  }
}
```

## Common Error Types
- `invalid_request_error`: Malformed request or invalid parameters
- `authentication_error`: Invalid API key
- `permission_error`: Lack necessary permissions
- `not_found_error`: Requested resource doesn't exist
- `rate_limit_error`: Exceeded rate limits
- `api_error`: Unexpected API error

## Best Practices
1. Implement proper error handling in your code
2. Use exponential backoff for retries on 429 errors
3. Log errors for debugging and monitoring
4. Handle different error types appropriately in your application
