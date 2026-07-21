import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { strToU8, zipSync } from "fflate";

const files = ["square-cover.png", "vertical-story-repaired.png", "landscape-banner.png", "poster.png"];

export async function GET() {
  const entries: Record<string, Uint8Array> = {};
  for (const file of files) {
    const bytes = await readFile(join(process.cwd(), "public", "media", file));
    entries[`approved-assets/${file}`] = new Uint8Array(bytes);
  }
  entries["README.txt"] = strToU8("CANONLOOP SIX-LINE HALO Replay package\nSynthetic evaluation media. B2 storage is not verified in this local Replay.\n");
  entries["campaign-manifest.json"] = strToU8(JSON.stringify({
    projectId: "six-line-halo", mode: "replay", approvedAssets: files,
    rejectedRun: "run-007", repairedRun: "run-007r", manifestVerified: true, storageVerified: false
  }, null, 2));
  entries["continuity-report.json"] = strToU8(JSON.stringify({
    finding: "Emblem has 4 wing lines; canon requires 6.",
    before: { symbol: 0.64, decision: "reject" }, after: { symbol: 0.94, decision: "approve" }
  }, null, 2));
  const archive = zipSync(entries, { level: 6 });
  return new Response(Buffer.from(archive), {
    headers: {
      "Content-Type": "application/zip",
      "Content-Disposition": 'attachment; filename="canonloop-six-line-halo.zip"',
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff"
    }
  });
}

