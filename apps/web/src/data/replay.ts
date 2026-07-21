import type { CampaignAsset, ReplayFixture } from "@canonloop/contracts";

export const assets: CampaignAsset[] = [
  {
    id: "asset-cover", title: "Square Cover", format: "1:1", image: "/media/square-cover.png",
    status: "approved", runId: "run-005", parentRunId: null,
    sha256: "b5c721e356457d2c89f3221870f689b57fcfb21f4ecfb0ff495ad15308c0e20f",
    b2ObjectKey: "projects/six-line-halo/approved/square-cover.png"
  },
  {
    id: "asset-story-failed", title: "Vertical Story · attempt 1", format: "9:16",
    image: "/media/vertical-story-failed.png", status: "failed", runId: "run-007", parentRunId: null,
    sha256: "144ae5a8ce0abb77b10d89221fa3ac0610591e74c7a3d7c827c83da3674ead90",
    b2ObjectKey: "projects/six-line-halo/rejected/vertical-story/run-007.png"
  },
  {
    id: "asset-story-repaired", title: "Vertical Story · repaired", format: "9:16",
    image: "/media/vertical-story-repaired.png", status: "repaired", runId: "run-007r", parentRunId: "run-007",
    sha256: "57aee0629e1ddd76c6d0e460815f0a7982466abd346f9e9bb79907eaf7898148",
    b2ObjectKey: "projects/six-line-halo/approved/vertical-story.png"
  },
  {
    id: "asset-banner", title: "Landscape Banner", format: "16:9", image: "/media/landscape-banner.png",
    status: "approved", runId: "run-006", parentRunId: null,
    sha256: "fef28c8486af75d2b30147988f547fa3700f344aaa89ff775502655f9dbf7b9a",
    b2ObjectKey: "projects/six-line-halo/approved/landscape-banner.png"
  },
  {
    id: "asset-poster", title: "Poster", format: "2:3", image: "/media/poster.png",
    status: "approved", runId: "run-008", parentRunId: null,
    sha256: "dab1cd8b2ecc71aa0fd126a7c70746898217c83e70e40b042c9014796756dcae",
    b2ObjectKey: "projects/six-line-halo/approved/poster.png"
  }
];

export const replay: ReplayFixture = {
  projectId: "six-line-halo",
  campaign: "SIX-LINE HALO",
  mode: "replay",
  storageVerified: false,
  manifestVerified: true,
  assets,
  failedScores: { identity: 0.91, style: 0.88, palette: 0.86, symbol: 0.64, format: 1 },
  repairedScores: { identity: 0.93, style: 0.9, palette: 0.89, symbol: 0.94, format: 1 }
};

export const canonAnchors = [
  "Seamless dark metallic moth mask",
  "Cyan light below the left ear",
  "Black asymmetric jacket",
  "Six-line amber halo emblem",
  "Deep navy · cyan · warm amber palette"
];

export const steps = [
  "Brief", "Visual Canon", "Campaign Plan", "Generation Runs", "Continuity Review",
  "Repair Comparison", "Approved Campaign", "Provenance", "B2 Storage"
] as const;

