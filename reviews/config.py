import os
from dotenv import load_dotenv
from google.cloud import bigquery
from google.oauth2 import service_account
from google.adk.sessions import InMemorySessionService

# Load environment variables from vars.env
load_dotenv("vars.env")

class Configuration:
    def __init__(self):
        self.bq_project = os.getenv("BQ_PROJECT")
        self.bq_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self._session_service = InMemorySessionService() 

    def get_bigquery_client(self):
        client_kwargs = {}
        if self.bq_project:
            client_kwargs["project"] = self.bq_project
        if self.bq_credentials_path:
            credentials = service_account.Credentials.from_service_account_file(self.bq_credentials_path)
            client_kwargs["credentials"] = credentials
        return bigquery.Client(**client_kwargs)

# Singleton config instance
config = Configuration() 