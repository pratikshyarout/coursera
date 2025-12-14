Feature: Product Management API
  As a client of the Product service
  I want to manage and query products
  So that I can read, update, delete, and search products efficiently

  Background:
    Given the database is populated with BDD test data
  Scenario: List all products
    When I send a GET request to "/api/products/"
    Then the response status code should be 200
    And the response should contain a list of products
  Scenario: Read a product by ID
    When I send a GET request to "/api/products/1/"
    Then the response status code should be 200
    And the response should contain product details
  Scenario: Update a product price
    When I send a PATCH request to "/api/products/1/" with payload:
      """
      {
        "price": 799
      }
      """
    Then the response status code should be 200
    And the product price should be updated to 799
  Scenario: Delete a product
    When I send a DELETE request to "/api/products/1/"
    Then the response status code should be 204
    And the product should no longer exist
  Scenario: Search products by name
    When I send a GET request to "/api/products/?name=iphone"
    Then the response status code should be 200
    And the response should contain products with name containing "iphone"
  Scenario: Search products by category
    When I send a GET request to "/api/products/?category=Electronics"
    Then the response status code should be 200
    And the response should contain only products from category "Electronics"
  Scenario: Search products by availability
    When I send a GET request to "/api/products/?available=true"
    Then the response status code should be 200
    And the response should contain only available products
