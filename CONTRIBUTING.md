# Contributing to OPC Startup

Thank you for your interest in contributing! This document provides guidelines and information for contributors.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). We expect all contributors to treat each other with respect.

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported in [Issues](https://github.com/dh18017588868-web/OPCStartup/issues).
- Use the **Bug Report** template to create a new issue.
- Include steps to reproduce, expected vs actual behavior, and relevant logs/screenshots.
- For security vulnerabilities, see **Security Policy** below.

### Suggesting Features

- Search existing issues to avoid duplicates.
- Use the **Feature Request** template.
- Provide a clear use case and explanation of the problem it solves.
- Include examples or mockups if applicable.

### Pull Requests

1. **Fork the repository** and create a feature branch from `main`.
2. **Set up your development environment**:

```bash
git clone https://github.com/your-username/OPCStartup.git
cd OPCStartup
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt -r requirements-dev.txt
```

3. **Make changes** with clear, descriptive commit messages. Follow [Conventional Commits](https://www.conventionalcommits.org/).

4. **Add tests** for any new functionality. Ensure all tests pass:

```bash
pytest -v
```

5. **Update documentation** if your changes affect user-facing features:

- Update `README.md`, `docs/`, or skill files.
- Keep changelog entries in `CHANGELOG.md` if needed.

6. **Verify CI** locally (optional):

```bash
python scripts/validate.py
make test
```

7. **Submit a Pull Request**: Use the PR template. Link to any related issues.

### Development Tips

- Use `make test` to run validation and tests.
- Use `make validate` to run validation only.
- Use `make docs` and `make docs-serve` to build/preview docs.
- Use `make release` to prepare for a release after your PR merges.

### Code Style

- Follow PEP 8. Use `black` and `flake8`:

```bash
black .
flake8 .
```

- Type hints are encouraged.
- Keep functions small and focused.

### Testing

- Write unit tests in `tests/unit/`.
- Write integration tests in `tests/integration/`.
- Aim for high coverage on new code. Use `pytest-cov` if needed.

### Documentation

- Update skill files (YAML frontmatter must be present) and `docs/`.
- For new skills, add a reference in `skills/all.md` and documentation index.

### Licensing

- By contributing, you agree your contributions will be licensed under the project's MIT License.
- Do not include code from other projects without proper attribution and compatible license.

## Release Process

Maintainers handle releases. After PR merge:

1. Update `CHANGELOG.md`.
2. Create a Git tag: `git tag v1.0.X && git push --tags`.
3. GitHub Actions will build and publish the release automatically.

## Questions?

Open an issue or reach out via GitHub Discussions.

---

Thank you for making OPC Startup better! 🚀
