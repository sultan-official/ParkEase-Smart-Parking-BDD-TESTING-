"""ParkEase - a small in-memory model of the exit payment (rules R1 to R8).

There is no real app, database or screen here. The class only keeps the
state that the business rules need: who is logged in, which vehicles are
linked, and the wallet balance.
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Business constants (all rule numbers live here, so they are easy to find)
# ---------------------------------------------------------------------------
GRACE_SECONDS = 15 * 60      # R2: up to and including 15:00 minutes is free
FIRST_HOUR_FEE = 100         # R3: first hour
EXTRA_HOUR_FEE = 60          # R3: each additional started hour
FEE_CAP = 800                # R4: cap for one visit
EV_DISCOUNT_PERCENT = 25     # R5: EV discount, applied AFTER the cap
SERVICE_CHARGE = 20          # R6: fixed, never discounted, not for free exits

# ---------------------------------------------------------------------------
# Part D3 only: break one rule on purpose.
# Normal value is "" (everything correct). Allowed values:
#   ""                        -> correct behaviour
#   "ev_before_cap"           -> EV discount applied BEFORE the cap (breaks R5)
#   "discount_service_charge" -> EV also gets a discount on Rs. 20 (breaks R6)
# ---------------------------------------------------------------------------
BUG_MODE = ""

# Messages (R7, R8 and the assumptions listed in the report)
MSG_SUCCESS = "Payment successful – gate opening"
MSG_FREE = "Free exit – gate opening"
MSG_INSUFFICIENT = "Insufficient wallet balance"
MSG_NOT_LOGGED_IN = "Please log in to pay by wallet"
MSG_NOT_LINKED = "Vehicle is not linked to your account"


@dataclass
class ExitResult:
    """What the exit gate shows after a driver tries to leave."""

    message: str
    parking_fee: int = 0      # fee after the cap, before the EV discount
    ev_discount: int = 0
    service_charge: int = 0
    total_paid: int = 0       # what was really taken from the wallet
    gate_open: bool = False


class ParkEase:
    def __init__(self):
        self._driver = None       # name of the logged-in driver, or None
        self._vehicles = {}       # plate -> True if electric vehicle
        self._wallet = 0

    # ----- set-up methods used by the Given steps --------------------------
    def login(self, driver):
        self._driver = driver

    def logout(self):
        self._driver = None

    def link_vehicle(self, plate, electric=False):
        self._vehicles[plate] = electric

    def set_wallet(self, rupees):
        self._wallet = rupees

    def wallet_balance(self):
        return self._wallet

    # ----- the exit action -------------------------------------------------
    def exit(self, plate, minutes_parked, seconds_parked=0):
        # R1: logged in, and the vehicle must be linked to the account
        if self._driver is None:
            return ExitResult(MSG_NOT_LOGGED_IN)
        if plate not in self._vehicles:
            return ExitResult(MSG_NOT_LINKED)

        total_seconds = minutes_parked * 60 + seconds_parked

        # R2: grace period (15:00 minutes is still free)
        if total_seconds <= GRACE_SECONDS:
            return ExitResult(MSG_FREE, gate_open=True)

        # R3: every started hour counts (61 minutes = 2 hours)
        started_hours = -(-total_seconds // 3600)          # round up
        fee_before_cap = FIRST_HOUR_FEE + EXTRA_HOUR_FEE * (started_hours - 1)

        is_ev = self._vehicles[plate]

        if BUG_MODE == "ev_before_cap" and is_ev:
            # WRONG ORDER (used only in Part D3): discount first, cap second
            discount = fee_before_cap * EV_DISCOUNT_PERCENT // 100
            parking_fee = fee_before_cap
            fee_after_discount = min(fee_before_cap - discount, FEE_CAP)
        else:
            # R4: cap first, then R5: EV discount on the capped fee
            parking_fee = min(fee_before_cap, FEE_CAP)
            discount = parking_fee * EV_DISCOUNT_PERCENT // 100 if is_ev else 0
            fee_after_discount = parking_fee - discount

        # R6: fixed service charge, never discounted
        service_charge = SERVICE_CHARGE
        if BUG_MODE == "discount_service_charge" and is_ev:
            service_charge = SERVICE_CHARGE - SERVICE_CHARGE * EV_DISCOUNT_PERCENT // 100

        total_payable = fee_after_discount + service_charge

        # R7: wallet must cover the total, otherwise nothing is deducted
        if self._wallet < total_payable:
            return ExitResult(
                MSG_INSUFFICIENT,
                parking_fee=parking_fee,
                ev_discount=discount,
                service_charge=service_charge,
                total_paid=0,
                gate_open=False,
            )

        # R8: successful payment
        self._wallet -= total_payable
        return ExitResult(
            MSG_SUCCESS,
            parking_fee=parking_fee,
            ev_discount=discount,
            service_charge=service_charge,
            total_paid=total_payable,
            gate_open=True,
        )
