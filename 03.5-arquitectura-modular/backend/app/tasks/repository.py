"""Adaptador concreto del puerto: SQLModel."""

from sqlmodel import Session, select

from app.tasks.schemas import Task, TaskUpdate


class SqlModelTaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def list_all(self) -> list[Task]:
        statement = select(Task).order_by(Task.id)
        return list(self.session.exec(statement).all())

    def get_by_id(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def create(self, title: str, project_id: int | None = None) -> Task:
        task = Task(title=title, project_id=project_id)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task: Task, data: TaskUpdate) -> Task:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()

    def count(self) -> int:
        from sqlalchemy import func
        statement = select(func.count()).select_from(Task)
        return self.session.exec(statement).one()
