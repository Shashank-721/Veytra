from enum import Enum


class RiskLevel(str, Enum):
    # Safe actions that only inspect system state.
    READ_ONLY = "READ_ONLY"

    # Actions that can be undone.
    REVERSIBLE = "REVERSIBLE"

    # Actions that can cause significant or irreversible impact.
    DESTRUCTIVE = "DESTRUCTIVE"


def requires_approval(risk_level: RiskLevel) -> bool:
    """
    Decide whether a human must approve an action.
    """

    if risk_level == RiskLevel.READ_ONLY:
        return False

    if risk_level == RiskLevel.REVERSIBLE:
        return True

    if risk_level == RiskLevel.DESTRUCTIVE:
        return True

    return True