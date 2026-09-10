# Lab 3 · Checks on the payments table

**Goal:** see which checks ring on 2 June, and why. **Time:** Part A 25 minutes, Part B 15 minutes.

## Part A · A normal morning

1. Open `soda/lab3_checks.yml`. It has three Soda checks: freshness, volume, and validity.
2. Run a scan. `NOW` is the morning that the scan pretends it is: Sunday 31 May, 09:00.

   ```bash
   uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml
   ```

   You see: `3/3 checks PASSED`, and `All is good`.
3. Answer: what does each check ask? Which ones are Module 1's pillars?

## Part B · Catch the case

4. Open `soda/lab3_repeat.yml`. It is Module 1's rule: ring when more than 20% of payments repeat the customer's last amount.
5. Scan 31 May with both files:

   ```bash
   uv run soda scan -d jaffle_shop -c soda/configuration.yml -v NOW="2026-05-31 09:00:00" soda/lab3_checks.yml soda/lab3_repeat.yml
   ```

   Then press ↑, change the date to `2026-06-01`, and run. Do the same for `2026-06-02`.

   You see: 31 May and 1 June are `All is good`. 2 June is `Oops! 2 failures`: validity with `check_value: 41`, and distribution with `check_value: 100.0`.
6. Answer: why is 1 June still green? What do 41 and 100 mean?
7. In `soda/lab3_repeat.yml`, change `repeat_rate < 20` to `repeat_rate < 5`. Save (Cmd+S). Scan `2026-05-26` with both files.

   You see: the distribution check fails on a normal day, with `check_value: 9.46`. Answer: what does a limit that is too tight cost you? Then change it back to `20`.

**Done early?** Scan `2026-06-15` with both files. Which checks ring? Which one is only the busy Sunday?

**Stuck?** `Configuration path ... does not exist`: open a new terminal in VS Code, so that it starts in `jaffle_shop`.
