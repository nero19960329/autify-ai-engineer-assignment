describe("Code Snippet Generator", () => {
  beforeEach(() => {
    cy.request("GET", "/snippets").then((response) => {
      response.body.forEach((snippet) => {
        cy.request("DELETE", `/snippets/${snippet.id}`);
      });
    });
    cy.visit("/");
  });

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
    cy.get("#snippet-detail .generate-code-btn").should("be.visible");
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
    cy.get("#snippet-detail .generate-code-btn").should("be.visible");
  });
});
