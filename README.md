# Remote Device Dashboard

## Problem
Operators managing remote content devices need a simple way to:
- See which devices are online
- Trigger predefined maintenance scripts
- Observe execution results without direct access

## Solution
A lightweight web dashboard backed by a central API and a polling agent
running on each device.

## Architecture
[Frontend] -> [FastAPI Backend] <- [Agent]
                    |
                 [SQLite]

## Core Capabilities
- Device registration and heartbeat
- Remote script execution (whitelisted)
- Execution logs and status visibility

## What This Is NOT
- Not a secure production-grade RMM
- No user management
- No dynamic script uploads
- No real-time streaming (polling only)

## Tech Stack
- Backend: FastAPI, Python 3.11, SQLite
- Agent: Python 3.11
- Frontend: SvelteKit (TypeScript)
- Deployment: Docker, Docker Compose

## How to Run (Local)

1. Install Docker and Docker Compose
2. Copy `.env.example` to `.env` (or use the existing `.env`)
3. Run the stack:
   ```bash
   docker compose up -d
   ```
4. Access the dashboard:
   - Frontend: http://localhost:4173
   - Backend API: http://localhost:8000

To stop: `docker compose down`

## Tradeoffs
- Simplicity over scalability
- Polling over websockets
- Static token over auth system
