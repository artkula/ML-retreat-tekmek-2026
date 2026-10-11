# ML Retreat TekMek 2026

Skepparholmen, 13 to 14 October 2026. Teachers: Artem Kulachenko and Marco Laudato.

Step 1 (2025): https://github.com/artkula/ML-retreat-tekmek-2025

## Before the retreat

Please follow [0-Setup/SETUP.md](0-Setup/SETUP.md): a Google account for Colab, a Gemini API key, a Claude account, and Ollama with a small local model to try.

## Running the notebooks

### Option 1: Google Colab (easiest, no setup)

Each notebook has an “Open in Colab” button at the top, and the links in the table below do the same. Colab opens the notebook from this repository and runs it in your browser. For the CNN notebook, choose Runtime, Change runtime type, T4 GPU.

### Option 2: your own computer (VS Code or Jupyter)

1. Install [Python](https://www.python.org/downloads/) 3.10 to 3.12 and [VS Code](https://code.visualstudio.com/) with the Python and Jupyter extensions.
2. Clone or download this repository and open the folder in VS Code.
3. Create a virtual environment and install the packages in a terminal:

   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

   On macOS or Linux, activate with `source venv/bin/activate`.
4. Open a notebook, select the interpreter from `venv` as the kernel, and run the cells.

The first code cell of each notebook installs any package that is still missing, so the notebooks also run in an existing Python environment. For the clinical data notebook, set your Gemini key as the environment variable `GOOGLE_API_KEY` before starting VS Code (in Colab it is read from Secrets). On the KTH network the notebook can also use the department GPU server instead of Gemini; choose it in the model list. Optional: with an Ollama key (created at ollama.com/settings/keys and stored as `OLLAMA_API_KEY`, in Colab Secrets or as an environment variable) the model list also offers open models through the Ollama Cloud API; the Free plan of Ollama includes a starter amount of usage.

## Sessions

| Day | Session | Notebook |
|---|---|---|
| Tue | CNN hands-on: convolution, pooling, CNN autoencoders for flow fields | [Open in Colab](https://colab.research.google.com/github/artkula/ML-retreat-tekmek-2026/blob/main/1-CNN/CNN_handson.ipynb) |
| Tue | GANs and PINNs: lecture and hands-on | from Marco |
| Wed | LLMs: unifying synthetic clinical records from five countries | [Open in Colab](https://colab.research.google.com/github/artkula/ML-retreat-tekmek-2026/blob/main/3-LLM/LLM_clinical_data.ipynb) |
| Wed | Agents with local models, Claude for science | demos |
| Wed | Hands-on with agents in two groups: teaching and administration (Artem), science (Marco) | group work |
