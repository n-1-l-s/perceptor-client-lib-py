from enum import Enum

from pydantic import BaseModel


class InstructionMethod(Enum):
    QUESTION = 1
    TABLE = 2


class InstructionContextData(BaseModel):
    context_type: str
    content: str


class ImageContextData(InstructionContextData):
    def __init__(self, data_uri: str):
        super().__init__(context_type="image", content=data_uri)


class TextContextData(InstructionContextData):
    def __init__(self, text_to_process: str):
        super().__init__(context_type="text", content=text_to_process)


class PerceptorRepositoryRequest(BaseModel):
    flavor: str
    params: dict
    context_data: InstructionContextData
    method: InstructionMethod = InstructionMethod.QUESTION
