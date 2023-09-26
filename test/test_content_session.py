import unittest

from perceptor_client_lib.content_session import _ContentSession, process_contents
from perceptor_client_lib.external_models import PerceptorRequest, InstructionError, InstructionResult
from perceptor_client_lib.internal_models import PerceptorRepositoryRequest, TextContextData, InstructionContextData, \
    ImageContextData, InstructionMethod
from perceptor_client_lib.perceptor_repository import _PerceptorRepository


class RepositoryMock(_PerceptorRepository):
    def __init__(self, error_response: str = None):
        self._error_response = error_response

    def send_instruction(self, request: PerceptorRepositoryRequest, instruction: str) -> InstructionResult:
        if self._error_response is None:
            return f"{instruction}  :: ok"
        return InstructionError(error_text=self._error_response)


mock_repository = RepositoryMock()


class ContentSessionTests(unittest.TestCase):
    def test_all_instructions_are_processed(self):
        content_session = _ContentSession(mock_repository,
                                          TextContextData("some_text"))

        instructions = [
            "1",
            "2",
            "3"
        ]
        result = content_session.process_instructions_request(request=PerceptorRequest(flavor="flavour", params={}),
                                                              method=InstructionMethod.QUESTION,
                                                              instructions=instructions,
                                                              max_number_of_threads=4)

        self.assertEqual(len(result), len(instructions))

        def get_instruction_from_tuple(t: tuple[str, str]) -> str:
            first, _ = t
            return first

        self.assertListEqual(list(map(get_instruction_from_tuple, result)),
                             instructions
                             )

    def test_all_contents_are_processed_with_all_instructions(self):
        data_contexts: list[InstructionContextData] = [
            ImageContextData(data_uri="some_uri_1"),
            ImageContextData(data_uri="some_uri_2"),
            ImageContextData(data_uri="some_uri_3"),
        ]
        instructions: list[str] = [
            "1",
            "2",
            "3"
        ]

        result = process_contents(mock_repository,
                                  data_contexts,
                                  PerceptorRequest(flavor="flavour", params={}),
                                  InstructionMethod.QUESTION,
                                  instructions,
                                  max_number_of_threads= 4
                                  )

        self.assertEqual(len(result), len(data_contexts))
        for r in result:
            self.assertEqual(len(r), len(instructions))

    def test_WHEN_repository_returns_error_THEN_error_in_response(self):
        repository = RepositoryMock(error_response='some error')
        content_session = _ContentSession(repository,
                                          TextContextData("some_text"))
        instructions = [
            "1",
            "2",
            "3"
        ]
        result = content_session.process_instructions_request(request=PerceptorRequest(flavor="flavour", params={}),
                                                              method=InstructionMethod.QUESTION,
                                                              instructions=instructions,
                                                              max_number_of_threads=4)

        self.assertEqual(len(result), len(instructions))
        for item in result:
            _, resp = item
            self.assertTrue(isinstance(resp, InstructionError), f"type is {type(resp).__name__}")


if __name__ == '__main__':
    unittest.main()
