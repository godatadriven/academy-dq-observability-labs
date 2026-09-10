# Setup guide · Module 2

The labs run in **GitHub Codespaces**: VS Code in your browser, with everything installed. It takes about 10 minutes.

## You need

- A laptop with a browser, and Wi-Fi.
- A GitHub account. No account? Create one for free at <https://github.com/signup>.
- Your standard from Module 1: the rule you wrote under your incident on the Miro board. A photo is fine.

## Steps

1. Sign in to GitHub.
2. Open <https://codespaces.new/godatadriven/academy-dq-observability-labs> and click **Create codespace**.
3. Wait about three minutes. VS Code opens in your browser, and the terminal at the bottom builds the labs by itself. The last line must be:

   ```
   Ready. Module 1's four tests pass, and Soda can read the tables.
   ```

4. Reply to the setup email with two lines: the `Ready` line, and whether you have used a terminal before (yes or no).

On the day, open <https://github.com/codespaces> and click your codespace. It keeps your work.

Want a head start? Read `basics.md`, five minutes.

## If it does not work

| You see | Do this |
| --- | --- |
| Your company blocks Codespaces | Use a personal laptop or browser. If that is not possible, follow `local-install.md`. |
| `Step N failed` in the terminal | Open a new terminal: menu ☰ > Terminal > New Terminal. Paste `uv run build.py`, and press Enter. |
| Still stuck | Email the trainer with a screenshot. On the day, arrive 20 minutes early. |
