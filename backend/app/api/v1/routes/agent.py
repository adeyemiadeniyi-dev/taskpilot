from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.api.v1.models.agent import Goal, Task
from app.api.v1.schemas.agent import (
    GoalStatusSchema,
    MilestoneSchema,
    PlanRequest,
    PlanResponse,
    StatusResponse,
    TaskSchema,
)

router = APIRouter(prefix="/agent", tags=["Agent"])


# ---- Execute agent ----
class AgentExecuteRequest(BaseModel):
    task_id: Optional[int] = None
    goal_id: Optional[int] = None
    instruction: Optional[str] = None


class AgentExecuteResponse(BaseModel):
    execution_id: str
    message: str


@router.post("/execute", response_model=AgentExecuteResponse)
def execute_agent(payload: AgentExecuteRequest, db: Session = Depends(get_db)):
    if payload.task_id is not None and payload.goal_id is not None:
        raise HTTPException(
            status_code=400, detail="Provide either task_id or goal_id, not both."
        )

    if payload.task_id is not None:
        task = db.get(Task, payload.task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        instruction = payload.instruction or f"Work on task: {task.title}"

    elif payload.goal_id is not None:
        goal = db.get(Goal, payload.goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        instruction = payload.instruction or f"Work on goal: {goal.goal}"

    else:
        raise HTTPException(
            status_code=400, detail="Either task_id or goal_id must be provided."
        )

    execution_id = f"exec_{payload.task_id or payload.goal_id}"
    return AgentExecuteResponse(
        execution_id=execution_id,
        message=f"Agent started with instruction: {instruction}",
    )


# ---- Goal planning ----
@router.post("/plan", response_model=PlanResponse)
def generate_plan(payload: PlanRequest, db: Session = Depends(get_db)) -> PlanResponse:
    db_goal = Goal(goal=payload.goal, status="in_progress")
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)

    milestones = [
        MilestoneSchema(
            title="Clarify and scope your goal",
            description="Define success metrics and timeline.",
            tasks=[
                TaskSchema(title="Write a clear goal statement"),
                TaskSchema(title="Define 2-3 success metrics"),
            ],
        ),
        MilestoneSchema(
            title="Break goal into weekly tasks",
            description="Create a breakdown of tasks.",
            tasks=[
                TaskSchema(title="List all sub-tasks needed"),
                TaskSchema(title="Group tasks by week and priority"),
            ],
        ),
        MilestoneSchema(
            title="Set up a tracking system",
            description="Choose how you will track progress.",
            tasks=[
                TaskSchema(title="Pick a tracking tool and create a project board"),
                TaskSchema(title="Set aside weekly review time"),
            ],
        ),
    ]

    # Batch insert tasks
    tasks_to_add = [
        Task(goal_id=db_goal.id, title=t.title, status=getattr(t, "status", "pending"))
        for m in milestones
        for t in m.tasks
    ]
    db.add_all(tasks_to_add)
    db.commit()

    # Reload tasks from DB and assign IDs
    db.refresh(db_goal)
    db_tasks = sorted(db_goal.tasks, key=lambda t: t.id)
    idx = 0
    for m in milestones:
        for t in m.tasks:
            if idx < len(db_tasks):
                t.id = db_tasks[idx].id
                idx += 1

    return PlanResponse(goal_id=db_goal.id, goal=db_goal.goal,milestones=milestones)


# ---- Get status ----
@router.get("/status", response_model=StatusResponse)
def get_status(goal_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Goal)
    if goal_id is not None:
        query = query.filter(Goal.id == goal_id)

    goals = query.order_by(Goal.created_at.desc()).all()

    result_goals = [
        GoalStatusSchema(
            id=g.id,
            goal=g.goal,
            status=g.status,
            tasks=[TaskSchema(id=t.id, title=t.title, status=t.status) for t in g.tasks],
        )
        for g in goals
    ]

    return StatusResponse(goals=result_goals)