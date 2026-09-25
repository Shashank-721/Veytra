# Import the function that fetches deployment data
# from our simulated deployment provider.
from backend.tools.deployments_provider import fetch_recent_deployments


# Tool function that Veytra will eventually call
# to investigate recent deployments.
def get_recent_deployments(service: str):

    # Fetch the raw deployment history for the requested service.
    deployments = fetch_recent_deployments(service)

    # Return the deployment information together with
    # the service name so Veytra knows where the evidence came from.
    return {
        "service": service,
        "deployments": deployments,
    }


# Run this test only when this file is executed directly.
if __name__ == "__main__":

    # Ask the tool for recent deployments of checkout-api.
    result = get_recent_deployments("checkout-api")

    # Print the result to verify that the tool works.
    print(result)