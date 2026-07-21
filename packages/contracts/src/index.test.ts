import { describe, expect, it } from "vitest";
import { replaySchema } from "./index.js";

describe("replay schema", () => {
  it("rejects missing evidence", () => {
    expect(replaySchema.safeParse({ projectId: "x" }).success).toBe(false);
  });
});

