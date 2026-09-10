# Setup guide · Module 2

Do these steps before the day. Allow 30 minutes. Setup on the day takes lab time.

## Step 1 — Bring

- A laptop where you can install software.
- Wi-Fi access. On a client site, ask your host for guest access.
- Your standard from Module 1: the rule you wrote under your incident on the Miro board. A photo is fine. You turn it into code at the end of the day.

## Step 2 — Install the tools

Install in this order. After Git and after uv, run the check. If the output does not match, fix that tool before you continue.

### 2.1 Git

macOS: `xcode-select --install` or `brew install git`. Windows: <https://git-scm.com/download/win>. Linux: `sudo apt install git`.

```bash
git --version
```

Expected: a version line, for example `git version 2.45.0`.

### 2.2 uv

`uv` installs Python and the packages for you. You do not need your own Python.

macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows, in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen the terminal. Then:

```bash
uv --version
```

Expected: `uv 0.x.x` or later.

### 2.3 An editor

Any editor works. The trainers use VS Code, <https://code.visualstudio.com>, with the **YAML** extension from Red Hat.

## Step 3 — Get the sandbox and build it

The sandbox and the lab files are in one public repo: <https://github.com/xebia/dq-observability-labs>.

1. Clone it, in any terminal:

```bash
git clone https://github.com/xebia/dq-observability-labs.git
```

2. In VS Code, open the whole `dq-observability-labs` folder: **File > Open Folder**. The lab files (`exercises/`) and the dbt project (`jaffle_shop/`) now sit in one sidebar. Work in this one window all day.
3. Open a terminal in VS Code: **Terminal > New Terminal**. It starts in `jaffle_shop/`. Run:

```bash
uv sync                      # install Python and the tools
source .venv/bin/activate    # use them in this terminal
dbt deps                     # get dbt's add-ons
dbt seed                     # load the CSV files as tables
dbt run                      # build the tables
```

On Windows, write `.venv\Scripts\activate` instead of `source .venv/bin/activate`. `uv sync` installs Python 3.12 and the tools for this project. The activate line makes `dbt`, `soda` and `python` use them. Run it once in every new terminal. The last line of `dbt run` must be:

```
Done. PASS=5 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=5
```

The database is DuckDB, one local file. Nothing connects to the cloud. The connection settings are already in the folder. You have nothing to set up.

## Step 4 — Check it

```bash
dbt test
soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/checks.yml
```

Expected:

- `dbt test` ends with `Done. PASS=4 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=4`.
- The Soda scan ends with `All is good. No failures. No warnings. No errors.`

The date in the Soda command picks a morning. Keep 31 May for now. The other dates are for the day.

## Step 5 — Tell your trainer

Reply to the setup email with the last line of `dbt test`. That is all we need.

## Common problems

| What you see | What to do |
| --- | --- |
| `uv: command not found` after the install | Close and reopen the terminal. If it still fails on macOS, run `source ~/.zshrc`. |
| `dbt: command not found` | The terminal is not activated. Run `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`) in `jaffle_shop/`, then try again. |
| `uv sync` hangs or fails on a company network | A proxy blocks the download. Ask IT for the proxy settings, or use a personal hotspot for the install. Then go back to the normal Wi-Fi. |
| `uv sync` tries to build `duckdb` and fails | The project needs Python 3.12. Run `uv python install 3.12`, then `uv sync` again. |
| `Could not set lock on file ... jaffle_shop.duckdb` | Another program has the database open. Close it, then run the command again. |
| `Configuration path 'soda/configuration.yml' does not exist` | You are in the wrong folder. `cd jaffle_shop` and run it again. |
| Windows: script execution is blocked | Run PowerShell as administrator and repeat the `uv` install command. |
| Windows: `activate` is blocked | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then try again. |
| Still stuck | Email the trainer before the day, with the full error text. On the day, arrive 20 minutes early. |

## Time

| Step | Minutes |
| --- | --- |
| Git, uv, an editor | 10 |
| Get the sandbox and build it | 10 |
| Check it | 2 |
| Room for problems | 8 |
