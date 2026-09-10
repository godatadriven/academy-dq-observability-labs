# Lab 3 · Checks on the payments table

**Goal:** see which checks ring on 2 June, and why. **Time:** Part A 15 minutes, Part B 10 minutes.

> Keep this page on the right: drag its tab to the right half of the window. Click a file name on the page to open the file.

## Part A · A normal morning

1. Open [`soda/lab3_checks.yml`](../soda/lab3_checks.yml). It has three Soda checks: freshness, volume, and validity.
2. Scan Sunday 31 May. `NOW` is the morning that the scan pretends it is.

   ```bash
   uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml
   ```

   You see: `3/3 checks PASSED`, and `All is good`.
3. Answer: what does each check ask? Which one rings if the copy did not run last night?

**Stop here.** Part B starts at the slide "Catch the Case".

## Part B · Catch the case

4. Open [`soda/lab3_repeat.yml`](../soda/lab3_repeat.yml). It is Module 1's rule: ring when more than 20% of payments repeat the customer's last amount.
5. Scan three mornings with both files, one command at a time:

   ```bash
   uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
   ```

   ```bash
   uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-06-01 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
   ```

   ```bash
   uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-06-02 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
   ```

   You see: 31 May and 1 June are `All is good`. 2 June is `Oops! 2 failures`: validity with `check_value: 41`, and distribution with `check_value: 100.0`.
6. Answer: why is 1 June still green? What do 41 and 100 mean? Module 1 said 99 in 100: here, every returning customer repeats.
7. In `soda/lab3_repeat.yml`, change `repeat_rate < 20` to `repeat_rate < 5`. Save (Cmd+S, or Ctrl+S on Windows). Scan 26 May, a normal day:

   ```bash
   uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-26 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
   ```

   You see: the distribution check fails, with `check_value: 9.46`. Answer: what does a limit that is too tight cost you? Then change it back to `20`.

**Done early?** Scan 15 June, the Monday after a busy Sunday. Which checks ring? Which one is only the busy Sunday?

```bash
uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-06-15 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
```

**Stuck?** `Configuration path ... does not exist`: open a new terminal (menu ☰ > Terminal > New Terminal), so that it starts in `jaffle_shop`.
