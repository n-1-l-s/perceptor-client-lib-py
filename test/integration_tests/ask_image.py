import logging

from perceptor_client_lib.external_models import PerceptorRequest
from tests_commons import create_client

logging.basicConfig(level=logging.DEBUG)

IMAGE_PATH = "../test_files/invoice.jpg"

perceptor_client = create_client()

req: PerceptorRequest = PerceptorRequest(params={
    "temperature": 0.01,
    "topK": 10,
    "topP": 0.9,
    "repetitionPenalty": 1,
    "lengthPenalty": 1,
    "penaltyAlpha": 1,
    "maxLength": 512
})

result = perceptor_client.ask_image(IMAGE_PATH,
                                    instructions=[
                                        "What is the invoice number?",
                                        "What is the invoice date?",
                                    ],
                                    request_parameters=req
                                    )

print(result)

