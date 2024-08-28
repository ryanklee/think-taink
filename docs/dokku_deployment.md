# Dokku Deployment Guide for Collaborative AI Reasoning System

## Prerequisites

1. A server with Dokku installed (follow the official Dokku installation guide)
2. SSH access to the Dokku server
3. Git installed on your local machine

## Initial Setup

1. Create the application on the Dokku server:
   ```
   ssh dokku@your-server-ip apps:create collaborative-ai-system
   ```

2. Set up the required plugins:
   ```
   ssh dokku@your-server-ip plugin:install https://github.com/dokku/dokku-postgres.git
   ssh dokku@your-server-ip plugin:install https://github.com/dokku/dokku-redis.git
   ```

3. Create and link the required services:
   ```
   ssh dokku@your-server-ip postgres:create collaborative-ai-db
   ssh dokku@your-server-ip postgres:link collaborative-ai-db collaborative-ai-system
   ssh dokku@your-server-ip redis:create collaborative-ai-cache
   ssh dokku@your-server-ip redis:link collaborative-ai-cache collaborative-ai-system
   ```

## Environment Variables

Set the required environment variables:

```
ssh dokku@your-server-ip config:set collaborative-ai-system \
  FLASK_APP=src/main.py \
  FLASK_ENV=production \
  OPENAI_API_KEY=your_openai_api_key \
  ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Persistent Storage

Set up persistent storage for the application:

```
ssh dokku@your-server-ip storage:ensure-directory collaborative-ai-system
ssh dokku@your-server-ip storage:mount collaborative-ai-system /var/lib/dokku/data/storage/collaborative-ai-system:/app/data
```

## Deployment

1. On your local machine, add the Dokku remote to your Git repository:
   ```
   git remote add dokku dokku@your-server-ip:collaborative-ai-system
   ```

2. Deploy the application:
   ```
   git push dokku main
   ```

## SSL/TLS Configuration

Enable SSL for your application:

```
ssh dokku@your-server-ip config:set --no-restart collaborative-ai-system DOKKU_LETSENCRYPT_EMAIL=your-email@example.com
ssh dokku@your-server-ip letsencrypt:enable collaborative-ai-system
```

## Scaling

Scale your application as needed:

```
ssh dokku@your-server-ip ps:scale collaborative-ai-system web=2
```

## Monitoring

View application logs:

```
ssh dokku@your-server-ip logs collaborative-ai-system -t
```

## Updating the Application

To update the application, simply push to the Dokku remote:

```
git push dokku main
```

## Troubleshooting

- If you encounter issues, check the application logs:
  ```
  ssh dokku@your-server-ip logs collaborative-ai-system
  ```
- Ensure all required environment variables are set correctly:
  ```
  ssh dokku@your-server-ip config:show collaborative-ai-system
  ```

For more detailed information on Dokku features and advanced usage, refer to the official Dokku documentation.
