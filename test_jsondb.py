# ============================================
# test_jsondb.py
# Tests para la clase JsonDB con pytest
# ============================================

import json
import pytest
from jsonDB import JsonDB


# ---------------------------------------------------
# TEST 1 — Crea archivo si no existe
# ---------------------------------------------------
def test_crea_archivo_si_no_existe(tmp_path):
    ruta = tmp_path / "test.json"
    db = JsonDB(ruta, default={"a": 1})

    assert ruta.exists()
    assert json.loads(ruta.read_text()) == {"a": 1}


# ---------------------------------------------------
# TEST 2 — Carga JSON existente
# ---------------------------------------------------
def test_carga_json_existente(tmp_path):
    ruta = tmp_path / "test.json"
    ruta.write_text('{"x": 10}')

    db = JsonDB(ruta)

    assert db.data == {"x": 10}


# ---------------------------------------------------
# TEST 3 — set() añade claves
# ---------------------------------------------------
def test_set_agrega_clave(tmp_path):
    ruta = tmp_path / "test.json"
    db = JsonDB(ruta, default={})

    db.set("user", "123")

    assert db.get("user") == "123"


# ---------------------------------------------------
# TEST 4 — exists() funciona
# ---------------------------------------------------
def test_exists(tmp_path):
    ruta = tmp_path / "test.json"
    db = JsonDB(ruta, default={"a": 1})

    assert db.exists("a") is True
    assert db.exists("b") is False


# ---------------------------------------------------
# TEST 5 — append() funciona en listas
# ---------------------------------------------------
def test_append_lista(tmp_path):
    ruta = tmp_path / "test.json"
    db = JsonDB(ruta, default=[])

    db.append({"x": 1})

    assert db.data == [{"x": 1}]


# ---------------------------------------------------
# TEST 6 — append() en diccionario → error
# ---------------------------------------------------
def test_append_en_diccionario_error(tmp_path):
    ruta = tmp_path / "test.json"
    db = JsonDB(ruta, default={})

    with pytest.raises(TypeError):
        db.append(123)


# ---------------------------------------------------
# TEST 7 — JSON corrupto → se restaura default
# ---------------------------------------------------
def test_json_corrupto(tmp_path):
    ruta = tmp_path / "test.json"
    ruta.write_text("{esto no es json}")

    db = JsonDB(ruta, default={"ok": True})

    assert db.data == {"ok": True}


# ---------------------------------------------------
# TEST 8 — extend() añade múltiples elementos
# ---------------------------------------------------
def test_extend(tmp_path):
    ruta = tmp_path / "test.json"
    db = JsonDB(ruta, default=[])

    db.extend([1, 2, 3])

    assert db.data == [1, 2, 3]


if __name__ == "__main__":
    # Ejecuta pytest sobre este mismo archivo
    pytest.main([__file__])