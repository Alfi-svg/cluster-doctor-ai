"""
Healing Pipeline

Prediction
    ↓
Safe Target
    ↓
Migration
    ↓
Recovery
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.node_repository import node_repository

from app.self_healing import (
    CandidateNode,
    migration_engine,
    migration_planner,
    recovery_verifier,
    checkpoint_manager,
)


class HealingPipeline:

    async def run(
        self,
        db: AsyncSession,
        prediction,
    ):

        # -----------------------------------
        # Normalize Input
        #
        # `prediction` may arrive as a raw dict
        # (HTTP JSON body) or as a Prediction
        # ORM instance (in-process call from the
        # AI orchestrator). Support both.
        # -----------------------------------

        if isinstance(prediction, dict):
            source_cluster_id = prediction.get("cluster_id")
            source_node_id = prediction.get("node_id")
        else:
            source_cluster_id = prediction.cluster_id
            source_node_id = prediction.node_id

        # -----------------------------------
        # Get Candidate Nodes
        # -----------------------------------

        nodes = await node_repository.get_by_cluster(
            db,
            source_cluster_id,
        )

        candidates = []

        for node in nodes:

            if node.id == source_node_id:
                continue

            # Node has no dedicated "health_score" column,
            # so derive one from its live telemetry fields
            # (all real, already-persisted values) instead
            # of a constant stub.
            cpu_usage = getattr(node, "cpu_usage", 0.0) or 0.0
            gpu_usage = getattr(node, "gpu_usage", 0.0) or 0.0
            memory_usage = getattr(node, "memory_usage", 0.0) or 0.0
            temperature = getattr(node, "temperature", 0.0) or 0.0

            health_score = round(
                max(
                    0.0,
                    100
                    - (
                        cpu_usage * 0.25
                        + gpu_usage * 0.25
                        + memory_usage * 0.25
                        + min(temperature, 100) * 0.25
                    ),
                ),
                2,
            )

            raw_status = getattr(node, "status", "online")
            status_value = getattr(raw_status, "value", raw_status)

            candidates.append(

                CandidateNode(

                    node_id=node.id,

                    health_score=health_score,

                    cpu_usage=cpu_usage,

                    ram_usage=memory_usage,

                    status=str(status_value).lower(),
                )
            )

        # -----------------------------------
        # Safe Target
        # -----------------------------------

        plan = migration_planner.plan(

            source_node=source_node_id,

            candidates=candidates,
        )

        if not plan["success"]:

            return {

                "success": False,

                "reason": "No migration target.",
            }

        # -----------------------------------
        # Migration
        # -----------------------------------

        migration = migration_engine.migrate(

            source_node=plan["source_node"],

            target_node=plan["target_node"],
        )

        # -----------------------------------
        # Checkpoint
        # -----------------------------------

        checkpoint = checkpoint_manager.restore(

            workload_id=f"node-{source_node_id}"
        )

        # -----------------------------------
        # Recovery
        # -----------------------------------

        recovery = recovery_verifier.verify(
            migration
        )

        return {

            "success": True,

            "plan": plan,

            "migration": migration,

            "checkpoint": checkpoint,

            "recovery": recovery,
        }


healing_pipeline = HealingPipeline()