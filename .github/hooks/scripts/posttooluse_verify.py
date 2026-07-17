import json
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
        return policy
    except Exception:
        return {}


def main():
    payload = read_input()
    tool_name = get_tool_name(payload)
    policy = load_policy()
    mutate_keywords = [str(x).lower() for x in policy.get("mutatingKeywords", []) if isinstance(x, str)]
    reminder = str(
        policy.get(
            "verificationReminder",
            "Policy reminder: include explicit read-back verification evidence after mutating operations.",
        )
    )
    if any(word in tool_name for word in mutate_keywords):
        output = {
            "systemMessage": reminder
        }
        print(json.dumps(output))
    else:
        print("{}")


if __name__ == "__main__":
    main()
