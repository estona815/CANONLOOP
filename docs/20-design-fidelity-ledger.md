# Design fidelity ledger

Compared sources:

- Landing concept: `artifacts/design/landing-concept.png`
- Workspace concept: `artifacts/design/workspace-concept.png`
- Final landing evidence: `artifacts/screenshots/01-landing.png`
- Final workspace evidence: `artifacts/screenshots/06-repair-comparison.png`

## Preserved decisions

1. **Information architecture** — The concept's campaign header, mode switch, action bar, nine-stage rail, central media canvas, and right-side inspector remain the dominant workspace structure.
2. **Visual system** — Deep navy surfaces, cyan interaction states, amber canon/repair cues, red failure states, green approvals, hairline borders, and compact uppercase metadata carry through to the implementation.
3. **Repair narrative** — The rejected vertical asset and parent-linked repaired asset remain adjacent, while approved square, landscape, and poster assets stay unchanged.
4. **Inspector density** — Weighted continuity scores, drift finding, constrained repair plan, provider/model disclosure, run lineage, and storage status remain visible together at desktop width.
5. **Landing hierarchy** — A large editorial claim, three proof-oriented actions, a multi-format product preview, the six-step loop, before/after comparison, and provenance flow match the landing concept's hierarchy.
6. **Responsive behavior** — At 390 px the workspace becomes a readable single column; the header actions wrap, assets stack, and the inspector follows the media without horizontal page overflow.

## Intentional implementation changes

- The concept's example `Lumina AI` provider label was replaced with the truthful `Genblaze MockProvider` and `canonloop-fixture-v1` labels.
- All B2 rows are labeled `Replay · unverified`; the concept's storage table is not presented as proof of a live upload.
- Generated synthetic masked-performer media replaced any ambiguous placeholder imagery and is documented in the asset manifest.
- Below-fold comparison and evidence images use eager loading so full-page evidence captures render consistently.

## Verification

- Desktop: 1440 × 1000 workspace evidence.
- Mobile: 390 × 844 viewport evidence in `10-mobile-landing.png` and `11-mobile-demo.png`.
- Browser console: no errors during desktop and mobile checks.
