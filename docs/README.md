# Multi-Agent Salon Management System

## Overview
A modular, event-driven, AI-powered salon management platform with specialized agents, local LLM integration, and React frontend.

## Architecture
- **Backend:** FastAPI with modular routers
- **Frontend:** React app
- **Agents:** Scheduler, Inventory, Staff, Reporting, Customer Service, Optimization, Orchestrator
- **Communication:** ZeroMQ pub-sub
- **LLM:** Local TinyLlama or similar
- **Database:** SQLite/Postgres

## Agents
### Scheduler
Manages appointments, reduces idle time.

### Inventory
Tracks stock, alerts low inventory.

### Staff
Manages schedules, attendance.

### Reporting
Generates reports, insights.

### Customer Service
Handles queries, FAQs via LLM.

### Optimization
Improves bookings, marketing.

### Orchestrator
Coordinates all agents.

## Setup
1. Clone repo
2. Setup Python venv, install dependencies
3. Run ZeroMQ broker
4. Start backend: `uvicorn main:app`
5. Start frontend: `npm start`

## API Endpoints
- `/scheduler`
- `/inventory`
- `/staff`
- `/reporting`
- `/customer_service`

## Development
- Modular code in `agents/`
- Event-driven design
- Continuous learning loop
- RL components for optimization

## Deployment
- Use Docker Compose
- Periodic model fine-tuning

## License
Open source, customizable.

