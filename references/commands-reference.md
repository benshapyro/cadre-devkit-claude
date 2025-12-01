# Common Commands Reference

## Development

```bash
npm run dev         # Start local dev server
npm run build       # Generate production build
npm run lint        # Run linting
npm run lint:fix    # Fix linting issues
```

## Git Workflow

```bash
git pull --rebase   # Sync feature branch
git checkout -b feat/name  # New feature branch
git add -p          # Interactive staging
git commit -m "type(scope): message"
git push -u origin HEAD
```

## Python

```bash
pytest -q           # Run Python tests
black . && isort .  # Python formatting
mypy src/           # Type checking
pip install -r requirements.txt
```

## Docker

```bash
docker-compose up -d      # Start services
docker-compose down       # Stop services
docker-compose logs -f    # Follow logs
docker exec -it <container> bash
```

## Database

```bash
# PostgreSQL
psql -U postgres -d dbname
\dt                 # List tables
\d+ tablename       # Describe table
```

## Debugging

```bash
# Node.js
node --inspect app.js
DEBUG=* npm run dev

# Python
python -m pdb script.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```
