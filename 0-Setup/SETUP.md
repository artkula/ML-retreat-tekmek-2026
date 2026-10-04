# AI Retreat 2026, step 2: setup before the retreat

Skepparholmen, 13 to 14 October 2026. Please do these steps before you leave. Most of the time goes into downloads, so plan about 45 minutes. Bring your laptop and charger.

Use only public or synthetic data with the cloud tools below (Colab, Gemini, Claude, Antigravity, Codex). KTH rules: intra.kth.se, “Recommendations for the use of AI”.

## Day 1: Google Colab

1. Sign in at [colab.research.google.com](https://colab.research.google.com) with a Google account. A personal Gmail account works.
2. Open the [CNN notebook in Colab](https://colab.research.google.com/github/artkula/ML-retreat-tekmek-2026/blob/main/1-CNN/CNN_handson.ipynb). All material is at [github.com/artkula/ML-retreat-tekmek-2026](https://github.com/artkula/ML-retreat-tekmek-2026).
3. In Colab, choose Runtime, Change runtime type, T4 GPU, and run the first cell. If it runs without an error, you are ready. The free plan gives enough GPU time for the day.

## Day 2: language models and agents

### Gemini API key, for the clinical data notebook

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey), sign in with your Google account and click “Create API key”. Copy the key.
2. In Colab, click the key icon (Secrets) in the left bar, add a secret named `GOOGLE_API_KEY` with your key as the value, and switch on “Notebook access”.

The free tier is enough. Keep the key in Secrets, never in the notebook text.

### Claude: choose one of two options

**Option A: Claude Pro (paid, recommended).** It includes Claude Code, the agent we use in the afternoon hands-on. Buy it at [claude.com/pricing](https://claude.com/pricing); it can be cancelled after the retreat. Then install Claude Code:

- Windows, in PowerShell: `irm https://claude.ai/install.ps1 | iex`. Also install [Git for Windows](https://git-scm.com/downloads/win).
- macOS or Linux, in a terminal: `curl -fsSL https://claude.ai/install.sh | bash`

Open a new terminal, type `claude` and log in when the browser opens. `claude --version` should print a version number.

**Option B: a free account** at [claude.ai](https://claude.ai). You can chat with Claude in the browser, but the free plan does not include Claude Code. In the hands-on you then work together with a colleague who has option A, or with Antigravity or Codex below.

### Optional: Antigravity or Codex

- **Antigravity** (Google, free for individuals): download from [antigravity.google](https://antigravity.google) and sign in with your Google account.
- **Codex** (OpenAI): needs a ChatGPT account, either KTH ChatGPT Edu or your own. Install the app or the command-line tool from [developers.openai.com/codex](https://developers.openai.com/codex), then sign in with ChatGPT.

### A local model with Ollama

A local model runs on your own laptop, and the data stay there.

1. Install Ollama from [ollama.com/download](https://ollama.com/download).
2. Pick the model in the table that fits your computer.
3. Download and try it in a terminal with the two commands below the table.

| Your computer | Model | Download |
|---|---|---|
| 8 GB memory | `qwen3.5:2b` | 2.7 GB |
| 16 GB memory | `qwen3.5:4b` | 3.4 GB |
| 32 GB memory, or a graphics card with 8 GB or more, or a Mac with Apple silicon and 16 GB | `qwen3.5:9b` | 6.6 GB |
| A graphics card with 24 GB or more, or a Mac with Apple silicon and 32 GB or more | `qwen3.5:27b` | 17 GB |

To see your memory: on Windows, Settings, System, About (“Installed RAM”), and Task Manager, Performance, GPU (“Dedicated GPU memory”); on a Mac, Apple menu, About This Mac.

Replace `4b` with your choice:

```
ollama pull qwen3.5:4b
ollama run qwen3.5:4b "Explain the finite element method in two sentences."
```

If the answer takes more than a minute, take the next smaller model. A laptop without a graphics card writes a few words per second, which is enough to try it.

## Questions

Artem Kulachenko, artem@kth.se
