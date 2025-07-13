from functools import reduce
from typing import Any, Generic, Type, TypeVar, Union

from sqlalchemy import Select, func
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from configs.database import ModelType
from exceptions.app_exception import ResourceNotFound

T = TypeVar("T", bound=DeclarativeMeta)


class BaseRepository(Generic[ModelType]):
    """Base class for data repositories."""

    model: Type[ModelType]

    def __init__(self, db_session: Session):
        """
        Initialize the repository with a database session.

        Args:
            db_session: SQLAlchemy session
        """
        self.session = db_session
        self.db = db_session

    def create(self, attributes: dict[str, Any] = None) -> ModelType:
        """
        Creates the model instance.

        :param attributes: The attributes to create the model with.
        :return: The created model instance.
        """
        if attributes is None:
            attributes = {}

        try:
            model = self.model(**attributes)
            self.session.add(model)
            self.session.flush()
            return model
        except Exception:
            self.session.rollback()
            raise

    def update(
        self,
        entity_id: Union[int, str],
        data: dict[str, Any],
        join_: set[str] | None = None,
        id_key: str = "id",
    ) -> ModelType:
        try:
            model_instance = self.get_by_id(entity_id, join_, id_key)

            if not model_instance:
                raise ResourceNotFound()

            for attr, value in data.items():
                setattr(model_instance, attr, value)

            return model_instance
        except Exception as e:
            if not isinstance(e, ResourceNotFound):
                self.session.rollback()
            raise

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        join_: set[str] | None = None,
        sort_by: str | None = None,
        sort_desc: bool = False,
    ) -> list[ModelType]:
        """
        Returns a list of model instances.

        :param skip: The number of records to skip.
        :param limit: The number of record to return.
        :param join_: The joins to make.
        :param sort_by: The field name to sort by. If None, no sorting is applied.
        :param sort_desc: If True, sort in descending order. If False, sort in ascending order.
        :return: A list of model instances.
        """
        query = self._query(join_)

        # Apply sorting if sort_by is provided
        if sort_by is not None:
            sort_column = getattr(self.model, sort_by, None)
            if sort_column is not None:
                if sort_desc:
                    query = query.order_by(sort_column.desc())
                else:
                    query = query.order_by(sort_column.asc())

        query = query.offset(skip).limit(limit)

        if join_ is not None:
            return self.all_unique(query)

        return self._all(query)

    def get_by_muti_fields(
        self,
        conditions: list,
        join_: set[str] | None = None,
    ) -> ModelType:
        """
        Returns the model instance matching the field and value.

        :param conditions: List of condition.
        :param join_: The joins to make.
        :return: The model instance.
        """
        query = self._query(join_)
        query = self._get_by_muti_fields(query, conditions)

        if join_ is not None:
            return self.all_unique(query)
        return self._one(query)

    def get_all_by_muti_fields(
        self,
        conditions: list,
        join_: set[str] | None = None,
    ) -> list[ModelType]:
        """
        Returns a list of model instances matching the provided conditions.

        :param conditions: List of conditions.
        :param join_: The joins to make.
        :return: A list of model instances.
        """
        query = self._query(join_)
        query = self._get_by_muti_fields(query, conditions)

        return self._all(query)

    def get_by(
        self,
        field: str,
        value: Any,
        join_: set[str] | None = None,
        unique: bool = False,
    ) -> ModelType | list[ModelType]:
        """
        Returns the model instance matching the field and value.

        :param field: The field to match.
        :param value: The value to match.
        :param join_: The joins to make.
        :return: The model instance.
        """
        query = self._query(join_)
        query = self._get_by(query, field, value)

        if join_ is not None:
            return self.all_unique(query)
        if unique:
            return self._one_or_none(query)

        return self._all(query)

    def get_by_id(
        self, value: Any, join_: set[str] | None = None, id_key="id"
    ) -> ModelType:
        """
        Returns the model instance matching the field and value.

        :param value: The value to match.
        :param join_: The joins to make.
        :param id_key: The id field name.
        :return: The model instance.
        """
        query = self._query(join_)
        query = self._get_by(query, id_key, value)

        if join_ is not None:
            return self.all_unique(query)
        return self._one_or_none(query)

    def delete(self, entity: ModelType) -> None:
        """
        Deletes the entity.

        :param entity: The entity to delete.
        :return: None
        """
        try:
            self.session.delete(entity)
        except Exception:
            self.session.rollback()
            raise

    def delete_by_id(self, id: int | str, id_key="id") -> None:
        """
        Deletes the entity by ID.

        :param id: The ID of the entity to delete.
        :param id_key: The id field name.
        :return: None
        """
        try:
            entity = self.get_by_id(id, id_key=id_key)

            self.session.delete(entity)
        except Exception:
            self.session.rollback()
            raise

    def _query(
        self,
        join_: set[str] | None = None,
        order_: dict | None = None,
    ) -> Select:
        """
        Returns a callable that can be used to query the model.

        :param join_: The joins to make.
        :param order_: The order of the results. (e.g desc, asc)
        :return: A callable that can be used to query the model.
        """
        query = select(self.model)  # pragma: no cover
        query = self._maybe_join(query, join_)  # pragma: no cover
        query = self._maybe_ordered(query, order_)  # pragma: no cover

        return query  # pragma: no cover

    def _all(self, query: Select) -> list[ModelType]:
        """
        Returns all results from the query.

        :param query: The query to execute.
        :return: A list of model instances.
        """
        query = self.session.scalars(query)
        return query.all()

    def _all_unique(self, query: Select) -> list[ModelType]:
        result = self.session.execute(query)
        return result.unique().scalars().all()

    def _first(self, query: Select) -> ModelType | None:
        """
        Returns the first result from the query.

        :param query: The query to execute.
        :return: The first model instance.
        """
        query = self.session.scalars(query)
        return query.first()

    def _one_or_none(self, query: Select) -> ModelType | None:
        """Returns the first result from the query or None."""
        query = self.session.scalars(query)
        return query.one_or_none()

    def _one(self, query: Select) -> ModelType:
        """
        Returns the first result from the query or raises NoResultFound.

        :param query: The query to execute.
        :return: The first model instance.
        """
        query = self.session.scalars(query)
        return query.one()

    def _count(self, query: Select) -> int:
        """
        Returns the count of the records.

        :param query: The query to execute.
        """
        query = query.subquery()  # pragma: no cover
        query = self.session.scalars(
            select(func.count()).select_from(query)
        )  # pragma: no cover
        return query.one()  # pragma: no cover

    def _sort_by(
        self,
        query: Select,
        sort_by: str,
        order: str | None = "asc",
        case_insensitive: bool = False,
    ) -> Select:
        """
        Returns the query sorted by the given column.

        :param query: The query to sort.
        :param sort_by: The column to sort by.
        :param order: The order to sort by.
        :param model: The model to sort.
        :param case_insensitive: Whether to sort case insensitively.
        :return: The sorted query.
        """

        order_column = None

        if case_insensitive:
            order_column = func.lower(getattr(self.model, sort_by))  # pragma: no cover
        else:
            order_column = getattr(self.model, sort_by)

        if order == "desc":
            return query.order_by(order_column.desc())  # pragma: no cover

        return query.order_by(order_column.asc())

    def _get_by(self, query: Select, field: str, value: Any) -> Select:
        """
        Returns the query filtered by the given column.

        :param query: The query to filter.
        :param field: The column to filter by.
        :param value: The value to filter by.
        :return: The filtered query.
        """
        return query.where(getattr(self.model, field) == value)

    def _get_by_muti_fields(self, query: Select, conditions: list) -> Select:
        """
        Returns the query filtered by the given column.

        :param query: The query to filter.
        :param conditions: list of conditions
        :return: The filtered query.
        """
        return query.filter(*conditions)

    def _maybe_join(self, query: Select, join_: set[str] | None = None) -> Select:
        """
        Returns the query with the given joins.

        :param query: The query to join.
        :param join_: The joins to make.
        :return: The query with the given joins.
        """
        if not join_:
            return query

        if not isinstance(join_, set):
            raise TypeError("join_ must be a set")

        return reduce(self._add_join_to_query, join_, query)

    def _maybe_ordered(self, query: Select, order_: dict | None = None) -> Select:
        """
        Returns the query ordered by the given column.

        :param query: The query to order.
        :param order_: The order to make.
        :return: The query ordered by the given column.
        """
        if order_:
            if order_["asc"]:
                for order in order_["asc"]:
                    query = query.order_by(getattr(self.model, order).asc())
            else:
                for order in order_["desc"]:
                    query = query.order_by(getattr(self.model, order).desc())

        return query

    def _add_join_to_query(self, query: Select, join_: set[str]) -> Select:
        """
        Returns the query with the given join.

        :param query: The query to join.
        :param join_: The join to make.
        :return: The query with the given join.
        """
        return getattr(self, "_join_" + join_)(query)  # pragma: no cover
