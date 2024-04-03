# Created by flouksac at 01/04/2024
Feature: Dish has crud operations on the database

  Scenario: Dish can be created
    Given API is running
    When We try to create a Dish
    Then Status code is "200"
    Then Dish is created in the database

  Scenario: Dish can be read
    Given API is running
    Given A Dish exists in the database
    When We try to read a Dish
    Then Status code is "200"
    Then Dish is retrieved from the database in the response


  Scenario: Dish can be updated
    Given API is running
    Given A Dish exists in the database
    When We try to update the Dish
    Then Status code is "200"
    Then Dish information is updated in the database

  Scenario: Dish can be deleted
    Given API is running
    Given A Dish exists in the database
    When We try to delete the Dish
    Then Status code is "200"
    Then Dish is removed from the database

  Scenario: Attempting to create a Dish that already exists
    Given API is running
    Given A Dish exists in the database
    When We try to create a Dish that already exists
    Then Dish creation fails
    And Status code is "412"

  Scenario: Attempting to read a non-existing Dish
    Given API is running
    When We try to read a non-existing Dish
    Then Dish is not found in the database
    And Status code is "412"

  Scenario: Attempting to update a non-existing Dish
    Given API is running
    When We try to update a non-existing Dish
    Then Dish update operation fails
    And Status code is "412"

  Scenario: Attempting to delete a non-existing Dish
    Given API is running
    When We try to delete a non-existing Dish
    Then Dish delete operation fails
    And Status code is "412"
