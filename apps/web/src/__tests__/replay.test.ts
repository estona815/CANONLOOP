import { describe, expect, it } from "vitest";
import { replaySchema } from "@canonloop/contracts";
import { assets, replay } from "@/data/replay";

describe("guided Replay", () => {
  it("matches the shared contract", () => {
    expect(replaySchema.safeParse(replay).success).toBe(true);
  });

  it("contains four release assets and one rejected attempt", () => {
    expect(assets.filter(asset => asset.status !== "failed")).toHaveLength(4);
    expect(assets.filter(asset => asset.status === "failed")).toHaveLength(1);
  });

  it("links the repaired run to the rejected parent", () => {
    const repaired = assets.find(asset => asset.status === "repaired");
    expect(repaired?.parentRunId).toBe("run-007");
    expect(replay.repairedScores.symbol).toBeGreaterThan(replay.failedScores.symbol);
  });
});

