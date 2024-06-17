#!/bin/bash

# tailwind.config.js ファイルのパス
FILE_PATH="tailwind.config.js"

# content: [], を content: ["/app/templates/**/*.{html,js}"], に書き換える
sed -i 's/content: \[\],/content: ["\/app\/templates\/\*\*\/\*.{html,js}"],/' "$FILE_PATH"