"""Tests del TaskService con un fake: corren SIN base de datos."""

import pytest
from pydantic import ValidationError

from app.tasks.schemas import TaskCreate, TaskUpdate
from app.tasks.service import TaskService
from tests.fakes import FakeTaskRepository


@pytest.fixture
def service() -> TaskService:
    return TaskService(FakeTaskRepository())


def test_create_normaliza_titulo(service):
    task = service.create_task(TaskCreate(title="  hola  ", project_id=7))
    assert task.title == "hola"
    assert task.project_id == 7


def test_list_vacio(service):
    assert service.list_tasks() == []


def test_get_inexistente_devuelve_none(service):
    assert service.get_task(999) is None


def test_update_parcial_no_pisa_titulo(service):
    task = service.create_task(TaskCreate(title="original"))
    updated = service.update_task(task.id, TaskUpdate(completed=True))
    assert updated.title == "original"
    assert updated.completed is True


def test_update_normaliza_titulo(service):
    task = service.create_task(TaskCreate(title="original"))
    assert service.update_task(task.id, TaskUpdate(title="  nuevo  ")).title == "nuevo"


def test_update_inexistente_devuelve_none(service):
    assert service.update_task(999, TaskUpdate(completed=True)) is None


def test_delete(service):
    task = service.create_task(TaskCreate(title="a borrar"))
    assert service.delete_task(task.id) is True
    assert service.get_task(task.id) is None
    assert service.delete_task(task.id) is False


def test_count(service):
    service.create_task(TaskCreate(title="a"))
    service.create_task(TaskCreate(title="b"))
    assert service.count_tasks() == 2


@pytest.mark.parametrize("title", ["   ", None])
def test_update_rechaza_titulo_blanco_o_nulo(title):
    with pytest.raises(ValidationError):
        TaskUpdate(title=title)
