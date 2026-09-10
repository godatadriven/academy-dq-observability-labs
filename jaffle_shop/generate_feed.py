"""Build the sandbox seeds for the running case: The Frozen Payments.
Every fact comes from ../../module_1/case.md. Deterministic: same output every run.

  seeds/raw_pos_payments.csv   the payment app's events, 17 May to 17 June 2026.
                               Until 31 May each event says  {"amount": 3.50}   (euros).
                               From 1 June (API v2.4) it says {"amount_cents": 450}.
                               The true amounts are in the file. The freeze is not:
                               it happens in models/staging/stg_pos_payments.sql,
                               where the note fills the missing amount.
  seeds/raw_customers.csv      jaffle_shop's 100 customers, plus the café customers.
  seeds/bank_deposits.csv      what the bank received per day. The truth Sam compares with.
  seeds/orders_daily_extract.csv  Module 1's "Spot the defects" table, row for row.

The story, as the data tells it:
  - About 600 payments a night. About 40 of them are a customer's first payment.
  - New menu prices on Monday 1 June: every price times 9/7. Anna's large coffee 3.50 -> 4.50.
  - A busy weekend 12 to 14 June. Sunday 14 June: 2,100 payments.
  - Each customer has a usual order, but it varies: about 6 in 100 payments
    equal that customer's previous payment on a normal day.

Run from jaffle_shop/:  python generate_feed.py
"""
import csv, json, random
from datetime import date, timedelta

SEED = 15
FIRST, LAST = date(2026, 5, 17), date(2026, 6, 17)
NEW_PRICES = date(2026, 6, 1)            # the payment app ships v2.4, the menu changes
ANNA = 20                                 # jaffle_shop customer 20 is Anna A.
CAFES = [f"cafe_{i:02d}" for i in range(1, 13)]
METHODS = ["credit_card"] * 6 + ["coupon", "bank_transfer", "gift_card"]

# The menu, old prices in cents, with a weight for how often it is ordered.
MENU = {
    "coffee": (300, 9), "large coffee": (350, 8), "flat white": (380, 6), "tea": (280, 4),
    "hot chocolate": (420, 3), "orange juice": (450, 3), "croissant": (320, 4),
    "banana bread": (390, 3), "cheese jaffle": (750, 6), "ham and cheese jaffle": (850, 6),
    "tuna melt jaffle": (890, 4), "mushroom jaffle": (820, 3), "soup of the day": (690, 3),
    "salad bowl": (1050, 2), "avocado toast": (1150, 3), "eggs benedict": (1350, 3),
    "pancake stack": (1250, 2), "big brunch plate": (1650, 2),
}
NAMES = list(MENU)
WEIGHTS = [MENU[n][1] for n in NAMES]


def new_price(old):
    """Every price times 9/7, to the nearest 10 cents. 350 -> 450."""
    return int(round(old * 9 / 7 / 10) * 10)


REGULARS, BRUNCH_SHARE, USUAL = 3500, 0.45, 0.15
SIZES = {"weekday": [10, 1, 0], "brunch": [5, 4, 1]}   # how many items, 1 to 3


def size_for(rng, kind):
    return rng.choices([1, 2, 3], weights=SIZES[kind])[0]


def basket(rng, size):
    return rng.choices(NAMES, weights=WEIGHTS, k=size)


def price(items, on):
    return sum(new_price(MENU[i][0]) if on >= NEW_PRICES else MENU[i][0] for i in items)


def event_for(customer, cents, on):
    """The payment app's event, as Module 1 draws it: {"amount": 3.50} or, from 1 June, {"amount_cents": 450}."""
    if on >= NEW_PRICES:
        return f'{{"customer": {customer}, "amount_cents": {cents}}}'
    return f'{{"customer": {customer}, "amount": {cents / 100:.2f}}}'


def nights():
    d = FIRST
    while d <= LAST:
        yield d
        d += timedelta(days=1)


def build(seed=SEED):
    rng = random.Random(seed)
    kind, usual = {}, {}                       # customer -> "weekday" or "brunch", their usual order
    known = set()                              # customers with a payment in the feed before June
    # jaffle_shop's customers 1..100, plus the café regulars
    regulars = list(range(1, REGULARS + 1))
    next_id = REGULARS + 1

    def meet(c, k):
        kind[c] = k
        usual[c] = basket(rng, size_for(rng, k))

    for c in regulars:
        meet(c, "brunch" if rng.random() < BRUNCH_SHARE else "weekday")
    kind[ANNA], usual[ANNA] = "weekday", ["large coffee"]

    rows, pid = [], 100001
    june_pool = None
    for day in nights():
        if day == NEW_PRICES:
            june_pool = sorted(known)
        weekend = day.weekday() >= 5
        busy = {date(2026, 6, 12): 900, date(2026, 6, 13): 1300, date(2026, 6, 14): 2100}
        n = busy.get(day, rng.randint(560, 640))
        n_new = 40 + rng.randint(-6, 6)
        # returning payers: before June anyone from the regulars, from June only
        # people already in the feed (a first payment is a first payment)
        pool = regulars if day < NEW_PRICES else june_pool
        want = "brunch" if weekend else "weekday"
        payers = [ANNA]
        while len(payers) < n - n_new:
            c = rng.choice(pool)
            if c == ANNA or c in payers[-50:]:
                continue
            if kind[c] != want and rng.random() < 0.75:
                continue
            payers.append(c)
        for _ in range(n_new):
            meet(next_id, "brunch" if (weekend and rng.random() < 0.8) else "weekday")
            payers.append(next_id)
            next_id += 1

        for c in payers:
            if c == ANNA:
                items, at, cafe = ["large coffee"], "07:40:00", "cafe_03"
            else:
                items = usual[c] if rng.random() < USUAL else basket(rng, size_for(rng, kind[c]))
                at = f"{rng.randint(7, 21):02d}:{rng.randint(0, 59):02d}:00"
                cafe = rng.choice(CAFES)
            cents = price(items, day)
            event = event_for(c, cents, day)
            rows.append({
                "payment_id": pid, "customer_id": c, "cafe_id": cafe,
                "payment_method": rng.choice(METHODS), "event": event, "true_cents": cents,
                "paid_at": f"{day.isoformat()} {at}",
                "_etl_loaded_at": f"{(day + timedelta(days=1)).isoformat()} 03:30:00",
            })
            if day < NEW_PRICES:
                known.add(c)
            pid += 1
    rows.sort(key=lambda r: (r["paid_at"], r["payment_id"]))
    sunday(rows, rng, kind)
    return rows, next_id - 1


def sunday(rows, rng, kind, bank=2_560_000, table=1_990_000, near=2_000):
    """Nudge Sunday 14 June onto the case numbers: bank EUR 25,600, dashboard EUR 19,900.
    Only Sunday rows change. Two moves: swap which regulars pay (the dashboard shows
    each one's last May amount), and change what people order (the bank sees the true price)."""
    last = {}
    for r in rows:
        if r["paid_at"] < "2026-06-01":
            last[r["customer_id"]] = r["true_cents"]
    sun = [r for r in rows if r["paid_at"].startswith("2026-06-14")]
    paying = {r["customer_id"] for r in sun}
    others = [c for c in last if c not in paying and c != ANNA and kind[c] == "brunch"]
    shown = lambda: sum(last.get(r["customer_id"], 0) for r in sun)
    while abs(shown() - table) > near:
        r = rng.choice([r for r in sun if r["customer_id"] in last and r["customer_id"] != ANNA])
        c = rng.choice(others)
        if abs(shown() - last[r["customer_id"]] + last[c] - table) < abs(shown() - table):
            others.remove(c); others.append(r["customer_id"])
            r["customer_id"] = c
            r["event"] = event_for(c, r["true_cents"], date(2026, 6, 14))
    got = lambda: sum(r["true_cents"] for r in sun)
    while abs(got() - bank) > near:
        r = rng.choice([r for r in sun if r["customer_id"] != ANNA])
        cents = price(basket(rng, size_for(rng, kind[r["customer_id"]])), date(2026, 6, 14))
        if abs(got() - r["true_cents"] + cents - bank) < abs(got() - bank):
            r["true_cents"] = cents
            r["event"] = event_for(r["customer_id"], cents, date(2026, 6, 14))


def the_copy(rows):
    """What models/staging/stg_pos_payments.sql does, in Python, to check the numbers."""
    last, out = {}, []
    for r in sorted(rows, key=lambda r: (r["paid_at"], r["payment_id"])):
        ev = json.loads(r["event"])
        feed = round(ev["amount"] * 100) if "amount" in ev else None
        amount = feed if feed is not None else last.get(r["customer_id"], 0)
        if feed is not None:
            last[r["customer_id"]] = feed
        out.append((r, amount))
    return out


def story(rows):
    """The case numbers the sandbox must reproduce."""
    copied = the_copy(rows)
    prev, by_day = {}, {}
    for r, amount in copied:
        d = r["paid_at"][:10]
        s = by_day.setdefault(d, {"n": 0, "bank": 0, "table": 0, "ret": 0, "rep": 0, "zero": 0})
        s["n"] += 1; s["bank"] += r["true_cents"]; s["table"] += amount; s["zero"] += amount == 0
        c = r["customer_id"]
        if c in prev:
            s["ret"] += 1; s["rep"] += prev[c] == amount
        prev[c] = amount
    june = [d for d in by_day if d >= "2026-06-01"]
    normal = [d for d in by_day if "2026-05-24" <= d <= "2026-05-31"]
    return {
        "sunday_bank": by_day["2026-06-14"]["bank"] / 100,
        "sunday_table": by_day["2026-06-14"]["table"] / 100,
        "gap_17_days": sum(by_day[d]["bank"] - by_day[d]["table"] for d in june) / 100,
        "baseline_pct": 100 * sum(by_day[d]["rep"] for d in normal) / sum(by_day[d]["ret"] for d in normal),
        "frozen_pct": 100 * by_day["2026-06-02"]["rep"] / by_day["2026-06-02"]["ret"],
        "zeros_a_night": sum(by_day[d]["zero"] for d in june) / len(june),
        "payments_a_night": sum(by_day[d]["n"] for d in normal) / len(normal),
        "by_day": by_day,
    }


if __name__ == "__main__":
    rows, last_customer = build()
    s = story(rows)

    with open("seeds/raw_pos_payments.csv", "w", newline="") as f:
        cols = ["payment_id", "customer_id", "cafe_id", "payment_method", "event", "paid_at", "_etl_loaded_at"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore", lineterminator="\n"); w.writeheader(); w.writerows(rows)

    with open("seeds/bank_deposits.csv", "w", newline="") as f:
        f.write("deposit_date,amount_eur\n")
        for d, v in sorted(s["by_day"].items()):
            f.write(f"{d},{v['bank'] / 100:.2f}\n")

    first = ["Noah", "Emma", "Liam", "Sophie", "Daan", "Julia", "Sem", "Mila", "Lucas", "Tess",
             "Finn", "Zoë", "Levi", "Sara", "Bram", "Eva", "Milan", "Lotte", "Jesse", "Fleur"]
    with open("seeds/raw_customers.csv") as f:
        jaffle = [r for r in csv.DictReader(f) if int(r["id"]) <= 100]
    with open("seeds/raw_customers.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "first_name", "last_name"], lineterminator="\n"); w.writeheader(); w.writerows(jaffle)
        rng = random.Random(7)
        for c in range(101, last_customer + 1):
            w.writerow({"id": c, "first_name": rng.choice(first), "last_name": f"{chr(65 + rng.randint(0, 25))}."})

    # Module 1, "Spot the defects", row for row. The caption's refresh date is the load column.
    with open("seeds/orders_daily_extract.csv", "w", newline="") as f:
        f.write("customer_id,name,email,order_date,order_total,updated_at,_loaded_at\n")
        f.write("C-1042,Eva Visser,e.visser@mail.com,2026-06-08,240.00,2026-06-08,2026-07-02 06:00:00\n")
        f.write("C-1043,Bram Bakker,,2026-06-09,89.50,2026-06-09,2026-07-02 06:00:00\n")
        f.write("C-1044,Priya Nair,priya.nair(at)mail,2026-06-10,-120.00,2026-06-10,2026-07-02 06:00:00\n")
        f.write("C-1042,Eva Visser,e.visser@mail.com,2027-01-14,240.00,2026-06-08,2026-07-02 06:00:00\n")
        f.write("C-1045,Jan de Wit,j.dewit@mail.com,2026-06-11,1310.00,2026-06-11,2026-07-02 06:00:00\n")

    print(f"raw_pos_payments: {len(rows)} events; customers: {last_customer}")
    for k in ["payments_a_night", "zeros_a_night", "baseline_pct", "frozen_pct", "sunday_bank", "sunday_table", "gap_17_days"]:
        print(f"  {k:18} {s[k]:,.2f}")
