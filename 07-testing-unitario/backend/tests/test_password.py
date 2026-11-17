"""Tests de referencia — leé estos ANTES de hacer el ejercicio.

Son tests COMPLETOS que pasan. Fijate en cada uno las tres fases AAA
(Arrange / Act / Assert) y cómo el nombre del test describe el comportamiento.
"""

from app.password import is_strong, validate_password


def test_validate_password_devuelve_vacio_si_es_valida():
    # Arrange
    password = "Supersecreta1"
    # Act
    errores = validate_password(password)
    # Assert
    assert errores == []


def test_validate_password_detecta_corta():
    errores = validate_password("abc")
    assert any("corta" in e for e in errores)


def test_validate_password_detecta_falta_mayuscula():
    errores = validate_password("supersecreta1")
    assert any("mayúscula" in e for e in errores)


def test_validate_password_detecta_falta_numero():
    errores = validate_password("Supersecreta")
    assert any("número" in e for e in errores)


def test_is_strong_true_cuando_no_hay_errores():
    assert is_strong("Supersecreta1") is True


def test_is_strong_false_cuando_hay_errores():
    assert is_strong("corta") is False


# ── Fase 4 · Casos de borde ────────────────────────────────────────────────

def test_validate_password_vacia_reporta_los_tres_problemas():
    errores = validate_password("")
    assert len(errores) == 3


def test_validate_password_solo_numeros_falta_mayuscula():
    errores = validate_password("12345678")
    assert errores == ["falta una mayúscula"]


def test_validate_password_exactamente_8_es_valida():
    # Límite: el mínimo es 8 inclusive (< 8 falla, == 8 pasa).
    assert validate_password("Abcdefg1") == []


def test_validate_password_7_caracteres_es_corta():
    assert validate_password("Abcdef1") == ["muy corta (mínimo 8 caracteres)"]
