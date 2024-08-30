# Heroku Deployment Guide

This guide provides comprehensive instructions for deploying the Collaborative AI Reasoning System on Heroku.

## Prerequisites

- Heroku account
- Heroku CLI installed and configured
- Git repository with your application code

## Steps for Deployment

### 1. Prepare Your Application

1.1. Create a `Procfile` in your project root:

```
web: gunicorn app:app
```

1.2. Create a `runtime.txt` file to specify the Python version:

```
python-3.9.x
```

1.3. Ensure your `requirements.txt` file is up to date:

```bash
pip freeze > requirements.txt
```

### 2. Set Up Heroku App

2.1. Create a new Heroku app:

```bash
heroku create your-app-name
```

2.2. Set up environment variables:

```bash
heroku config:set KEY1=VALUE1 KEY2=VALUE2
```

### 3. Database Configuration

3.1. Add Heroku Postgres add-on:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

3.2. Update your application to use the DATABASE_URL config var.

### 4. Deploy Your Application

4.1. Push your code to Heroku:

```bash
git push heroku main
```

4.2. Ensure at least one instance of the app is running:

```bash
heroku ps:scale web=1
```

### 5. Post-Deployment Tasks

5.1. Run database migrations (if applicable):

```bash
heroku run python manage.py db upgrade
```

5.2. Open your application:

```bash
heroku open
```

## Continuous Deployment

To set up continuous deployment:

1. Go to your Heroku dashboard and select your app.
2. Navigate to the "Deploy" tab.
3. In the "Deployment method" section, choose GitHub.
4. Connect your GitHub repository and enable automatic deploys from your main branch.

## Monitoring and Scaling

- Use `heroku logs --tail` to monitor your application logs.
- Scale your application using `heroku ps:scale web=X` where X is the number of dynos.

## Troubleshooting

If you encounter issues:

1. Check your Heroku logs: `heroku logs --tail`
2. Ensure all environment variables are correctly set
3. Verify that your `Procfile` and `runtime.txt` are correctly configured
4. Check that all required dependencies are in your `requirements.txt`

For more detailed information, refer to the [Heroku Dev Center](https://devcenter.heroku.com/).
# Heroku Deployment Guide

This guide provides comprehensive instructions for deploying the Collaborative AI Reasoning System on Heroku.

## Prerequisites

- Heroku account
- Heroku CLI installed and configured
- Git repository with your application code

## Steps for Deployment

### 1. Prepare Your Application

1.1. Create a `Procfile` in your project root:

```
web: gunicorn app:app
```

1.2. Create a `runtime.txt` file to specify the Python version:

```
python-3.9.x
```

1.3. Ensure your `requirements.txt` file is up to date:

```bash
pip freeze > requirements.txt
```

### 2. Set Up Heroku App

2.1. Create a new Heroku app:

```bash
heroku create your-app-name
```

2.2. Set up environment variables:

```bash
heroku config:set KEY1=VALUE1 KEY2=VALUE2
```

### 3. Database Configuration

3.1. Add Heroku Postgres add-on:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

3.2. Update your application to use the DATABASE_URL config var.

### 4. Deploy Your Application

4.1. Push your code to Heroku:

```bash
git push heroku main
```

4.2. Ensure at least one instance of the app is running:

```bash
heroku ps:scale web=1
```

### 5. Post-Deployment Tasks

5.1. Run database migrations (if applicable):

```bash
heroku run python manage.py db upgrade
```

5.2. Open your application:

```bash
heroku open
```

## Continuous Deployment

To set up continuous deployment:

1. Go to your Heroku dashboard and select your app.
2. Navigate to the "Deploy" tab.
3. In the "Deployment method" section, choose GitHub.
4. Connect your GitHub repository and enable automatic deploys from your main branch.

## Monitoring and Scaling

- Use `heroku logs --tail` to monitor your application logs.
- Scale your application using `heroku ps:scale web=X` where X is the number of dynos.

## Troubleshooting

If you encounter issues:

1. Check your Heroku logs: `heroku logs --tail`
2. Ensure all environment variables are correctly set
3. Verify that your `Procfile` and `runtime.txt` are correctly configured
4. Check that all required dependencies are in your `requirements.txt`

For more detailed information, refer to the [Heroku Dev Center](https://devcenter.heroku.com/).
