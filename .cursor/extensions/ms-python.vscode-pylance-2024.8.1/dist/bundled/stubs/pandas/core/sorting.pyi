from typing import Any

def get_group_index(labels: Any, shape: Any, sort: bool, xnull: bool) -> Any: ...
def get_compressed_ids(labels: Any, sizes: Any): ...
def is_int64_overflow_possible(shape: Any) -> bool: ...
def decons_group_index(comp_labels: Any, shape: Any): ...
def decons_obs_group_ids(
    comp_ids: Any, obs_ids: Any, shape: Any, labels: Any, xnull: bool
) -> Any: ...
def indexer_from_factorized(labels: Any, shape: Any, compress: bool = ...) -> Any: ...
def lexsort_indexer(keys: Any, orders: Any = ..., na_position: str = ...) -> Any: ...
def nargsort(
    items: Any, kind: str = ..., ascending: bool = ..., na_position: str = ...
) -> Any: ...

class _KeyMapper:
    levels: Any = ...
    labels: Any = ...
    comp_ids: Any = ...
    k: Any = ...
    tables: Any = ...
    def __init__(
        self, comp_ids: Any, ngroups: int, levels: Any, labels: Any
    ) -> None: ...
    def get_key(self, comp_id: Any): ...

def get_flattened_iterator(comp_ids: Any, ngroups: Any, levels: Any, labels: Any): ...
def get_indexer_dict(label_list: Any, keys: Any): ...
def get_group_index_sorter(group_index: Any, ngroups: int) -> Any: ...
def compress_group_index(group_index: Any, sort: bool = ...) -> Any: ...
