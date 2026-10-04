# AI Retreat 2026, step 2: setup before the retreat

Skepparholmen, 13 to 14 October 2026. Please do these steps, including all downloads, before you leave: the hotel network is shared by everyone. Plan about 45 minutes. Bring your laptop and charger.

Use the synthetic data we supply, or public material that you are allowed to process, with the cloud tools below (Colab, Gemini, Claude, Antigravity, Codex). KTH rules: [Recommendations for the use of AI](https://intra.kth.se/en/it/natverk/regler-policys/rekommendationer-vid-anvandning-av-ai-1.1446862).

## Day 1: Google Colab

1. Sign in at [colab.research.google.com](https://colab.research.google.com) with a Google account. A personal Gmail account works.
2. Open the [CNN notebook in Colab](https://colab.research.google.com/github/artkula/ML-retreat-tekmek-2026/blob/main/1-CNN/CNN_handson.ipynb). All material is at [github.com/artkula/ML-retreat-tekmek-2026](https://github.com/artkula/ML-retreat-tekmek-2026).
3. In Colab, choose Runtime, Change runtime type, T4 GPU, and run the first cell. If it runs without an error, you are ready.

Free GPU time in Colab is limited and not guaranteed. If Colab offers you no GPU on the day, tell us at the start of the session.

## Day 2: language models and agents

### Gemini API key, for the clinical data notebook

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey), sign in with your Google account and click “Create API key”. If it asks for a project, take the one it offers. Copy the key.
2. Open the [clinical data notebook in Colab](https://colab.research.google.com/github/artkula/ML-retreat-tekmek-2026/blob/main/3-LLM/LLM_clinical_data.ipynb).
3. In that notebook, click the key icon (Secrets) in the left bar, add a secret named `GOOGLE_API_KEY` with your key as the value, and switch on “Notebook access”.

Keep the key in Secrets, never in the notebook text.

### Claude: choose one of two options

**Option A: Claude Pro (paid, recommended).** It includes Claude Code, the agent we use in the afternoon hands-on. Take the monthly plan at [claude.com/pricing](https://claude.com/pricing) and cancel the renewal after the retreat if you do not want to keep it. Then install Claude Code (no administrator rights needed):

- Windows, in PowerShell: `irm https://claude.ai/install.ps1 | iex`. [Git for Windows](https://git-scm.com/downloads/win) is useful but optional; skip it if the installer is blocked.
- macOS or Linux, in a terminal: `curl -fsSL https://claude.ai/install.sh | bash`

Open a new terminal and type `claude --version`; it should print a version number. Then type `claude` and log in when the browser opens.

**Option B: a free account** at [claude.ai](https://claude.ai). You can chat with Claude in the browser, but the free plan does not include Claude Code. In the hands-on you then work together with a colleague who has option A, or with Antigravity or Codex below.

### Optional: Antigravity or Codex

- **Antigravity** (Google, free for individuals with usage limits): download from [antigravity.google/download](https://antigravity.google/download) and sign in with a personal Google account.
- **Codex** (OpenAI): needs a ChatGPT account. A KTH ChatGPT Edu licence must be [ordered in advance](https://intra.kth.se/it/programvara-o-system/programvara/installera/download/ai-services/chat-gpt/chatgpt-edu-1.1447849); otherwise use your own account. Install on Windows in PowerShell with `irm https://chatgpt.com/codex/install.ps1 | iex`, on a Mac with `curl -fsSL https://chatgpt.com/codex/install.sh | sh`. Then type `codex` and sign in with ChatGPT.

### A local model with Ollama

The model runs on your own laptop, so your prompts and data are not sent anywhere. Use only models without “cloud” in the name.

1. Install Ollama from [ollama.com/download](https://ollama.com/download). On a Mac, open the Ollama app once after installing. Keep about 5 GB of disk free plus the size of the model.
2. Pick the model in the table that fits your computer. Most laptops take `4b` or `9b`. The table is a rough guide: the model needs more memory while it runs than its download size.
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

If the answer takes more than a minute, take the next smaller model.

## Questions

Artem Kulachenko, artem@kth.se
