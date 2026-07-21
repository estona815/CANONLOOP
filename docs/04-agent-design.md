# Agent Design

Eight bounded agent classes implement Intake, Canon Builder, Campaign Planner, Generation,
Continuity Critic, Repair, Provenance Archivist, and Release Packager. Every `AgentSpec` records its
input/output contract, tool allowlist, failure conditions, retry policy, and approval boundary.
Automatic repair stops after two attempts; a third failure requires human review.

