# Setup guide · Module 2

Do both parts before the day. Part 1 installs the labs, in about 45 minutes. Part 2 shows how the labs work, in about 10 minutes. Setup on the day takes lab time.

# Part 1 · Install the labs

## Step 0 — Check that you can install software

Try to install one small program today. If your laptop blocks it, ask your IT desk now, not on the day.

## Step 1 — Bring

- A laptop where you can install software.
- Wi-Fi access. On a client site, ask your host for guest access.
- Your standard from Module 1: the rule you wrote under your incident on the Miro board. A photo is fine.

## Step 2 — Open a terminal

A terminal is a window where you type a command and press Enter.

- **Mac:** press Cmd+Space, type `Terminal`, press Enter.
- **Windows:** press the Start key, type `PowerShell`, press Enter.

How to use it:

- Copy one command at a time from this guide. Paste it, press Enter, and wait until the terminal is ready for the next line.
- The text before your cursor is the **prompt**. It shows the folder you are in.
- Press ↑ to get the last command back. Change it, then press Enter.
- Press Ctrl+C to stop a command. It also clears a stuck line, for example `quote>`.
- Read the last line of the output first. It tells you the result.

## Step 3 — Install the tools

After each tool, run its check. If the output does not match, fix that tool before you continue.

### 3.1 Git

Mac:

```bash
xcode-select --install
```

A window opens. Click Install. It can take 15 minutes.

Windows: download and run the installer from <https://git-scm.com/download/win>. Keep every default.

Check:

```bash
git --version
```

Expected: a version line, for example `git version 2.45.0`.

### 3.2 uv

`uv` installs Python and the tools for you. You do not need your own Python.

Windows, in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Mac:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close the terminal and open a new one. Then check:

```bash
uv --version
```

Expected: `uv 0.x.x` or later.

### 3.3 VS Code

Install VS Code from <https://code.visualstudio.com>. The labs use it: one window holds the lab files and the terminal.

## Step 4 — Get the labs and build them

1. Go to your home folder, so you can find the labs later:

```bash
cd ~
```

2. Get the labs. Do not use "Download ZIP" on GitHub: the labs need git.

```bash
git clone https://github.com/xebia/dq-observability-labs.git
```

3. In VS Code, choose **File > Open Folder**, and open the folder `dq-observability-labs` in your home folder. When VS Code asks if you trust the authors, click **Yes, I trust the authors**.
4. In VS Code, choose **Terminal > New Terminal**. The terminal opens at the bottom. From now on, use this terminal. The last folder name before your cursor must be `jaffle_shop`. If it is not, see "Common problems".
5. Build the sandbox:

```bash
uv run build.py
```

It takes about one minute. It installs Python and the two tools of the day, builds the tables, and checks them:

- **dbt** builds tables from SQL files and tests them.
- **Soda** checks a table and says PASSED or FAILED for each rule.

The last line must be:

```
Ready. Module 1's four tests pass, and Soda can read the tables.
```

The database is one local file, `jaffle_shop.duckdb`. Nothing connects to the cloud.

In the labs, you type dbt and Soda commands the same way, with `uv run` in front, for example `uv run dbt test`.

## Step 5 — Tell your trainer

Reply to the setup email with two lines: the last line of `uv run build.py`, and whether you had used a terminal before today (yes or no).

## Common problems

| What you see | What to do |
| --- | --- |
| The last folder name before the cursor is not `jaffle_shop` | Close the terminal. In VS Code, check that you opened the folder `dq-observability-labs`. Open a new terminal. |
| `No pyproject.toml found` | You are in the wrong folder. Same fix as above. |
| `quote>` or `>` and nothing happens | The terminal waits for a closing quote. Press Ctrl+C and paste the command again. |
| `uv: command not found` after the install | Close and open the terminal. If it still fails on a Mac, run `source ~/.zshrc`. |
| Windows: script execution is blocked when you install uv | Run PowerShell as administrator and repeat the `uv` install command. |
| `uv run build.py` hangs or fails on a company network | A proxy blocks the download. Ask IT for the proxy settings, or use a personal hotspot for the install. |
| It tries to build `duckdb` and fails | Run `uv python install 3.12`, then `uv run build.py` again. |
| `Could not set lock on file ... jaffle_shop.duckdb` | Another program has the database open. Close it, then run the command again. |
| `Configuration path 'soda/configuration.yml' does not exist` | You are in the wrong folder. Open a new terminal in VS Code. |
| `Step N failed` | Read the lines above it. Then find them in this table. |
| Still stuck | Email the trainer before the day, with the full error text. On the day, arrive 20 minutes early. |

# Part 2 · How the labs work

Read this once, with the labs open in VS Code. Nobody expects you to know YAML or dbt before the day.

## The terminal in VS Code

Mac:

```
you@laptop jaffle_shop %
```

Windows:

```
PS C:\Users\you\dq-observability-labs\jaffle_shop>
```

- The last folder name in the prompt must be `jaffle_shop`.
- Put `uv run` in front of every dbt, Soda, or Python command. It uses the tools that `build.py` installed.
- Lost? Close the terminal and open a new one.

The last line of the output tells you the result:

| Last line | Meaning |
| --- | --- |
| `Done. PASS=4 WARN=0 ERROR=0 ...` | dbt: four tests passed, none failed. |
| `Done. PASS=0 WARN=0 ERROR=6 ...` | dbt: six tests failed. dbt counts a failed test as an error. |
| `All is good. No failures. No warnings. No errors.` | Soda: every check passed. |
| `Oops! 2 failures. 0 warnings. 0 errors. 2 pass.` | Soda: two checks failed, two passed. The lines above say which ones. |

## A YAML file

A YAML file holds settings as plain text. dbt and Soda read their tests and checks from YAML files. Here is part of `jaffle_shop/models/schema.yml`:

```yaml
# The payments table and its tests.
models:
  - name: stg_pos_payments
    columns:
      - name: payment_id
        data_tests: [unique]
      - name: payment_method
        data_tests:
          - accepted_values:
              arguments:
                values: ['credit_card', 'coupon']
```

| You see | It means |
| --- | --- |
| `# The payments table` | A comment: a note for people. The tool ignores everything after `#` on the line. |
| `name: payment_id` | A setting: a name, a colon, a space, then the value. |
| `- name: ...` | A dash starts one item of a list. Here, each dash is one column. |
| The spaces at the start | They show what belongs to what. `data_tests` is inside the column `payment_id`. |
| `[unique]` | A short list on one line. `[a, b]` is the same as two dash lines. |
| `'credit_card'` | A value in quotes. Keep the quotes that are there. |

Three rules prevent most errors:

- Use spaces, never tabs.
- Keep the same number of spaces as the line above, or two more to go one level in.
- Put one space after each colon and after each dash.

## A query

A dbt test can also be a SQL query. It returns the bad rows. No rows back means that the test passes.

```sql
select customer_id, order_date
from {{ ref('orders_daily_extract') }}
where order_date > current_date
```

- `select` names the columns to show. `from` names the table. `where` keeps only the rows that match.
- `{{ ref('orders_daily_extract') }}` is how dbt names the table `orders_daily_extract`.
- `current_date` is today.

## The folders

Everything happens in `jaffle_shop/`.

| Folder or file | What is in it |
| --- | --- |
| `labs/` | One page per lab: the steps, what you see, and the questions. |
| `seeds/` | CSV files that dbt loads as tables, and YAML files with their tests. Lab 1 is here. |
| `models/` | SQL files that dbt turns into tables, and YAML files about them. Labs 2 and 4 are here. |
| `tests/` | SQL queries that are tests. Lab 1's query is here. |
| `soda/` | The Soda connection, the setup check, and Lab 3. |
| `agent_tools.py` | The reorder agent's two commands. Lab 4 changes it. |
| `target/`, `logs/`, `dbt_packages/`, `profiles.yml` | Files that dbt makes and uses. Do not change them. |

## How a lab works

Open the lab's page, for example `labs/lab1.md`. To read it as a page, right-click it and choose **Open Preview**. Then follow the steps: open a file, run a command, compare with "You see", and answer the questions. Some steps ask you to change one value. Save the file (Cmd+S, Windows: Ctrl+S) before you run the command again.

To put a file back as it was, run `git checkout` and the file name, for example `git checkout seeds/lab1_tests.yml`.
