"""Tests del ProjectService con un fake: corren SIN base de datos."""

import pytest
from pydantic import ValidationError

from app.projects.schemas import ProjectCreate, ProjectUpdate
from app.projects.service import ProjectService
from tests.fakes import FakeProjectRepository


@pytest.fixture
def service() -> ProjectService:
    return ProjectService(FakeProjectRepository())


def test_create_normaliza_nombre(service):
    assert service.create_project(ProjectCreate(name="  backend  ")).name == "backend"


def test_update_parcial_no_pisa_nombre(service):
    project = service.create_project(ProjectCreate(name="original"))
    updated = service.update_project(project.id, ProjectUpdate(description="desc"))
    assert updated.name == "original"
    assert updated.description == "desc"


def test_update_inexistente_devuelve_none(service):
    assert service.update_project(999, ProjectUpdate(name="x")) is None


def test_delete(service):
    project = service.create_project(ProjectCreate(name="a borrar"))
    assert service.delete_project(project.id) is True
    assert service.delete_project(project.id) is False


def test_update_rechaza_nombre_nulo():
    with pytest.raises(ValidationError):
        ProjectUpdate(name=None)
