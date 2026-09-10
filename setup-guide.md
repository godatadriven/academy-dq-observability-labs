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
5. Run these commands, one at a time. On Windows, use `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

```bash
uv sync
```

```bash
source .venv/bin/activate
```

```bash
dbt deps
```

```bash
dbt seed
```

```bash
dbt run
```

The two tools of the day: **dbt** builds tables from SQL files and tests them. **Soda** checks a table and says PASSED or FAILED for each rule.

What the commands do:

- `uv sync` installs Python, dbt, and Soda.
- The activate line makes this terminal use them. `(jaffle-shop-dq)` appears at the start of the line. Every new terminal needs the activate line once.
- `dbt deps` gets dbt's add-ons, called packages. One of them, `dbt_expectations`, adds more kinds of tests.
- `dbt seed` loads the CSV files as tables.
- `dbt run` builds the tables.

The last line of `dbt run` must be:

```
Done. PASS=5 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=5
```

The database is one local file, `jaffle_shop.duckdb`. Nothing connects to the cloud.

## Step 5 — Check it

```bash
dbt test
```

Expected: the last line is `Done. PASS=4 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=4`.

```bash
soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/setup_check.yml
```

Expected: the last line is `All is good. No failures. No warnings. No errors.`

## Step 6 — Tell your trainer

Reply to the setup email with two lines: the last line of `dbt test`, and whether you had used a terminal before today (yes or no).

## Common problems

| What you see | What to do |
| --- | --- |
| The last folder name before the cursor is not `jaffle_shop` | Close the terminal. In VS Code, check that you opened the folder `dq-observability-labs`. Open a new terminal. |
| `No pyproject.toml found` | You are in the wrong folder. Same fix as above. |
| `quote>` or `>` and nothing happens | The terminal waits for a closing quote. Press Ctrl+C and paste the command again. |
| `uv: command not found` after the install | Close and open the terminal. If it still fails on a Mac, run `source ~/.zshrc`. |
| `dbt: command not found` | This terminal is not activated. Run the activate line again. Every new terminal needs it. |
| `(jaffle-shop-dq)` is not at the start of the line | Same: run the activate line again. |
| Windows: `activate` is blocked | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then try again. |
| Windows: script execution is blocked when you install uv | Run PowerShell as administrator and repeat the `uv` install command. |
| `uv sync` hangs or fails on a company network | A proxy blocks the download. Ask IT for the proxy settings, or use a personal hotspot for the install. |
| `uv sync` tries to build `duckdb` and fails | Run `uv python install 3.12`, then `uv sync` again. |
| `Could not set lock on file ... jaffle_shop.duckdb` | Another program has the database open. Close it, then run the command again. |
| `Configuration path 'soda/configuration.yml' does not exist` | You are in the wrong folder. Open a new terminal in VS Code. |
| Still stuck | Email the trainer before the day, with the full error text. On the day, arrive 20 minutes early. |

# Part 2 · How the labs work

Read this once, with the labs open in VS Code. Nobody expects you to know YAML or dbt before the day.

## The terminal in VS Code

Mac:

```
(jaffle-shop-dq) you@laptop jaffle_shop %
```

Windows:

```
(jaffle-shop-dq) PS C:\Users\you\dq-observability-labs\jaffle_shop>
```

- The last folder name in the prompt must be `jaffle_shop`.
- `(jaffle-shop-dq)` at the start means that the terminal can use dbt and Soda. If it is not there, run the activate line again.
- Lost? Close the terminal and open a new one. Then run the activate line again.

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

Everything happens in `jaffle_shop/`. dbt and Soda read the lab files where they are.

| Folder or file | What is in it |
| --- | --- |
| `LABS.md` | Every lab: the file to open, the command, the time, and what to do when it does not work. |
| `seeds/` | CSV files that dbt loads as tables, and YAML files with their tests. Lab 1 is here. |
| `models/` | SQL files that dbt turns into tables, and YAML files with their tests. Labs 2 and 4 are here. |
| `tests/` | SQL queries that are tests. Lab 1's query is here. |
| `soda/` | The Soda connection, the setup check, and Lab 3. |
| `agent_tools.py` | The reorder agent's two commands. Lab 4 changes it. |
| `lab5_worksheet.md` | Lab 5. |
| `target/`, `logs/`, `dbt_packages/`, `profiles.yml` | Files that dbt makes and uses. Do not change them. |

## A lab file starts switched off

Each lab file has blanks: `______` or `___`. A blank in a file that dbt reads breaks every dbt command. So each lab file starts switched off, and you switch it on when its lab starts:

- A YAML file is switched off with a `#` at the start of every line. To switch it on, select the lines below `START` and press Cmd+/ (Windows: Ctrl+/). Press it again to switch the lines off.
- A SQL file starts with `{{ config(enabled=false) }}`. Change `false` to `true`.
- `agent_tools.py` has `GATE = False`. Change it to `True`.

Then fill the blanks, save the file, run the command, and compare the last line. Every lab file has its steps in the comment at the top. Do not switch on a lab before the day. To start a file over, run `git checkout` and the file name.
