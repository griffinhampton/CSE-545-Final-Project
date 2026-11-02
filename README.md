# CSE 545 Group Project

## Setup

You need Python 3.13. Check your version with:

```bash
python --version
```

On Windows, if `python` points to a different version, use the launcher instead: `py -3.13`.

### 1. Create the virtual environment

Run this once from the project root:

```bash
python -m venv .venv
```

On Windows with several Python versions installed:

```powershell
py -3.13 -m venv .venv
```

### 2. Activate it

Activate the environment each time you open a new terminal:

| Shell | Command |
| --- | --- |
| PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Command Prompt | `.venv\Scripts\activate.bat` |
| Git Bash | `source .venv/Scripts/activate` |
| macOS / Linux | `source .venv/bin/activate` |

Once it's active, your prompt starts with `(.venv)`.

If PowerShell says running scripts is disabled, allow local scripts for your user account and try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 3. Install dependencies

If the project has a `requirements.txt`, install it with:

```bash
pip install -r requirements.txt
```

### 4. Deactivate

```bash
deactivate
```

## Adding a dependency

With the environment active, install the package, then update `requirements.txt` so everyone gets the same versions:

```bash
pip install <package>
pip freeze > requirements.txt
```

Commit the updated `requirements.txt`. Don't commit the `.venv/` folder; `.gitignore` already excludes it.
