from pydantic import BaseModel, Field, TypeAdapter, ValidationError
from typing import Annotated, Union
from .utils.reflection import get_all_subclasses


class BaseEnvironment(BaseModel):
    kind: str

    @staticmethod
    def create_from_dict(d: dict) -> "BaseEnvironment":
        EnvironmentType = Annotated[Union[*get_all_subclasses(BaseEnvironment)], Field(discriminator="kind")]
        adapter = TypeAdapter(EnvironmentType)
        try:
            o = adapter.validate_python(d)
        except ValidationError as e:
            invalid_types = [err["ctx"]["tag"] for err in e.errors() if err["type"] == "union_tag_invalid"]
            if len(invalid_types) > 0:
                raise Exception(f"These kinds of environments are not registered: {invalid_types}")
            else:
                raise
        return o
