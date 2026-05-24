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
    And the user has 0 consecutive failed FaceID attempts recorded
    When the user presents their face to the FaceID sensor
    And the biometric authentication system validates the face successfully
    Then the user should be granted access to the mobile banking dashboard
    And the consecutive failed attempt counter should remain at 0
    And no lockout should be applied to the account

  Scenario: Successful FaceID login after 1 prior failed attempt resets the failure counter
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has 1 consecutive failed FaceID attempt recorded
    When the user presents their face to the FaceID sensor
    And the biometric authentication system validates the face successfully
    Then the user should be granted access to the mobile banking dashboard
    And the consecutive failed attempt counter should be reset to 0
    And no lockout should be applied to the account
    And no warning push notification should be dispatched

  Scenario: Successful FaceID login after 2 prior failed attempts resets the failure counter
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has 2 consecutive failed FaceID attempts recorded
    And a warning push notification was previously dispatched
    When the user presents their face to the FaceID sensor
    And the biometric authentication system validates the face successfully
    Then the user should be granted access to the mobile banking dashboard
    And the consecutive failed attempt counter should be reset to 0
    And no lockout should be applied to the account

  Scenario: System administrator successfully unlocks a locked account via the secure admin dashboard
    Given a user account is currently locked due to 3 consecutive failed FaceID attempts
    And the lockout has been active for less than 15 minutes
    And a system administrator is authenticated on the secure admin dashboard
    When the administrator locates the locked user profile by account ID
    And the administrator triggers the manual override unlock action
    Then the user account status should be updated to "unlocked"
    And the consecutive failed attempt counter should be reset to 0
    And the lockout timer should be cleared
    And an audit log entry should be created recording the administrator ID, timestamp, and override action
    And the user should be able to attempt FaceID login immediately

  # ============================================================
  # SAD PATH / EDGE CASE SCENARIOS
  # ============================================================

  Scenario: Account locks after exactly 3 consecutive failed FaceID attempts
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has 2 consecutive failed FaceID attempts recorded
    And a warning push notification has already been dispatched
    When the user presents their face to the FaceID sensor for the 3rd consecutive time
    And the biometric authentication system fails to validate the face
    Then the user account should be immediately locked
    And the consecutive failed attempt counter should be set to 3
    And the lockout duration should be set to exactly 15 minutes
    And the user should be presented with an in-app message stating "Your account has been locked due to multiple failed login attempts. Please try again in 15 minutes."
    And the user should be denied access to the mobile banking dashboard

  Scenario: Warning push notification is dispatched on exactly the 2nd consecutive failed FaceID attempt
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has 1 consecutive failed FaceID attempt recorded
    When the user presents their face to the FaceID sensor for the 2nd consecutive time
    And the biometric authentication system fails to validate the face
    Then the consecutive failed attempt counter should be incremented to 2
    And a warning push notification should be dispatched to the user's registered device
    And the push notification message should read "Warning: One more failed Face ID attempt will lock your account."
    And the user account should remain unlocked
    And the user should be allowed to attempt FaceID login again

  Scenario: No warning push notification is dispatched on the 1st failed FaceID attempt
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has 0 consecutive failed FaceID attempts recorded
    When the user presents their face to the FaceID sensor
    And the biometric authentication system fails to validate the face
    Then the consecutive failed attempt counter should be incremented to 1
    And no push notification should be dispatched to the user's device
    And the user account should remain unlocked
    And the user should be allowed to attempt FaceID login again

  Scenario: Locked account automatically unlocks after exactly 15 minutes and resets the failure counter
    Given the user account is locked due to 3 consecutive failed FaceID attempts
    And the lockout timer was started at a recorded timestamp
    When exactly 15 minutes have elapsed since the lockout was initiated
    Then the user account status should be automatically updated to "unlocked"
    And the consecutive failed attempt counter should be reset to 0
    And the user should be able to attempt FaceID login again
    And no administrator intervention should be required

  Scenario: Locked account remains locked if fewer than 15 minutes have elapsed
    Given the user account is locked due to 3 consecutive failed FaceID attempts
    And the lockout timer has been active for 14 minutes and 59 seconds
    When the user attempts to authenticate via FaceID
    Then the user should be denied access to the mobile banking dashboard
    And the user should be presented with a message indicating the remaining lockout time
    And the account status should remain "locked"

  Scenario: FaceID failure counter does not increment beyond 3 while account is locked
    Given the user account is locked due to 3 consecutive failed FaceID attempts
    And the lockout timer has been active for 5 minutes
    When the user attempts to authenticate via FaceID multiple times during the lockout period
    Then each attempt should be rejected with a lockout message
    And the consecutive failed attempt counter should remain at 3 and not increment further
    And no additional push notifications should be dispatched
    And the lockout timer should not be reset by the additional attempts

  Scenario: Unauthorized user cannot access the admin unlock override without valid admin credentials
    Given a user account is currently locked due to 3 consecutive failed FaceID attempts
    When an unauthenticated actor attempts to access the secure admin dashboard unlock function
    Then access to the admin dashboard should be denied
    And an unauthorized access attempt should be logged in the security audit trail
    And the user account should remain locked
    And the lockout timer should continue unaffected

  Scenario: Warning push notification is not re-dispatched if the 2nd failed attempt notification was already sent and the account becomes locked on the 3rd attempt
    Given the user has a registered FaceID profile linked to their mobile banking account
    And the user has 2 consecutive failed FaceID attempts recorded
    And a warning push notification has already been dispatched for the 2nd failed attempt
    When the user presents their face to the FaceID sensor for the 3rd consecutive time
    And the biometric authentication system fails to validate the face
    Then the account should be locked
    And only one push notification should have been dispatched in total during this lockout cycle
    And no duplicate or additional warning push notification should be sent on the 3rd failed attempt

  Scenario: Consecutive failed attempt counter resets to zero after a successful login following a manual admin unlock
    Given a user account was locked due to 3 consecutive failed FaceID attempts
    And a system administrator has manually unlocked the account via the secure admin dashboard
    When the user presents their face to the FaceID sensor
    And the biometric authentication system validates the face successfully
    Then the user should be granted access to the mobile banking dashboard
    And the consecutive failed attempt counter should be 0
    And the account status should be "unlocked"
```