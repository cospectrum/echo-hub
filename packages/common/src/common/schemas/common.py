from pydantic import UUID4, BaseModel


TraceId = UUID4

TaskId = UUID4


class BaseTask(BaseModel):
    id: TaskId
    trace_id: TraceId
