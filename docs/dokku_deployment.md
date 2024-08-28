# Dokku Deployment Guide

## Installation

1. Install Dokku on a server:
   ```
   wget https://raw.githubusercontent.com/dokku/dokku/v0.30.x/bootstrap.sh
   sudo DOKKU_TAG=v0.30.x bash bootstrap.sh
   ```

2. Visit the server's IP in a browser to complete the setup.

## Application Deployment

1. On your local machine, add the Dokku server as a remote:
   ```
   git remote add dokku dokku@your-server-ip:your-app-name
   ```

2. Deploy your application:
   ```
   git push dokku main
   ```

## Application Management

- List applications: `dokku apps:list`
- Rename an app: `dokku apps:rename old-name new-name`
- Destroy an app: `dokku apps:destroy app-name`

## Logs

- View logs: `dokku logs app-name`
- View live logs: `dokku logs app-name -t`

## Remote Commands

Execute commands on the Dokku server:
```
ssh dokku@your-server-ip command
```

## User Management

- Add SSH key: `dokku ssh-keys:add key-name path/to/key.pub`
- List SSH keys: `dokku ssh-keys:list`

## Zero Downtime Deploys

Dokku supports zero downtime deploys by default using the `DOKKU_WAIT_TO_RETIRE` environment variable.

## Builders

Dokku supports various builders:
- Cloud Native Buildpacks
- Herokuish Buildpacks
- Dockerfiles
- Lambda
- Nixpacks
- Null (for static sites)

## Deployment Methods

- Git push
- Docker image

## Environment Variables

- Set an env var: `dokku config:set app-name KEY=VALUE`
- Get all env vars: `dokku config:show app-name`

For more detailed information, refer to the official Dokku documentation.
