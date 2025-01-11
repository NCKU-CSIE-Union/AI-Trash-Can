#/bin/bash

# Generate env.h header file from .env file

# Check if .env file exists
if [ ! -f .env ]; then
    echo ".env file not found!"
    exit 1
fi

# Read .env file and generate env.h
echo "#ifndef ENV_H" > env.h
echo "#define ENV_H" >> env.h

while IFS= read -r line; do
    # Skip empty lines and comments
    if [[ -n "$line" && "$line" != \#* ]]; then
        # Split the line into key and value
        IFS='=' read -r key value <<< "$line"
        # Convert key to uppercase and replace dots with underscores
        key=$(echo "$key" | tr '[:lower:]' '[:upper:]' | tr '.' '_')
        echo "#define $key \"$value\"" >> env.h
        echo "Added $key = $value"
    fi
done < .env

echo "#endif // ENV_H" >> env.h
