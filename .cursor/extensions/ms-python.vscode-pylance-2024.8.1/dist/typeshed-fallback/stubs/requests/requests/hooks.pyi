from typing import Any

HOOKS: Any

def default_hooks(): ...
def dispatch_hook(key, hooks, hook_data, **kwargs): ...
