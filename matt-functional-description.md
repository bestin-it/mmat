# MMAT 1 – Concept, Scope & Architecture

---

## 1. System Goal

The goal is to build a modular **MMAT** (Multi Modal AI Tester) framework for autonomous E2E testing of web pages using LLMs (multimodal and reasoning). The system combines visual analysis (screenshots) and HTML structure analysis (via Playwright), builds a local knowledge graph, enables feedback cycles, and full CLI support. **Framework written in Python.**

---

## 2. Functional Scope

| No.  | Functionality                                             | Description                                                     |
| ---- | --------------------------------------------------------- | --------------------------------------------------------------- |
| 2.1  | E2E tests for web pages                                   | Testing any portal based on user description                    |
| 2.2  | Playwright integration                                    | Browser automation, DOM reading, actions execution              |
| 2.3  | Visual analysis (screenshots) via multimodal model        | Sending screenshots to AI model; recognizing graphical layout   |
| 2.4  | HTML structure analysis via reasoning model               | Sending DOM structure to AI; locating/understanding elements    |
| 2.5  | Building a local knowledge graph of elements/interactions | Graph reflecting relationships and actions between DOM elements |
| 2.6  | Initial test plan from description                        | Interpreting test plan from text/YAML                           |
| 2.7  | Autonomous exploration, graph updates                     | Gathering knowledge while performing actions                    |
| 2.8  | Post-test knowledge analysis                              | Summary & reasoning phase                                       |
| 2.9  | Generating summary and test report                        | Automated documentation of run/effects                          |
| 2.10 | Ability to update test based on user feedback             | Improvement mode; test editing based on graph                   |
| 2.11 | Separation layer for local graph API                      | Python interface for easy backend graph swap                    |
| 2.12 | Full CLI support                                          | All features available from command line                        |
| 2.13 | Clear step numbering and per-step feedback                | Each step numbered, referable in CLI and feedback               |
| 2.14 | Bidirectional conversion: description <-> E2E test        | Generate test steps from prompt and reverse                     |
| 2.15 | Automatic description/test sync after changes             | Textual and step test always in sync                            |
| 2.16 | Test listing/statuses via CLI                             | Browse/filter tests from CLI                                    |
| 2.17 | Start from any step                                       | Start from description, E2E test or Playwright code             |
| 2.18 | Export/run E2E test in Playwright                         | Generate & run Playwright code from JSON                        |
| 2.19 | **Visual element identification**                         | Ability to mark elements only via screenshot if DOM unavailable |

---

## 3. System Architecture

```
+-------------------+
|    Test Runner    |<-------------------------------+
+-------------------+                                |
         |                                           |
         v                                           |
+-------------------+      +---------------------+    |
|   Plan Builder    +----->|     Graph API       +--->|     
+-------------------+      +---------------------+    |
         |                    |       |               |
         v                    v       v               |
+-------------------+   +-----------+  +----------+   |
| Playwright Driver |   |  Reason-  |  |  Vision  |   |
+-------------------+   |   ing     |  |  Model   |   |
         |              |  Model     |  | (Multi-) |   |
         v              +-----------+  +----------+   |
+-------------------+                                |
|    HTML Analyzer  |------------------------------->|
+-------------------+                                |
         |
         v
+-------------------+
| Screenshot Analyz |
+-------------------+
         |
         v
+-------------------+
|Test Summary/Feedback|
+-------------------+
```

---

## 4. Knowledge Graph

**Nodes:**

| Node           | Description                                   |
| -------------- | --------------------------------------------- |
| DOM Element    | Any significant page element                  |
| Action         | Interaction with an element                   |
| State          | Effect of action (e.g. 'logged in')           |
| Screenshot     | Visual object                                 |
| **Visual Ref** | **Visual-only mark – bbox, OCR, description** |

**Edges:**

| Edge     | Description                 |
| -------- | --------------------------- |
| Relation | "Click", "fill", "leads to" |
| Result   | State change/new element    |

---

### 4.1. Visual-only Element Marking

When DOM code is unavailable (e.g., dynamic apps, technical restrictions), MMAT marks elements using only visual analysis of the screenshot.

**Marking methods:**

* **Bounding box (BBOX):** Rectangle coordinates (`x, y, width, height`) on the screenshot (origin top-left).
* **OCR:** Text recognized by optical character recognition in the field/button.
* **Textual description:** (optional) e.g., “blue button bottom right,” generated by LLM or user.
* **Fallback:** Element in MMAT graph gets `visual_ref` field with this data.

If an element lacks a DOM selector, MMAT marks it as type: “visual,” and documentation/CLI display coordinates and optional OCR/text.

---

## 5. Example test (YAML)

```yaml
description: |
  Open bestin-it.com login page, find email & password fields, enter test data,
  click login, check if dashboard appears.
start_url: "https://bestin-it.com/login"
test_data:
  email: test@abc.com
  password: test123
```

---

## 6. Non-functional requirements

| No. | Requirement                | Description                                  |
| --- | -------------------------- | -------------------------------------------- |
| N1  | Modular architecture       | Each layer is a separate module              |
| N2  | Easy swap of graph backend | Just replace Graph API class                 |
| N3  | Local-only operation       | No graph/state leaves user machine           |
| N4  | CLI/Notebook/Web interface | Run tests via CLI, notebook or web           |
| N5  | Readable reports           | Clear, understandable test summaries/reports |


# MMAT 2 – CLI, Usage Scenarios & Feedback Cycle

---

## 7. CLI – detailed commands, alias and example results

### 7.1. Creating an alias `mmat` (Windows 10/11, Bash/Linux/Mac)

#### Windows 10/11

**Command line (cmd):**

1. Create a `mmat.bat` file in a directory from your `PATH` (e.g. `C:\Users\YourName\Scripts\`).
2. Paste in:

   ```bat
   @echo off
   python -m mmat %*
   ```
3. Save the file and add the directory to PATH if needed.

**PowerShell:**

1. Open your PowerShell profile (`$PROFILE`), e.g. `C:\Users\YourName\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`.
2. Add:

   ```powershell
   function mmat { python -m mmat $args }
   ```
3. Save and start a new session.

**Pip install:**

* If MMAT installed via pip, the `mmat` command may be available immediately.

#### Linux/Mac (Bash/Zsh)

Add to `.bashrc` or `.zshrc`:

```bash
alias mmat='python -m mmat'
```

or:

```bash
alias mmat='mmat'
```

Then:

```bash
source ~/.bashrc
# or
source ~/.zshrc
```

---

### 7.2. Detailed command descriptions, examples and results

#### Command: `generate`

**Description:**
Creates a new E2E test (JSON format) from a text description or YAML file. May overwrite existing test with `--force`.

**Example:**

```bash
mmat generate --desc "Open page, enter data..." --output ./tests/login.json
```

**Parameters:**

* `--desc` – test description (text or file)
* `--output` – output JSON file
* `--force` – overwrite and use LLM

**Sample result:**

```
[MMAT] Generating E2E test...
[MMAT] Reasoning model generated 5 steps.
[MMAT] Test saved to ./tests/login.json
```

#### Command: `run`

**Description:**
Runs the given E2E test (JSON) step-by-step in Playwright. Can start from any step.

**Example:**

```bash
mmat run --test ./tests/login.json
mmat run --test ./tests/login.json --step 3
```

**Parameters:**

* `--test` – JSON file
* `--step` – starting step number

**Sample result:**

```
[MMAT] Running test: ./tests/login.json
Step 3/5: Enter e-mail test@abc.com   ✔️ OK
Step 4/5: Enter password test123      ✔️ OK
Step 5/5: Click 'Login'               ❌ Element button[type=submit] not found!
[MMAT] Test ended with errors. Use 'mmat feedback --test ...' to fix.
```

#### Command: `export`

**Description:**
Exports E2E test (JSON) to Playwright code (Python or JS).

**Example:**

```bash
mmat export --test ./tests/login.json --to playwright --lang python --output ./tests/login.py
```

**Parameters:**

* `--test` – JSON file
* `--to playwright`
* `--lang` – python/js
* `--output` – output file

**Sample result:**

```
[MMAT] Exporting test to Playwright (Python)...
[MMAT] Generated: ./tests/login.py
```

#### Command: `describe`

**Description:**
Creates or updates human-readable test description from JSON.

**Example:**

```bash
mmat describe --test ./tests/login.json --output ./tests/login.desc
```

**Parameters:**

* `--test` – JSON file
* `--output` – description file

**Sample result:**

```
[MMAT] Generating test description ./tests/login.json
[MMAT] Description saved in ./tests/login.desc
```

#### Command: `feedback`

**Description:**
Improvement mode – allows fixing selected test steps after execution (feedback cycle).

**Example:**

```bash
mmat feedback --test ./tests/login.json
```

**Parameters:**

* `--test` – JSON file

**Sample result (visual step):**

```
Step 4/7: Click button (Type: Screenshot, BBOX: 120,430,88,36, OCR: 'Login')
❗ No DOM element found.
Would you like to modify coordinates (Y/n)? [Enter new: x,y,w,h]
Or provide new text description: (e.g. 'red button bottom right')
```

#### Command: `list`

**Description:**
Lists tests and statuses using given filters.

**Example:**

```bash
mmat list --all
mmat list --only-desc
mmat list --with-desc --with-json --without-playwright
```

**Parameters:**

* `--all`, `--only-desc`, `--with-desc`, `--with-json`, `--without-playwright`

**Sample result:**

```
ID        | Description         | JSON    | Playwright | Status
------------------------------------------------------------------
login_001 | YES                 | YES     | YES        | ready
signup_002| YES                 | NO      | NO         | only desc
reset_003 | YES                 | YES     | NO         | not exported
```

#### Command: `show`

**Description:**
Displays test details: steps, statuses, dates. Visual-only steps display bbox/OCR/description.

**Example:**

```bash
mmat show --test ./tests/login.json
```

**Parameters:**

* `--test` – test file

**Sample result:**

```
Test: login_001
Description: Logging into bestin-it.com
Steps:
1. Open page ...         ✔️
2. Find email field      ✔️
4. Click button (Type: Screenshot, BBOX: 120,430,88,36, OCR: 'Login')
...
Status: ready to run
Last modified: 2025-05-31 12:34
```

---

## 8. Full workflow – usage scenarios

### 8.1. Generating and running a test (happy path)

1. User prepares test description.
2. Generates E2E test:

   ```bash
   mmat generate --desc ./tests/login.desc --output ./tests/login.json
   ```
3. Runs test:

   ```bash
   mmat run --test ./tests/login.json
   ```
4. Exports to Playwright:

   ```bash
   mmat export --test ./tests/login.json --to playwright --lang python --output ./tests/login.py
   ```

### 8.2. Running test from a specific step

* Start from step 2:

  ```bash
  mmat run --test ./tests/login.json --step 2
  ```

### 8.3. Improvement mode (feedback) after test – including visual steps

1. User completes test, wants to fix a step (e.g. visual step):

   ```bash
   mmat feedback --test ./tests/login.json
   ```
2. Framework shows numbered steps, including visual steps with bbox/OCR/description, asks for changes.
3. User can provide new coordinates, OCR text or verbal description.
4. After update, test and description are synced.
5. Repeatable until user is satisfied.

### 8.4. Listing and filtering tests

* All tests:

  ```bash
  mmat list --all
  ```
* Only tests with description, no JSON:

  ```bash
  mmat list --only-desc
  ```
* Tests with description & JSON, no Playwright:

  ```bash
  mmat list --with-desc --with-json --without-playwright
  ```

### 8.5. Export and run Playwright test

1. Export:

   ```bash
   mmat export --test ./tests/login.json --to playwright --lang python --output ./tests/login.py
   ```
2. Run Playwright code:

   ```bash
   pytest ./tests/login.py
   ```

   or

   ```bash
   python ./tests/login.py
   ```

### 8.6. Start from any step

* From description: `generate` → `run` → `export`
* From E2E JSON test: `run` → `export` → `describe`
* From Playwright code: `show` → `describe` → feedback/edit

