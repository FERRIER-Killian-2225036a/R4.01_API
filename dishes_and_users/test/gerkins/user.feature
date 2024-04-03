# Created by flouksac at 01/04/2024
Feature: User has crud operations on the database

  Scenario: User can be created
    Given API is running
    When We try to create a User
    Then Status code is "200"
    Then User is created in the database

  Scenario: User can be read
    Given API is running
    Given A User exists in the database
    When We try to read a User
    Then Status code is "200"
    Then User is retrieved from the database in the response


  Scenario: User can be updated
    Given API is running
    Given A User exists in the database
    When We try to update the User
    Then Status code is "200"
    Then User information is updated in the database



  Scenario: User can be deleted
    Given API is running
    Given A User exists in the database
    When We try to delete the User
    Then Status code is "200"
    Then User is removed from the database

  Scenario: Attempting to create a User that already exists
    Given API is running
    Given A User exists in the database
    When We try to create a User that already exists
    Then User creation fails
    And Status code is "412"

  Scenario: Attempting to read a non-existing User
    Given API is running
    When We try to read a non-existing User
    Then User is not found in the database
    And Status code is "412"

  Scenario: Attempting to update a non-existing User
    Given API is running
    When We try to update a non-existing User
    Then User update operation fails
    And Status code is "412"

  Scenario: Attempting to delete a non-existing User
    Given API is running
    When We try to delete a non-existing User
    Then User delete operation fails
    And Status code is "412"
