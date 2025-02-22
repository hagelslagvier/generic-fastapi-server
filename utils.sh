#!/bin/bash

load_env() {
    if [ -z "$1" ]; then  # Check if the file path is provided
        echo "Error: Please provide the path to the .env file."
        return 1
    fi

    if [ ! -f "$1" ]; then  # Check if the file exists
        echo "Error: The file '$1' does not exist."
        return 1
    fi

    export $(grep -v '^#' "$1" | xargs)  # Load the environment variables from the file
    echo "Loaded env variables from $1"
}
