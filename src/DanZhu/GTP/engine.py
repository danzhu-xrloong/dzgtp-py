from . import interpreter
from contextlib import redirect_stdout
from contextlib import contextmanager
from dataclasses import dataclass

@contextmanager
def redirect_stdin(new_stdin):
    import sys

    old_stdin = sys.stdin
    try:
        sys.stdin = new_stdin
        yield
    finally:
        sys.stdin = old_stdin

class GtpEngine:
    PROTOCOL_VERSION = 2

    @dataclass(frozen=True)
    class Config:
        name: str
        version: str

    def __init__(self,
                 config: Config,
                 streamIn,
                 streamOut
                 ):
        self.config = config
        self.streamIn = streamIn
        self.streamOut = streamOut
        self._command_registry = {}
        self._register_builtin_commands()

    def register_command(self, name):
        def decorator(func):
            self._command_registry[name] = func
            return func
        return decorator

    def input(self) -> str:
        line = self.streamIn.readline()
        return line

    def output(self, message: str):
        self.streamOut.write(interpreter.interpretResponse(message))
        self.streamOut.flush()

    def outputSuccess(self, response: str, id: int | None):
        message = interpreter.interpretSuccess(response, id = id)
        self.output(message)

    def outputFailure(self, error: str, id: int | None):
        message = interpreter.interpretFailure(error, id = id)
        self.output(message,)

    def outputPanic(self):
        message = interpreter.interpretPanic()
        self.output(message)

    def start(self):
        with redirect_stdin(self.streamIn), redirect_stdout(self.streamOut):
            while True:
                line = self.input()
                if len(line) == 0:
                    break
                isDone = self.interpretCommand(line)
                if isDone:
                    break

    def interpretCommand(self, line):
        # Remove comments
        line = line.split('#')[0]
        line = line.strip()
        if len(line) == 0:
            return
        parts = line.split(' ')

        id = None
        try:
            id = int(parts[0])
            command = parts[1]
            args = parts[2:]
        except ValueError:
            id = None
            command = parts[0]
            args = parts[1:]

        handler = self._command_registry.get(command)
        if handler:
            return handler(id, *args)
        else:
            self.outputFailure("unknown command", id)

    def _register_builtin_commands(self):
        @self.register_command("quit")
        def _quit(id, *args):
            self.outputSuccess("", id)
            self.streamIn.close()
            self.streamOut.close()
            return True

        @self.register_command("protocol_version")
        def _protocol_version(id, *args):
            self.outputSuccess(f"{GtpEngine.PROTOCOL_VERSION}", id)

        @self.register_command("name")
        def _name(id, *args):
            self.outputSuccess(f"{self.config.name}", id)

        @self.register_command("version")
        def _version(id, *args):
            self.outputSuccess(f"{self.config.version}", id)

        @self.register_command("list_commands")
        def _list_commands(id, *args) -> str:
            commands = '\n'.join(sorted(self._command_registry.keys()))
            self.outputSuccess(f"{commands}", id)

