import logging

from perceptor_client_lib.external_models import PerceptorRequest
from tests_commons import create_client

logging.basicConfig(level=logging.DEBUG)

IMAGE_PATH = "../test_files/image_with_invoice_table.png"

perceptor_client = create_client()

req: PerceptorRequest = PerceptorRequest(flavor='default',
                                         params={
                                             "temperature": 0.5,
                                             "topK": 10,
                                             "topP": 0.9,
                                             "repetitionPenalty": 1,
                                             "lengthPenalty": 1,
                                             "penaltyAlpha": 1,
                                             "maxLength": 512
                                         })

result = perceptor_client.ask_table_from_image(IMAGE_PATH,
                                               instruction=
                                               "GENERATE TABLE Artikelnummer, Beschreibung, Betrag GUIDED BY Betrag",
                                               request_parameters=req
                                               )

print(result)
