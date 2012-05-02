Feature: Test Lai

    In order to play with Lettuce

    Scenario: Make an update without transaction_id
        When I request the url "/" with the method "GET"
        I see a list of documents
