"""Health check."""

from fastapi import APIRouter, Depends

from app.projects.controller import get_project_service
from app.projects.service import ProjectService
from app.tasks.controller import get_task_service
from app.tasks.service import TaskService

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health_check(
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service),
):
    return {
        "status": "Funciona",
        "service": "03.5-arquitectura-modular",
        "tasks_count": task_service.count_tasks(),
        "projects_count": project_service.count_projects(),
    }
