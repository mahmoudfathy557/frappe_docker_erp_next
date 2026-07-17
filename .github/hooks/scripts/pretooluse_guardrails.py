import json
import os
import sys
from pathlib import Path


POLICY_PATH = Path(__file__).resolve().parents[1] / "policy" / "environment-policy.json"


def read_input():
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def get_tool_name(payload):
    for key in ("toolName", "tool_name", "name"):
        if isinstance(payload.get(key), str):
            return payload[key].lower()
    tool = payload.get("tool")
    if isinstance(tool, dict):
        for key in ("name", "toolName"):
            if isinstance(tool.get(key), str):
                return tool[key].lower()
    return "unknown"


def load_policy():
    try:
        raw = POLICY_PATH.read_text(encoding="utf-8")
        policy = json.loads(raw)
        if not isinstance(policy, dict):
            raise ValueError("policy must be an object")
        return policy, None
    except Exception as exc:
        return {}, str(exc)


def env_class(policy):
    env_var = str(policy.get("environmentVariable", "")).strip()
    default_env = str(policy.get("defaultEnvironment", "development")).strip().lower()
    value = os.getenv(env_var, default_env).strip().lower() if env_var else default_env
    production_like = {str(v).lower() for v in policy.get("productionLike", []) if isinstance(v, str)}
    if value in production_like:
        return "production"
    return "development"


def main():
    payload = read_input()
    tool_name = get_tool_name(payload)
    policy, policy_error = load_policy()
    destructive_keywords = [str(x).lower() for x in policy.get("destructiveKeywords", []) if isinstance(x, str)]
    mutate_keywords = [str(x).lower() for x in policy.get("mutatingKeywords", []) if isinstance(x, str)]

    decision = "allow"
    reason = "Allowed by default policy"

    if policy_error:
        fallback_policy = policy.get("fallbackPolicy", {}) if isinstance(policy, dict) else {}
        fallback_decision = str(fallback_policy.get("invalidPolicyFile", "ask")).lower()
        if fallback_decision not in {"allow", "ask", "deny"}:
            fallback_decision = "ask"
        decision = fallback_decision
        reason = f"Policy load failure: {policy_error}"

    if decision == "allow" and any(word in tool_name for word in destructive_keywords):
        decision = "deny"
        reason = "Destructive action blocked by policy"
    elif decision == "allow" and any(word in tool_name for word in mutate_keywords) and env_class(policy) == "production":
        decision = "ask"
        reason = "Production-like environment requires explicit confirmation"

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
