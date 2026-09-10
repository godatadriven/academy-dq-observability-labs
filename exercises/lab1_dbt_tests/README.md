# Lab 1 · Six defects, six tests

**Goal:** write one dbt test for each of the six defects from Module 1. All six tests must fail.

A failing test is good news here. It means the test found the bad row. Do not fix the data.

## Three ways to write a test

- **Built in:** one word. dbt has four: `unique`, `not_null`, `accepted_values`, `relationships`.
- **From a package:** a test from `dbt_expectations`, with settings.
- **A query:** a SQL file in `tests/` that returns the bad rows. No rows back means it passes.

## The table

It is Module 1's "Spot the defects" table, loaded as `orders_daily_extract`. In dbt, `{{ ref('x') }}` names the table x. To see it, run this from `jaffle_shop/`:

```bash
dbt show --inline "select * from {{ ref('orders_daily_extract') }}"
```

## Steps

1. Open `extract_tests.yml`. Each comment names one defect, its rule, and a hint.
2. Fill the six blanks (`______` or `___`).
3. Open `extract_updated_before_placed.sql`. Fill the one blank after `where`.
4. From `jaffle_shop/`, copy both files into place:

```bash
cp ../exercises/lab1_dbt_tests/extract_tests.yml seeds/
cp ../exercises/lab1_dbt_tests/extract_updated_before_placed.sql tests/
```

5. Run the tests:

```bash
dbt test --select orders_daily_extract
```

## When it works

Six lines say `FAIL 1`. The last line is:

```
Done. PASS=0 WARN=0 ERROR=6 SKIP=0 NO-OP=0 REUSED=0 TOTAL=6
```

dbt counts a failed test as an error. Six errors is the goal.

## If it does not work

| You see | Do this |
| --- | --- |
| `Nothing to do` | The files are not in `seeds/` and `tests/`. Copy them again. |
| An error with `______` in it | A blank is still empty. |
| An error about the pattern, an escape, or a syntax error | In the pattern, write each backslash twice: `\\.` |
| A test says `PASS` | One of your blanks is wrong. Read the rule in the comment again. |

After a fix in `exercises/`, copy the file again before you run the tests.
