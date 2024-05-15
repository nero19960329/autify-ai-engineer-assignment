# AI Engineer Assignment: Code Snippet Generation

For detailed documentation on this project, please visit [https://nero19960329.github.io/code-snippet-generator/](https://nero19960329.github.io/code-snippet-generator/).

## Quick Start

1. **Set Up Environment**:
    - Install Docker on your machine.
    - Create a `.env` file in the project root directory based on the `.env.example` file and add the required environment variables.

2. **Run the Application**:
    - Start the application using Docker:

    ```bash
    IMAGE_NAME=code-snippet-app ./start-docker-server.sh
    ```

3. **Access the Application**:
    - Open your browser and go to [http://localhost:8000](http://localhost:8000) to access the application.

## Running Tests

### Unit Tests
- Use `pytest` to run unit tests.

```bash
ENV=test pytest tests/unit
```

### Integration Tests
- Use Cypress to run integration tests. Make sure the application is running before running the tests.

```bash
cd tests/integration
yarn
yarn test
```

## Features

- **Multi-language Support**: Generate code snippets in Python, JavaScript, and Ruby.
- **Bilingual Feedback**: Supports snippet description and feedback in both English and Japanese.
- **Stream-based Responses**: Utilizes streaming API responses for efficient and responsive data handling.
- **OpenAI Integration**: Integrates with OpenAI's ChatGPT 3.5 turbo model for high-quality code generation and improvement.
- **Secure Execution**: Runs Python code snippets and their tests securely with resource limits to prevent malicious or inefficient code execution.
- **Comprehensive Testing**: Includes both unit tests (pytest) and integration tests (Cypress) to ensure code quality and functionality.
- **CI/CD Pipelines**: Uses GitHub Actions for automated testing and deployment, ensuring a robust and reliable development workflow.
- **Dockerized Deployment**: Containerized application for consistent and easy deployment across different environments.

## CI/CD

- This project uses GitHub Actions for Continuous Integration (CI).
- Check the `.github/workflows` directory for CI configuration details.

For more detailed instructions, refer to the [developer guide](https://nero19960329.github.io/code-snippet-generator/developer_guide.html).
