from typing import Union, Optional

from pydantic import BaseModel


class PerceptorRequest(BaseModel):
    flavor: str = 'original'
    params: dict = {}


class InstructionError(BaseModel):
    """
    Information on error occurred during instruction's processing.
    """
    error_text: str


InstructionResult = Union[Optional[str], InstructionError]

InstructionWithResult = tuple[str, InstructionResult]
