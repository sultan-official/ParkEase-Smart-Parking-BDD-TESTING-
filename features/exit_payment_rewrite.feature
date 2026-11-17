Feature: Rewritten scenarios from the critique (Part C4)
  As a registered ParkEase driver
  I want my parking fee to be charged automatically from my wallet when I exit
  So that I can leave the plaza without queuing at a payment booth

  @rewrite
  Scenario: Registered driver pays the exit fee from the wallet
    Given the driver "Ali" is logged in
    And the driver has a linked petrol car with plate "LEA-1234"
    And the wallet balance is Rs. 500
    And the vehicle entered the plaza 2 hours and 10 minutes ago
    When the driver exits the plaza
    Then the screen shows "Payment successful – gate opening"
    And the parking fee is Rs. 220
    And the service charge is Rs. 20
    And the wallet balance is now Rs. 260

  @rewrite
  Scenario: Gate opens after a successful payment
    Given the driver "Ali" is logged in
    And the driver has a linked petrol car with plate "LEA-1234"
    And the wallet balance is Rs. 500
    And the vehicle entered the plaza 2 hours and 10 minutes ago
    When the driver exits the plaza
    Then the total paid is Rs. 240
    And the gate is open
