# NeMo Guardrails boundary

The project keeps NeMo Guardrails configuration as an explicit safety layer. NVIDIA documents input, retrieval, dialog, execution, and output rails as distinct enforcement points. Tool-call validation can additionally be provided through the IORails engine, which validates OpenAI Chat Completions tool traffic and fails closed on malformed or disallowed payloads.

The prototype's deterministic `PolicyEngine` remains authoritative for infrastructure actions. NeMo Guardrails is complementary: it filters unsafe interaction patterns and validates the model/tool boundary, while the application policy decides whether an infrastructure action belongs inside the autonomous risk envelope.
