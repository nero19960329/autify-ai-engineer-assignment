describe("Code Snippet Generator E2E Tests", () => {
  // Setup before each test
  beforeEach(() => {
    cy.request("GET", "/api/snippets").then((response) => {
      response.body.forEach((snippet) => {
        cy.request("DELETE", `/api/snippets/${snippet.id}`);
      });
    });
    cy.visit("/");
  });

  // Snippet Tests

  it("should have no snippets initially", () => {
    cy.get("#snippet-list").children().should("have.length", 0);
    cy.get("#snippet-detail").should(
      "contain",
      "Select a snippet from the list to view details.",
    );
  });

  it("should create a new snippet, highlight it, and display its details", () => {
    cy.get("#create-snippet-btn").click();
    cy.get("#snippet-list").children().should("have.length", 1);
    cy.get("#snippet-list .snippet-item")
      .first()
      .should("have.class", "bg-gray-500");
    cy.get("#snippet-detail textarea").should("be.visible");
    cy.get("#snippet-detail #generate-code-btn").should("be.visible");
  });

  it("should not show delete button when there is only one snippet", () => {
    cy.get("#create-snippet-btn").click();
    cy.get("#snippet-list").children().should("have.length", 1);
    cy.get("#snippet-list .delete-btn").should("not.exist");
  });

  it("should delete a snippet when there are multiple snippets", () => {
    cy.get("#create-snippet-btn").click();
    cy.get("#create-snippet-btn").click();
    cy.get("#create-snippet-btn").click();
    cy.get("#snippet-list").children().should("have.length", 3);

    cy.get("#snippet-list .delete-btn").first().click();
    cy.get("#snippet-list").children().should("have.length", 2);

    cy.get("#snippet-list .delete-btn").first().click();
    cy.get("#snippet-list").children().should("have.length", 1);
    cy.get("#snippet-list .delete-btn").should("not.exist");

    cy.get("#snippet-list .snippet-item")
      .first()
      .should("have.class", "bg-gray-500");
    cy.get("#snippet-detail textarea").should("be.visible");
    cy.get("#snippet-detail #generate-code-btn").should("be.visible");
  });

  it("should hide delete button and highlight the selected snippet when a snippet is selected", () => {
    // Create multiple snippets
    cy.get("#create-snippet-btn").click();
    cy.get("#create-snippet-btn").click();
    cy.get("#create-snippet-btn").click();
    cy.get("#snippet-list").children().should("have.length", 3);

    // Select the second snippet
    cy.get("#snippet-list .snippet-item").eq(1).click();
    cy.get("#snippet-list .snippet-item")
      .eq(1)
      .should("have.class", "bg-gray-500");
    cy.get("#snippet-list .delete-btn").should("have.length", 2);
    cy.get("#snippet-list .snippet-item")
      .eq(0)
      .should("not.have.class", "bg-gray-500");
    cy.get("#snippet-list .snippet-item")
      .eq(2)
      .should("not.have.class", "bg-gray-500");

    // Select the first snippet
    cy.get("#snippet-list .snippet-item").eq(0).click();
    cy.get("#snippet-list .snippet-item")
      .eq(0)
      .should("have.class", "bg-gray-500");
    cy.get("#snippet-list .delete-btn").should("have.length", 2);
    cy.get("#snippet-list .snippet-item")
      .eq(1)
      .should("not.have.class", "bg-gray-500");
    cy.get("#snippet-list .snippet-item")
      .eq(2)
      .should("not.have.class", "bg-gray-500");
  });

  // UI Tests

  it("should hide test generation section initially", () => {
    cy.get("#create-snippet-btn").click();
    cy.get("#test-generation-section").should("not.be.visible");
  });

  it("should display test generation section after code generation", () => {
    // Simulate code generation
    cy.intercept("POST", "/api/generate/code", {
      body: "def add(a, b): return a + b",
    }).as("generateCode");

    // Simulate title generation
    cy.intercept("POST", "/api/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Simulate language detection
    cy.intercept("POST", "/api/generate/detect_language", {
      body: '{"language": "python"}',
    }).as("detectLanguage");

    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type("Write a function to add two numbers.");
    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    cy.get("#generated-code code").should("not.be.empty");
    cy.get("#test-generation-section").should("be.visible");
  });

  it("should retain test generation section visibility after improving code", () => {
    // Simulate code generation
    cy.intercept("POST", "/api/generate/code", {
      body: "def add(a, b): return a + b",
    }).as("generateCode");

    // Simulate title generation
    cy.intercept("POST", "/api/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Simulate language detection
    cy.intercept("POST", "/api/generate/detect_language", {
      body: '{"language": "python"}',
    }).as("detectLanguage");

    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type("Write a function to add two numbers.");
    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    cy.get("#generated-code code").should("not.be.empty");
    cy.get("#test-generation-section").should("be.visible");

    // Improve code
    cy.intercept("POST", "/api/generate/code_from_feedback", {
      body: "def add(a: int, b: int) -> int: return a + b",
    }).as("improveCode");

    cy.get("#code-feedback").type("Add type hints to the parameters.");
    cy.get("#improve-code-btn").click();

    cy.wait("@improveCode");

    cy.get("#generated-code code").should(
      "contain",
      "def add(a: int, b: int) -> int: return a + b",
    );
    cy.get("#test-generation-section").should("be.visible");
  });

  it("should handle multiple code generations and retain test generation section visibility", () => {
    // Simulate initial code generation
    cy.intercept("POST", "/api/generate/code", {
      body: "def add(a, b): return a + b",
    }).as("generateCode");

    // Simulate initial title generation
    cy.intercept("POST", "/api/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Simulate initial language detection
    cy.intercept("POST", "/api/generate/detect_language", {
      body: '{"language": "python"}',
    }).as("detectLanguage");

    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type("Write a function to add two numbers.");
    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    cy.get("#generated-code code").should("not.be.empty");
    cy.get("#test-generation-section").should("be.visible");

    // Simulate second code generation
    cy.intercept("POST", "/api/generate/code", {
      body: "def subtract(a, b): return a - b",
    }).as("generateCodeAgain");

    // Simulate second title generation
    cy.intercept("POST", "/api/generate/title", {
      body: "Subtraction Function",
    }).as("generateTitleAgain");

    // Simulate second language detection
    cy.intercept("POST", "/api/generate/detect_language", {
      body: '{"language": "python"}',
    }).as("detectLanguageAgain");

    cy.get("#code-description")
      .clear()
      .type("Write a function to subtract two numbers.");
    cy.get("#generate-code-btn").click();

    cy.wait("@generateCodeAgain");
    cy.wait("@generateTitleAgain");
    cy.wait("@detectLanguageAgain");

    cy.get("#generated-code code").should(
      "contain",
      "def subtract(a, b): return a - b",
    );
    cy.get("#test-generation-section").should("be.visible");
  });

  it("should enable the regenerate button when tests fail", () => {
    // Simulate code generation
    cy.intercept("POST", "/api/generate/code", {
      body: "def add(a, b): return a + b",
    }).as("generateCode");

    // Simulate title generation
    cy.intercept("POST", "/api/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Simulate language detection
    cy.intercept("POST", "/api/generate/detect_language", {
      body: '{"language": "python"}',
    }).as("detectLanguage");

    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type("Write a function to add two numbers.");
    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    cy.get("#generated-code code").should("not.be.empty");
    cy.get("#test-generation-section").should("be.visible");

    // Simulate test generation
    cy.intercept("POST", "/api/generate/tests", {
      body: "assert add(1, 2) == 3",
    }).as("generateTests");

    cy.get("#generate-tests-btn").click();
    cy.wait("@generateTests");

    cy.get("#generated-tests code").should("not.be.empty");

    // Simulate running tests with a failing test case
    cy.intercept("POST", "/api/run/python", {
      body: {
        result: "failure",
        message: "AssertionError: assert add(1, 2) == 3",
      },
    }).as("runTests");

    cy.get("#run-tests-btn").click();
    cy.wait("@runTests");

    cy.get("#test-results").should(
      "contain",
      "AssertionError: assert add(1, 2) == 3",
    );
    cy.get("#regenerate-btn").should("not.be.disabled");
    cy.get("#regenerate-btn").should("have.class", "bg-green-500");
  });

  it("should disable the regenerate button when tests pass", () => {
    // Simulate code generation
    cy.intercept("POST", "/api/generate/code", {
      body: "def add(a, b): return a + b",
    }).as("generateCode");

    // Simulate title generation
    cy.intercept("POST", "/api/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Simulate language detection
    cy.intercept("POST", "/api/generate/detect_language", {
      body: '{"language": "python"}',
    }).as("detectLanguage");

    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type("Write a function to add two numbers.");
    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    cy.get("#generated-code code").should("not.be.empty");
    cy.get("#test-generation-section").should("be.visible");

    // Simulate test generation
    cy.intercept("POST", "/api/generate/tests", {
      body: "assert add(1, 2) == 3",
    }).as("generateTests");

    cy.get("#generate-tests-btn").click();
    cy.wait("@generateTests");

    cy.get("#generated-tests code").should("not.be.empty");

    // Simulate running tests with a passing test case
    cy.intercept("POST", "/api/run/python", {
      body: {
        result: "success",
        message: "Code Executed Successfully",
      },
    }).as("runTests");

    cy.get("#run-tests-btn").click();
    cy.wait("@runTests");

    cy.get("#test-results").should("contain", "Code Executed Successfully");
    cy.get("#regenerate-btn").should("be.disabled");
    cy.get("#regenerate-btn").should("have.class", "bg-gray-500");
  });

  it("should highlight generated Python code correctly", () => {
    // Simulate code generation for Python
    cy.intercept("POST", "/api/generate/code", {
      body: "def add(a, b): return a + b",
    }).as("generateCode");

    // Simulate title generation
    cy.intercept("POST", "/api/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Simulate language detection
    cy.intercept("POST", "/api/generate/detect_language", {
      body: '{"language": "python"}',
    }).as("detectLanguage");

    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type("Write a function to add two numbers.");
    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    cy.get("#generated-code code").should("not.be.empty");
    cy.get("#generated-code code").should("have.class", "python");
    cy.get("#generated-code code").within(() => {
      cy.get(".hljs-keyword").should("contain.text", "def");
      cy.get(".hljs-title").should("contain.text", "add");
      cy.get(".hljs-params").should("contain.text", "a, b");
    });
  });

  it("should highlight generated JavaScript code correctly", () => {
    // Simulate code generation for JavaScript
    cy.intercept("POST", "/api/generate/code", {
      body: "function add(a, b) { return a + b; }",
    }).as("generateCode");

    // Simulate title generation
    cy.intercept("POST", "/api/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Simulate language detection
    cy.intercept("POST", "/api/generate/detect_language", {
      body: '{"language": "javascript"}',
    }).as("detectLanguage");

    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type(
      "Write a function to add two numbers in JavaScript.",
    );
    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    cy.get("#generated-code code").should("not.be.empty");
    cy.get("#generated-code code").should("have.class", "javascript");
    cy.get("#generated-code code").within(() => {
      cy.get(".hljs-keyword").should("contain.text", "function");
      cy.get(".hljs-title").should("contain.text", "add");
      cy.get(".hljs-params").should("contain.text", "a, b");
    });
  });

  it("should highlight generated Ruby code correctly", () => {
    // Simulate code generation for Ruby
    cy.intercept("POST", "/api/generate/code", {
      body: "def add(a, b)\n  a + b\nend",
    }).as("generateCode");

    // Simulate title generation
    cy.intercept("POST", "/api/generate/title", {
      body: "Addition Function",
    }).as("generateTitle");

    // Simulate language detection
    cy.intercept("POST", "/api/generate/detect_language", {
      body: '{"language": "ruby"}',
    }).as("detectLanguage");

    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type(
      "Write a function to add two numbers in Ruby.",
    );
    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode");
    cy.wait("@generateTitle");
    cy.wait("@detectLanguage");

    cy.get("#generated-code code").should("not.be.empty");
    cy.get("#generated-code code").should("have.class", "ruby");
    cy.get("#generated-code code").within(() => {
      cy.get(".hljs-keyword").should("contain.text", "def");
      cy.get(".hljs-title").should("contain.text", "add");
      cy.get(".hljs-params").should("contain.text", "a, b");
    });
  });
});
