# TaskPilot
An AI-powered goal planning, executiontracking and workflow orchestration assistant.

🌐 **Live Demo:** https://taskpilotaifinal.vercel.app/  
📦 **Repository:** https://github.com/Raheem2010/taskpilot  

---

## Why TaskPilot Matters

Most productivity tools help you **organize thoughts**.  
TaskPilot helps you **execute goals**.

TaskPilot turns vague, high-level goals into **structured milestones and actionable tasks**, then keeps them **trackable across UI, CLI, and automation workflows**. It bridges the gap between *planning* and *execution*.

### Who benefits?
- **Individuals & founders**: Instantly break down goals into achievable steps.
- **Builders & teams**: Align execution around clear milestones and task states.
- **Automation-first workflows**: Integrate planning directly into agents, pipelines, and orchestration tools.

### Why TaskPilot is different
| Tool | Limitation | TaskPilot Advantage |
|----|----|----|
| Notion / Docs | Flexible but manual | Opinionated, execution-first plans |
| ChatGPT | One-off responses | Persistent plans + task state |
| To-do apps | Task lists only | Goal → milestone → task hierarchy |
| Generic planners | UI-only | **UI + CLI + automation-ready API** |

TaskPilot is built to be **agent-native** — usable by humans *and* machines.

---

## ✨ Core Features

- 🧠 **AI-assisted planning**: Convert goals into milestones and tasks
- 📊 **Status dashboard**: Track all goals and progress in one place
- 🔄 **Persistent task states**: Pending, in-progress, completed
- 🧩 **CLI support**: Plan, check status, and verify backend health from terminal
- ⚙️ **Automation-ready API**: Designed for orchestration and agent execution
- 🚀 **Production deployment** on Vercel

---

## 🧰 Tech Stack & Sponsor Tools

This project intentionally integrates sponsor technologies:

- **Cline CLI** – Core CLI experience for interacting with TaskPilot  
- **Kestra** – Workflow orchestration & automation hooks  
- **Vercel** – Production frontend deployment  
- **CodeRabbit AI** – AI-powered PR review and code quality feedback  
- **Oumi (underground)** – Agent experimentation & reasoning support  

**Backend**
- FastAPI
- SQLAlchemy
- PostgreSQL

**Frontend**
- Next.js (App Router)
- Tailwind CSS

**CLI**
- Typer
- Python requests

---

## 🔌 API Overview

| Method | Endpoint | Description |
|----|----|----|
| GET | `/health` | Backend health check |
| POST | `/api/v1/plan` | Generate plan from goal |
| GET | `/api/v1/status` | Fetch all goals + tasks |
| PATCH | `/api/v1/tasks/update-status` | Update task status |
| POST | `/api/v1/agent/execute` | Trigger agent execution |

📘 Swagger docs available at `/docs` when running backend locally.

---

## 🖥️ Running Locally

### Backend
```bash
cd backend
# activate venv
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Frontend
cd frontend
npm install
npm run dev


Frontend runs on:

<http://localhost:3000>

💻 CLI Usage (Cline-powered)
taskpilot health
taskpilot plan "Launch Neyux brand and hit 50 sales in 30 days"
taskpilot status


The same backend powers UI, CLI, and automation workflows.

🎥 Demo Flow (2 minutes)

Enter a goal on the UI → generate plan

View all goals on the dashboard

Run taskpilot plan from the CLI

Check progress with taskpilot status

Highlight automation readiness via agent execution endpoint

🏁 Why TaskPilot Wins

Demonstrates end-to-end agent workflow (UI → API → CLI → orchestration)

Clear business value beyond a demo app

Strong automation and execution focus

Clean separation of concerns (frontend, backend, CLI)

Production-ready deployment

Built with ❤️ for AI Agents Assemble
By Fortune Techies
