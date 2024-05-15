Quick Start
===========

Follow these steps to get started:

1. **Set Up Environment**:
    Install Docker and Docker Compose on your machine.

    - `Install Docker <https://docs.docker.com/get-docker/>`_

2. **Create .env File**:
    Create a `.env` file in the project root directory based on the `.env.example` file and add the required environment variables.

3. **Run the Application**:
    Start the application using Docker.

    .. code-block:: bash

        IMAGE_NAME=code-snippet-app ./start-docker-server.sh

4. **Access the Application**:
    Open your browser and go to `http://localhost:8000 <http://localhost:8000>`_ to access the application.

5. **Explore the Features**:
    - Create, view, and delete code snippets.
    - Generate and improve code snippets and tests.
    - Run tests to validate code snippets.
    - Regenerate when tests failed.
