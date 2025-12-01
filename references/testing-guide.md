# Testing Guide

## Test Frameworks

- **JavaScript/TypeScript:** Jest
- **Python:** Pytest

## Directory Structure

- Place tests in `__tests__/` or `tests/` directories
- Mirror source structure in test directories
- Name test files with `.test.ts` or `_test.py` suffix

## Test Guidelines

- Include at least one negative test per feature
- Run full test suite before pushing: `npm run test` or `pytest -q`
- Aim for high coverage but prioritize quality over quantity
- Test edge cases and error conditions

## Test Commands

```bash
# JavaScript/TypeScript
npm run test           # Run all tests
npm run test -- --watch # Watch mode
npm run test -- --coverage # Coverage report

# Python
pytest -q              # Quick run
pytest -v              # Verbose output
pytest --cov=src       # Coverage report
pytest -x              # Stop on first failure
```

## Writing Good Tests

1. **Arrange** - Set up test data and conditions
2. **Act** - Execute the code under test
3. **Assert** - Verify expected outcomes

## Mocking Best Practices

- Mock external dependencies (APIs, databases)
- Use real implementations for unit logic
- Avoid over-mocking; test real behavior when possible
