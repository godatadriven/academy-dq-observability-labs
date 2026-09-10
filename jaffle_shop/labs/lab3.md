# Lab 3 · Checks on the payments table

**Part A 15 minutes, Part B 10 minutes** · Write a Soda check, and set a limit that catches the Frozen Payments.

> This page stays on the left. Click a file name to open it on the right.

## Part A · A normal morning

### 1 · Scan Sunday 31 May

Open [`soda/lab3_checks.yml`](../soda/lab3_checks.yml): three checks. `NOW` is the morning the scan pretends it is.

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml
```

**You see:** `All is good`.

### 2 · Your turn

Add a fourth check: every payment has a customer. Add these lines under the others, and save:

```yaml
  - missing_count(customer_id) = 0:
      name: "completeness: every payment has a customer"
```

```bash
uv run check.py 3a
```

**You see:** `2 of 2 done. Well done.`

**Stop here.** Part B starts at the slide "Catch the Case".

## Part B · Catch the case

### 3 · Scan a normal day

Open [`soda/lab3_repeat.yml`](../soda/lab3_repeat.yml): it rings when too many payments repeat the last amount. The limit is 5.

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-26 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
```

**You see:** it fails on a normal day, 26 May. The limit is too tight.

### 4 · Your turn

Change the `5` to a limit that is quiet all of May, but rings on 2 June. Save, and check:

```bash
uv run check.py 3b
```

**You see:** `2 of 2 done. Well done.` A ✗ line names the day your limit gets wrong.

### 5 · Scan 2 June

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-06-02 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
```

**You see:** `Oops! 2 failures`. Your checks catch the Frozen Payments.

**Talk:** why is the 1 June scan still green?

**Stuck?** `Configuration path ... does not exist`: open a new terminal (menu ☰ > Terminal > New Terminal).
