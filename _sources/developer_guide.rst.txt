Developer Guide
===============

This section provides useful instructions for developers working on this project.

1. **Setting Up Development Environment**:
    - Clone the repository and create a new Python environment.

      .. code-block:: bash

          git clone https://github.com/nero19960329/code-snippet-generator.git
          cd code-snippet-generator
          python -m venv env
          source env/bin/activate
          pip install -r requirements.txt -r requirements-dev.txt

2. **Running Tests**:
    - Use `pytest` to run unit tests.

      .. code-block:: bash

          ENV=test pytest tests/unit

    - Use Cypress to run integration tests.

      .. code-block:: bash

          cd tests/integration
          yarn
          yarn test

3. **GitHub Actions**:
    - This project uses GitHub Actions for Continuous Integration (CI).
    - There are three workflows configured: `integration.yml`, `module.yml`, and `repo.yml`.
    - **Integration Workflow**:
      - Triggered on push and pull request events to the main branch.
      - Sets up the environment, starts services, and runs integration tests using Cypress.
      - Results are uploaded as artifacts.
    - **Module Workflow**:
      - Triggered on push and pull request events to the main branch.
      - Sets up the environment, checks code formatting, and runs unit tests using pytest.
    - **Repo Workflow**:
      - Triggered on pull request events to the main branch.
      - Runs commitlint to ensure commit messages follow the conventional commit standard.
    - **Viewing Results**:
      - You can view the results of the workflows by navigating to the "Actions" tab of the GitHub repository.
      - Each workflow run will show detailed logs and the status of each step.

4. **Building and Running Docker Containers**:
    - Build the Docker image.

      .. code-block:: bash

          docker build -t code-snippet-app .

    - Run the Docker container.

      .. code-block:: bash

          docker run --rm -p 8000:8000 --env-file .env code-snippet-app

5. **Adding New Features**:
    - Follow the existing project structure and coding conventions.
    - Document new features and endpoints in the appropriate `.rst` files.
    - Update tests to cover new features.

6. **Deployment**:
    - Ensure all changes are committed and pushed to the repository.
    - Use CI/CD pipelines to automate the build and deployment process.

By following these guidelines, you can effectively develop and maintain this project.
