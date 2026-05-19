# ToolSandbox Evaluation Data Package (2026-05-18)

This folder is prepared for direct inclusion in the paper repository as a reproducible benchmark artifact bundle.

## Contents

- `raw/`
  - `glm51_toolsandbox_report.json`: Full raw evaluation output for GLM-5.1.
  - `rkllm_toolsandbox_report.json`: Full raw evaluation output for RKLLM.
- `reports/`
  - `glm51_toolsandbox_report.md`: Human-readable GLM-5.1 report.
  - `rkllm_toolsandbox_report.md`: Human-readable RKLLM report.
- `summary/`
  - `model_summary.csv`: Model-level aggregate metrics.
  - `category_summary.csv`: Category-level aggregate metrics.
  - `summary.md`: Paper-ready markdown summary tables.
- `metadata/`
  - `run_metadata.json`: Run timestamps, model endpoint metadata, and source file mapping.

## Recommended Citation in Paper

Use `raw/*.json` as the primary source of record for quantitative analysis, and `summary/*.csv` for generated tables/plots.

## Notes

- All data in this package is generated from the local rerun on 2026-05-18.
- JSON files preserve per-case details including tool calls, final responses, errors, and full response traces.
