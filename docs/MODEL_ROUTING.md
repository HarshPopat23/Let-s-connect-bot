# Model Routing

OLLM avoids using a model to select another model. A deterministic router classifies the question from length, number of parts and topic words.

## Easy tier

Default model: `qwen3:4b`

Used for short definitions, link requests, basic navigation and simple first-step questions. This model is smaller and usually faster on CPU.

Examples:

- What is a pull request?
- How do I start contributing?
- Where is the LFX guide?

## Standard tier

Default model: `mistral:7b-instruct`

Used for normal workflow guidance that requires several retrieved chunks and practical steps.

Examples:

- My pull request has not been reviewed for two weeks. What should I do?
- How should I explore a large Go repository for this issue?

## Complex tier

Default model: `mistral-nemo:12b`

Used for architecture, security, license compatibility, governance, proposal review, debugging strategy and long multi-part questions. It needs more memory and is slow on free CPU infrastructure.

## Fallback behavior

Before generation, OLLM asks Ollama which models are installed. If the selected model is missing, it chooses an installed lower-cost model. If no configured model exists, it returns an operational error instead of silently using a cloud API.

All model names are configurable in `.env`. Model tiers affect answer generation only. Retrieval always uses the configured embedding model.

