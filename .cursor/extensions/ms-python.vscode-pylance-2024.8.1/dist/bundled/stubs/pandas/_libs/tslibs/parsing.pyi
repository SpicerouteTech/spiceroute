from typing import Any

def parse_time_string(*args, **kwargs) -> Any: ...

class DateParseError(ValueError):
    def __init__(self, *args, **kwargs) -> None: ...
