import inspect
import dataclasses
from typing import Optional, Type, Any, Set, List, Dict, Tuple, ForwardRef, Union, TypeVar, get_type_hints
import typing
import yaml
NoneType = type(None)
DataType = TypeVar('DataType')

def unwrap_type(t: Type) -> Type:
    """
    Unwrap a type by recursively following any type aliases until a concrete type is reached.
    """
    if isinstance(t, ForwardRef):
        return t.__forward_arg__
    if hasattr(t, "__origin__"):
        if t.__origin__ in (list, List):
            return List[unwrap_type(t.__args__[0])]
        elif t.__origin__ in (dict, Dict):
            return Dict[unwrap_type(t.__args__[0]), unwrap_type(t.__args__[1])]
        elif t.__origin__ in (set, Set):
            return Set[unwrap_type(t.__args__[0])]
        elif t.__origin__ in (tuple, Tuple):
            return type(tuple(unwrap_type(arg) for arg in t.__args__))
    return t

def get_dependent_classes(t: Type, seen: Optional[Set[Type]] = None) -> Set[Type]:
    """
    Recursively walk the fields of a type and return a set of all dependent classes.
    """
    if seen is None:
        seen = set()

    t = unwrap_type(t)
    if t in [None, NoneType, True, False, int, float, str, bytes, bytearray]:
        return set()
    if t in seen:
        return set()
    seen.add(t)
    if dataclasses.is_dataclass(t):
        fields = t.__dataclass_fields__.values()
        type_hints = typing.get_type_hints(t)
        return set.union(seen, *[get_dependent_classes(type_hints[field.name], seen) for field in fields])
    elif hasattr(t, "__args__"):
        seen.remove(t)
        return set.union(seen, *[get_dependent_classes(arg, seen) for arg in t.__args__])
    elif t in [None, NoneType, True, False, bool, int, float, str, bytes, bytearray, list, dict, tuple, set, frozenset]:
        seen.remove(t)
        return set()
    else:
        return set([t])
    
def get_source(my_cls : Type) -> str:
    source = ""
    for x in get_dependent_classes(my_cls):
        source += str(inspect.getsource(x))
    return source

def is_optional_type_hint(tp):
    return getattr(tp, "__origin__", None) is Optional

def from_yaml(yaml_str: str, cls: Type[DataType]) -> Union[DataType, List[DataType]]:
    type_hints = get_type_hints(cls)
    def _from_yaml(data: Any, cls: Type[DataType]) -> Union[DataType, List[DataType]]:
        if isinstance(data, list):
            return [_from_yaml(x, cls) for x in data]
        elif isinstance(data, dict):
            kwargs = {}
            for key, value in data.items():
                if isinstance(value, list):
                    result = []
                    for item in value:
                        result.append(_from_yaml(item, type_hints[key].__args__[0]))
                    kwargs[key] = result
                elif isinstance(value, dict):
                    try:
                        kwargs[key] = _from_yaml(value, type_hints[key].__args__[1])
                    except:
                        kwargs[key] = value
                else:
                    kwargs[key] = value
            return cls(**kwargs)
        else:
            return data
    data = yaml.safe_load(yaml_str)
    return _from_yaml(data, cls)

def deserialize(message : str, t: Type[DataType]) -> List[DataType]:
    result = from_yaml(message, t)
    if not isinstance(result, List):
        result = [result]
    return result
