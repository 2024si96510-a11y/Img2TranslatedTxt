# Contributing to This Project

## Creating a Pull Request

Follow these steps to submit your contributions:

### 1. Fork and Clone
- Fork the repository on GitHub
- Clone your fork locally:
    ```bash
    git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
    cd REPO_NAME
    ```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Write code following PEP 8 style guide
- Add unit tests in the `tests/` directory
- Update documentation as needed

### 4. Test Your Changes
```bash
pytest tests/
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "Brief description of your changes"
```

### 6. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 7. Open a Pull Request
- Go to the original repository on GitHub
- Click "New Pull Request"
- Select your fork and branch
- Fill in the PR template with:
    - Description of changes
    - Related issue number (if applicable)
    - Testing performed
- Submit the pull request

### 8. Address Review Feedback
- Respond to reviewer comments
- Make requested changes
- Push updates to the same branch

## Code Review Process
- All PRs require at least one approval
- CI tests must pass
- Code must follow project guidelines