describe("Code Generation Functionality", () => {
  beforeEach(() => {
    cy.request("GET", "/api/snippets").then((response) => {
      response.body.forEach((snippet) => {
        cy.request("DELETE", `/api/snippets/${snippet.id}`);
      });
    });
    cy.visit("/");
  });

  it("should generate a Python code snippet", () => {
    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type(
      "Write a Python function to add two numbers.",
    );

    cy.intercept("POST", "/api/generate/code").as("generateCode");
    cy.intercept("POST", "/api/generate/title").as("generateTitle");
    cy.intercept("POST", "/api/generate/detect_language").as("detectLanguage");

    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode").its("response.statusCode").should("eq", 200);
    cy.wait("@generateTitle").its("response.statusCode").should("eq", 200);
    cy.wait("@detectLanguage").its("response.statusCode").should("eq", 200);

    cy.get("#generated-code code").should("contain.text", "def ");
    cy.get("#generated-code code").should("have.class", "python");
  });

  it("should generate a JavaScript code snippet", () => {
    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type(
      "Write a JavaScript function to add two numbers.",
    );

    cy.intercept("POST", "/api/generate/code").as("generateCode");
    cy.intercept("POST", "/api/generate/title").as("generateTitle");
    cy.intercept("POST", "/api/generate/detect_language").as("detectLanguage");

    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode").its("response.statusCode").should("eq", 200);
    cy.wait("@generateTitle").its("response.statusCode").should("eq", 200);
    cy.wait("@detectLanguage").its("response.statusCode").should("eq", 200);

    cy.get("#generated-code code").should("contain.text", "function ");
    cy.get("#generated-code code").should("have.class", "javascript");
  });

  it("should generate a Ruby code snippet", () => {
    cy.get("#create-snippet-btn").click();
    cy.get("#code-description").type(
      "Write a Ruby function to add two numbers.",
    );

    cy.intercept("POST", "/api/generate/code").as("generateCode");
    cy.intercept("POST", "/api/generate/title").as("generateTitle");
    cy.intercept("POST", "/api/generate/detect_language").as("detectLanguage");

    cy.get("#generate-code-btn").click();

    cy.wait("@generateCode").its("response.statusCode").should("eq", 200);
    cy.wait("@generateTitle").its("response.statusCode").should("eq", 200);
    cy.wait("@detectLanguage").its("response.statusCode").should("eq", 200);

    cy.get("#generated-code code").should("contain.text", "def ");
    cy.get("#generated-code code").should("have.class", "ruby");
  });

  it("should improve Python code snippet with English feedback", () => {
    cy.request("POST", "/api/snippets", {
      title: "Addition Function",
      language: "python",
      description: "Write a Python function to add two numbers.",
      code: "def add(a, b): return a + b",
    }).then((response) => {
      const snippetId = response.body.id;
      cy.visit("/");
      cy.get(`a[data-id="${snippetId}"]`).click();

      cy.get("#code-feedback").type(
        "Add type hints to the function parameters and return type.",
      );

      cy.intercept("POST", "/api/generate/code_from_feedback").as(
        "improveCode",
      );

      cy.get("#improve-code-btn").click();

      cy.wait("@improveCode").its("response.statusCode").should("eq", 200);

      cy.get("#generated-code code").should("contain.text", "def ");
      cy.get("#generated-code code").should("contain.text", ": int");
      cy.get("#generated-code code").should("have.class", "python");
    });
  });

  it("should improve Python code snippet with Japanese feedback", () => {
    cy.request("POST", "/api/snippets", {
      title: "Addition Function",
      language: "python",
      description: "Write a Python function to add two numbers.",
      code: "def add(a, b): return a + b",
    }).then((response) => {
      const snippetId = response.body.id;
      cy.visit("/");
      cy.get(`a[data-id="${snippetId}"]`).click();

      cy.get("#code-feedback").type(
        "関数のパラメーターと戻り値に型ヒントを追加してください。",
      );

      cy.intercept("POST", "/api/generate/code_from_feedback").as(
        "improveCode",
      );

      cy.get("#improve-code-btn").click();

      cy.wait("@improveCode").its("response.statusCode").should("eq", 200);

      cy.get("#generated-code code").should("contain.text", "def ");
      cy.get("#generated-code code").should("contain.text", ": int");
      cy.get("#generated-code code").should("have.class", "python");
    });
  });

  it("should generate tests for a Python code snippet", () => {
    cy.request("POST", "/api/snippets", {
      title: "Addition Function",
      language: "python",
      description: "Write a Python function to add two numbers.",
      code: "def add(a, b): return a + b",
    }).then((response) => {
      const snippetId = response.body.id;
      cy.visit("/");
      cy.get(`a[data-id="${snippetId}"]`).click();

      cy.intercept("POST", "/api/generate/tests").as("generateTests");

      cy.get("#generate-tests-btn").click();

      cy.wait("@generateTests").its("response.statusCode").should("eq", 200);

      cy.get("#generated-tests code").should("contain.text", "assert ");
      cy.get("#generated-tests code").should("have.class", "python");
    });
  });

  it("should improve Python tests with English feedback", () => {
    cy.request("POST", "/api/snippets", {
      title: "Addition Function",
      language: "python",
      description: "Write a Python function to add two numbers.",
      code: "def add(a, b): return a + b",
      test_code: "assert add(1, 2) == 3",
    }).then((response) => {
      const snippetId = response.body.id;
      cy.visit("/");
      cy.get(`a[data-id="${snippetId}"]`).click();

      cy.get("#tests-feedback").type("Add edge cases and error handling.");

      cy.intercept("POST", "/api/generate/tests_from_feedback").as(
        "improveTests",
      );

      cy.get("#improve-tests-btn").click();

      cy.wait("@improveTests").its("response.statusCode").should("eq", 200);

      cy.get("#generated-tests code").should("contain.text", "assert ");
      cy.get("#generated-tests code").should("have.class", "python");
    });
  });

  it("should improve Python tests with Japanese feedback", () => {
    cy.request("POST", "/api/snippets", {
      title: "Addition Function",
      language: "python",
      description: "Write a Python function to add two numbers.",
      code: "def add(a, b): return a + b",
      test_code: "assert add(1, 2) == 3",
    }).then((response) => {
      const snippetId = response.body.id;
      cy.visit("/");
      cy.get(`a[data-id="${snippetId}"]`).click();

      cy.get("#tests-feedback").type(
        "エッジケースとエラーハンドリングを追加してください。",
      );

      cy.intercept("POST", "/api/generate/tests_from_feedback").as(
        "improveTests",
      );

      cy.get("#improve-tests-btn").click();

      cy.wait("@improveTests").its("response.statusCode").should("eq", 200);

      cy.get("#generated-tests code").should("contain.text", "assert ");
      cy.get("#generated-tests code").should("have.class", "python");
    });
  });

  it("should run tests to validate the Python code", () => {
    cy.request("POST", "/api/snippets", {
      title: "Addition Function",
      language: "python",
      description: "Write a Python function to add two numbers.",
      code: "def add(a, b): return a + b",
      test_code: "assert add(1, 2) == 3",
    }).then((response) => {
      const snippetId = response.body.id;
      cy.visit("/");
      cy.get(`a[data-id="${snippetId}"]`).click();

      cy.intercept("POST", "/api/run/python").as("runTests");

      cy.get("#run-tests-btn").click();

      cy.wait("@runTests").its("response.statusCode").should("eq", 200);

      cy.get("#test-results").should(
        "contain.text",
        "Code Executed Successfully",
      );
    });
  });

  it("should not enable the run tests button for non-Python code", () => {
    cy.request("POST", "/api/snippets", {
      title: "Addition Function",
      language: "javascript",
      description: "Write a JavaScript function to add two numbers.",
      code: "function add(a, b) { return a + b; }",
    }).then((response) => {
      const snippetId = response.body.id;
      cy.visit("/");
      cy.get(`a[data-id="${snippetId}"]`).click();

      cy.get("#generate-tests-btn").click();

      cy.get("#run-tests-btn").should("be.disabled");
    });
  });
});
