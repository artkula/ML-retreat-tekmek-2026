# AI Retreat 2026: Claude Science setup

This guide assumes you have accepted the invitation to the Claude Team plan for scientists. Install the app named **Claude Science** and complete the test below before the retreat.

## Download and check your computer

Download from [claude.com/product/claude-science](https://claude.com/product/claude-science).

Have internet access and about **5 GB of free disk space**. Supported systems: **macOS 13 or later** (Intel or Apple silicon), **Windows 11** (x64), or **Linux** (x64, glibc). The Team owner must have enabled Claude Science.

## Install for your operating system

### Mac

1. Choose the Mac download for your processor: Apple silicon or Intel. To check, open Apple menu, About This Mac.
2. Open the installer, then launch Claude Science from Applications or the Dock.
3. Its interface opens in your browser.

### Windows

1. Download and open the Windows installer.
2. Launch Claude Science from the Start menu. It opens in its own window.
3. Follow any Windows permission prompt needed for shell tools.

### Linux

On Ubuntu or Debian, install the dependencies and check the version in a terminal:

```
sudo apt-get update
sudo apt-get install -y curl bubblewrap socat
bwrap --version
```

**Continue only if bubblewrap is 0.8.0 or newer.** Ubuntu 22.04 packages are too old. For other distributions, use the [official Linux instructions](https://claude.com/docs/claude-science/get-started). The sandbox also needs unprivileged user namespaces; ask IT if these are blocked.

Then install and start Claude Science:

```
curl -fsSL https://claude.ai/install-claude-science.sh | bash
claude-science serve
```

Open the local URL printed in the terminal if no browser tab appears. If the command is not found, follow the installer's PATH instructions and open a new terminal. To start it next time, run `claude-science serve`.

## Sign in and run a quick test

1. Sign in with the invited Claude account and select the retreat's **Team organization** when asked.
2. Let the first-launch Python and R setup finish. **No Anthropic API key is required.**
3. Create a project and send:

```
Create a file called claude-science-test.txt in my Documents folder containing the text: Claude Science is working.
```

Allow read and write access to Documents and code execution when asked. Open `claude-science-test.txt` in Documents and check its contents. **You are ready when the file exists and contains the requested text.**

If sign-in says Science is unavailable, check that you selected the Team organization and contact the retreat organizers. If the browser sign-in does not return to the app, use **Paste code instead**.

## Official guides

- [Installation and troubleshooting](https://claude.com/docs/claude-science/get-started)
- [System requirements](https://claude.com/docs/claude-science/overview)
- [Team access](https://claude.com/docs/claude-science/enable-claude-science)
- [Permissions](https://claude.com/docs/claude-science/core-concepts)

Instructions checked 12 October 2026.
