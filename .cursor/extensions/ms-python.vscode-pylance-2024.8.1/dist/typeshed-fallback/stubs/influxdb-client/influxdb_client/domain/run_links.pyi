from _typeshed import Incomplete

class RunLinks:
    openapi_types: Incomplete
    attribute_map: Incomplete
    discriminator: Incomplete
    def __init__(
        self, _self: Incomplete | None = None, task: Incomplete | None = None, retry: Incomplete | None = None
    ) -> None: ...
    @property
    def task(self): ...
    @task.setter
    def task(self, task) -> None: ...
    @property
    def retry(self): ...
    @retry.setter
    def retry(self, retry) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
