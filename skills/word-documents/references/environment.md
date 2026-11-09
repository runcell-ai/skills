# Environment setup

Use an existing project virtual environment, or create a task-specific one.
The commands below are examples for an environment you control:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install 'python-docx>=1.2,<2'
```

On Windows, the interpreter is `.venv\Scripts\python.exe`. A notebook may use
the same interpreter via its kernel; do not assume bare `pip` targets it.

Rendering uses command-line LibreOffice and Poppler:

- macOS: `brew install --cask libreoffice` and `brew install poppler`.
  If LibreOffice is not on `PATH`, pass
  `--soffice /Applications/LibreOffice.app/Contents/MacOS/soffice`.
- Debian/Ubuntu: install `libreoffice-writer` and `poppler-utils` with the
  system package manager.
- Windows: install LibreOffice and Poppler, then expose their executables on
  `PATH` or pass explicit `--soffice` and `--pdftoppm` paths.

System installs follow the host's permissions. If unavailable, complete the
supported edits and state that page rendering remains unverified.

Install fonts needed by the document, particularly for CJK and mathematical
notation. Font substitution can change pagination even if conversion succeeds.
No internet connection is required after dependencies are installed.
