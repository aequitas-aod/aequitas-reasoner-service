import json

from pydantic import BaseModel
import app.domain.core as _core_domain


def _is_admissible_type(obj: type) -> bool:
    for name in dir(_core_domain):
        symbol = getattr(_core_domain, name)
        if isinstance(symbol, type) and issubclass(obj, symbol):
            return True
    return False


def serialize(obj: BaseModel) -> dict:
    if not _is_admissible_type(type(obj)):
        raise ValueError(f"Type {type(obj)} is not admissible")
    return json.loads(obj.model_dump_json())


def deserialize(obj: dict, type: type) -> BaseModel:
    if not _is_admissible_type(type):
        raise ValueError(f"Type {type} is not admissible")
    return type(**obj)
