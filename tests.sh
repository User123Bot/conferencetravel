#!/bin/bash

#  ctetproject directory
CTET_PROJECT_DIR="$(pwd)/ctetproject"

install_requirements() {
    echo "Installing Python packages from requirements.txt..."
    pip install -r "requirements.txt"
    if [ $? -ne 0 ]; then
        echo "Failed to install Python packages."
        exit 1  # Exit if installation fails
    fi
    echo "Python packages installed successfully."
}

# Function to test backend
test_backend() {
    echo "Navigating to $CTET_PROJECT_DIR"
    cd "$CTET_PROJECT_DIR" || exit
    echo "Running backend tests..."
    python manage.py test ctetproject/
    echo "Backend tests completed."
}

# Function to start backend server
start_backend_server() {
    echo "Starting backend server..."
    cd "$CTET_PROJECT_DIR" || exit
    python manage.py runserver &
    BACKEND_PID=$!
    echo "Backend server started with PID $BACKEND_PID."
}

# Function to start frontend server
start_frontend_server() {
    echo "Starting frontend server..."
    cd "$CTET_PROJECT_DIR/frontend/" || exit
    npm start &
    FRONTEND_PID=$!
    echo "Frontend server started with PID $FRONTEND_PID."
}

# Function to test frontend & hybrid
test_frontend_hybrid() {
    echo "Navigating to the testing directory..."
    cd "$CTET_PROJECT_DIR/testing" || exit
    echo "Running automated tests..."

    # Run the first test and check for successful completion
    python testing_automated_full_pipeline.py
    if [ $? -ne 0 ]; then
        echo "Failed to complete full pipeline testing."
        return 1  # Exit the function with an error status
    fi

    # Run the second test and check for successful completion
    python testing_automated_manual_entry.py
    if [ $? -ne 0 ]; then
        echo "Failed to complete manual entry testing."
        return 1
    fi

    # Run the third test and check for successful completion
    python testing_automated_csv.py
    if [ $? -ne 0 ]; then
        echo "Failed to complete CSV testing."
        return 1
    fi

    echo "Frontend and hybrid tests completed."
}


# Function to run unit tests
run_unit_tests() {
    echo "Navigating to $CTET_PROJECT_DIR"
    cd "$CTET_PROJECT_DIR" || exit
    echo "Running unit tests..."
    pytest
    echo "Unit tests completed."
}

# Start testing
install_requirements
test_backend
start_backend_server
start_frontend_server
test_frontend_hybrid
run_unit_tests

# Killing the backend and frontend servers
echo "Shutting down servers..."
echo "Killing backend server with PID $BACKEND_PID."
kill $BACKEND_PID
echo "Killing frontend server with PID $FRONTEND_PID."
kill $FRONTEND_PID
echo "Servers shutdown completed."

echo "All tests and servers have been handled."
