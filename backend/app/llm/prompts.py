"""
Centralized Prompt Templates

All prompts used by the LLM are defined here.
Never hardcode prompts inside services.
"""

from __future__ import annotations

# ==========================================================
# Base System Prompt
# ==========================================================

SYSTEM_PROMPT = """
You are Cluster Doctor AI, an intelligent AI assistant integrated into the Cluster Doctor platform.

Your primary responsibility is to help users understand the platform, analyze cluster health, explain monitoring results, and assist with decision-making using the information provided by the system.

==================================================
YOUR ROLE
==================================================

You are NOT a general-purpose chatbot.

You are an AI Operations Engineer specialized in:

- Kubernetes
- Cluster Monitoring
- AI Prediction
- Digital Twin
- Telemetry Analysis
- Autonomous Recovery
- Intelligent Workload Migration
- Infrastructure Health
- Performance Optimization
- Failure Prevention

Always answer professionally, clearly, and accurately.

==================================================
AVAILABLE PLATFORM FEATURES
==================================================

You can help users with the following platform features:

1. Dashboard
- Explain overall cluster health.
- Explain health score.
- Explain risk score.
- Explain performance metrics.
- Explain AI-generated summaries.

2. Cluster Monitoring
- Explain cluster status.
- Explain healthy and unhealthy clusters.
- Explain cluster utilization.
- Explain node distribution.

3. Node Monitoring
- Explain node health.
- Explain CPU usage.
- Explain memory usage.
- Explain disk usage.
- Explain network usage.

4. Live Telemetry
You can explain:

- CPU
- Memory
- Disk
- Network
- Temperature
- Power Consumption
- Latency
- Throughput
- Resource Utilization

5. AI Prediction
Explain:

- Future failures
- Risk prediction
- Failure probability
- Resource bottlenecks
- Predicted anomalies

6. Digital Twin
Explain:

- What Digital Twin is
- How Digital Twin mirrors the real cluster
- Why Twin Reality Gap occurs
- How simulation works
- Benefits of Digital Twin

7. Twin Reality Gap
Explain:

- Difference between live system and digital twin
- Why the gap occurs
- Possible causes
- Impact on operations

8. Autonomous Migration
Explain:

- Why workload migration happens
- Which workload should migrate
- Safe migration process
- Benefits of migration
- Zero downtime migration

9. Autonomous Recovery
Explain:

- Recovery process
- Recovery confirmation
- System stabilization
- Recovery success

10. AI Reports
Help users understand:

- AI explanations
- Health reports
- Risk reports
- Prediction reports

==================================================
HOW TO ANSWER
==================================================

Always use the provided context.

If telemetry, prediction, node, or cluster information is available, use it.

Never invent metrics.

Never fabricate node names.

Never fabricate health scores.

Never fabricate predictions.

If information is unavailable, clearly say:

"I don't have enough data to answer that accurately."

==================================================
WHEN USERS ASK ABOUT FEATURES
==================================================

If users ask:

"What can you do?"

Reply by explaining the available Cluster Doctor features including:

- Dashboard
- Cluster Monitoring
- Node Monitoring
- Live Telemetry
- AI Prediction
- Digital Twin
- Twin Reality Gap
- Autonomous Migration
- Autonomous Recovery
- AI Reports

==================================================
GENERAL KNOWLEDGE
==================================================

You may answer general questions related to:

- Kubernetes
- Docker
- DevOps
- Cloud Computing
- Containers
- Monitoring
- AI Operations (AIOps)
- Distributed Systems
- Infrastructure
- Linux
- Networking

==================================================
LIMITATIONS
==================================================

Never pretend you executed an operation.

Never claim a node was recovered unless the provided context says so.

Never claim migration happened unless provided.

Never invent telemetry.

Never generate fake alerts.

==================================================
STYLE
==================================================

Be professional.

Be concise.

Be helpful.

Use bullet points whenever appropriate.

Explain technical concepts in simple language if the user is a beginner.

Always prioritize accuracy over speculation.
"""


# ==========================================================
# Prediction Explanation Template
# ==========================================================

PREDICTION_EXPLAIN_PROMPT = """
Analyze the following prediction.

Prediction:
{prediction}

Risk Score:
{risk_score}

Telemetry:
{telemetry}

Return ONLY valid JSON in this format:

{{
    "summary": "...",
    "root_cause": "...",
    "risk_level": "...",
    "confidence": 95.5,
    "recommendations": [
        {{
            "title": "...",
            "description": "...",
            "priority": "HIGH"
        }}
    ]
}}

Do not include markdown.
Do not include explanations outside JSON.
"""


def build_prediction_prompt(
    prediction: dict,
    telemetry: dict | str,
) -> str:
    """
    Build prediction explanation prompt.
    """

    risk_score = (
        prediction.get("risk_score")
        or prediction.get("risk")
        or prediction.get("failure_probability")
        or "Unknown"
    )

    return PREDICTION_EXPLAIN_PROMPT.format(
        prediction=prediction,
        risk_score=risk_score,
        telemetry=telemetry,
    )


# ==========================================================
# Recommendation Template
# ==========================================================

RECOMMENDATION_PROMPT = """
Prediction:

{prediction}

Telemetry:

{telemetry}

Return ONLY valid JSON:

{{
    "summary": "...",
    "recommendations": [
        {{
            "title": "...",
            "description": "...",
            "priority": "HIGH"
        }}
    ]
}}
"""


def build_recommendation_prompt(
    prediction: dict,
    telemetry: dict | str,
) -> str:
    return RECOMMENDATION_PROMPT.format(
        prediction=prediction,
        telemetry=telemetry,
    )


# ==========================================================
# Dashboard Summary
# ==========================================================

DASHBOARD_SUMMARY_PROMPT = """
Cluster:

{cluster}

Nodes:

{nodes}

Predictions:

{predictions}

Telemetry:

{telemetry}

Return ONLY valid JSON:

{{
    "overall_health": "...",
    "summary": "...",
    "critical_nodes": [],
    "warnings": [],
    "recommendations": []
}}
"""


def build_dashboard_prompt(
    cluster: dict,
    nodes: list,
    predictions: list,
    telemetry: list,
) -> str:
    return DASHBOARD_SUMMARY_PROMPT.format(
        cluster=cluster,
        nodes=nodes,
        predictions=predictions,
        telemetry=telemetry,
    )


# ==========================================================
# Chat Prompt
# ==========================================================

CHATBOT_PROMPT = """
Conversation:

{history}

User Question:

{question}

Cluster Context:

{context}

Return ONLY valid JSON:

{{
    "answer": "...",
    "confidence": 97.0,
    "sources": []
}}
"""


def build_chat_prompt(
    history: str,
    question: str,
    context: str,
) -> str:
    return CHATBOT_PROMPT.format(
        history=history,
        question=question,
        context=context,
    )


# ==========================================================
# Alert Prompt
# ==========================================================

ALERT_PROMPT = """
Alert:

{alert}

Telemetry:

{telemetry}

Prediction:

{prediction}

Return ONLY valid JSON:

{{
    "severity": "...",
    "explanation": "...",
    "recommendation": "..."
}}
"""


def build_alert_prompt(
    alert: dict,
    telemetry: dict | str,
    prediction: dict,
) -> str:
    return ALERT_PROMPT.format(
        alert=alert,
        telemetry=telemetry,
        prediction=prediction,
    )


# ==========================================================
# Recovery Prompt
# ==========================================================

RECOVERY_PROMPT = """
Node:

{node}

Prediction:

{prediction}

Telemetry:

{telemetry}

Return ONLY valid JSON:

{{
    "summary": "...",
    "estimated_downtime": "...",
    "confidence": 95.0,
    "steps": [
        "...",
        "..."
    ]
}}
"""


def build_recovery_prompt(
    node: dict,
    prediction: dict,
    telemetry: dict | str,
) -> str:
    return RECOVERY_PROMPT.format(
        node=node,
        prediction=prediction,
        telemetry=telemetry,
    )


# ==========================================================
# Report Prompt
# ==========================================================

REPORT_PROMPT = """
Cluster:

{cluster}

Telemetry:

{telemetry}

Predictions:

{predictions}

Return ONLY valid JSON:

{{
    "executive_summary": "...",
    "findings": [],
    "recommendations": [],
    "conclusion": "..."
}}
"""


def build_report_prompt(
    cluster: dict,
    telemetry: list,
    predictions: list,
) -> str:
    return REPORT_PROMPT.format(
        cluster=cluster,
        telemetry=telemetry,
        predictions=predictions,
    )