from tests_commons import create_client
import logging

from perceptor_client_lib.external_models import PerceptorRequest


logging.basicConfig(level=logging.DEBUG)

DOCUMENT_PATH = "../test_files/pdf_with_2_pages.pdf"

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

result = perceptor_client.ask_document(DOCUMENT_PATH,
                                       instructions=[
                                           "Vorname und Nachname des Kunden?",
                                           "Ist der Kunde ein VIP? (Ja oder nein)",
                                       ]
                                       )

print(result)
