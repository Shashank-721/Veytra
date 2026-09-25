# Import the function that fetches database health
# from our simulated database provider.
from backend.tools.database_provider import fetch_database_health


# Tool function that Veytra will eventually call
# to investigate database health.
def get_database_health(service: str):

    # Fetch the raw database health information
    # for the requested service.
    database_health = fetch_database_health(service)

    # Return the database information together with
    # the service name so Veytra has the necessary context.
    return {
        "service": service,
        "database": database_health,
    }


# Run this test only when the file is executed directly.
if __name__ == "__main__":

    # Ask the tool for the database health of checkout-api.
    result = get_database_health("checkout-api")

    # Print the result so we can verify that the tool works.
    print(result)