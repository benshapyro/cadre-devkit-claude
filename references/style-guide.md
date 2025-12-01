# Code Style Guidelines

## Naming Conventions

- **Files:** `lowercase_with_underscores`
- **Variables:** `camelCase`
- **Components/Classes:** `PascalCase`

## General Guidelines

- Write minimal, clear comments only where logic is non-obvious
- Prefer explicit imports (no wildcard imports)
- Use ES Modules exclusively (no `require`); default to `async/await` for promises
- Follow PEP 8 for Python and strict TypeScript mode for JS/TS

## Lint Rules

- Max line length: 100 chars
- Trailing commas for multi-line objects/arrays

## TypeScript Specific

- Use `strict` mode in tsconfig.json
- Prefer `interface` over `type` for object shapes
- Use explicit return types for public functions
- Avoid `any`; use `unknown` with type guards

## Python Specific

- Use type hints for all function signatures
- Use dataclasses or pydantic for structured data
- Format with `black --line-length 100`
- Sort imports with `isort`
