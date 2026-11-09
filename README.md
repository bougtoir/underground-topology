# Beyond Like-for-Like Undergrounding

Reproducible study pipeline for:
**"The Value of Topology Flexibility at Infrastructure Renewal: A Feasibility-Gated Geospatial Assessment of Low-Voltage Re-Layout During Undergrounding"**
(journal-neutral repository; see `manuscript/` for the current submission target)

## Layout
- `config/study.yaml` — frozen parameters (single source of truth)
- `provenance/` — source_registry.csv, municipality_candidates.csv, decision_log.md, CHARACTER_AUDIT.txt
- `data/raw/` — immutable downloaded data + per-file sha256 (never overwrite originals)
- `data/processed/` — derived artifacts
- `scripts/` — numbered phase scripts (run in order)
- `analysis/` — machine-readable outputs (feeds manuscript_values.csv)
- `manuscript/` — DOCX build + submission package
- `tests/` — unit/integration tests

## Reproduce
```
python3 -m venv .venv && .venv/bin/pip install -r requirements.lock.txt
make all
```

## Labels
Every quantity is labelled observed / reconstructed / modeled / assumed / sensitivity.
Never call a reconstructed network an observed utility network.
