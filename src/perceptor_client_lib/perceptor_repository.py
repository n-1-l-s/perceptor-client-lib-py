import json
from json import JSONDecodeError

import requests
import sseclient
from pydantic import BaseModel
from requests import Response

from perceptor_client_lib.external_models import InstructionResult, InstructionError
from perceptor_client_lib.internal_models import PerceptorRepositoryRequest, InstructionMethod


class PerceptorRepositoryHttpClientSettings(BaseModel):
    api_key: str
    request_url: str
    wait_timeout: int


class _PerceptorRepository:
    def send_instruction(self, request: PerceptorRepositoryRequest, instruction: str) -> InstructionResult:
        raise Exception("not implemented, must override")


class _PerceptorRepositoryHttpClient(_PerceptorRepository):

    def __init__(self, settings: PerceptorRepositoryHttpClientSettings):
        self._settings: PerceptorRepositoryHttpClientSettings = settings
        self._headers: dict[str, str] = {
            'Accept': 'text/event-stream',
            'Authorization': 'Bearer ' + self._settings.api_key
        }

    @staticmethod
    def _fiter_events(event: sseclient.Event) -> bool:
        return event.event == 'finished'

    def _create_body(self, request: PerceptorRepositoryRequest, instruction: str) -> dict:
        return {
            "flavor": request.flavor,
            "contextType": request.context_data.context_type,
            "context": request.context_data.content,
            "params": request.params,
            "waitTimeout": self._settings.wait_timeout,
            "instruction": instruction
        }

    def _map_successful_response(self, request_response: Response) -> InstructionResult:
        with request_response:
            if len(request_response.content) == 0:
                event_list = []
            else:
                client = sseclient.SSEClient(request_response)
                client_events = client.events()
                event_list = list(filter(self._fiter_events, client_events))

        if len(event_list) > 0:
            return event_list[0].data

        return None

    @staticmethod
    def _parse_bad_response_text(request_response: Response) -> InstructionError:
        try:
            parsed_json = json.loads(request_response.text)
            return InstructionError(error_text=parsed_json['detail'])
        except JSONDecodeError:
            return InstructionError(error_text=request_response.text)

    def send_instruction(self, request: PerceptorRepositoryRequest, instruction: str) -> InstructionResult:

        body = self._create_body(request, instruction)

        def resolve_method():
            if request.method == InstructionMethod.TABLE:
                return 'generate_table'
            return 'generate'

        request_url = f"{self._settings.request_url}{resolve_method()}"

        request_response: Response = requests.post(request_url,
                                                   stream=True,
                                                   headers=self._headers,
                                                   json=body)

        with request_response:
            if request_response.status_code == 200:
                return self._map_successful_response(request_response)

            if request_response.status_code == 403:
                return InstructionError(error_text="invalid api_key")

            if request_response.status_code == 400:
                return self._parse_bad_response_text(request_response)

            return InstructionError(error_text=str(request_response.content))
