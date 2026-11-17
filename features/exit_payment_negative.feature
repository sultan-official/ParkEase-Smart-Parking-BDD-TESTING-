Feature: Exit payment is refused when it cannot be completed
  As a registered ParkEase driver
  I want my parking fee to be charged automatically from my wallet when I exit
  So that I can leave the plaza without queuing at a payment booth

  @negative
  Scenario: Wallet is Rs. 1 short of the total payable
    Given the driver "Ali" is logged in
    And the driver has a linked petrol car with plate "LEA-1234"
    And the wallet balance is Rs. 239
    And the vehicle entered the plaza 2 hours and 10 minutes ago
    When the driver exits the plaza
    Then the screen shows "Insufficient wallet balance"
    And the total paid is Rs. 0
    And the wallet balance is now Rs. 239
    And the gate stays closed

  @negative
  Scenario: Driver who is not logged in cannot pay by wallet
    Given the driver "Ali" is not logged in
    And the driver has a linked petrol car with plate "LEA-1234"
    And the wallet balance is Rs. 1,000
    And the vehicle entered the plaza 2 hours and 10 minutes ago
    When the driver exits the plaza
    Then the screen shows "Please log in to pay by wallet"
    And the wallet balance is now Rs. 1,000
    And the gate stays closed
