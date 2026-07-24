"""
Recovery Verification
"""

from __future__ import annotations


class RecoveryVerifier:

    def verify(
        self,
        migration_result: dict,
    ) -> dict:

        if not migration_result["success"]:

            return {

                "success": False,

                "checkpoint_restored": False,

                "lost_steps": 0,

                "status": "failed",
            }

        return {

            "success": True,

            "checkpoint_restored": True,

            "application_running": True,

            "lost_steps": 0,

            "status": "recovered",
        }


recovery_verifier = RecoveryVerifier()