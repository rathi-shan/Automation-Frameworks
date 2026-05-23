```gherkin
Feature: Biometric Bi-weekly Authentication Bypass Lockout
  As a mobile banking user
  I want the application to automatically lock my account after 3 consecutive failed FaceID attempts
  So that my financial data remains secure against unauthorized biometric access

  # ============================================================
  # HAPPY PATH SCENARIOS
  # ============================================================

  Scenario: Successful FaceID login on the first attempt clears any prior failed attempt counter
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has previously failed FaceID authentication 1 time
    And the account is not currently locked
    When the user presents a valid biometric face scan
    Then the application should authenticate the user successfully
    And the user should be granted access to the mobile banking dashboard
    And the consecutive failed FaceID attempt counter should be reset to 0
    And no lockout warning notification should be dispatched

  Scenario: Successful FaceID login on the second attempt after one failure resets the counter
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has previously failed FaceID authentication 1 time
    And the account is not currently locked
    When the user presents a valid biometric face scan on the second attempt
    Then the application should authenticate the user successfully
    And the user should be granted access to the mobile banking dashboard
    And the consecutive failed FaceID attempt counter should be reset to 0
    And any pending lockout warning state should be cleared

  Scenario: System administrator successfully unlocks a locked account via the secure admin dashboard
    Given a user account is currently locked due to 3 consecutive failed FaceID attempts
    And a system administrator is authenticated on the secure admin dashboard
    When the administrator locates the locked user profile by account ID
    And the administrator triggers the manual unlock override action
    Then the user account status should be updated to unlocked
    And the consecutive failed FaceID attempt counter should be reset to 0
    And the lockout timer should be cleared immediately
    And the user should be able to attempt FaceID authentication again
    And an audit log entry should be recorded capturing the administrator ID, timestamp, and override action

  Scenario: Account lockout expires automatically after exactly 15 minutes and user can re-authenticate
    Given a user account has been locked due to 3 consecutive failed FaceID attempts
    And the lockout timer has been running for exactly 15 minutes
    When the lockout duration of 15 minutes elapses
    Then the account should be automatically unlocked by the system
    And the consecutive failed FaceID attempt counter should be reset to 0
    And the user should be able to attempt FaceID authentication again without administrator intervention

  # ============================================================
  # SAD PATH / EDGE CASE SCENARIOS
  # ============================================================

  Scenario: Warning push notification is dispatched on exactly the 2nd consecutive failed FaceID attempt
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has previously failed FaceID authentication 1 time
    And the account is not currently locked
    And push notifications are enabled for the mobile banking application
    When the user presents an invalid biometric face scan for the 2nd consecutive time
    Then the FaceID authentication should fail
    And a warning push notification should be dispatched immediately to the user's registered device
    And the warning notification message should indicate that one more failed attempt will lock the account
    And the account should remain unlocked
    And the consecutive failed FaceID attempt counter should be incremented to 2

  Scenario: Account is locked immediately and precisely on the 3rd consecutive failed FaceID attempt
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has previously failed FaceID authentication 2 consecutive times
    And a warning push notification has already been dispatched
    And the account is not currently locked
    When the user presents an invalid biometric face scan for the 3rd consecutive time
    Then the FaceID authentication should fail
    And the account should be locked immediately
    And the 15-minute lockout countdown timer should start at the moment of the 3rd failure
    And the user should be presented with a message stating the account is locked for 15 minutes
    And the user should not be able to attempt FaceID authentication while the account is locked
    And the consecutive failed FaceID attempt counter should reflect 3 failed attempts

  Scenario: Account remains locked if the user attempts FaceID authentication before the 15-minute lockout expires
    Given a user account has been locked due to 3 consecutive failed FaceID attempts
    And the lockout timer has been running for only 7 minutes and 30 seconds
    When the user attempts FaceID authentication before the 15-minute lockout period has elapsed
    Then the authentication attempt should be rejected without processing the biometric scan
    And the user should be presented with a message indicating the remaining lockout duration
    And the account should remain in a locked state
    And the lockout timer should not be reset by the premature authentication attempt

  Scenario: Warning push notification is NOT dispatched on the 1st failed FaceID attempt
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the consecutive failed FaceID attempt counter is at 0
    And the account is not currently locked
    When the user presents an invalid biometric face scan for the 1st time
    Then the FaceID authentication should fail
    And no warning push notification should be dispatched
    And the user should be presented with a generic authentication failure message
    And the consecutive failed FaceID attempt counter should be incremented to 1
    And the account should remain unlocked

  Scenario: Failed FaceID attempts are not counted as consecutive when interrupted by a successful login
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has previously failed FaceID authentication 2 consecutive times
    And the user subsequently authenticated successfully resetting the counter to 0
    When the user presents an invalid biometric face scan
    Then the FaceID authentication should fail
    And the consecutive failed FaceID attempt counter should be incremented to 1
    And no warning push notification should be dispatched
    And the account should not be locked

  Scenario: System administrator cannot unlock an account that is not in a locked state
    Given a user account is currently in an active and unlocked state
    And a system administrator is authenticated on the secure admin dashboard
    When the administrator attempts to trigger the manual unlock override action on the active account
    Then the system should reject the override action
    And the administrator should be presented with an error message indicating the account is not locked
    And the user account status should remain unchanged
    And no audit log entry for an unlock override should be recorded

  Scenario: Lockout timer boundary condition - account remains locked at 14 minutes and 59 seconds
    Given a user account has been locked due to 3 consecutive failed FaceID attempts
    And the lockout timer has been running for 14 minutes and 59 seconds
    When the user attempts FaceID authentication at 14 minutes and 59 seconds into the lockout
    Then the authentication attempt should be rejected
    And the account should remain in a locked state
    And the system should not unlock the account until the full 15-minute duration has elapsed
```