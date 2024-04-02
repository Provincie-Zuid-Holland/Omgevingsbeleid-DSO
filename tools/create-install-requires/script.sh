#!/bin/bash

if [ ! -f ../../requirements.txt ]; then
    echo "requirements.txt not found."
    exit 1
fi

echo "    install_requires=["
while IFS= read -r line
do
    if [[ "$line" == *"=="* ]]; then
        echo "        '${line//==/>=}',"
    fi
done < ../../requirements.txt
echo "    ]"
