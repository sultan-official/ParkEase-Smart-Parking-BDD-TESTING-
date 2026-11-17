# ParkEase BDD project (Python + behave)

Automated Software Testing assignment: BDD for the ParkEase smart parking
exit payment (rules R1 to R8).

Author: Bushra Bilal (BSE241020) - Software Engineering, Capital University of Science and Technology

## Folder layout

```
ParkEase_BDD/
├── parkease.py                      in-memory ParkEase class (rules R1-R8)
├── behave.ini                       behave settings
├── requirements.txt
├── features/
│   ├── exit_payment_smoke.feature       C1  @smoke
│   ├── exit_fee_boundaries.feature      C2  @boundary
│   ├── exit_payment_negative.feature    C3  @negative
│   ├── exit_payment_rewrite.feature     C4  @rewrite
│   ├── environment.py                   hooks (fresh ParkEase for every scenario)
│   └── steps/
│       └── parkease_steps.py            thin step definitions + Money type
└── .github/workflows/smoke.yml      bonus: runs @smoke on every push
```

## Set up (once)

```
pip install -r requirements.txt
```

## Run all tests (one command)

```
behave
```

## Other useful commands

```
behave --tags=@smoke        # only the smoke scenario
behave --tags=@boundary     # only the boundary scenarios
behave --tags=@negative     # only the negative scenarios
```

## Break a rule on purpose (Part D3)

Open `parkease.py`, find the line `BUG_MODE = ""` and change it to
`BUG_MODE = "ev_before_cap"`. Run `behave` again and one scenario fails.
Change it back to `BUG_MODE = ""` afterwards.
