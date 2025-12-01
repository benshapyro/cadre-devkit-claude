---
name: test-generator
description: Generates Jest or Pytest tests following Ben's testing standards. Use when creating tests, adding test coverage, or when user mentions testing, test cases, Jest, or Pytest.
---

# Test Generator Skill

Generate high-quality tests using Jest (JavaScript/TypeScript) or Pytest (Python) following established best practices.

## Test Frameworks

- **JavaScript/TypeScript**: Jest
- **Python**: Pytest

## Test Directory Structure

- Place tests in `__tests__/` or `tests/` directories
- Mirror source structure in test directories
- Use clear, descriptive test file names

**JavaScript/TypeScript**:
```
src/
  utils/
    validator.ts
__tests__/
  utils/
    validator.test.ts
```

**Python**:
```
src/
  utils/
    validator.py
tests/
  utils/
    test_validator.py
```

## Test Writing Standards

### Coverage Requirements
- Include at least one negative test per feature
- Test edge cases and boundary conditions
- Aim for high coverage but prioritize quality over quantity

### Test Structure
Follow the Arrange-Act-Assert pattern:
```javascript
// Jest example
describe('functionName', () => {
  it('should handle valid input correctly', () => {
    // Arrange
    const input = 'valid';

    // Act
    const result = functionName(input);

    // Assert
    expect(result).toBe(expected);
  });

  it('should throw error for invalid input', () => {
    // Negative test case
    expect(() => functionName(null)).toThrow();
  });
});
```

```python
# Pytest example
class TestFunctionName:
    def test_valid_input(self):
        # Arrange
        input_val = 'valid'

        # Act
        result = function_name(input_val)

        # Assert
        assert result == expected

    def test_invalid_input_raises_error(self):
        # Negative test case
        with pytest.raises(ValueError):
            function_name(None)
```

### Test Naming
- Use descriptive names that explain what's being tested
- Format: `test_<what>_<condition>_<expected_result>`
- Examples:
  - `test_user_login_with_valid_credentials_returns_token`
  - `test_api_call_with_invalid_auth_raises_401`

### Test Quality Checklist
- [ ] Tests are independent and can run in any order
- [ ] Each test has a single, clear purpose
- [ ] Mock external dependencies (APIs, databases, file systems)
- [ ] Include both positive and negative test cases
- [ ] Test error handling and edge cases
- [ ] Use meaningful assertion messages
- [ ] Tests are fast and deterministic

## Common Test Patterns

### Mocking (Jest)
```javascript
jest.mock('../api/client');

it('should handle API errors gracefully', async () => {
  apiClient.get.mockRejectedValue(new Error('Network error'));
  await expect(fetchData()).rejects.toThrow('Network error');
});
```

### Fixtures (Pytest)
```python
@pytest.fixture
def sample_user():
    return User(name='Test User', email='test@example.com')

def test_user_creation(sample_user):
    assert sample_user.name == 'Test User'
```

### Parameterized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```

## Running Tests

Before committing:
```bash
# JavaScript/TypeScript
npm run test

# Python
pytest -q
```

## Generation Process

When generating tests:
1. Analyze the code to understand functionality
2. Identify edge cases and potential failure points
3. Create test structure with descriptive names
4. Write positive tests (happy path)
5. Write negative tests (error cases)
6. Add parameterized tests for multiple inputs
7. Include setup/teardown if needed

Always explain what each test validates and why it's important.
