# Luna & Quasar

Open-source fine-tuning of small and large agentic coding models, trained on
**real extracted engineering work** rather than synthetic toy problems.

- **Luna 1** — small model, fine-tune of Qwen2.5-Coder (small variant)
- **Quasar 1** — large model, fine-tune of Qwen2.5-Coder (large variant), planned

Both are scoped to teach exactly three things on top of what the base model
already knows how to do (write correct code):

1. **Updated framework/SDK/library knowledge**
2. **Reasoning and planning before acting** (real agentic behavior — read
   context, plan, then act, don't guess)
3. **Efficient tool/token usage** (no wasted tool calls, no rambling)

## What lives where

- **Dataset** — hosted entirely on the HuggingFace Hub:
  [huggingface.co/datasets/sinamsv00/Luna](https://huggingface.co/datasets/sinamsv00/Luna).
  Raw records, the ChatML conversion script, and the dataset card (schema,
  extraction methodology, source projects) all live there. This GitHub repo
  does **not** store or mirror the dataset.
- **This repo (GitHub)** — the Google Colab notebook(s) for turning that
  Hub-hosted dataset into a trained model, plus the fine-tuning
  documentation and any training-time code.

This project is fully open-source end-to-end: dataset, scripts, notebooks,
fine-tuning documentation, and eventually the **trained model weights
themselves** will all be published publicly.

```
.
├── notebooks/
│   └── 01_prepare_chatml.ipynb   # pulls raw data from the HF Hub, converts to ChatML
│                                  # (also mirrored in the HF dataset repo for convenience)
├── training/                     # (coming soon) LoRA/QLoRA SFT notebooks + scripts for Luna 1
├── eval/                         # (coming soon) eval harness, optimal vs wasteful comparisons
└── docs/                         # (coming soon) fine-tuning write-up: config choices, hardware,
                                   # hyperparameters, what worked / what didn't
```

## Source projects being mined for training data

- **[Nebula](#)** — Rust/Python AI assistant with Web, Telegram, and Discord
  adapters over a shared core (auth, memory, coin/usage limits, AI provider
  routing).
- **[NumRS](#)** — Rust linear algebra library.

Real bugs, refactors, feature additions, and multi-file changes from these
projects' commit history and code structure are extracted into training
records. Full schema and methodology are documented on the HF dataset card,
not here.

## Quickstart

`notebooks/01_prepare_chatml.ipynb` runs standalone in Google Colab — no
local setup needed. It pulls the raw dataset directly from the HF Hub,
converts it to Qwen2.5-Coder's ChatML format, and validates the output
against the actual tokenizer/chat template for whichever checkpoint you're
targeting.

Open it in Colab, set `HF_REPO_ID` to the dataset repo, and run top to
bottom.

## Status

- [x] First dataset topic batch published on HF (`nebula_backend`, 8 records)
- [x] ChatML conversion + Colab prep notebook
- [ ] Additional dataset topic batches (published on HF, not here)
- [ ] LoRA/QLoRA training notebook for Luna 1 (Colab-compatible, small
      footprint by design)
- [ ] Fine-tuning documentation (config, hardware, hyperparameters)
- [ ] Eval harness
- [ ] Quasar 1 pipeline

## Contributing

This project is fully open. Dataset contributions (new topic batches) go
through the HF dataset repo, not here — see its dataset card for the record
schema and quality bar. Contributions to this repo (notebooks, training
code, eval tooling, docs) are welcome via PR once those pieces exist.

## License

MIT.
