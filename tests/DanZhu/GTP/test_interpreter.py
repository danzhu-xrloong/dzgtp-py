from types import ModuleType
import pytest

@pytest.fixture
def interpreter():
    from DanZhu.GTP import interpreter
    return interpreter

def test_import_interpreter():
    from DanZhu.GTP import interpreter

def test_interpret_empty_respose__with_id(interpreter: ModuleType):
    response = interpreter.interpretSuccess(response = "", id = 2397)
    assert response == "=2397"

def test_interpret_empty_respose__without_id(interpreter: ModuleType):
    response = interpreter.interpretSuccess(response = "")
    assert response == "="

def test_interpret_response__with_id(interpreter: ModuleType):
    response = interpreter.interpretSuccess(response = "test-response", id = 2397)
    assert response == "=2397 test-response"

def test_interpret_response__without_id(interpreter: ModuleType):
    response = interpreter.interpretSuccess(response = "test-response")
    assert response == "= test-response"

def test_interpret_failure__with_id(interpreter: ModuleType):
    response = interpreter.interpretFailure(error = "test-error", id = 2397)
    assert response == "?2397 test-error"

def test_interpret_failure__without_id(interpreter: ModuleType):
    response = interpreter.interpretFailure(error = "test-error")
    assert response == "? test-error"

def test_interpret_panic(interpreter: ModuleType):
    response = interpreter.interpretPanic()
    assert response == "! panic"

def test_interpret_response(interpreter: ModuleType):
    strResponse = interpreter.interpretResponse("=1234 test-response")
    assert strResponse == "=1234 test-response\n\n"

    strError = interpreter.interpretResponse("?1234 test-error")
    assert strError == "?1234 test-error\n\n"

    strPanic = interpreter.interpretResponse("! panic")
    assert strPanic == "! panic\n\n"

