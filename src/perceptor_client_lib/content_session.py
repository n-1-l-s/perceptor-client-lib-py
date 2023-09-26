import logging
from typing import Union
from multiprocessing.pool import ThreadPool

from perceptor_client_lib.external_models import PerceptorRequest, InstructionResult, InstructionError, \
    InstructionWithResult
from perceptor_client_lib.internal_models import InstructionContextData, PerceptorRepositoryRequest, InstructionMethod
from perceptor_client_lib.perceptor_repository import _PerceptorRepository


class _ContentSession:

    def __init__(self, repository: _PerceptorRepository, context_data: InstructionContextData):
        self._repository: _PerceptorRepository = repository
        self._logger = logging.getLogger(self.__class__.__name__)
        self._context_data: InstructionContextData = context_data

    def process_instructions_request(self, request: PerceptorRequest,
                                     method: InstructionMethod,
                                     instructions: Union[str,list[str]],
                                     max_number_of_threads: int) -> list[tuple[str, InstructionResult]]:
        if len(instructions) == 0:
            return []

        def send_single_instruction(instruction: str) -> tuple[str, str]:
            response = self._process_instruction(request, method, instruction)
            return instruction, response

        if isinstance(instructions, str):
            return send_single_instruction(instructions)

        with ThreadPool(min(len(instructions), max_number_of_threads)) as thread_pool:
            results = thread_pool.map(send_single_instruction, instructions)

        return results

    def _process_instruction(self, request: PerceptorRequest, method: InstructionMethod,
                             instruction: str) -> InstructionResult:
        self._logger.debug("processing instruction: %s", dict(instruction=instruction, req=request))

        req: PerceptorRepositoryRequest = PerceptorRepositoryRequest(
            params=request.params, flavor=request.flavor, context_data=self._context_data,
            method=method
        )

        try:
            result = self._repository.send_instruction(req, instruction)
            return result
        except Exception as exc:
            self._logger.error(exc)
            return InstructionError(error_text=str(exc))


def process_contents(repository: _PerceptorRepository,
                     data_context: Union[InstructionContextData, list[InstructionContextData]],
                     request: PerceptorRequest,
                     method: InstructionMethod,
                     instructions: Union[str, list[str]],
                     max_number_of_threads: int
                     ) -> Union[InstructionWithResult, list[InstructionWithResult], list[list[InstructionWithResult]]]:

    if isinstance(data_context, InstructionContextData):
        session = _ContentSession(repository, data_context)
        return session.process_instructions_request(request, method, instructions,max_number_of_threads)

    if not isinstance(data_context, list):
        raise Exception('data_context must be either InstructionContextData or list[InstructionContextData]')

    if len(data_context) == 0:
        return []

    multiple_contexts: list[InstructionContextData] = data_context

    def process_data_context(ctx: InstructionContextData):
        single_session = _ContentSession(repository, ctx)
        return single_session.process_instructions_request(request, method, instructions, max_number_of_threads)

    with ThreadPool(len(multiple_contexts)) as thread_pool:
        results = thread_pool.map(process_data_context, multiple_contexts)

    return results
