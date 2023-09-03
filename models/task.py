from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import expression as sql

from config.db import Base


class Task(Base):
    __tablename__ = "task"
    task_id = Column(String, primary_key=True)
    user_id = Column(String, default=None)
    title = Column(String, default=None)
    description = Column(String, default=None)
    due_date = Column(DateTime, index=True, default=None)
    status = Column(String, default=None)
    created_at = Column(DateTime, index=True, default=None)
    created_by = Column(String, default=None)
    updated_at = Column(DateTime, index=True, default=None)
    updated_by = Column(String, default=None)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"task_id={self.task_id}, "
            f"user_id={self.user_id}, "
            f"title={self.title}, "
            f"description={self.description}, "
            f"due_date={self.due_date}, "
            f"status={self.status}, "
            f"created_at={self.created_at}, "
            f"created_by={self.created_by}, "
            f"updated_at={self.updated_at}, "
            f"updated_by={self.updated_by}, "
            f")>"
        )

    @classmethod
    async def create(cls, db, **kwargs) -> "Task":
        query = (
            sql.insert(cls)
            .values(task_id=str(uuid4()), created_at=datetime.utcnow(), updated_by=kwargs['created_by'], updated_at=datetime.utcnow(), **kwargs)
            .returning(cls.task_id, cls.title)
        )
        users = await db.execute(query)
        await db.commit()
        return users.first()

    @classmethod
    async def update(cls, db, task_id, **kwargs) -> "Task":
        query = (
            sql.update(cls)
            .where(cls.task_id == task_id)
            .values(updated_at=datetime.utcnow(), **kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(cls.task_id, cls.user_id, cls.title, cls.description, cls.due_date, cls.status, cls.created_at, cls.created_by, cls.updated_at, cls.updated_by)
        )
        users = await db.execute(query)
        await db.commit()
        return users.first()

    @classmethod
    async def get(cls, db, **kwargs) -> "Task":
        query = sql.select(cls).where(**kwargs)
        users = await db.execute(query)
        (user,) = users.first()
        return user

    @classmethod
    async def get_all(cls, db) -> list["Task"]:
        query = sql.select(cls)
        users = await db.execute(query)
        users = users.scalars().all()
        return users

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
