from typing import Callable, Protocol, Any, Dict, TypeVar, no_type_check
from sqladmin._types import MODEL_PROPERTY
from wtforms.fields.core import UnboundField
from wtforms import StringField
from sqladmin.forms import ModelConverter
from sqlalchemy.orm import ColumnProperty


class ConverterCallable(Protocol):
    def __call__(
        self,
        model: type,
        prop: MODEL_PROPERTY,
        kwargs: Dict[str, Any],
    ) -> UnboundField: ...  # pragma: no cover


T_CC = TypeVar("T_CC", bound=ConverterCallable)

_WTFORMS_PRIVATE_ATTRS = {"data", "errors", "process", "validate", "populate_obj"}
WTFORMS_ATTRS = {key: key + "_" for key in _WTFORMS_PRIVATE_ATTRS}
WTFORMS_ATTRS_REVERSED = {v: k for k, v in WTFORMS_ATTRS.items()}


@no_type_check
def converts(*args: str) -> Callable[[T_CC], T_CC]:
    def _inner(func: T_CC) -> T_CC:
        func._converter_for = frozenset(args)
        return func

    return _inner


class UserConverter(ModelConverter):
    @converts("sqlalchemy_utils.types.password.PasswordType")
    def conv_password(
        self, model: type, prop: ColumnProperty, kwargs: Dict[str, Any]
    ) -> UnboundField:
        extra_validators = self._string_common(prop)
        kwargs.setdefault("validators", [])
        kwargs["validators"].extend(extra_validators)
        return StringField(**kwargs)

    # @converts("sqlalchemy.sql.sqltypes.String")
    # def conv_string(
    #    self, model: type, prop: ColumnProperty, kwargs: Dict[str, Any]
    # ) -> UnboundField:
    #    extra_validators = self._string_common(prop)
    #    kwargs.setdefault("validators", [])
    #    kwargs["validators"].extend(extra_validators)
    #    return StringField(**kwargs)
