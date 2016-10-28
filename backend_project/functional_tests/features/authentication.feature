Feature: User authentication
  As the owner of the system, I want the system have the authentication which will support authenticating the users.

  Scenario Outline: The unauthenticated users will be rejected
  As the anauthorized user, I will not log in successfully to the system

    Given I input <page> into browser address bar
    And I click on the login link
    And I Input username: <username> and password: <password>
    When I click on the sign in button
    Then I will see the error message: "<error_message>"

    Examples:
      | page                   | username   | password        | error_message       |
      | http://localhost:8000/ | ubknowuser | strangepassword | User is not existed |

  Scenario Outline: The existed users will be logged successfully
  As the valid user, I will log in successfully to the system

    Given I input <page> into browser address bar
    And I click on the login link
    And I Input username: <username> and password: <password>
    When I click on the sign in button
    Then I will see first <num> recipes in the page

    Examples:
      | page                   | username   | password        | num |
      | http://localhost:8000/ | ubknowuser | strangepassword | 25  |


  Scenario Outline: The unauthenticated users can see the public recipes
  As the new user who visit the first time the homne page, I want to see the list of public recipes in the home page

    Given The system now have 100 recipes
    When I input <page> into browser address bar
    Then I will see first <num> recipes in the page

    Examples:
      | page                   | num |
      | http://localhost:8000/ | 25  |

  Scenario Outline: The authenticated users can see the public recipes
  As the new user who visit the first time the homne page, I want to see the list of public recipes in the home page

    Given The system now have 100 recipes
    When I input <page> into browser address bar
    Then I will see first <num> recipes in the page

    Examples:
      | page                   | num |
      | http://localhost:8000/ | 20  |

