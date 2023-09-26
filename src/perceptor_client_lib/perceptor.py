from io import BufferedReader
from typing import Union, Optional

import perceptor_client_lib.perceptor_repository
from perceptor_client_lib.content_session import process_contents
from perceptor_client_lib.external_models import PerceptorRequest, InstructionWithResult
from perceptor_client_lib.image_parsing import convert_image_to_contextdata
from perceptor_client_lib.internal_models import *
from perceptor_client_lib.pdf_parsing import get_images_from_document_pages
from perceptor_client_lib.perceptor_repository import _PerceptorRepositoryHttpClient, \
    PerceptorRepositoryHttpClientSettings


class Client:
    """
    TamedAI client for the api.
    """
    def __init__(self, api_key: str,
                 request_url: str = 'https://perceptor-api.tamed.ai/1/model/',
                 wait_timeout: int = 60,
                 max_level_of_parallelization: int = 10):
        """
        Creates Client instance
        :param api_key: api key to use.
        :param request_url: request url.
        :param wait_timeout: timeout for request (in seconds), default is 60s
        """
        self._repository: perceptor_client_lib.perceptor_repository._PerceptorRepository = _PerceptorRepositoryHttpClient(
            PerceptorRepositoryHttpClientSettings(
                api_key=api_key,
                request_url=request_url,
                wait_timeout=wait_timeout
            ))
        self._max_level_of_parallelization = max_level_of_parallelization

    def ask_text(self, text_to_process: str,
                 instructions: list[str], request_parameters: PerceptorRequest = PerceptorRequest()) \
            -> list[InstructionWithResult]:
        """
        Sends instruction(s) for the specified text
        :param text_to_process: text to be processed.
        :param instructions: instruction(s) to perform on text.
        :param request_parameters: (optional) refined request parameters.
        :return: list of tuples containing instruction and InstructionResult.
                InstructionResult can be either text or instance of InstructionError.
        """
        return process_contents(self._repository,
                                TextContextData(text_to_process),
                                request_parameters,
                                InstructionMethod.QUESTION,
                                instructions,
                                self._max_level_of_parallelization
                                )

    def ask_image(self, image: Union[str, bytes, BufferedReader],
                  instructions: list[str],
                  request_parameters: PerceptorRequest = PerceptorRequest(),
                  file_type: Optional[str] = None) -> list[InstructionWithResult]:
        """
        Sends instruction(s) for the specified image
        :param image: image to be processed. Either a path to file, opened file handle, or bytearray.
        :param instructions: instruction(s) to perform on the image.
        :param request_parameters: (optional) refined request parameters.
        :param file_type: mandatory if image specified as handle or bytearray, must be either 'png' or 'jpg'.
        :return: list of tuples containing instruction and InstructionResult.
                InstructionResult can be either text or instance of InstructionError.
        """
        image_content_data = convert_image_to_contextdata(image, file_type=file_type)
        return process_contents(self._repository,
                                image_content_data,
                                request_parameters,
                                InstructionMethod.QUESTION,
                                instructions,
                                self._max_level_of_parallelization
                                )

    def ask_table_from_image(self, image: Union[str, bytes, BufferedReader],
                             instruction: str,
                             request_parameters: PerceptorRequest = PerceptorRequest(),
                             file_type: Optional[str] = None
                             ) -> InstructionWithResult:
        """
        Sends a table instruction for the specified image.
        :param image: image to be processed. Either a path to file, opened file handle, or bytearray
        :param instruction: instruction to perform, for example 'GENERATE TABLE Article, Amount, Value GUIDED BY Value'
        :param request_parameters: (optional) refined request parameters.
        :param file_type: mandatory if image specified as handle or bytearray, must be either 'png' or 'jpg'.
        :return: tuple containing original instruction and InstructionResult.
                InstructionResult can be either text or instance of InstructionError.
        """
        image_content_data = convert_image_to_contextdata(image, file_type=file_type)
        return process_contents(self._repository,
                                image_content_data,
                                request_parameters,
                                InstructionMethod.TABLE,
                                instruction,
                                self._max_level_of_parallelization
                                )

    def ask_document(self, pdf_doc: Union[str, bytes, BufferedReader],
                     instructions: list[str],
                     request_parameters: PerceptorRequest = PerceptorRequest()) \
            -> list[list[InstructionWithResult]]:
        """
        Sends instruction(s) for the specified pdf document.
        :param pdf_doc: document to be processed. Either a path to file, opened file handle, or bytearray
        :param instructions: instruction(s) to perform on the document.
        :param request_parameters: (optional) refined request parameters.
        :return: list (corresponding to document pages), with list of tuples containing
            instruction and InstructionResult. InstructionResult can be either text or instance of InstructionError.
        """

        return self._process_images_from_document(pdf_doc, instructions, InstructionMethod.QUESTION, request_parameters)

    def ask_table_from_document(self, pdf_doc: Union[str, bytes, BufferedReader],
                                instruction: str,
                                request_parameters: PerceptorRequest = PerceptorRequest()) -> list[InstructionWithResult]:
        """
        Sends a table instruction for the specified document.
        :param pdf_doc: document to be processed. Either a path to file, opened file handle, or bytearr
        :param instruction: instruction to perform, for example 'GENERATE TABLE Article, Amount, Value GUIDED BY Value'
        :param request_parameters: (optional) refined request parameters.
        :return: list (corresponding to document pages), wish tuples containing original
            instruction and InstructionResult. InstructionResult can be either text or instance of InstructionError.
        """
        return self._process_images_from_document(pdf_doc, instruction, InstructionMethod.TABLE, request_parameters)

    def _process_images_from_document(self, pdf_doc: Union[str, bytes, BufferedReader],
                                      instruction: Union[str, list[str]],
                                      method: InstructionMethod,
                                      request_parameters) \
            -> Union[list[InstructionWithResult], list[list[InstructionWithResult]]]:
        images = get_images_from_document_pages(pdf_doc)
        mapped_images = list(map(lambda i: convert_image_to_contextdata(i, file_type="png"), images))

        return process_contents(self._repository,
                                mapped_images,
                                request_parameters,
                                method,
                                instruction,
                                self._max_level_of_parallelization
                                )
