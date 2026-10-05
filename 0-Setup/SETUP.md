# AI Retreat 2026: setup before the retreat

Skepparholmen, 13 to 14 October 2026. Please do these steps, including all downloads, before you leave: the hotel network is shared by everyone. Plan about 45 minutes. Bring your laptop and charger.

Use the synthetic data we supply, or public material that you are allowed to process, with the cloud tools below (Colab, Gemini, Claude, Antigravity, Codex). KTH rules: [Recommendations for the use of AI](https://intra.kth.se/en/it/natverk/regler-policys/rekommendationer-vid-anvandning-av-ai-1.1446862).

## Day 1: Google Colab

1. Sign in at [colab.research.google.com](https://colab.research.google.com) with a Google account. A personal Gmail account works.
2. Open the [CNN notebook in Colab](https://colab.research.google.com/github/artkula/ML-retreat-tekmek-2026/blob/main/1-CNN/CNN_handson.ipynb). All material is at [github.com/artkula/ML-retreat-tekmek-2026](https://github.com/artkula/ML-retreat-tekmek-2026).
3. In Colab, choose Runtime, Change runtime type, T4 GPU, and run the first cell. If it runs without an error, you are ready.

Free GPU time in Colab is limited and not guaranteed. If Colab offers you no GPU on the day, tell us at the start of the session.

## Day 2: language models and agents

### Gemini API key, for the clinical data notebook

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey), sign in with your own Google account and click “Create API key”. If it asks for a project, take the one it offers or create a new one. Copy the key.
2. In Colab, click the key icon (Secrets) in the left bar, choose “Add new secret”, name it `GOOGLE_API_KEY` and paste your key as the value. Secrets are stored in your Google account, visible only to you, and are not saved in any notebook.
3. Open the [clinical data notebook in Colab](https://colab.research.google.com/github/artkula/ML-retreat-tekmek-2026/blob/main/3-LLM/LLM_clinical_data.ipynb) and run the first cells. When it asks for access to `GOOGLE_API_KEY`, click “Grant access”.

### Claude, with Claude Code

Claude Code is the agent we use in the afternoon hands-on. Choose one of two free options:

**Option A: join the Claude for Science workspace of your group.** On day 2 the hands-on runs in two groups: teaching and administration, led by Artem, and science, led by Marco. Each group has its own workspace, and the join link comes with the invitation mail. Every seat includes Claude Code and the Claude Science tools. The group leader administers the workspace. Please read the conditions of use.

**Option B: apply for your own lab.** As a principal investigator you can apply for Anthropic’s [Team plan for scientists](https://claude.com/programs/team-plan-for-scientists): free seats for you and up to 24 members of your group for 12 months, with Claude Code included. Approval takes about a week, so apply now; until then, use option A.

A paid Claude Pro subscription also includes Claude Code. The free claude.ai plan does not.

Install Claude Code (no administrator rights needed):

- Windows, in PowerShell: `irm https://claude.ai/install.ps1 | iex`. [Git for Windows](https://git-scm.com/downloads/win) is useful but optional; skip it if the installer is blocked.
- macOS or Linux, in a terminal: `curl -fsSL https://claude.ai/install.sh | bash`

Open a new terminal and type `claude --version`; it should print a version number. Then type `claude` and log in with the account from option A or B when the browser opens.

### Optional: Antigravity, Codex or Warp

- **Antigravity** (Google, free for individuals with usage limits): download from [antigravity.google/download](https://antigravity.google/download) and sign in with a personal Google account.
- **Codex** (OpenAI): needs a ChatGPT account. A KTH ChatGPT Edu licence must be [ordered in advance](https://intra.kth.se/it/programvara-o-system/programvara/installera/download/ai-services/chat-gpt/chatgpt-edu-1.1447849); otherwise use your own account. Install on Windows in PowerShell with `irm https://chatgpt.com/codex/install.ps1 | iex`, on a Mac with `curl -fsSL https://chatgpt.com/codex/install.sh | sh`. Then type `codex` and sign in with ChatGPT.
- **Warp**: a terminal for running and managing several agents (Claude Code, Codex) side by side. Download from [warp.dev/download](https://www.warp.dev/download).

### A local model with Ollama

The model runs on your own laptop, so the model itself sends nothing to the cloud. Use only models without “cloud” in the name.

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

### Claude Code with your local model

No Claude account is needed for this.

1. In the Ollama app, open Settings and set the context length to 64k (32k on a laptop with 16 GB or less). The default 4k is too small for an agent.
2. In an empty folder, open a terminal, run `ollama launch claude --model qwen3.5:4b` and give it a small task.

Without a graphics card, one step can take a few minutes.

## Questions

Artem Kulachenko, artem@kth.se
