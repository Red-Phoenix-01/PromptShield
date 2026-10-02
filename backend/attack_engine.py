from analyzer import analyze_response   
from remediation import get_remediation


def run_attack_suite(attacks, response_provider):
    """
    Execute the configured attack suite against a target,
    analyze each response, and generate remediation guidance.
    """

    results = []

    for attack in attacks:

        attack_id = attack["id"]

        try:
            # ------------------------------------------------
            # Execute attack
            # ------------------------------------------------

            target_response = response_provider(attack)

            # ------------------------------------------------
            # Analyze response
            # ------------------------------------------------

            analysis = analyze_response(
                attack,
                target_response
            )

            # ------------------------------------------------
            # Generate remediation
            # ------------------------------------------------

            remediation = get_remediation(
                attack,
                analysis
            )

            # ------------------------------------------------
            # Build finding
            # ------------------------------------------------

            results.append({
                "id": attack_id,
                "name": attack["name"],
                "category": attack["category"],
                "attack_prompt": attack["prompt"],
                "target_response": target_response,

                "status": analysis["status"],
                "severity": analysis["severity"],
                "reason": analysis["reason"],
                "evidence": analysis["evidence"],

                "impact": remediation["impact"],
                "remediation": remediation["remediation"],
                "security_controls": remediation["controls"],

                "mode": "DEMO",
            })

        except Exception as error:

            results.append({
                "id": attack_id,
                "name": attack["name"],
                "category": attack["category"],
                "attack_prompt": attack["prompt"],
                "target_response": None,

                "status": "TEST_FAILED",
                "severity": "N/A",
                "reason": f"Attack execution failed: {str(error)}",
                "evidence": [],

                "impact": "The security test could not be completed.",
                "remediation": (
                    "Investigate the target or test execution failure "
                    "before considering the security result valid."
                ),
                "security_controls": [
                    "Test execution monitoring",
                    "Failure handling",
                ],

                "mode": "DEMO",
            })

    return results