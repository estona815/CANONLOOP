import Image from "next/image";
import Link from "next/link";
import {
  ArrowRight, Archive, Check, CircleDot, GitBranch, LockKeyhole, RotateCcw,
  ScanSearch, ShieldCheck, Sparkles, Workflow
} from "lucide-react";

const workflow = [
  { name: "Canon", detail: "Lock identity anchors", icon: CircleDot },
  { name: "Plan", detail: "Brief every format", icon: Workflow },
  { name: "Generate", detail: "Run provider steps", icon: Sparkles },
  { name: "Critique", detail: "Classify drift", icon: ScanSearch },
  { name: "Repair", detail: "Patch only failures", icon: RotateCcw },
  { name: "Archive", detail: "Preserve evidence", icon: Archive }
];

export default function Home() {
  return (
    <main className="landing">
      <header className="site-header">
        <Link className="brand" href="/" aria-label="CANONLOOP home"><span className="brand-orbit" />CANONLOOP</Link>
        <nav aria-label="Primary navigation">
          <a href="#workflow">How it works</a><a href="#provenance">Provenance</a><a href="#security">Security</a>
        </nav>
        <Link className="quiet-button" href="/demo?mode=replay">Open workspace <ArrowRight size={15} /></Link>
      </header>

      <section className="hero section-shell">
        <div className="hero-copy">
          <h1>Keep generative campaigns visually consistent without reviewing every asset by hand.</h1>
          <p>CanonLoop plans, generates, critiques, repairs, and archives multi-format media with autonomous agents and verifiable provenance.</p>
          <div className="hero-actions">
            <Link className="primary-button" href="/demo?scenario=six-line-halo&mode=replay&autoplay=1">Watch the Guided Demo <ArrowRight size={17} /></Link>
            <Link className="secondary-button" href="/demo?view=canon">Build a Visual Canon</Link>
            <Link className="text-button" href="/demo?view=provenance">Explore a Verified Run <ArrowRight size={15} /></Link>
          </div>
          <p className="hero-note"><ShieldCheck size={15} /> Synthetic references · deterministic Replay · no account required</p>
        </div>
        <div className="hero-product" aria-label="Campaign continuity preview">
          <div className="product-topline"><span>SIX-LINE HALO</span><span className="verified"><Check size={13} /> Replay ready</span></div>
          <div className="campaign-preview">
            <figure className="preview-square"><Image src="/media/square-cover.png" fill sizes="260px" alt="Synthetic masked performer square cover" /></figure>
            <figure className="preview-story"><Image src="/media/vertical-story-repaired.png" fill sizes="180px" alt="Synthetic masked performer vertical story" /></figure>
            <figure className="preview-banner"><Image src="/media/landscape-banner.png" fill sizes="360px" alt="Synthetic masked performer landscape banner" /></figure>
          </div>
          <div className="drift-strip"><span className="warning-dot" /><div><strong>Drift detected</strong><small>Symbol: 4 lines observed · 6 required</small></div><ArrowRight size={16} /><div><strong className="approved-copy">Repaired</strong><small>Only the emblem constraint changed</small></div></div>
        </div>
      </section>

      <section id="workflow" className="workflow-section section-shell">
        <div className="section-heading"><h2>Autonomous visual continuity workflow</h2><p>One controlled loop keeps the identity stable while formats change.</p></div>
        <div className="workflow-rail">
          {workflow.map(({ name, detail, icon: Icon }, index) => (
            <div className={name === "Repair" ? "workflow-item active" : "workflow-item"} key={name}>
              <div className="workflow-node"><Icon size={21} /></div><strong>{name}</strong><span>{detail}</span>
              {index < workflow.length - 1 && <i aria-hidden="true" />}
            </div>
          ))}
        </div>
      </section>

      <section className="comparison-section section-shell">
        <div className="section-heading"><h2>Detect drift. Repair only what fails.</h2><p>Passing assets stay untouched; the failed constraint gets a parent-linked second attempt.</p></div>
        <div className="comparison-layout">
          <figure className="compare-frame failed-frame"><Image src="/media/vertical-story-failed.png" fill sizes="420px" loading="eager" alt="Rejected synthetic story attempt" /><figcaption><span>Attempt 1 · rejected</span><strong>4-line emblem</strong></figcaption></figure>
          <div className="repair-bridge"><GitBranch size={24} /><span>constraint patch</span><strong>symbol only</strong><ArrowRight size={19} /></div>
          <figure className="compare-frame approved-frame"><Image src="/media/vertical-story-repaired.png" fill sizes="420px" loading="eager" alt="Approved repaired synthetic story" /><figcaption><span>Attempt 2 · approved</span><strong>6-line emblem</strong></figcaption></figure>
        </div>
      </section>

      <section id="provenance" className="evidence-section section-shell">
        <div className="evidence-copy"><h2>Every decision leaves evidence.</h2><p>Provider, model, prompt version, asset hash, critic result, repair lineage, and object path are captured in one replayable record.</p><Link className="primary-button compact" href="/demo?view=provenance">Inspect provenance <ArrowRight size={16} /></Link></div>
        <div className="evidence-flow">
          <div><Image src="/media/landscape-banner.png" fill sizes="210px" loading="eager" alt="Synthetic campaign asset" /></div><ArrowRight />
          <div className="manifest-card"><small>manifest.json</small><code>{`{\n  "runId": "run-007r",\n  "parent": "run-007",\n  "verified": true\n}`}</code></div><ArrowRight />
          <div className="storage-block"><LockKeyhole size={27} /><strong>Backblaze B2</strong><small>Replay object index is clearly marked unverified until live credentials are supplied.</small></div>
        </div>
      </section>

      <section id="security" className="production-section section-shell">
        <div><ShieldCheck size={24} /><h3>Rights first</h3><p>Only synthetic or authorized references enter the pipeline.</p></div>
        <div><LockKeyhole size={24} /><h3>Server-only secrets</h3><p>Provider and B2 keys never reach the browser.</p></div>
        <div><GitBranch size={24} /><h3>Bounded autonomy</h3><p>Cost caps, two repairs, then human review.</p></div>
      </section>

      <section className="final-cta section-shell"><div><h2>One visual identity. Every format. No drift.</h2><p>Run the complete failure-to-repair workflow without an account or API key.</p></div><Link className="primary-button" href="/demo?scenario=six-line-halo&mode=replay&autoplay=1">Run Guided Demo <ArrowRight size={17} /></Link></section>
      <footer className="site-footer"><span>CANONLOOP · Autonomous visual continuity director</span><span>MIT licensed · Synthetic demo media</span></footer>
    </main>
  );
}
