# Project Dharma

AI-powered social media monitoring platform for detecting and analyzing coordinated disinformation campaigns.

## Architecture

This project follows a microservices architecture with the following services:

- **data-collection-service**: Multi-platform data ingestion
- **ai-analysis-service**: ML-powered content analysis
- **campaign-detection-service**: Coordinated behavior identification
- **alert-management-service**: Notification and escalation system
- **api-gateway-service**: Authentication, routing, and rate limiting
- **dashboard-service**: User interface and visualizations
- **monitoring-service**: System health and performance tracking
- **configuration-service**: Service discovery and configuration management
- **event-bus-service**: Cross-service communication

## Development Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up pre-commit hooks: `pre-commit install`
3. Start services: `docker-compose up -d`

## Requirements

- Python 3.11+
- Docker & Docker Compose
- Node.js 18+ (for frontend components)