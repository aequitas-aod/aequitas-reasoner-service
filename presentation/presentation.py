import json
from typing import Type, TypeVar

from pydantic import BaseModel

import domain.graph.core as _graph_core_domain
import domain.project.core as _project_core_domain

T = TypeVar("T", bound=BaseModel)


def _is_admissible_type(obj: type) -> bool:
    for name in dir(_graph_core_domain) + dir(_project_core_domain):
        symbol = getattr(_graph_core_domain, name)
        if isinstance(symbol, type) and issubclass(obj, symbol):
            return True
    return False


def serialize(obj: BaseModel) -> dict:
    if not _is_admissible_type(type(obj)):
        raise ValueError(f"Type {type(obj)} is not admissible")
    return json.loads(obj.model_dump_json())


def deserialize(obj: dict, klass: Type[T]) -> T:
    if not _is_admissible_type(klass):
        raise ValueError(f"Type {klass} is not admissible")
    return klass(**obj)
