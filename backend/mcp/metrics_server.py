from fastmcp import FastMCP
from backend.tools.metrics import get_service_metrics

mcp = FastMCP("Veytra Metrics Server")


@mcp.tool
def get_metrics(service: str):
    """
    Get current metrics and health status for a service.
    """
    return get_service_metrics(service)


if __name__ == "__main__":
    mcp.run()