# Import the function that fetches logs from our simulated log provider.
from backend.tools.logs_provider import fetch_recent_logs


# Tool function that Veytra will eventually call to get recent logs.
def get_recent_logs(service: str):

    # Fetch the raw logs for the requested service.
    logs = fetch_recent_logs(service)

    # Return the logs together with the service name.
    # This gives Veytra context about where the evidence came from.
    return {
        "service": service,
        "logs": logs,
    }


# Run this test only when this file is executed directly.
if __name__ == "__main__":

    # Ask the tool for the recent logs of checkout-api.
    result = get_recent_logs("checkout-api")

    # Print the result so we can verify that the tool works.
    print(result)