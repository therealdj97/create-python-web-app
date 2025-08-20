#!/bin/bash
set -e

PACKAGE_NAME="create_python_web_app"
VERSION="0.1.0"

echo "🚀 Setting up package: $PACKAGE_NAME version $VERSION"

# Step 1: Create pyproject.toml if missing
if [ ! -f pyproject.toml ]; then
cat <<EOL > pyproject.toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "$PACKAGE_NAME"
version = "$VERSION"
description = "My awesome Python package"
readme = "README.md"
authors = [{name="Your Name", email="you@example.com"}]
license = {text = "MIT"}
dependencies = []
EOL
echo "✅ Created pyproject.toml"
fi

# Step 2: Create README.md if missing
if [ ! -f README.md ]; then
cat <<EOL > README.md
# $PACKAGE_NAME

A short description of your package.

## Installation
\`\`\`bash
pip install $PACKAGE_NAME
\`\`\`

## Usage
\`\`\`python
import $PACKAGE_NAME
\`\`\`
EOL
echo "✅ Created README.md"
fi

# Step 3: Build package
echo "📦 Building package..."
pip install --upgrade build twine >/dev/null
python -m build

# Step 4: Upload to PyPI
echo "☁️ Uploading to PyPI..."
twine upload dist/*

echo "🎉 Done! Your package $PACKAGE_NAME $VERSION is published."