from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile

from common.schemas import (
    TaskId,
    TraceId,
)
from common import asr

from asr_api.services.queue_mode_transcriber import QueueModeTranscriber
from asr_api import dependencies as deps


router = APIRouter()

ServiceDep = Annotated[QueueModeTranscriber, Depends(QueueModeTranscriber)]


@router.post("/transcribe/task")
async def post_transcribe_task(
    service: ServiceDep,
    trace_id: Annotated[TraceId, Depends(deps.get_trace_id)],
    audio: UploadFile,
    options: asr.TranscribeOptions | None = None,
) -> TaskId:
    return await service.post_task(audio, options, trace_id=trace_id)


@router.get("/transcribe/task")
async def get_transcribe_task(
    service: ServiceDep, task_id: TaskId
) -> asr.TranscribeResult | None:
    return await service.get_task_result(task_id)
