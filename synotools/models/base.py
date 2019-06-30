from typing import Any, Dict, List, Tuple

from synotools.common.exceptions import ObjectDoesNotExist


class ModelBase(type):
    """
    The base type that is used for all models.
    Similar to Django's base model
    https://github.com/django/django/blob/master/django/db/models/base.py
    """

    DoesNotExist: ObjectDoesNotExist = None

    def __new__(
        cls, name: str, bases: Tuple[type], attrs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)  # type: ignore
        parents = [base for base in bases if isinstance(base, ModelBase)]

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        if not parents:
            return new_class

        # Create list of defined fields on FIELDS for future validation and assignment.
        # Exclude built-in properties and any callable methods.
        fields = [
            attr
            for attr, value in attrs.items()
            if not attr.startswith(("_", "__")) and not callable(value)
        ]
        new_class.FIELDS = fields
        new_class.DoesNotExist = ObjectDoesNotExist
        return new_class


class Model(metaclass=ModelBase):
    FIELDS: List[str] = None

    @property
    def dict(self) -> Dict:
        output: Dict = {}
        for field in self.FIELDS:
            value = getattr(self, field)
            if isinstance(value, Model):
                output[field] = value.dict
            else:
                output[field] = value

        return output

    def __init__(self, **data: Any) -> None:
        for key, value in data.items():
            if key not in self.FIELDS:
                raise TypeError(
                    f"{self.__class__.__name__}() got unexpected keyword argument '{key}'"
                )

            if hasattr(self, f"set_{key}"):
                setter = getattr(self, f"set_{key}")
                setter(value)
            else:
                setattr(self, key, value)

    def validate(self) -> None:
        for field in self.FIELDS:
            try:
                validator = getattr(self, f"validate_{field}")
                validator()
            except AttributeError:
                pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        self_data = self.dict
        other_data = other.dict

        return self_data == other_data

    def __str__(self):
        return str(self.dict)

    def __repl__(self):
        return str(self.dict)
