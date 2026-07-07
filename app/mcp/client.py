import requests
from app.utils.config import FastAPI_MCP_API_KEY,FastAPI_MCP_URL


API_URL = FastAPI_MCP_URL
API_KEY = FastAPI_MCP_API_KEY


class MCPClient:

    def sync_all(self):

        try:

            print(">>> Calling MCP Server...")

            response = requests.post(
                f"{API_URL}/sync-all",
                headers={
                    "x-api-key": API_KEY
                },
                timeout=5
            )

            print(response.status_code)
            print(response.text)

        except Exception as e:

            print(f"MCP Sync Failed: {e}")