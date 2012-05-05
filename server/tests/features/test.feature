Feature: Test Lai

    In order to play with Lettuce

    Scenario: Make an update without transaction_id
        When I request the url "/" with the method "GET"
        Then The response status code should be 200

    Scenario: Make an update without transaction_id
        When I request the url "/" with the method "GET"
        Then I should get a json list

    Scenario: Make an update with transaction_id
        When I request the url "/1" with the method "GET"
        Then I should get a json list

    Scenario: Make an update with transaction_id
        When I request the url "/1" with the method "GET"
        Then The response status code should be 200

    Scenario: Make a commit without transaction_id and docs
        When I request the url "/" with the method "POST"
        Then The response status code should be 400

    Scenario: Make a commit with transaction_id and without docs
        When I request the url "/1" with the method "POST"
        Then The response status code should be 400
