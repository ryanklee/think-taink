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
