import pytest
from app.services.update_task_service import update_task_service
from app.models.task import Task
from app.schemas.task_update import TaskUpdateSchema

class MockSession:
    def __init__(self):
        self.updated_task = None

    async def execute(self, query):
        self.updated_task = Task(
            task_id=1,
            user_id=1,
            title="Updated Task",
            description="Updated Description",
            due_date="2023-12-31",
            status="completed",
            created_at="2023-08-01T00:00:00",
            created_by="Alice",
            updated_at="2023-08-02T00:00:00",
            updated_by="Bob",
        )
        return self.updated_task

@pytest.fixture
def mock_db_session():
    return MockSession()

def test_update_task_service(mock_db_session):
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "due_date": "2023-12-31",
        "status": "completed",
    }
    task_update_schema = TaskUpdateSchema(**update_data)

    is_success, updated_task = update_task_service(mock_db_session, task_update_schema)

    assert is_success is True
    assert updated_task.task_id == 1
    assert updated_task.title == "Updated Task"
    assert updated_task.status == "completed"

    assert mock_db_session.updated_task is not None
    assert mock_db_session.updated_task.title == "Updated Task"
    assert mock_db_session.updated_task.status == "completed"

