from backend.tools.metrics_provider import (
    fetch_service_metrics,
    evaluate_service_health,
)

def get_service_metrics(service: str):
    metrics = fetch_service_metrics(service)
    health = evaluate_service_health(metrics)

    return {
        "service": service,
        **metrics,
        "health": health,
    }

if __name__ == "__main__":
    result = get_service_metrics("checkout-api")
    print(result)