"""Fakes in-memory que cumplen los puertos. Sin base de datos."""

from app.projects.schemas import Project, ProjectUpdate
from app.tasks.schemas import Task, TaskUpdate


class FakeTaskRepository:
    def __init__(self):
        self._store: dict[int, Task] = {}
        self._next = 1

    def list_all(self) -> list[Task]:
        return sorted(self._store.values(), key=lambda t: t.id)

    def get_by_id(self, task_id: int) -> Task | None:
        return self._store.get(task_id)

    def create(self, title: str, project_id: int | None = None) -> Task:
        task = Task(id=self._next, title=title, project_id=project_id)
        self._store[task.id] = task
        self._next += 1
        return task

    def update(self, task: Task, data: TaskUpdate) -> Task:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        return task

    def delete(self, task: Task) -> None:
        self._store.pop(task.id, None)

    def count(self) -> int:
        return len(self._store)


class FakeProjectRepository:
    def __init__(self):
        self._store: dict[int, Project] = {}
        self._next = 1

    def list_all(self) -> list[Project]:
        return sorted(self._store.values(), key=lambda p: p.id)

    def get_by_id(self, project_id: int) -> Project | None:
        return self._store.get(project_id)

    def create(self, name: str, description: str | None = None) -> Project:
        project = Project(id=self._next, name=name, description=description)
        self._store[project.id] = project
        self._next += 1
        return project

    def update(self, project: Project, data: ProjectUpdate) -> Project:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)
        return project

    def delete(self, project: Project) -> None:
        self._store.pop(project.id, None)

    def count(self) -> int:
        return len(self._store)
