from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import expression as sql

from config.db import Base


class Task(Base):
    __tablename__ = "task"
    task_id = Column(String, primary_key=True)
    user_id = Column(String)
    title = Column(String)
    description = Column(String)
    due_date = Column(DateTime, index=True)
    status = Column(String)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    created_by = Column(String)
    updated_at = Column(DateTime, index=True, default=datetime.utcnow)
    updated_by = Column(String)

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
            .values(id=str(uuid4()), **kwargs)
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
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(cls.task_id, cls.title)
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
