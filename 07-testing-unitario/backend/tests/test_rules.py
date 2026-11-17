"""Tests de autorización — EJERCICIO.

Los dos primeros son la REFERENCIA (ya completos, pasan). Los cuatro de abajo
tienen `assert False, "TODO..."` y FALLAN a propósito: son tu trabajo en la
Fase 1 de la guía.

Reglas:
  - Un test = un comportamiento. No pruebes todo junto.
  - Pensá el caso de borde (¿rol vacío? ¿scope vacío?).
  - Corré `uv run pytest` después de cada uno hasta verlo verde.
"""

import pytest

from app.rules import (
    can_change_role,
    can_delete,
    can_edit,
    can_manage_users,
    scope_allows_write,
)


# ── Referencia (no tocar) ──────────────────────────────────────────────────

def test_scope_allows_write_con_write():
    # Arrange
    scope = "read write"
    # Act
    resultado = scope_allows_write(scope)
    # Assert
    assert resultado is True


def test_scope_allows_write_solo_read():
    assert scope_allows_write("read") is False


# ── Fase 1 · Completá los TODO ─────────────────────────────────────────────

def test_can_manage_users_solo_admin():
    assert can_manage_users("admin") is True
    assert can_manage_users("viewer") is False


def test_can_manage_users_rol_vacio_no_puede():
    # Caso de borde: un rol vacío no es admin (deny-by-default).
    assert can_manage_users("") is False


def test_can_change_role_solo_admin():
    assert can_change_role("admin") is True
    assert can_change_role("editor") is False


# Fase 3 · parametrize: reescritura de test_can_delete_solo_admin.
# Cada tupla es un test aparte en el reporte; sumar un caso es una línea.
@pytest.mark.parametrize("role,esperado", [
    ("admin", True),
    ("editor", False),
    ("viewer", False),
    ("", False),
])
def test_can_delete_por_rol(role, esperado):
    assert can_delete(role) is esperado


def test_can_edit_dueño_puede():
    # Arrange: el usuario 5 es dueño del documento del usuario 5
    owner_id, user_id = 5, 5
    # Act
    resultado = can_edit(owner_id=owner_id, user_id=user_id, role="editor")
    # Assert
    assert resultado is True


def test_can_edit_admin_puede_sobre_ajeno():
    # El segundo camino del OR: no es dueño, pero es admin.
    assert can_edit(owner_id=5, user_id=9, role="admin") is True


def test_can_edit_editor_no_puede_sobre_ajeno():
    # Ni dueño ni admin → no edita.
    assert can_edit(owner_id=5, user_id=9, role="editor") is False


def test_scope_allows_write_scope_vacio():
    # Caso de borde: "".split() == [] → sin write.
    assert scope_allows_write("") is False


# ── Fase 4 · Casos de borde ────────────────────────────────────────────────

def test_scope_allows_write_tolera_espacio_final():
    # split() sin argumentos descarta espacios sobrantes: "write " == ["write"].
    assert scope_allows_write("write ") is True


def test_scope_allows_write_es_case_sensitive():
    # Decisión: los scopes son case-sensitive (OAuth 2.0, RFC 6749 §3.3).
    # "WRITE" no es el scope "write" → no habilita escritura.
    assert scope_allows_write("WRITE") is False


def test_scope_allows_write_no_acepta_substring():
    # "rewrite" contiene la palabra "write" pero NO es el scope "write".
    assert scope_allows_write("read rewrite") is False


def test_can_edit_dueño_viewer_puede_lo_suyo():
    # Matriz del 06: canEdit (doc propio) → viewer ✅. La regla es dueño OR admin;
    # el rol no importa si es el dueño. (En el 06 el viewer igual queda afuera
    # por su scope "read", pero eso es otra regla: scope_allows_write.)
    assert can_edit(owner_id=3, user_id=3, role="viewer") is True
