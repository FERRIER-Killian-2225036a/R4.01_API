# Created by killian at 01/04/2024
Feature: Menu has crud operations on the database

  Scenario: Menu can be created
    Given API is running
    When We try to create a Menu
    Then Status code is "200"
    Then Menu is created in the database

  Scenario: Menu can be read
    Given API is running
    Given A Menu exists in the database
    When We try to read a Menu
    Then Status code is "200"
    Then Menu is retrieved from the database in the response


  Scenario: Menu can be updated
    Given API is running
    Given A Menu exists in the database
    When We try to update the Menu
    Then Status code is "200"
    Then Menu information is updated in the database

  Scenario: Menu can be deleted
    Given API is running
    Given A Menu exists in the database
    When We try to delete the Menu
    Then Status code is "200"
    Then Menu is removed from the database

  Scenario: Attempting to create a Menu that already exists
    Given API is running
    Given A Menu exists in the database
    When We try to create a Menu that already exists
    Then Menu creation fails
    And Status code is "412"

  Scenario: Attempting to read a non-existing Menu
    Given API is running
    When We try to read a non-existing Menu
    Then Menu is not found in the database
    And Status code is "412"

  Scenario: Attempting to update a non-existing Menu
    Given API is running
    When We try to update a non-existing Menu
    Then Menu update operation fails
    And Status code is "412"

  Scenario: Attempting to delete a non-existing Menu
    Given API is running
    When We try to delete a non-existing Menu
    Then Menu delete operation fails
    And Status code is "412"
