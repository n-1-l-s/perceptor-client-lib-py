import sys, os
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH, "..", "..", "src"
)
sys.path.append(SOURCE_PATH)

import perceptor_client_lib.perceptor as perceptor

API_KEY = "api.4zAhccIfthXOWkcSzK9bCf"


def create_client():
    return perceptor.Client(api_key=API_KEY)
