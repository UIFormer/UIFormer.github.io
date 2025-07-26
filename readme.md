# Artifact: From User Interface to Agent Interface: Efficiency Optimization of UI Representations for LLM Agents

This artifact includes anonymized code, traces, and logs used in our experiments, and demonstrates the effectiveness of our proposed UIFormer.

## Directory Overview

- `uiformer/` – Runtime framework for executing UIFormer transformations.
It contains the core logic used to apply UI representation transformations during agent execution.
A lightweight script `sample_use.py` demonstrates how to run UIFormer on a sample UI input. 
- `traces/` – Agent interaction traces on the Sphinx benchmark.
To comply with anonymization requirements, we have manually selected a subset of traces that are free of any identifiable or proprietary content.
These traces are used to showcase how UIFormer operates in real-world scenarios.
- `logs/` – Evaluation logs used to reproduce the main results reported in the paper.
This folder contains aggregated metrics such as token counts and success rates across different LLM agents and UI benchmarks.
All logs are generated from anonymized traces and aligned with the experimental results shown in the paper.

All components have been anonymized or masked to remove sensitive or proprietary information.