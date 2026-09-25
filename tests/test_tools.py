# Import the metrics tool that we want to test.
from backend.tools.metrics import get_service_metrics

# Import the logs tool that we want to test.
from backend.tools.logs import get_recent_logs

# Import the deployment tool that we want to test.
from backend.tools.deployments import get_recent_deployments

# Import the database health tool that we want to test.
from backend.tools.database import get_database_health


# Test that the metrics tool returns the expected information.
def test_get_service_metrics():

    # Call the tool for checkout-api.
    result = get_service_metrics("checkout-api")

    # Verify that the correct service is returned.
    assert result["service"] == "checkout-api"

    # Verify that the simulated error rate is returned.
    assert result["error_rate"] == 0.07

    # Verify that the service is correctly classified as abnormal.
    assert result["health"] == "ABNORMAL"


# Test that the logs tool returns the expected information.
def test_get_recent_logs():

    # Call the tool for checkout-api.
    result = get_recent_logs("checkout-api")

    # Verify that the correct service is returned.
    assert result["service"] == "checkout-api"

    # Verify that logs were returned.
    assert len(result["logs"]) > 0

    # Verify that the logs contain an important database error.
    assert "ERROR Database connection timeout" in result["logs"]


# Test that the deployment tool returns the expected information.
def test_get_recent_deployments():

    # Call the tool for checkout-api.
    result = get_recent_deployments("checkout-api")

    # Verify that the correct service is returned.
    assert result["service"] == "checkout-api"

    # Verify that deployment information was returned.
    assert len(result["deployments"]) > 0

    # Verify that the latest deployment version is present.
    assert result["deployments"][0]["version"] == "v2.4.1"

# Test that the database health tool returns the expected information.
def test_get_database_health():

    # Call the tool for checkout-api.
    result = get_database_health("checkout-api")

    # Verify that the correct service is returned.
    assert result["service"] == "checkout-api"

    # Verify that database information was returned.
    assert result["database"] is not None

    # Verify that the correct database is being checked.
    assert result["database"]["database"] == "checkout-db"

    # Verify that the simulated database is unhealthy.
    assert result["database"]["health"] == "UNHEALTHY"