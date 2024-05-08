from dataclasses import dataclass
from enum import Enum
from uuid import UUID

@dataclass(kw_only=True)
class item:
    name: str | None

class parameter_mode(Enum):
    mode_in = 1
    mode_out = 2
    mode_inout = 3
    
@dataclass(kw_only=True)
class parameter(item):
    mode: parameter_mode | None
    
@dataclass(kw_only=True)
class function(item):
    parameters: list[UUID] | None
    
@dataclass(kw_only=True)
class variable(item):
    mut: bool | None
    
@dataclass(kw_only=True)
class package(item):
    func: list[UUID] | None
    var: list[UUID] | None
    
class ongoing_mode(Enum):
    not_created=1
    ano=2
    decl_ano=3
    pre_defi=4
    defi=5
    pre_decl=6
    decl=7
    term=8
    
@dataclass
class parsed_file:
    name: str
    items: dict[UUID, item]
    active_items: list[tuple[UUID, ongoing_mode]]
    pkg: UUID | None
    