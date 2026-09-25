# Simulated deployment history for each service.
# In a real system, this could come from GitHub, GitLab,
# Kubernetes, AWS, or another deployment platform.

SIMULATED_DEPLOYMENTS = {
    "checkout-api": [
        {
            "version": "v2.4.1",
            "deployed_at": "2026-09-24 14:30:00",
            "deployed_by": "deployment-pipeline",
        },
        {
            "version": "v2.4.0",
            "deployed_at": "2026-09-20 10:15:00",
            "deployed_by": "deployment-pipeline",
        },
    ],
    "payment-api": [
        {
            "version": "v1.8.2",
            "deployed_at": "2026-09-22 09:00:00",
            "deployed_by": "deployment-pipeline",
        }
    ],
    "inventory-api": [
        {
            "version": "v3.1.0",
            "deployed_at": "2026-09-21 16:45:00",
            "deployed_by": "deployment-pipeline",
        }
    ],
}


# Fetch recent deployments for a specific service.
def fetch_recent_deployments(service: str):

    # Look for the requested service in our simulated data.
    deployments = SIMULATED_DEPLOYMENTS.get(service)

    # Raise an error if the service does not exist.
    if deployments is None:
        raise ValueError(f"Service '{service}' not found")

    # Return the deployment history for the service.
    return deployments


# Run a simple test when this file is executed directly.
if __name__ == "__main__":

    # Fetch deployments for checkout-api.
    result = fetch_recent_deployments("checkout-api")

    # Print the result so we can verify the provider works.
    print(result)