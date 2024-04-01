# Created by flouksac at 01/04/2024
Feature: Utils and Authentication from a user

  Scenario: Authentication from a user with good credentials
    Given API is running
    Given a user with a username and a password
    When the user tries to authenticate correctly
    Then Status code is "200"
    Then the api should return a good response

    
  Scenario: Authentication from a user with bad credentials
    Given API is running
    Given a user with a username and a password
    When the user tries to authenticate with bad credentials
    Then Status code is "412"

    Then the api should return a bad response