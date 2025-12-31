import pytest
import io
from typing import TypeAlias
from DanZhu.GTP.engine import GtpEngine

EngineHandler: TypeAlias = tuple[GtpEngine, io.TextIOWrapper, io.TextIOWrapper]

@pytest.fixture
def engineHandler():
    import os
    from DanZhu.GTP import engine

    pipeOutsideToEngine = os.pipe()
    pipeEngineToOutside = os.pipe()
    streamOutsideToEngineReceiver = open(pipeOutsideToEngine[0], "r")
    streamOutsideToEngineSender = open(pipeOutsideToEngine[1], "w")
    streamEngineToOutsideReceiver = open(pipeEngineToOutside[0], "r")
    streamEngineToOutsideSender = open(pipeEngineToOutside[1], "w")

    e = engine.GtpEngine(streamIn = streamOutsideToEngineReceiver, streamOut = streamEngineToOutsideSender)
    yield (e, streamOutsideToEngineSender, streamEngineToOutsideReceiver)

    streamOutsideToEngineReceiver.close()
    streamOutsideToEngineSender.close()
    streamEngineToOutsideReceiver.close()
    streamEngineToOutsideSender.close()

def test_import_engine():
    from DanZhu.GTP import engine

def test_engine_output(engineHandler: EngineHandler):
    engine, _, streamEngineToOutsideReceiver = engineHandler
    engine.output(message = "test-message")
    assert streamEngineToOutsideReceiver.readline() == "test-message\n"
    assert streamEngineToOutsideReceiver.readline() == "\n"

def test_engine_input(engineHandler: EngineHandler):
    engine, streamOutsideToEngineSender, _ = engineHandler

    streamOutsideToEngineSender.write("test-message\n")
    streamOutsideToEngineSender.flush()
    line = engine.input()
    assert line == "test-message\n"

@pytest.mark.parametrize(
    argnames='command, expected',
    argvalues=[
        ("2397 protocol_version", "=2397 2"),
        ("protocol_version", "= 2"),
        ("2397 test-command", "?2397 unknown command"),
        ("test-command", "? unknown command"),
        ]
)
def test_interpretSuccess(
        engineHandler: EngineHandler,
        command: str,
        expected: str
    ):
    engine, streamOutsideToEngineSender, streamEngineToOutsideReceiver = engineHandler

    streamOutsideToEngineSender.write("{}\n".format(command))
    streamOutsideToEngineSender.flush()
    streamOutsideToEngineSender.close()
    engine.start()
    line = streamEngineToOutsideReceiver.readline()
    assert line.strip() == expected


@pytest.mark.parametrize(
    argnames='command, expected, expectedDone',
    argvalues=[
        ("2397 protocol_version", "=2397 2", None),
        ("2397 quit", "=2397", True),
        ("2397 test-command", "?2397 unknown command", None),
        ]
)
def test_interpretCommand(
        engineHandler: EngineHandler,
        command: str,
        expected: str,
        expectedDone: bool
    ):
    engine, _, streamEngineToOutsideReceiver = engineHandler

    done = engine.interpretCommand(command)
    line = streamEngineToOutsideReceiver.readline()
    assert done == expectedDone
    assert line.strip() == expected