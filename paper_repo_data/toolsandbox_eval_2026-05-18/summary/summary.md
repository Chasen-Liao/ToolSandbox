# ToolSandbox Evaluation Summary (2026-05-18)

## Model-Level Comparison

| Model | Passed/Total | Pass Rate | Avg Score | Avg Latency (ms) | Tool Call Acc | Tool Args Acc |
|---|---:|---:|---:|---:|---:|---:|
| GLM-5.1 | 19/24 | 79.2% | 0.808 | 9751 | 79.2% | 79.2% |
| RKLLM | 17/24 | 70.8% | 0.767 | 21406 | 70.8% | 70.8% |

## Category Breakdown - GLM-5.1

| Category | Passed/Total | Pass Rate | Avg Score | Avg Latency (ms) |
|---|---:|---:|---:|---:|
| 10 Distraction Tools | 2/2 | 100.0% | 1.000 | 11111 |
| 3 Distraction Tools | 2/2 | 100.0% | 1.000 | 5441 |
| All Tools Available | 2/2 | 100.0% | 1.000 | 12018 |
| Canonicalization | 2/2 | 100.0% | 1.000 | 7085 |
| Multi-Tool / State Dependency | 0/2 | 0.0% | 0.100 | 22601 |
| No Tool Required | 1/1 | 100.0% | 1.000 | 2297 |
| Single Tool Call - Contacts | 4/4 | 100.0% | 1.000 | 11581 |
| Single Tool Call - Messaging | 2/2 | 100.0% | 1.000 | 5148 |
| Single Tool Call - Search | 2/3 | 66.7% | 0.733 | 9190 |
| Single Tool Call - Settings | 2/4 | 50.0% | 0.500 | 7758 |

## Category Breakdown - RKLLM

| Category | Passed/Total | Pass Rate | Avg Score | Avg Latency (ms) |
|---|---:|---:|---:|---:|
| 10 Distraction Tools | 2/2 | 100.0% | 1.000 | 28430 |
| 3 Distraction Tools | 1/2 | 50.0% | 0.600 | 13471 |
| All Tools Available | 0/2 | 0.0% | 0.200 | 73029 |
| Canonicalization | 1/2 | 50.0% | 0.600 | 14009 |
| Multi-Tool / State Dependency | 1/2 | 50.0% | 0.600 | 34841 |
| No Tool Required | 1/1 | 100.0% | 1.000 | 6177 |
| Single Tool Call - Contacts | 3/4 | 75.0% | 0.800 | 15506 |
| Single Tool Call - Messaging | 2/2 | 100.0% | 1.000 | 19426 |
| Single Tool Call - Search | 2/3 | 66.7% | 0.733 | 13561 |
| Single Tool Call - Settings | 4/4 | 100.0% | 1.000 | 9608 |
