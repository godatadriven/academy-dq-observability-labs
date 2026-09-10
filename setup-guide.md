# Setup guide · Module 2

The labs run in **GitHub Codespaces**: VS Code in your browser, with everything already installed. You install nothing on your laptop.

Do both parts before the day. Part 1 takes about 10 minutes. Part 2 takes about 10 minutes.

# Part 1 · Open your codespace

## Step 1 — Bring

- A laptop with a browser, and Wi-Fi. On a client site, ask your host for guest access.
- A GitHub account. No account? Create one for free at <https://github.com/signup>.
- Your standard from Module 1: the rule you wrote under your incident on the Miro board. A photo is fine.

## Step 2 — Create your codespace

1. Sign in to GitHub.
2. Open <https://github.com/xebia/dq-observability-labs>.
3. Click the green **Code** button, then the **Codespaces** tab, then **Create codespace on main**.
4. Wait about three minutes. VS Code opens in your browser. The terminal at the bottom builds the sandbox by itself.

The last line in the terminal must be:

```
Ready. Module 1's four tests pass, and Soda can read the tables.
```

The two tools of the day are already in it:

- **dbt** builds tables from SQL files and tests them.
- **Soda** checks a table and says PASSED or FAILED for each rule.

## Step 3 — Tell your trainer

Reply to the setup email with two lines: the `Ready` line, and whether you had used a terminal before (yes or no).

## Step 4 — On the day

Open <https://github.com/codespaces> and click your codespace. It keeps your work. It stops by itself when you do not use it, and it does not use up your free hours while it is stopped.

## Common problems

| What you see | What to do |
| --- | --- |
| No **Codespaces** tab, or your company blocks it | Use a personal laptop or a personal browser profile. Or follow "No Codespaces?" at the end. |
| The terminal shows `Step N failed` | Click in the terminal and run `uv run build.py`. |
| No `Ready` line, and the terminal is gone | Choose the menu (☰) > **Terminal** > **New Terminal**. Then run `uv run build.py`. |
| You deleted the codespace | Create a new one, as in Step 2. |
| Still stuck | Email the trainer before the day, with a screenshot. On the day, arrive 20 minutes early. |

# Part 2 · How the labs work

Read this once, with your codespace open. Nobody expects you to know YAML or dbt before the day.

## The terminal

A terminal is where you type a command and press Enter. In your codespace, it is at the bottom of the window. If it is not there, choose the menu (☰) > **Terminal** > **New Terminal**.

```
@you ➜ /workspaces/dq-observability-labs/jaffle_shop $
```

- The text before your cursor is the **prompt**. The last folder name in it must be `jaffle_shop`.
- Copy one command from a lab page, paste it, and press Enter. Wait until the prompt comes back.
- Put `uv run` in front of every dbt, Soda, or Python command. The lab pages already do.
- Press ↑ to get the last command back. Press Ctrl+C to stop a command.
- Lost? Close the terminal with the bin icon, and open a new one.

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

Open the lab's page, for example `labs/lab1.md`. It opens as a formatted page. Drag its tab to the right half of the window, so it stays next to your files. Then follow the steps: open a file, run a command, compare with "You see", and answer the questions. Some steps ask you to change one value. Save the file (Cmd+S on a Mac, Ctrl+S on Windows) before you run the command again.

To put a file back as it was, run `git checkout` and the file name, for example `git checkout seeds/lab1_tests.yml`.

# No Codespaces? Install it on your laptop

Use this only when Codespaces is blocked. It takes about 45 minutes.

1. Install git: on a Mac, run `xcode-select --install` in the Terminal app. On Windows, install it from <https://git-scm.com/download/win>.
2. Install uv: follow <https://docs.astral.sh/uv/getting-started/installation/>. Then close and open the terminal.
3. Install VS Code from <https://code.visualstudio.com>.
4. In a terminal, run these, one at a time:

```bash
cd ~
```

```bash
git clone https://github.com/xebia/dq-observability-labs.git
```

5. In VS Code, choose **File > Open Folder**, open `dq-observability-labs`, and trust the authors.
6. Choose **Terminal > New Terminal**. It starts in `jaffle_shop`. Run:

```bash
uv run build.py
```

The last line must start with `Ready`. If a company network blocks the download, use a personal hotspot.
