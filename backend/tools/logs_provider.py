# Simulated production logs for each service.
# In a real system, this data could come from a logging platform
# such as CloudWatch, Elasticsearch, Datadog, etc.
SIMULATED_LOGS = {
    "checkout-api": [
        "ERROR Database connection timeout",
        "ERROR PostgreSQL connection pool exhausted",
        "ERROR Failed to process checkout request",
    ],
    "payment-api": [
        "INFO Payment request processed",
        "INFO Payment completed successfully",
    ],
    "inventory-api": [
        "INFO Inventory request processed",
        "INFO Stock lookup completed successfully",
    ],
}


# Fetch recent logs for a specific service.
def fetch_recent_logs(service: str):
    # Look for the requested service in our simulated log data.
    logs = SIMULATED_LOGS.get(service)

    # If the service doesn't exist, raise a clear error.
    if logs is None:
        raise ValueError(f"Service '{service}' not found")

    # Return the logs for the requested service.
    return logs


# Test the provider when this file is run directly.
if __name__ == "__main__":
    print(fetch_recent_logs("checkout-api"))