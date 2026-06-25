---
name: mlops-model-lifecycle
description: "Umbrella workflow for ML/AI model lifecycle work: Hugging Face assets, local and server inference, evaluation, experiment tracking, DSPy programs, model surgery, audio/image model utilities, and deployment verification."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mlops, models, inference, evaluation, deployment, huggingface, vllm, llama-cpp, wandb, dspy]
    related_skills: []
---

# MLOps model lifecycle

Use this umbrella when the user asks to operate models, datasets, inference servers, evaluation harnesses, experiment trackers, or model-transformation utilities. Prefer one class-level routing pass here over loading many narrow provider/tool skills.

## Routing map

| User need | Section |
|---|---|
| Find/download/upload HF models or datasets | Hugging Face assets |
| Run local GGUF inference or convert/quantize for local use | Local inference with llama.cpp |
| Serve an OpenAI-compatible LLM endpoint | High-throughput serving with vLLM |
| Benchmark LLMs on MMLU/GSM8K/etc. | LLM evaluation |
| Track experiments/sweeps/artifacts | Experiment tracking |
| Build prompt/RAG programs with optimization | DSPy research programs |
| Abliterate/refuse-surgery experiments | Model surgery |
| Generate audio/music or segment images | Modality-specific model utilities |

## Shared workflow

1. Identify the artifact class first: model weights, dataset, inference endpoint, benchmark run, experiment log, or generated media/masks.
2. Check credentials and commands before promising work (`HF_TOKEN`, `WANDB_API_KEY`, CUDA/GPU availability, model files, ports).
3. Use a disposable work directory for downloads/conversions unless the user specifies a project path.
4. Prefer small smoke tests before long runs: one prompt, one batch, one sample, one benchmark task, or one API health check.
5. Record exact commands, model IDs, revisions, quantization/evaluation settings, output paths, and verification output.

## Tool-specific notes

### Hugging Face assets
Use `hf`/`huggingface-cli` for login, search, download, upload, and repo management. Always pin model IDs and revisions when reproducibility matters. For large downloads, verify file presence and size after completion.

### Local inference with llama.cpp
Use llama.cpp for GGUF local inference, quantization, and simple local servers. Verify the binary exists, model path is valid, and the chosen context/threads/GPU layers fit the host.

### High-throughput serving with vLLM
Use vLLM when the user needs an OpenAI-compatible server, batching, GPU throughput, quantized serving, or production-ish endpoint behavior. Verify startup with `/v1/models` or a minimal `/v1/chat/completions` call.

### LLM evaluation
Use lm-eval-harness for benchmark runs. Start with a tiny task/limit smoke test, then scale. Preserve task names, few-shot count, model args, seeds, and result JSON paths.

### Experiment tracking
Use W&B for experiment logs, artifacts, sweeps, and model registry operations. Confirm project/entity, offline vs online mode, and auth before launching a run.

### DSPy research programs
Use DSPy for declarative LM programs, prompt/RAG optimization, and metric-driven compilation. Keep the metric and train/dev split explicit.

### Model surgery
Use OBLITERATUS-style workflows only for controlled research. Keep source model, layer/direction settings, refusal/eval prompts, and before/after tests together.

### Modality-specific model utilities
AudioCraft/MusicGen/AudioGen and Segment Anything/SAM are model-utility workflows. Verify dependencies and run one small generation/segmentation before scaling.

## Preserved source playbooks

Full original skill packages from absorbed narrow skills are preserved under `references/source-packages/<skill-name>/` with the former `SKILL.md` renamed to `source-skill.md` to avoid registering nested skills. Consult those packages for detailed command recipes, templates, scripts, and provider quirks.

## Verification checklist

- [ ] Required CLI commands and credentials are present or the blocker is reported.
- [ ] A smoke test was run before long jobs.
- [ ] Output paths, endpoint URLs, benchmark result files, or artifact IDs are reported.
- [ ] Model IDs/revisions/settings are captured for reproducibility.
