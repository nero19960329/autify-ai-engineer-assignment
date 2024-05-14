describe("Snippet List Functionality", () => {
  // Setup before each test
  beforeEach(() => {
    cy.request("GET", "/snippets").then((response) => {
      response.body.forEach((snippet) => {
        cy.request("DELETE", `/snippets/${snippet.id}`);
      });
    });
    cy.visit("/");
  });

  it("should be able to click and load previously generated snippets", () => {
    // Create a new snippet
    cy.request("POST", "/snippets", {
      title: "Test Snippet",
      language: "python",
      description: "This is a test snippet.",
      code: "print('Hello, world!')",
    }).then((response) => {
      const snippetId = response.body.id;

      // Visit the page and ensure the snippet is listed
      cy.visit("/");
      cy.get("#snippet-list").children().should("have.length", 1);

      // Click on the snippet and verify that its details are loaded
      cy.get(`a[data-id="${snippetId}"]`).click();
      cy.get("#snippet-detail textarea").should(
        "have.value",
        "This is a test snippet.",
      );
      cy.get("#generated-code code").should(
        "contain.text",
        "print('Hello, world!')",
      );
    });
  });

  it("should be able to delete previously generated snippets", () => {
    // Create two new snippets
    cy.request("POST", "/snippets", {
      title: "Test Snippet 1",
      language: "python",
      description: "This is test snippet 1.",
      code: "print('Hello, world 1!')",
    });
    cy.request("POST", "/snippets", {
      title: "Test Snippet 2",
      language: "python",
      description: "This is test snippet 2.",
      code: "print('Hello, world 2!')",
    }).then(() => {
      // Visit the page and ensure the snippets are listed
      cy.visit("/");
      cy.get("#snippet-list").children().should("have.length", 2);

      // Click the delete button for the first snippet
      cy.get("#snippet-list .delete-btn").first().click();

      // Confirm that the first snippet is deleted
      cy.get("#snippet-list").children().should("have.length", 1);

      // Confirm that the remaining snippet is the second snippet
      cy.get("#snippet-list .snippet-item")
        .first()
        .should("contain.text", "Test Snippet 2");
    });
  });

  it("should be able to create new snippets", () => {
    // Click the create new snippet button
    cy.get("#create-snippet-btn").click();

    // Verify that a new snippet is added to the list
    cy.get("#snippet-list").children().should("have.length", 1);

    // Verify that the new snippet's detail is loaded in the editor
    cy.get("#snippet-detail textarea").should("be.visible");
    cy.get("#snippet-detail #generate-code-btn").should("be.visible");

    // Check if the new snippet is selected and highlighted
    cy.get("#snippet-list .snippet-item")
      .first()
      .should("have.class", "bg-gray-500");
  });

  it("should automatically save snippet when the 'Generate' button is clicked", () => {
    // Click the create new snippet button
    cy.get("#create-snippet-btn").click();

    // Input description for the new snippet
    cy.get("#code-description").type("Write a function to add two numbers.");

    // Intercept the generate code API request
    cy.intercept("POST", "/generate/code", {
      body: "def add(a, b): return a + b",
    }).as("generateCode");

    // Intercept the generate title API request
    cy.intercept("POST", "/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Intercept the detect language API request
    cy.intercept("POST", "/generate/detect_language", {
      body: '{"language": "python"}',
    }).as("detectLanguage");

    // Click the generate code button
    cy.get("#generate-code-btn").click();

    // Wait for the generate code API request to complete
    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    // Verify that the generated code is displayed
    cy.get("#generated-code code").should(
      "contain.text",
      "def add(a, b): return a + b",
    );

    // Verify that the snippet is saved and can be retrieved
    cy.request("GET", "/snippets").then((response) => {
      expect(response.body.length).to.equal(1);
      const snippet = response.body[0];
      expect(snippet.description).to.equal(
        "Write a function to add two numbers.",
      );
      expect(snippet.code).to.equal("def add(a, b): return a + b");
      expect(snippet.language).to.equal("python");
    });
  });

  it("should automatically generate title and language of the snippets", () => {
    // Click the create new snippet button
    cy.get("#create-snippet-btn").click();

    // Input description for the new snippet
    cy.get("#code-description").type("Write a function to add two numbers.");

    // Intercept the generate code API request
    cy.intercept("POST", "/generate/code", {
      body: "def add(a, b): return a + b",
    }).as("generateCode");

    // Intercept the generate title API request
    cy.intercept("POST", "/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Intercept the detect language API request
    cy.intercept("POST", "/generate/detect_language", {
      body: '{"language": "python"}',
    }).as("detectLanguage");

    // Click the generate code button
    cy.get("#generate-code-btn").click();

    // Wait for the generate code, title, and detect language API requests to complete
    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    // Verify that the generated code is displayed
    cy.get("#generated-code code").should(
      "contain.text",
      "def add(a, b): return a + b",
    );

    // Verify that the snippet title and language are generated and saved
    cy.request("GET", "/snippets").then((response) => {
      expect(response.body.length).to.equal(1);
      const snippet = response.body[0];
      expect(snippet.title).to.equal("Addition Function");
      expect(snippet.language).to.equal("python");
    });
  });
});
