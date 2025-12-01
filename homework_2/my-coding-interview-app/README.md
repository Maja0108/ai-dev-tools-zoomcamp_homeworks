# Code Interview Platform

This platform allows real-time collaborative coding interviews with a shared code panel, syntax highlighting, and WebSocket integration for instant code sharing.

## Features

- **Real-Time Collaboration**: Interviewers and candidates can edit the code simultaneously.
- **Syntax Highlighting**: Supports JavaScript and Python syntax highlighting.
- **WebSocket Communication**: WebSocket is used to synchronize code updates between the client and server.
- **Simple Setup**: All frontend and backend code are integrated in a single application.
- **Docker Integration**: Deploy the application in a Docker container for easier management and deployment.

## Installation

### Prerequisites

Ensure that you have the following installed on your machine:

- **Node.js** (v14 or higher)
- **npm** (Node Package Manager)
- **Docker** (if you plan to containerize the app)

### Steps to Run the Application

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/my-coding-interview-app.git
    cd my-coding-interview-app
    ```

2. **Install Dependencies**:

    Install both the frontend and backend dependencies by running the following command:

    ```bash
    npm install
    ```

3. **Run the Application**:

    Start the application by running the development server:

    ```bash
    npm run dev
    ```

    This will start the server on `http://localhost:5000`. Open this URL in your browser to access the app.

### How It Works

1. **Frontend**: The app uses **React** to render the UI, which includes:
    - A **Code Editor** where interviewers and candidates can write and edit code.
    - A **WebSocket Status** indicator showing the connection status to the server.
    - A **Connect Button** to establish the WebSocket connection.
  
2. **Backend**: The server runs on **Express.js** and handles:
    - Serving the frontend React code.
    - WebSocket communication to synchronize changes in real-time between connected clients.
    - Running on **port 5000** by default.

3. **WebSocket Communication**: When the **Connect Button** is clicked:
    - A WebSocket connection is established between the frontend (React) and backend (Express).
    - Once connected, both the interviewer and candidate can edit code in real-time.

### Docker Integration

To deploy the app in a Docker container, follow these steps:

1. **Dockerfile**:

    Create a `Dockerfile` in the root of the project directory.

    ```Dockerfile
    # Step 1: Use a Node.js base image
    FROM node:16

    # Step 2: Set the working directory
    WORKDIR /app

    # Step 3: Copy package.json and install dependencies
    COPY package*.json ./
    RUN npm install

    # Step 4: Copy all source files
    COPY . .

    # Step 5: Expose the app on port 5000
    EXPOSE 5000

    # Step 6: Run the server when the container starts
    CMD ["npm", "run", "dev"]
    ```

2. **Build and Run Docker Container**:

    Build the Docker image:

    ```bash
    docker build -t code-interview-platform .
    ```

    Once the image is built, you can run the container:

    ```bash
    docker run -p 5000:5000 code-interview-platform
    ```

    The application will be accessible at `http://localhost:5000` inside the Docker container.

### Testing

The app can be tested by manually verifying the WebSocket connection. Once the application is running:

1. Open the URL `http://localhost:5000` in multiple tabs or different browsers.
2. Click the **Connect WebSocket** button in each tab.
3. Observe the **WebSocket Status** changing to **Connected** once the connection is established.

### Running Tests (Optional)

To add automated testing (e.g., with Jest or Mocha):

1. Add testing libraries to the `package.json` and write your test cases.
2. Run the tests with the following command:

    ```bash
    npm run test
    ```

### Troubleshooting

If you encounter issues with the WebSocket connection:

1. **CORS Issues**: If you're running the backend and frontend separately (e.g., different ports), make sure that the backend is properly configured to handle Cross-Origin Resource Sharing (CORS) requests.
2. **Check the WebSocket Connection**: Open the browser's developer tools (F12), and navigate to the "Console" tab to see if there are any error messages related to WebSocket connections.
3. **Ensure Dependencies are Installed**: Run `npm install` to make sure all required packages are installed.

## Contribution

Feel free to fork the repository, create issues, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

