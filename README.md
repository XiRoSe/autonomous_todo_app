# ToDo Application with OpenAI GPT Enhancement

## Overview

This project develops a basic ToDo application with a backend powered by FastAPI and a SQLite database for managing ToDo items. It features an innovative enhancement mechanism using OpenAI's GPT to suggest improvements, refactor code, and potentially fix bugs automatically. This integration aims to streamline the development process, making the application more efficient and reducing manual debugging time.

## Features

- **Basic ToDo Operations**: Create, read, update, and delete (CRUD) functionalities for managing ToDo items.
- **OpenAI GPT Integration**: Leverages the capabilities of OpenAI's GPT for code review, suggesting improvements, and automatic bug fixes based on AI insights.
- **Interactive Development**: Offers a framework for developers to interact with GPT for code enhancements and problem-solving directly within their development workflow.

## Prerequisites

- Python 3.8 or newer
- FastAPI
- Uvicorn
- SQLAlchemy
- OpenAI API Key

## Installation

1. **Clone the Repository**

```bash
git clone https://yourrepositorylink.git
cd your_project_directory
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Set Up Environment Variables**

Create a `.env` file in the project root and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

1. **Start the FastAPI Server**

```bash
uvicorn app.main:app --reload
```

The server will start, and the ToDo application API will be accessible at `http://127.0.0.1:8000`.

2. **Using the OpenAI GPT Enhancement Feature**

The enhancement script is designed to read the project code, interact with OpenAI's GPT for improvements, and apply them based on your confirmation. Run the script as follows:

```bash
python enhancement_script.py
```

Follow the on-screen instructions to review and apply suggested improvements.

## API Documentation

After starting the FastAPI server, access the automatic API documentation by navigating to `http://127.0.0.1:8000/docs` in your web browser. This documentation provides an interactive interface to test and explore all API endpoints.

## Contributing

Contributions to enhance and expand the ToDo application are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## Reporting Issues

If you encounter any bugs or issues, please report them in the project's issues section with a detailed description, steps to reproduce the problem, and any relevant logs or screenshots.

## License

Distributed under the MIT License. See `LICENSE` for more information.
