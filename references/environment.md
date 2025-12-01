# Environment Setup

## Required Versions

- **Node.js:** v20+ (use `nvm`)
- **Python:** 3.11+ (use `pyenv`)
- **Postgres:** 15+ (if applicable)
- **IDE:** VS Code + recommended extensions

## VS Code Extensions

- ESLint
- Prettier
- Python
- GitLens
- TypeScript Hero

## Node.js Setup

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install and use Node 20
nvm install 20
nvm use 20
nvm alias default 20
```

## Python Setup

```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python 3.11
pyenv install 3.11
pyenv global 3.11

# Create virtual environment
python -m venv .venv
source .venv/bin/activate
```

## Environment Variables

- Store secrets in `.env` files (never commit)
- Use `.env.example` for documentation
- Load with `dotenv` (Node) or `python-dotenv` (Python)
