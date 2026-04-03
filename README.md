# FeedOracle + ToolOracle — A2A Compliance & Trust Runtime Sample

A production A2A implementation demonstrating how specialized compliance and trust agents can be discovered and orchestrated by other agents.

## What this sample shows

- **Agent Cards** deployed at `/.well-known/agent.json` with A2A v0.3 format
- **16 skills** across 2 agents (compliance + trust infrastructure)
- **ES256K signed responses** with independent verification
- **Blockchain-anchored evidence** on Polygon and XRPL
- **x402 micropayments** — agents pay per call with USDC

## Live Agent Cards

| Agent | Agent Card | Skills | Description |
|---|---|---|---|
| FeedOracle | [feedoracle.io/.well-known/agent.json](https://feedoracle.io/.well-known/agent.json) | 8 | DORA/MiCA/AML compliance for regulated finance |
| ToolOracle | [tooloracle.io/.well-known/agent.json](https://tooloracle.io/.well-known/agent.json) | 8 | Agent Trust Runtime (identity, policy, fraud, passports) |

## Architecture

```
Client Agent
    │
    ├─ Discovers FeedOracle via /.well-known/agent.json
    │   └─ Skills: compliance_preflight, dora_readiness, sanctions_aml, ...
    │   └─ Endpoint: https://feedoracle.io/a2a/tasks
    │
    └─ Discovers ToolOracle via /.well-known/agent.json
        └─ Skills: agent_identity, policy_enforcement, fraud_detection, ...
        └─ Endpoint: https://tooloracle.io/a2a/tasks
```

## Quick Start — Discover and call

### 1. Fetch Agent Card

```bash
curl https://feedoracle.io/.well-known/agent.json
```

### 2. Send a task (compliance preflight)

```bash
curl -X POST https://feedoracle.io/a2a/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "id": "req-001",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "Run compliance preflight on USDT"}],
        "messageId": "msg-001"
      }
    }
  }'
```

### 3. Verify the response signature

Every response includes an ES256K signature. Verify against:
```
https://feedoracle.io/.well-known/jwks.json
```

## Why this matters for A2A

Most A2A samples show "hello world" agents. This is a **production compliance infrastructure** that demonstrates:

1. **Trust problem**: How does Agent A trust Agent B's compliance data? → ES256K signing + blockchain anchoring
2. **Payment problem**: How do agents pay for services? → x402 USDC micropayments ($0.01/call)
3. **Policy problem**: How do you enforce rules across 1,043 tools? → AgentGuard with 258 policies
4. **Discovery problem**: How do agents find specialized services? → A2A Agent Cards with tagged skills

## Stack

- **Protocol**: A2A v0.3 + MCP (Streamable HTTP)
- **Signing**: ES256K (secp256k1)
- **Blockchain**: Polygon Mainnet + XRPL
- **Payment**: x402 USDC on Base
- **Hosting**: Self-hosted (Germany)
- **Tools**: 1,043 across 89 MCP servers

## Links

- [FeedOracle](https://feedoracle.io) — Compliance evidence infrastructure
- [ToolOracle](https://tooloracle.io) — Agent Trust Runtime
- [Agent Card Spec](https://a2a-protocol.org/latest/specification/)

## License

Apache 2.0
