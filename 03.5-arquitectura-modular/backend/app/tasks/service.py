"""Service Task — depende del PUERTO (TaskRepository), no del adaptador."""

from app.tasks.schemas import Task, TaskCreate, TaskUpdate
from app.tasks.ports import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self) -> list[Task]:
        return self.repository.list_all()

    def get_task(self, task_id: int) -> Task | None:
        return self.repository.get_by_id(task_id)

    def create_task(self, body: TaskCreate) -> Task:
        return self.repository.create(body.title.strip(), body.project_id)

    def update_task(self, task_id: int, body: TaskUpdate) -> Task | None:
        task = self.repository.get_by_id(task_id)
        if task is None:
            return None
        if body.title is not None:
            body = body.model_copy(update={"title": body.title.strip()})
        return self.repository.update(task, body)

    def delete_task(self, task_id: int) -> bool:
        task = self.repository.get_by_id(task_id)
        if task is None:
            return False
        self.repository.delete(task)
        return True

    def count_tasks(self) -> int:
        return self.repository.count()
