from typing import Annotated, Sequence

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.classifiers import crud
from app.api.v1.classifiers.schemas import ReadTaskStatus
from app.db import db_helper
from app.db.models import TaskStatus

router = APIRouter(tags=["classifiers"])


@router.get("/task_status/", response_model=Sequence[ReadTaskStatus])
async def get_list_task_status(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> Sequence[TaskStatus]:
    """Получение содержимого классификатора статусов задач."""
    return await crud.get_list_task_status_repo(session)
