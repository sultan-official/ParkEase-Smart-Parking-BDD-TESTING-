"""Step definitions for the ParkEase scenarios.

The steps are thin: they only call ParkEase or compare values.
There is no fee arithmetic in this file. All rules live in parkease.py.
"""

from behave import given, when, then, register_type


# ---------------------------------------------------------------------------
# Custom parameter type: turns "Rs. 1,000" into the integer 1000
# ---------------------------------------------------------------------------
def parse_money(text):
    return int(text.replace("Rs.", "").replace(",", "").strip())


parse_money.pattern = r"Rs\. [\d,]+"
register_type(Money=parse_money)


# ---------------------------------------------------------------------------
# Helpers for clear failure messages (expected vs actual)
# ---------------------------------------------------------------------------
def rs(value):
    return f"Rs. {value:,}"


def check_amount(label, expected, actual):
    assert actual == expected, (
        f"{label}: expected {rs(expected)} but got {rs(actual)}"
    )


# ---------------------------------------------------------------------------
# Given
# ---------------------------------------------------------------------------
@given('the driver "{name}" is logged in')
def step_logged_in(context, name):
    context.app.login(name)


@given('the driver "{name}" is not logged in')
def step_not_logged_in(context, name):
    context.app.logout()


@given('the driver has a linked {kind} car with plate "{plate}"')
def step_linked_car(context, kind, plate):
    assert kind in ("electric", "petrol"), f"unknown car type: {kind}"
    context.app.link_vehicle(plate, electric=(kind == "electric"))
    context.plate = plate


@given("the wallet balance is {amount:Money}")
def step_wallet(context, amount):
    context.app.set_wallet(amount)


@given("the vehicle entered the plaza {hours:d} hours and {minutes:d} minutes ago")
def step_entry_hours_minutes(context, hours, minutes):
    context.minutes = hours * 60 + minutes
    context.seconds = 0


@given("the vehicle entered the plaza {minutes:d} minutes and {seconds:d} seconds ago")
def step_entry_minutes_seconds(context, minutes, seconds):
    context.minutes = minutes
    context.seconds = seconds


# ---------------------------------------------------------------------------
# When
# ---------------------------------------------------------------------------
@when("the driver exits the plaza")
def step_exit(context):
    context.result = context.app.exit(context.plate, context.minutes, context.seconds)


# ---------------------------------------------------------------------------
# Then
# ---------------------------------------------------------------------------
@then('the screen shows "{message}"')
def step_message(context, message):
    actual = context.result.message
    assert actual == message, f'message: expected "{message}" but got "{actual}"'


@then("the parking fee is {amount:Money}")
def step_parking_fee(context, amount):
    check_amount("parking fee", amount, context.result.parking_fee)


@then("the EV discount is {amount:Money}")
def step_ev_discount(context, amount):
    check_amount("EV discount", amount, context.result.ev_discount)


@then("the service charge is {amount:Money}")
def step_service_charge(context, amount):
    check_amount("service charge", amount, context.result.service_charge)


@then("the total paid is {amount:Money}")
def step_total_paid(context, amount):
    check_amount("total paid", amount, context.result.total_paid)


@then("the wallet balance is now {amount:Money}")
def step_wallet_now(context, amount):
    check_amount("wallet balance", amount, context.app.wallet_balance())


@then("the gate is open")
def step_gate_open(context):
    assert context.result.gate_open is True, "gate: expected open but it is closed"


@then("the gate stays closed")
def step_gate_closed(context):
    assert context.result.gate_open is False, "gate: expected closed but it is open"
