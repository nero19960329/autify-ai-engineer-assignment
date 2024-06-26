System Design
=============

This project is designed with a microservices architecture, leveraging FastAPI for the backend and Docker for deployment. The key components include:

1. **Backend Services**:
    - **API Service**: Provides endpoints for generating, improving, and running code snippets.
    - **Runner**: A component within the backend that executes Python code snippets and their tests securely with resource limits as subprocesses.

2. **Frontend**:
    - **Single-Page Application (SPA)**: Implements the user interface using HTML, CSS (TailwindCSS), and JavaScript.

3. **Database**:
    - Uses SQLAlchemy with SQLite for storing snippet data, including code, tests, feedback, and results.

4. **Integrations**:
    - **OpenAI API**: Integrates with ChatGPT 3.5 turbo model for generating and improving code snippets based on descriptions and feedback.

5. **Deployment**:
    - **Docker**: Containerizes the application for consistent and easy deployment.
    - **Supervisor**: Manages the backend service as background process.

6. **Testing**:
    - **Unit Tests**: Utilizes pytest for testing individual units of code, ensuring each part functions as expected.
    - **Integration Tests**: Utilizes Cypress for end-to-end testing, ensuring the entire system works together as expected.

The following diagram illustrates the system architecture:

.. mermaid::

    graph TD
        A[User] -->|Creates/Views Snippets| B[Frontend SPA]
        B -->|API Requests| C[FastAPI Backend]
        C -->|Database Access| D[SQLite Database]
        C -->|Calls| E[OpenAI API]
        C -->|Spawns Subprocesses| F[Runner]

        subgraph Deployment
            G[Docker Container]
            H[Supervisor]
        end

        C -->|Managed by| H
        G -->|Contains| C
        G -->|Contains| B
        
        subgraph Testing
            I[Unit Testing with pytest]
            J[Integration Testing with Cypress]
        end
        
        I --> C
        J --> B
        J --> C
