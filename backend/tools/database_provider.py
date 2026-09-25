# Simulated database health information.
# In a real production system, this data could come from
# PostgreSQL, AWS RDS, CloudWatch, Datadog, or another
# database monitoring system.

SIMULATED_DATABASE_HEALTH = {
    "checkout-api": {
        "database": "checkout-db",
        "connection_pool_usage": 0.95,
        "active_connections": 95,
        "max_connections": 100,
        "latency_ms": 1200,
        "health": "UNHEALTHY",
    },
    "payment-api": {
        "database": "payment-db",
        "connection_pool_usage": 0.30,
        "active_connections": 30,
        "max_connections": 100,
        "latency_ms": 80,
        "health": "HEALTHY",
    },
    "inventory-api": {
        "database": "inventory-db",
        "connection_pool_usage": 0.25,
        "active_connections": 25,
        "max_connections": 100,
        "latency_ms": 70,
        "health": "HEALTHY",
    },
}


# Fetch database health information for a specific service.
def fetch_database_health(service: str):

    # Look for the database information associated
    # with the requested service.
    database_health = SIMULATED_DATABASE_HEALTH.get(service)

    # Raise an error if the service does not exist.
    if database_health is None:
        raise ValueError(f"Service '{service}' not found")

    # Return the database health information.
    return database_health


# Run a simple test when this file is executed directly.
if __name__ == "__main__":

    # Fetch database health for checkout-api.
    result = fetch_database_health("checkout-api")

    # Print the result so we can verify the provider works.
    print(result)