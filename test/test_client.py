import os
import unittest

from perceptor_client_lib.external_models import InstructionResult
from perceptor_client_lib.internal_models import PerceptorRepositoryRequest
from perceptor_client_lib.perceptor import Client
from perceptor_client_lib.perceptor_repository import _PerceptorRepository

_image_path = os.path.join(os.path.dirname(__file__), "test_files", "binary_file.png")
_pdf_path = os.path.join(os.path.dirname(__file__), "test_files", "pdf_with_2_pages.pdf")


class RepositoryMock(_PerceptorRepository):
    def send_instruction(self, request: PerceptorRepositoryRequest, instruction: str) -> InstructionResult:
        return f"{instruction}  :: ok"


def _create_client_with_mock_repository():
    client = Client("api_key")
    client._repository = RepositoryMock()
    return client


_client_with_mock_repository = _create_client_with_mock_repository()


class ClientMethodsTest(unittest.TestCase):

    def test_ask_image_from_file(self):
        instructions = ["1", "2"]
        result = _client_with_mock_repository.ask_image(_image_path, instructions=instructions)
        self.assertEqual(len(result), len(instructions))

    def test_ask_image_from_file_reader(self):
        instructions = ["1", "2"]

        reader = open(_image_path, 'rb')
        with reader:
            result = _client_with_mock_repository.ask_image(reader, file_type="png", instructions=instructions)
            self.assertEqual(len(result), len(instructions))

    def test_ask_table_from_image_file(self):
        instruction = "instruction query text"
        _, result = _client_with_mock_repository.ask_table_from_image(_image_path, instruction=instruction)
        self.assertEqual(f"{instruction}  :: ok", result)

    def test_ask_document_from_file(self):
        instructions = ["1", "2"]
        result = _client_with_mock_repository.ask_document(_pdf_path, instructions=instructions)
        self.assertEqual(len(result), len(instructions))

    def test_ask_table_from_document_file(self):
        instruction = "instruction query text"
        results = _client_with_mock_repository.ask_table_from_document(_pdf_path, instruction=instruction)
        self.assertEqual(len(results), 2)
        for r in results:
            _, single_result = r
            self.assertEqual(f"{instruction}  :: ok", single_result)


if __name__ == '__main__':
    unittest.main()
