from __future__ import annotations

from dataclasses import dataclass, fields, asdict
from typing import Any, Dict, Type, TypeVar

T = TypeVar('T', bound='Model')


@dataclass
class Model:
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        known = {f.name for f in fields(cls)}
        kwargs = {k: v for k, v in data.items() if k in known}
        return cls(**kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)