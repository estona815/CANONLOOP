import { z } from "zod";

export const modeSchema = z.enum(["replay", "mock", "live"]);
export type RunMode = z.infer<typeof modeSchema>;

export const scoreSchema = z.object({
  identity: z.number().min(0).max(1),
  style: z.number().min(0).max(1),
  palette: z.number().min(0).max(1),
  symbol: z.number().min(0).max(1),
  format: z.number().min(0).max(1),
});
export type ContinuityScores = z.infer<typeof scoreSchema>;

export const assetSchema = z.object({
  id: z.string().min(1),
  title: z.string().min(1),
  format: z.string().min(1),
  image: z.string().min(1),
  status: z.enum(["approved", "failed", "repaired"]),
  runId: z.string().min(1),
  parentRunId: z.string().nullable(),
  sha256: z.string().regex(/^[a-f0-9]{64}$/),
  b2ObjectKey: z.string().min(1),
});
export type CampaignAsset = z.infer<typeof assetSchema>;

export const replaySchema = z.object({
  projectId: z.string(),
  campaign: z.string(),
  mode: modeSchema,
  storageVerified: z.boolean(),
  manifestVerified: z.boolean(),
  assets: z.array(assetSchema).min(4),
  failedScores: scoreSchema,
  repairedScores: scoreSchema,
});
export type ReplayFixture = z.infer<typeof replaySchema>;

