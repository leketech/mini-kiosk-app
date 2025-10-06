# Mini Kiosk DevOps Demo

A beginner-friendly simulation of a retail kiosk app with health monitoring.

## How to Run
1. `docker build -t kiosk-app .`
2. `docker run -p 5000:5000 kiosk-app`
3. `./health-check.sh`

## Why I Built This
To learn how DevOps ensures customer-facing apps stay reliable—even on remote devices.
# My Kiosk DevOps Project (Week 2)

A beginner-friendly kiosk app with PostgreSQL and Git automation.

## Features
- ✅ Flask web app
- ✅ PostgreSQL visit counter
- ✅ Health check endpoint (`/health`)
- ✅ Docker & Docker Compose
- ✅ Git with pre-push validation

## How to Run
1. Install Docker
2. `docker-compose up --build`
3. Visit http://localhost:5000

## What I Learned
- How apps connect to databases in containers
- Why health checks matter for remote devices
- How Git hooks can prevent broken code from being shared
![CI Pipeline](https://github.com/yourname/my-kiosk-devops/actions/workflows/ci.yml/badge.svg)

## CI/CD Pipeline
- On every pull request: runs unit tests + builds Docker image
- On merge to `main`: simulates staging deployment
- Fails fast if health check fails

Built with **GitHub Actions**—no external tools required.
