from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, Boolean, desc
from sqlalchemy.sql import expression as sql

from config.db import Base
from schemas.task_history_search_by_criteria import TaskHistorySearchByCriteriaSchema


class TaskHistory(Base):
    __tablename__ = "task_history"
    task_history_id = Column(String, primary_key=True)
    task_id = Column(String)
    action_type = Column(String, default=None)
    user_id = Column(String, default=None)
    title = Column(String, default=None)
    description = Column(String, default=None)
    due_date = Column(DateTime, index=True, default=None)
    status = Column(String, default=None)
    created_at = Column(DateTime, index=True, default=None)
    created_by = Column(String, default=None)
    updated_at = Column(DateTime, index=True, default=None)
    updated_by = Column(String, default=None)
    logged_at = Column(DateTime, index=True, default=None)
    is_archived = Column(Boolean, default=False)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"task_history_id={self.task_history_id}, "
            f"task_id={self.task_id}, "
            f"action_type={self.task_id}, "
            f"user_id={self.user_id}, "
            f"title={self.title}, "
            f"description={self.description}, "
            f"due_date={self.due_date}, "
            f"status={self.status}, "
            f"created_at={self.created_at}, "
            f"created_by={self.created_by}, "
            f"updated_at={self.updated_at}, "
            f"updated_by={self.updated_by}, "
            f"logged_at={self.updated_at}, "
            f"is_archived={self.updated_by}, "
            f")>"
        )

    @classmethod
    async def create(cls, db, task_id, action_type, **kwargs) -> "TaskHistory":
        query = (
            sql.insert(cls)
            .values(task_history_id=str(uuid4()), task_id=task_id, action_type=action_type, logged_at=datetime.utcnow(), **kwargs)
            .returning(cls.task_id)
        )
        tasks = await db.execute(query)
        await db.commit()
        return tasks.first()

    async def update(cls, db, task_history_id, **kwargs) -> "TaskHistory":
        query = (
            sql.update(cls)
            .where(cls.task_history_id == task_history_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(cls.task_id, cls.user_id, cls.title, cls.description, cls.due_date, cls.status, cls.created_at, cls.created_by, cls.updated_at, cls.updated_by)
        )
        tasks = await db.execute(query)
        await db.commit()
        return tasks.first()

    @classmethod
    async def get(cls, db, criteria: TaskHistorySearchByCriteriaSchema) -> list["TaskHistory"]:
        query = sql.select(cls)
        query = _filter_by_criteria(cls, query, criteria)
        query = query.order_by(desc(cls.logged_at)).limit(10)
        tasks = await db.execute(query)
        tasks = tasks.scalars().all()
        return tasks

    @classmethod
    async def get_all(cls, db) -> list["TaskHistory"]:
        query = sql.select(cls)
        query = query.order_by(desc(cls.logged_at))
        tasks = await db.execute(query)
        tasks = tasks.scalars().all()
        return tasks

    @classmethod
    async def delete(cls, db, task_id) -> bool:
        query = (
            sql.delete(cls)
            .where(cls.task_id == task_id)
            .returning(
                cls.task_id,
                cls.title,
            )
        )
        await db.execute(query)
        await db.commit()
        return True


def _filter_by_criteria(cls, query, criteria: TaskHistorySearchByCriteriaSchema):
    if criteria.task_id:
        query = query.filter(cls.task_id == criteria.task_id)
    if criteria.title:
        query = query.filter(cls.title == criteria.title)
    if criteria.user_id:
        query = query.filter(cls.user_id == criteria.user_id)
    if criteria.due_date:
        query = query.filter(cls.due_date == criteria.title)
    if criteria.status:
        query = query.filter(cls.status == criteria.status)
    if criteria.created_by:
        query = query.filter(cls.created_by == criteria.created_by)
    if criteria.updated_by:
        query = query.filter(cls.updated_by == criteria.updated_by)
    if criteria.action_type:
        query = query.filter(cls.action_type == criteria.action_type)
    if criteria.logged_at:
        query = query.filter(cls.logged_at == criteria.logged_at)
    if criteria.is_archived:
        query = query.filter(cls.is_archived == criteria.is_archived)
    return query
