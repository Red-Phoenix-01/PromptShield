"""
PromptShield Remediation Engine

Maps detected security weaknesses to structured remediation
guidance that can be displayed in findings and reports.
"""


REMEDIATION_LIBRARY = {
    "Prompt Injection": {
        "impact": (
            "An attacker may influence the model to disregard intended "
            "instructions, alter its behavior, or perform unintended actions."
        ),
        "remediation": (
            "Enforce a clear instruction hierarchy, isolate untrusted user "
            "content from trusted instructions, and validate model outputs "
            "before using them in downstream operations."
        ),
        "controls": [
            "Strong system/developer instruction hierarchy",
            "Input boundary separation",
            "Output validation",
            "Adversarial prompt testing",
        ],
    },

    "System Prompt Extraction": {
        "impact": (
            "Sensitive system-level instructions may be exposed, potentially "
            "revealing application logic, security controls, or confidential configuration."
        ),
        "remediation": (
            "Do not place secrets or sensitive configuration in prompts. "
            "Treat system instructions as protected data and explicitly test "
            "the model's resistance to instruction-disclosure attempts."
        ),
        "controls": [
            "System prompt confidentiality",
            "Secret isolation",
            "Output filtering",
            "Prompt extraction testing",
        ],
    },

    "Jailbreak": {
        "impact": (
            "An attacker may attempt to bypass intended behavioral restrictions "
            "and cause the model to produce responses outside the application's policy."
        ),
        "remediation": (
            "Use layered safety controls, strengthen instruction hierarchy, "
            "apply policy checks to model inputs and outputs, and continuously "
            "test against evolving jailbreak patterns."
        ),
        "controls": [
            "Layered safety controls",
            "Policy enforcement",
            "Input/output moderation",
            "Jailbreak regression testing",
        ],
    },

    "Data Exfiltration": {
        "impact": (
            "The model may disclose confidential information, hidden context, "
            "or data that should not be exposed to the requesting user."
        ),
        "remediation": (
            "Minimize sensitive information available to the model, enforce "
            "access controls outside the model, and validate responses for "
            "potential confidential-data disclosure."
        ),
        "controls": [
            "Least-privilege data access",
            "External authorization",
            "Sensitive-data filtering",
            "Disclosure testing",
        ],
    },

    "Context Manipulation": {
        "impact": (
            "An attacker may manipulate contextual boundaries and attempt to "
            "replace trusted instructions with attacker-controlled instructions."
        ),
        "remediation": (
            "Clearly separate trusted instructions from untrusted content, "
            "label external data as untrusted, and prevent user-controlled "
            "content from modifying instruction priority."
        ),
        "controls": [
            "Context isolation",
            "Trusted/untrusted data separation",
            "Instruction priority enforcement",
            "Context manipulation testing",
        ],
    },
}


DEFAULT_REMEDIATION = {
    "impact": (
        "The target response indicates behavior that may require additional "
        "security validation."
    ),
    "remediation": (
        "Review the affected prompt flow, strengthen instruction boundaries, "
        "validate model outputs, and add regression tests for the detected behavior."
    ),
    "controls": [
        "Instruction hierarchy",
        "Input validation",
        "Output validation",
        "Regression testing",
    ],
}


def get_remediation(attack, analysis):
    """
    Generate structured remediation guidance for an analyzed attack result.
    """

    if analysis["status"] != "VULNERABLE":
        return {
            "impact": "No security impact identified.",
            "remediation": (
                "No immediate remediation is required. Continue regression "
                "testing to ensure the target remains resistant to this attack."
            ),
            "controls": [
                "Continuous security testing",
                "Regression testing",
            ],
        }

    category = attack.get("category", "")

    guidance = REMEDIATION_LIBRARY.get(
        category,
        DEFAULT_REMEDIATION
    )

    return {
        "impact": guidance["impact"],
        "remediation": guidance["remediation"],
        "controls": guidance["controls"],
    }