Feature: Automatic exit payment from the wallet
  As a registered ParkEase driver
  I want my parking fee to be charged automatically from my wallet when I exit
  So that I can leave the plaza without queuing at a payment booth

  @smoke
  Scenario: Registered EV pays for a stay of 3 hours and 40 minutes
    Given the driver "Ali" is logged in
    And the driver has a linked electric car with plate "LEB-2024"
    And the wallet balance is Rs. 1,000
    And the vehicle entered the plaza 3 hours and 40 minutes ago
    When the driver exits the plaza
    Then the screen shows "Payment successful – gate opening"
    And the parking fee is Rs. 280
    And the EV discount is Rs. 70
    And the service charge is Rs. 20
    And the total paid is Rs. 230
    And the wallet balance is now Rs. 770
    And the gate is open
