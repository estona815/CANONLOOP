"use client";

import Image from "next/image";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import {
  Check, CheckCircle2, ChevronRight, Database, Download,
  FileCheck2, FileText, GitBranch, ImageIcon, Play, RotateCcw,
  ScanSearch, ShieldCheck, Sparkles, TriangleAlert, Workflow, XCircle
} from "lucide-react";
import { assets, canonAnchors, replay, steps } from "@/data/replay";

const iconMap = [FileText, ShieldCheck, Workflow, Sparkles, ScanSearch, RotateCcw, ImageIcon, GitBranch, Database];

const stageCopy = [
  ["Project brief", "A four-format launch campaign using only synthetic references and affirmative rights confirmation."],
  ["Visual Canon v1", "Five fixed identity anchors define what may not drift across formats."],
  ["Campaign plan", "Four deliverables share one prompt prefix, a two-retry budget, and a bounded cost cap."],
  ["Generation runs", "Four formats generated; the vertical story is routed to the critic after a deterministic fault fixture."],
  ["Continuity review", "The critic rejects one symbol constraint while preserving passing identity, style, palette, and format checks."],
  ["Repair comparison", "A parent-linked repair patches only the emblem geometry and keeps every passing element unchanged."],
  ["Approved campaign", "Four approved formats move to the release package. The rejected attempt remains in provenance."],
  ["Provenance explorer", "Every asset exposes provider, model, hashes, parent run, evaluation, and decision evidence."],
  ["B2 storage inspector", "The Replay object layout is representative and explicitly unverified until a real B2 round trip succeeds."]
] as const;

export function DemoWorkspace() {
  const search = useSearchParams();
  const requestedView = search.get("view");
  const initial = requestedView === "canon" ? 1 : requestedView === "provenance" ? 7 : 4;
  const [activeStep, setActiveStep] = useState(initial);
  const [running, setRunning] = useState(() => search.get("autoplay") === "1");
  const [mode, setMode] = useState<"replay" | "mock" | "live">("replay");

  useEffect(() => {
    if (!running) return;
    const timer = window.setInterval(() => setActiveStep(current => {
      if (current >= steps.length - 1) { setRunning(false); return current; }
      return current + 1;
    }), 1800);
    return () => window.clearInterval(timer);
  }, [running]);

  const selected = useMemo(() => stageCopy[activeStep], [activeStep]);
  const progress = Math.round(((activeStep + 1) / steps.length) * 100);

  return (
    <main className="workspace-shell">
      <header className="workspace-header">
        <Link className="brand" href="/"><span className="brand-orbit" />CANONLOOP</Link>
        <div className="campaign-crumb">Campaign <ChevronRight size={13} /><strong>SIX-LINE HALO</strong></div>
        <div className="mode-switch" aria-label="Run mode">
          {(["replay", "mock", "live"] as const).map(item => <button key={item} className={mode === item ? "selected" : ""} onClick={() => setMode(item)}>{item === "replay" && <Play size={12} />}{item}</button>)}
        </div>
        <div className="workspace-actions">
          <button className="primary-button compact" onClick={() => { setActiveStep(0); setRunning(true); }}><Play size={15} /> {running ? "Running…" : "Run Guided Demo"}</button>
          <button className="secondary-button compact" onClick={() => setActiveStep(7)}><GitBranch size={15} /> Inspect Provenance</button>
          <a className="quiet-button compact" href="/api/package"><Download size={15} /> Download Package</a>
        </div>
      </header>

      <aside className="step-rail">
        <div className="rail-scroll">
          {steps.map((step, index) => {
            const Icon = iconMap[index];
            return <button key={step} className={activeStep === index ? "step active" : "step"} onClick={() => { setRunning(false); setActiveStep(index); }}>
              <span>{index < activeStep ? <CheckCircle2 size={17} /> : <Icon size={17} />}</span>{step}
            </button>;
          })}
        </div>
        <div className="campaign-status"><small>Campaign status</small><strong>{selected[0]}</strong><div className="progress"><i style={{ width: `${progress}%` }} /></div><span>{progress}% complete</span></div>
        <div className="mode-disclosure"><TriangleAlert size={15} /><div><strong>{mode.toUpperCase()} MODE</strong><span>{mode === "live" ? "Credentials required. No call has been made." : mode === "mock" ? "Local development simulation." : "Recorded local fixture · B2 unverified."}</span></div></div>
      </aside>

      <section className="workspace-canvas">
        <div className="canvas-heading"><div><small>{steps[activeStep]}</small><h1>{selected[0]}</h1><p>{selected[1]}</p></div><button className="quiet-button compact" onClick={() => setActiveStep(1)}>View Canon <ChevronRight size={14} /></button></div>
        {activeStep === 0 && <BriefStage />}
        {activeStep === 1 && <CanonStage />}
        {activeStep === 2 && <PlanStage />}
        {activeStep >= 3 && activeStep <= 6 && <MediaStage activeStep={activeStep} />}
        {activeStep === 7 && <ProvenanceStage />}
        {activeStep === 8 && <StorageStage />}
        <RunTimeline activeRun={activeStep >= 5 ? "run-007r" : "run-007"} />
      </section>

      <aside className="inspector"><ContinuityInspector activeStep={activeStep} /></aside>
    </main>
  );
}

function BriefStage() {
  return <div className="brief-stage"><div><small>Objective</small><h2>Launch one fictional single across four production formats.</h2><p>Maintain the masked performer, jacket, cyan ear light, six-line emblem, palette, and cinematic editorial treatment.</p></div><div className="brief-list"><span><Check /> Synthetic reference set</span><span><Check /> Rights confirmed</span><span><Check /> Four image deliverables</span><span><Check /> Two-repair maximum</span></div></div>;
}

function CanonStage() {
  return <div className="canon-stage"><figure><Image src="/media/square-cover.png" fill sizes="520px" alt="Synthetic Visual Canon reference" /></figure><div><small>Fixed attributes</small><ul>{canonAnchors.map(anchor => <li key={anchor}><ShieldCheck size={17} />{anchor}</li>)}</ul><div className="palette-row"><i /><i /><i /></div><p>Mutable: crop, pose, negative space, and layout safe areas.</p></div></div>;
}

function PlanStage() {
  return <div className="plan-stage">{assets.filter(asset => asset.status !== "failed").map((asset, index) => <div key={asset.id}><span>0{index + 1}</span><Image src={asset.image} width={86} height={86} alt="" /><section><small>{asset.format}</small><h3>{asset.title.replace(" · repaired", "")}</h3><p>Preserve five anchors · priority {index + 1} · retry budget {index === 1 ? 2 : 1}</p></section><strong>READY</strong></div>)}</div>;
}

function MediaStage({ activeStep }: { activeStep: number }) {
  const showRepair = activeStep >= 5;
  return <div className="media-stage">
    <figure className="asset-card square"><Image src="/media/square-cover.png" fill sizes="320px" alt="Approved square cover" /><figcaption><span>Square Cover · 1:1</span><strong><CheckCircle2 /> Approved</strong></figcaption></figure>
    <div className="story-pair">
      <figure className="asset-card story failed"><Image src="/media/vertical-story-failed.png" fill sizes="220px" alt="Rejected vertical story" /><figcaption><span>Attempt 1</span><strong><XCircle /> Symbol failed</strong></figcaption></figure>
      {showRepair && <><ChevronRight className="pair-arrow" /><figure className="asset-card story repaired"><Image src="/media/vertical-story-repaired.png" fill sizes="220px" alt="Repaired vertical story" /><figcaption><span>Attempt 2</span><strong><CheckCircle2 /> Repaired</strong></figcaption></figure></>}
    </div>
    <div className="right-assets"><figure className="asset-card banner"><Image src="/media/landscape-banner.png" fill sizes="420px" alt="Approved landscape banner" /><figcaption><span>Landscape Banner · 16:9</span><strong><CheckCircle2 /> Approved</strong></figcaption></figure><figure className="asset-card poster"><Image src="/media/poster.png" fill sizes="180px" alt="Approved poster" /><figcaption><span>Poster · 2:3</span><strong><CheckCircle2 /> Approved</strong></figcaption></figure></div>
  </div>;
}

function ProvenanceStage() {
  return <div className="provenance-stage"><div className="lineage-node"><FileCheck2 /><small>run-007</small><strong>Rejected</strong><span>symbol 0.64</span></div><ChevronRight /><div className="lineage-node repair"><RotateCcw /><small>repair-v1</small><strong>Constraint patch</strong><span>symbol only</span></div><ChevronRight /><div className="lineage-node approved"><ShieldCheck /><small>run-007r</small><strong>Approved</strong><span>symbol 0.94</span></div><div className="manifest-json"><code>{`{
  "pipeline": "canonloop-image-v1",
  "provider": "mock",
  "model": "canonloop-fixture-v1",
  "run_id": "run-007r",
  "parent_run_id": "run-007",
  "canonical_hash": "2f5b…c81a",
  "manifest_verified": true,
  "storage_verified": false
}`}</code></div></div>;
}

function StorageStage() {
  return <div className="storage-stage"><div className="storage-banner"><Database /><div><h2>Replay object index</h2><p>Representative B2 layout. No live HEAD or round-trip claim is made.</p></div><strong>UNVERIFIED</strong></div><table><thead><tr><th>Object key</th><th>Run</th><th>State</th><th>SHA-256</th></tr></thead><tbody>{assets.map(asset => <tr key={asset.id}><td>{asset.b2ObjectKey}</td><td>{asset.runId}</td><td>{asset.status}</td><td>{asset.sha256.slice(0, 12)}…</td></tr>)}</tbody></table></div>;
}

function RunTimeline({ activeRun }: { activeRun: string }) {
  const runs = ["run-005", "run-006", "run-007", "run-007r", "run-008"];
  return <div className="run-timeline"><div className="timeline-title"><span>Generation run lineage</span><small>Local fixture timestamps · no live claim</small></div><div className="timeline-runs">{runs.map((run, index) => <div className={run === activeRun ? "timeline-run current" : run === "run-007" ? "timeline-run failed" : "timeline-run"} key={run}><span>{run === "run-007" ? <XCircle /> : <CheckCircle2 />}</span><strong>{run}</strong><small>{index === 2 ? "Failed symbol" : index === 3 ? "Parent: run-007" : assets.filter(a => a.runId === run)[0]?.title ?? "Approved"}</small></div>)}</div></div>;
}

function ContinuityInspector({ activeStep }: { activeStep: number }) {
  const repaired = activeStep >= 5;
  const scores = repaired ? replay.repairedScores : replay.failedScores;
  return <><div className="inspector-heading"><div><small>Selected run</small><strong>{repaired ? "run-007r · repaired" : "run-007 · attempt 1"}</strong></div><span className={repaired ? "status approved" : "status failed"}>{repaired ? "APPROVED" : "FAILED"}</span></div><section className="score-section"><h2>Continuity scores</h2>{Object.entries(scores).map(([label, value]) => <div className={label === "symbol" ? "score-row focus" : "score-row"} key={label}><span>{label}</span><strong>{value.toFixed(2)}</strong><i><b style={{ width: `${value * 100}%` }} /></i></div>)}</section><section className="finding-section"><small>Drift finding</small><h3>Emblem has 4 wing lines; canon requires 6.</h3><div className="symbol-compare"><div><span>RUN OUTPUT</span><b className="symbol four">Ⅱ</b></div><ChevronRight /><div><span>CANON</span><b className="symbol six">Ⅲ</b></div></div></section><section className="repair-plan"><small>Repair plan · constrained</small><p><strong>Preserve</strong> identity, wardrobe, palette, lighting, crop</p><p><strong>Change</strong> emblem geometry to six lines</p><p><strong>Budget</strong> 1 of 2 repairs used</p></section><section className="provider-section"><small>Provider / model</small><dl><div><dt>Provider</dt><dd>Genblaze MockProvider</dd></div><div><dt>Model</dt><dd>canonloop-fixture-v1</dd></div><div><dt>Manifest</dt><dd>verified locally</dd></div><div><dt>B2</dt><dd>replay · unverified</dd></div></dl></section></>;
}
