# /bin/bash

for i in {2..31}; do
  day=$(printf "%02d" $i)
  path="$(pwd)/src/day$day"

  if [ -d $path ]; then
    echo "Directory $path already exists"
    continue
  fi

  cp -r src/day01/ $path
done