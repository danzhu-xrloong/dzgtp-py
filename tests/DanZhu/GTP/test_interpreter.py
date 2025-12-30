from types import ModuleType
import pytest

@pytest.fixture
def interpreter():
    from DanZhu.GTP import interpreter
    return interpreter

def test_import_interpreter():
    from DanZhu.GTP import interpreter

@pytest.mark.parametrize(
    argnames='id, response, expected',
    argvalues=[
        (2397, "test-response", "=2397 test-response"),
        (None, "test-response", "= test-response"),
        (2397, "", "=2397"),
        (None, "", "="),
        ]
)
def test_interpretSuccess(
    interpreter: ModuleType,
    id: int | None,
    response: str,
    expected: str
    ):
    response = interpreter.interpretSuccess(response = response, id = id)
    assert response == expected

@pytest.mark.parametrize(
    argnames='id, error, expected',
    argvalues=[
        (2397, "test-error", "?2397 test-error"),
        (None, "test-error", "? test-error"),
        ]
)
def test_interpretFailure(
    interpreter: ModuleType,
    id: int | None,
    error: str,
    expected: str
    ):
    response = interpreter.interpretFailure(error = error, id = id)
    assert response == expected

def test_interpret_panic(interpreter: ModuleType):
    response = interpreter.interpretPanic()
    assert response == "! panic"

@pytest.mark.parametrize(
    argnames='message, expected',
    argvalues=[
        ("=1234 test-response", "=1234 test-response\n\n"),
        ("?1234 test-error", "?1234 test-error\n\n"),
        ("! panic", "! panic\n\n"),
        ]
)
def test_interpret_response(
    interpreter: ModuleType,
    message: str,
    expected: str
    ):
    response = interpreter.interpretResponse(message)
    assert response == expected
