Feature: Parking fee at the boundaries
  As a registered ParkEase driver
  I want my parking fee to be charged automatically from my wallet when I exit
  So that I can leave the plaza without queuing at a payment booth

  @boundary
  Scenario Outline: Petrol car fee for the grace, rounding and cap boundaries
    Given the driver "Ali" is logged in
    And the driver has a linked petrol car with plate "LEA-1234"
    And the wallet balance is Rs. 1,000
    And the vehicle entered the plaza <minutes> minutes and <seconds> seconds ago
    When the driver exits the plaza
    Then the screen shows "<message>"
    And the parking fee is Rs. <fee>
    And the service charge is Rs. <service>
    And the total paid is Rs. <total>
    And the wallet balance is now Rs. <balance>

    Examples: Free and rounding
      | minutes | seconds | message                           | fee | service | total | balance |
      | 15      | 0       | Free exit – gate opening          | 0   | 0       | 0     | 1,000   |
      | 15      | 1       | Payment successful – gate opening | 100 | 20      | 120   | 880     |
      | 60      | 0       | Payment successful – gate opening | 100 | 20      | 120   | 880     |
      | 61      | 0       | Payment successful – gate opening | 160 | 20      | 180   | 820     |
      | 121     | 0       | Payment successful – gate opening | 220 | 20      | 240   | 760     |

    Examples: Daily cap
      | minutes | seconds | message                           | fee | service | total | balance |
      | 720     | 0       | Payment successful – gate opening | 760 | 20      | 780   | 220     |
      | 721     | 0       | Payment successful – gate opening | 800 | 20      | 820   | 180     |
      | 1440    | 0       | Payment successful – gate opening | 800 | 20      | 820   | 180     |

  @boundary
  Scenario: EV discount is calculated after the cap
    Given the driver "Sara" is logged in
    And the driver has a linked electric car with plate "LEB-2024"
    And the wallet balance is Rs. 1,000
    And the vehicle entered the plaza 13 hours and 0 minutes ago
    When the driver exits the plaza
    Then the screen shows "Payment successful – gate opening"
    And the parking fee is Rs. 800
    And the EV discount is Rs. 200
    And the service charge is Rs. 20
    And the total paid is Rs. 620
    And the wallet balance is now Rs. 380

  @boundary
  Scenario: EV leaving inside the grace period pays nothing
    Given the driver "Sara" is logged in
    And the driver has a linked electric car with plate "LEB-2024"
    And the wallet balance is Rs. 1,000
    And the vehicle entered the plaza 15 minutes and 0 seconds ago
    When the driver exits the plaza
    Then the screen shows "Free exit – gate opening"
    And the service charge is Rs. 0
    And the total paid is Rs. 0
    And the wallet balance is now Rs. 1,000
    And the gate is open
