import { Suspense } from "react";
import { DemoWorkspace } from "@/components/demo-workspace";

export default function DemoPage() {
  return <Suspense fallback={<div className="loading-screen">Loading deterministic Replay…</div>}><DemoWorkspace /></Suspense>;
}

