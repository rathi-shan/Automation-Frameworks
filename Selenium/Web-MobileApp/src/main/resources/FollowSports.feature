// Feature file

  Feature: Follow sports feature
    As a News App user
    I want to follow my favourite sports
    So that I get personlized push notification

    Scenario: User follows Hocky for olympics
      Given the user is logged into the CBC News app
      When the user navigates to the "Follow Sports" section
      And selects "Hockey"
      Then the "Hockey" sport should be added to the "My Followed Sports" list


