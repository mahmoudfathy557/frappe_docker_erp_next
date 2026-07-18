---
description: "MCP-first routing policy with allowed bench fallbacks for ERPNext operations."
applyTo: ".github/agents/**/*.agent.md"
---

# MCP Routing Policy

## Core Rule

1. Use ERPNext MCP tools first for all supported operations.
2. Use bench fallback only when one of these reason codes applies:
   - MCP_UNSUPPORTED_OPERATION
   - MCP_TOOL_UNAVAILABLE
   - MCP_RUNTIME_FAILURE

## Discovery Before Mutation

1. For mutating operations, first inspect existing document workflow states, linked documents, and module touchpoints.
2. Prefer MCP read/list/get calls to establish current behavior before submit/cancel/update/delete actions.
3. Do not introduce new command paths when an existing module workflow can be integrated.

## Fallback Contract

1. Report the reason code.
2. Use explicit docker exec + bench commands.
3. Perform a read-back verification step.

## Prohibited Pattern

1. Do not default to shell command execution when MCP support exists.
