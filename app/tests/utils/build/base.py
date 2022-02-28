from typing import Any, Generic, List, Optional, TypeVar

from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


from pydantic_factories import ModelFactory


class BUILDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: ModelType = None,
        create_schema: Optional[CreateSchemaType] = None,
        update_schema: Optional[UpdateSchemaType] = None,
    ):
        self.model = model
        self.create_model = create_schema
        self.update_model = update_schema
        self.objects = []

    def build_object(self, size: int = 1) -> ModelType | List[ModelType]:
        object_Factory = ModelFactory.create_factory(self.model)
        # Return object if list size is 1
        if size == 1:
            return object_Factory.build()
        # Return list of objects if list size is greater than 1
        return object_Factory.batch(size=size)

    def build_create_object(
        self, size: int = 1
    ) -> CreateSchemaType | List[CreateSchemaType]:
        object_Factory = ModelFactory.create_factory(self.create_model)
        # Return object if list size is 1
        if size == 1:
            return object_Factory.build()
        # Return list of objects if list size is greater than 1
        return object_Factory.batch(size=size)

    def build_update_object(
        self, size: int = 1
    ) -> UpdateSchemaType | List[UpdateSchemaType]:
        object_Factory = ModelFactory.create_factory(self.update_model)
        # Return object if list size is 1
        if size == 1:
            return object_Factory.build()
        # Return list of objects if list size is greater than 1
        return object_Factory.batch(size=size)
