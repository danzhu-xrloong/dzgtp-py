def _interpret(
    response: str = "",
    error: str = "",
    panic: str = "",
    id: int | None = None
    ) -> str:
    idStr = id if id != None else ""
    if len(panic) > 0:
        responsePrefix = "!"
        data = panic
    elif len(error) > 0:
        responsePrefix = "?{id}".format(id = idStr)
        data = error
    else:
        responsePrefix = "={id}".format(id = idStr)
        data = response
    return "{prefix}{seperator}{data}".format(
        prefix = responsePrefix,
        seperator = " " if len(data) != 0 else "",
        data = data
    )

def interpretSuccess(response: str, id: int | None = None) -> str:
    return _interpret(response = response, id = id)

def interpretFailure(error: str, id: int | None = None) -> str:
    return _interpret(error = error, id = id)

def interpretPanic() -> str:
    return _interpret(panic = "panic")

def interpretResponse(message: str) -> str:
    return "{}\n\n".format(message)

