SIMULATED_METRICS = {
    "checkout-api": {
        "requests_per_second": 120,
        "error_rate": 0.07,
        "latency_ms": 850,
    },
    "payment-api": {
        "requests_per_second": 80,
        "error_rate": 0.005,
        "latency_ms": 120,
    },
    "inventory-api": {
        "requests_per_second": 60,
        "error_rate": 0.002,
        "latency_ms": 90,
    },
}
#to find if the service exist or no
def fetch_service_metrics(service: str):
    metrics = SIMULATED_METRICS.get(service)
    if metrics is None:
        raise ValueError(f"Service '{service}' not found")
    return metrics
#to find if we have any abnormal latency or error-rate
def evaluate_service_health(metrics):
    error_rate = metrics["error_rate"]
    latency = metrics["latency_ms"]

    if error_rate >= 0.05 or latency >= 500:
        return "ABNORMAL"

    return "NORMAL"

if __name__ == "__main__":
    checkout_metrics = fetch_service_metrics("checkout-api")
    payment_metrics = fetch_service_metrics("payment-api")

    print("Checkout:", evaluate_service_health(checkout_metrics))
    print("Payment:", evaluate_service_health(payment_metrics))

