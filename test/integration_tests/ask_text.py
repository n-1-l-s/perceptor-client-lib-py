import logging

from tests_commons import create_client

logging.basicConfig(level=logging.DEBUG)

TEXT_TO_PROCESS = """
Ich melde einen Schaden für meinen Kunden Hans Helvetia. Er hatte einen Schaden durch eine Überschwemmung. 
Er hat Rechnungen in Höhe von 150000 Euro eingereicht. Der Schaden soll in 2 Chargen bezahlt werden. 
Seine  IBAN ist DE02300606010002474689. Versicherungsbeginn war der 01.10.2022. Er ist abgesichert bis 750.000 EUR. Der Ablauf der Versicherung ist der 01.10.2026. 
Der Kunde hat VIP-Kennzeichen und hatte schonmal einen Leitungswasserschaden in Höhe von 3840 Euro. 
Der Schaden ist 2021 aufgetreten. Die Anschrift des Kunden ist: Berliner Straße 56, 60311 Frankfurt am Main.

Meine Vermittlernumer ist die 090.100.
"""

perceptor_client = create_client()

result = perceptor_client.ask_text(TEXT_TO_PROCESS,
                                   instructions=[
                                       "Vorname und Nachname des Kunden?",
                                       "Ist der Kunde ein VIP? (Ja oder nein)",
                                   ]
                                   )

print(result)