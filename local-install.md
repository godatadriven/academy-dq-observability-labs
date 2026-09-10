# Local install · only when Codespaces is blocked

Use this only when Codespaces is blocked. It takes about 45 minutes.

1. Install git: on a Mac, run `xcode-select --install` in the Terminal app. On Windows, install it from <https://git-scm.com/download/win>.
2. Install uv: follow <https://docs.astral.sh/uv/getting-started/installation/>. Then close and open the terminal.
3. Install VS Code from <https://code.visualstudio.com>.
4. In a terminal, run these, one at a time:

```bash
cd ~
```

```bash
git clone https://github.com/godatadriven/academy-dq-observability-labs.git
```

5. In VS Code, choose **File > Open Folder**, open `academy-dq-observability-labs`, and trust the authors.
6. Choose **Terminal > New Terminal**. It starts in `jaffle_shop`. Run:

```bash
uv run build.py
```

The last line must start with `Ready`. If a company network blocks the download, use a personal hotspot.
