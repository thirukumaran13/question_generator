# Question Generator

A browser-based tool for creating, managing, and generating randomized question papers from structured JSON question banks. Built entirely with HTML, CSS, and vanilla JavaScript — no build step required.

**Live demo:** https://thirukumaran13.github.io/question_generator/

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Running the App](#running-the-app)
- [Question Generator (`index.html`)](#question-generator-indexhtml)
  - [Loading Questions](#loading-questions)
  - [Filtering and Configuring](#filtering-and-configuring)
  - [Generating Questions](#generating-questions)
  - [Viewing and Printing](#viewing-and-printing)
- [Question Creator (`question-creator.html`)](#question-creator-question-creatorhtml)
  - [Question Types](#question-types)
  - [Rich Text Editor](#rich-text-editor)
  - [LaTeX Math Support](#latex-math-support)
  - [Saving and Downloading](#saving-and-downloading)
  - [Importing Existing JSON](#importing-existing-json)
- [Question Bank Structure](#question-bank-structure)
  - [Manifest (`manifest.json`)](#manifest-manifestjson)
  - [Question File Format](#question-file-format)
  - [Context-Based Questions](#context-based-questions)
- [Validating JSON Files](#validating-json-files)
- [Adding Questions to the Bank](#adding-questions-to-the-bank)

---

## Overview

This project consists of two tools:

| Tool | File | Purpose |
|---|---|---|
| **Question Generator** | `index.html` | Load a question bank, filter by type, and generate a randomized question paper |
| **Question Creator** | `question-creator.html` | Build questions visually and export them as a JSON file |

---

## Project Structure

```
question_generator/
├── index.html              # Question Generator (main app)
├── question-creator.html   # Question Creator tool
├── server.py               # Local Python HTTP server
├── start_server.bat        # Windows shortcut to start the server
├── validate_json.py        # CLI tool to validate question JSON files
└── questions/
    ├── manifest.json        # Index of all question bank entries
    ├── manifest-schema.json # JSON Schema for manifest.json
    ├── question-schema.json # JSON Schema for question files
    └── X/
        └── ICSE/
            ├── Biology/
            │   ├── Unit-1/Unit-1.json
            │   └── Unit-2/Unit-2.json
            └── Mathematics/
                └── Unit-1/Unit-1.json
```

---

## Getting Started

### Prerequisites

- Python 3.7 or later (for the local server)
- A modern browser (Chrome, Firefox, Edge, Safari)

> The app **must** be served over HTTP (not opened as a local `file://` URL) because it uses `fetch()` to load JSON files. The included server handles this.

### Running the App

#### Online (GitHub Pages)

The app is hosted publicly — no installation needed:

- **Question Generator:** https://thirukumaran13.github.io/question_generator/
- **Question Creator:** https://thirukumaran13.github.io/question_generator/question-creator.html

> The online version uses the question bank bundled in the repository. To use your own question files you will need to run it locally.

#### Locally

**Windows:**

Double-click `start_server.bat`. This starts the server on port 8080 and opens the app in your default browser automatically.

**Any platform:**

```bash
python server.py
```

Or on a custom port:

```bash
python server.py 5000
```

Then open `http://localhost:8080` (or your chosen port) in your browser.

To open the Question Creator locally, navigate to `http://localhost:8080/question-creator.html`.

---

## Question Generator (`index.html`)

The main app for generating randomized question papers.

### Loading Questions

There are three ways to load questions:

#### 1. Question Bank

Uses `questions/manifest.json` to discover available question files. A cascading set of dropdowns lets you narrow down the selection:

1. **Class** — e.g., `X`
2. **Syllabus / Board** — e.g., `ICSE`
3. **Subject** — e.g., `Biology`
4. **Unit / Chapter** — check one or more units from the list, then click **Load Selected Units**

Multiple units from the same subject can be loaded at once. Their questions are merged into a single pool.

> If `manifest.json` is missing or empty, a warning is shown and you can still use the Upload or URL tabs.

#### 2. Upload File

Click the upload area (or drag and drop) to load any `.json` question file directly from your computer. Supports both flat question arrays and context-based formats.

#### 3. Load from URL

Paste a URL pointing to a `.json` question file hosted anywhere (e.g., a GitHub raw URL) and click **Load JSON**.

---

### Filtering and Configuring

After questions are loaded, a filter panel appears:

#### Filter by Question Type

Clickable chips show each question type present in the loaded bank along with the count available. Toggle chips on/off to include or exclude specific types. Types with zero available questions are automatically disabled.

#### Stats

A summary row shows:
- Total questions available
- Total marks value in the loaded pool

#### Count by Type

For each included question type, you can specify exactly how many questions to pick. The row shows how many are available so you can stay within bounds.

Rows can be **drag-and-dropped** to set the order in which question types appear in the generated paper.

#### Total Marks Limit

Enable the **Limit to N marks** toggle and set a number to cap the total marks of the generated paper. The generator will stop picking questions once the marks limit would be exceeded.

---

### Generating Questions

Click **✨ Generate Questions**. The app randomly selects the requested number of questions per type from the loaded pool. Each click with the same settings produces a different random set.

---

### Viewing and Printing

The generated paper screen shows:

- A numbered list of questions, rendered with full formatting (LaTeX math, images, tables, bold/italic text)
- Question type badges (MCQ, Fill, Match, Sequence, True/False, marks-based)
- Marks value per question


**Actions available:**

| Button | Description |
|---|---|
| 🔄 Regenerate | Pick a fresh random set using the same settings |
| 🖨 Print | Open the browser print dialog. The paper prints clean (no UI chrome). A separate **Answer Sheet** is appended as the final printed page |
| ← Back | Return to the setup screen to change filters or load a different bank |

---

## Question Creator (`question-creator.html`)

A visual editor for authoring question JSON files.

### Question Types

| Type | Description |
|---|---|
| **Multi Choice** | A question with 2–6 answer options. One option is marked as correct |
| **Fill in the blanks** | A statement with a blank; the answer is the word or phrase that fills it |
| **Match the following** | A list of pairs (Column A → Column B). The answer is a text description of the correct matches |
| **Arrange in logical sequence** | A list of items (2–8) that must be ordered correctly. The answer describes the correct sequence |
| **True or False** | A statement with a True/False toggle for the answer |
| **1 marks – 5 marks** | Open-ended short/long answer questions. The answer is a model answer |
| **Context Based** | A shared reading passage followed by up to 10 sub-questions. Each sub-question can be any supported type |

---

### Rich Text Editor

Each text field (question, choices, answer, reason, context) uses a built-in WYSIWYG editor with a formatting toolbar:

| Feature | Toolbar controls |
|---|---|
| Text styling | Bold, Italic, Underline, Strikethrough |
| Script | Superscript, Subscript |
| Code | Inline code |
| Color | Text color and highlight color (split-button with color picker) |
| Lists | Unordered list, Ordered list |
| Block elements | Blockquote |
| Media | Insert image (URL or relative path), Insert table |
| LaTeX | Insert math equation (inline or display block) |

**Raw HTML mode:** Click the **Raw HTML** toggle in the editor card header to switch between the rich editor and a plain textarea where you can type or paste HTML directly.

---

### LaTeX Math Support

Click the **Σ LaTeX** button in the toolbar (or the ∑ button in the question editor) to open the LaTeX insert dialog:

1. Type your LaTeX expression (e.g., `x^2 + \frac{a}{b} = 0`)
2. Choose **Inline** (renders within a sentence) or **Display** (centered on its own line)
3. A live preview renders the equation using KaTeX
4. Click **Insert** to embed it in the editor

LaTeX nodes are highlighted in purple in the editor. Formatting toolbar controls are disabled while the cursor is inside a LaTeX node.

---

### Saving and Downloading

- Fill in the question form and click **✔ Save Question** to add it to the question list at the bottom of the page.
- Questions in the list show a truncated preview, their type, and marks value.
- Click the **edit** icon (✏) on any saved question to expand it inline and modify it.
- Click the **delete** icon (🗑) to remove a question.
- Once you have at least one question, **⬇ Download JSON** becomes active. Click it to save the full question set as a `.json` file.
- Click **👁 Preview JSON** to see the raw JSON output in an overlay before downloading.

---

### Importing Existing JSON

Use the **Import Existing JSON** card at the top to load a previously created question file:

- Click the drop zone or drag and drop a `.json` file
- The questions from the file are loaded into the question list
- You can then add, edit, or delete questions and re-download

---

## Question Bank Structure

### Manifest (`manifest.json`)

The manifest is an array of entries that tells the Question Generator where to find question files:

```json
{
  "entries": [
    {
      "class": "X",
      "syllabus": "ICSE",
      "subject": "Biology",
      "unit": "Unit 1 – Cell: The Structural and Functional Unit of Life",
      "folder": "X/ICSE/Biology/Unit-1",
      "files": ["Unit-1.json"]
    }
  ]
}
```

| Field | Description |
|---|---|
| `class` | Grade or class level (e.g., `"X"`, `"IX"`) |
| `syllabus` | Board or curriculum (e.g., `"ICSE"`, `"CBSE"`) |
| `subject` | Subject name (e.g., `"Biology"`, `"Mathematics"`) |
| `unit` | Human-readable unit/chapter name shown in the UI |
| `folder` | Path to the folder, relative to the `questions/` directory |
| `files` | List of JSON filenames inside that folder |

---

### Question File Format

A question file is a JSON array. Each element is either a standalone question object or a context group.

**Standalone question:**

```json
{
  "type": "Multi Choice",
  "question": "Which organelle is known as the powerhouse of the cell?",
  "choices": ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"],
  "answer": 1,
  "reason": "Mitochondria produce ATP through cellular respiration."
}
```

**Fields:**

| Field | Required | Description |
|---|---|---|
| `type` | Yes | Question type (see supported types below) |
| `question` | Yes | Question text. HTML is allowed |
| `answer` | Yes | For Multi Choice: zero-based integer index of the correct choice. For all other types: a string |
| `choices` | MCQ and Arrange in logical sequence only | Array of 2–6 answer option strings |
| `reason` | No | Explanation for the correct answer (shown when answer is revealed) |

**Supported type values:**

```
"Multi Choice"
"Fill in the blanks"
"Match the following"
"Arrange in logical sequence"
"True or False"
"1 marks" | "2 marks" | "3 marks" | "4 marks" | "5 marks"
```

---

### Context-Based Questions

Wrap questions under a shared passage using a context group:

```json
{
  "context": "<p>Read the following passage and answer the questions below.</p><p>The cell membrane controls what enters and exits the cell...</p>",
  "questions": [
    {
      "type": "Multi Choice",
      "question": "What is the primary role of the cell membrane?",
      "choices": ["Energy production", "Selective permeability", "Protein synthesis", "DNA replication"],
      "answer": 1
    },
    {
      "type": "True or False",
      "question": "The cell membrane is fully permeable to all substances.",
      "answer": "False",
      "reason": "The cell membrane is selectively permeable."
    }
  ]
}
```

The `context` field supports HTML. In the generated paper, the passage is displayed above all sub-questions, and each sub-question is numbered continuously with the rest of the paper.

---

## Validating JSON Files

Before adding question files to the bank, validate them against the schema:

```bash
pip install jsonschema
python validate_json.py
```

The validator:
- Checks `manifest.json` against `manifest-schema.json`
- Checks every question file referenced in the manifest against `question-schema.json`
- Reports any files referenced in the manifest that are missing on disk
- Reports any `.json` files in the `questions/` folder that are not referenced in the manifest

Output example:
```
Validating manifest.json ...
  PASS: manifest.json
Validating X/ICSE/Biology/Unit-1/Unit-1.json ...
  PASS: X/ICSE/Biology/Unit-1/Unit-1.json (12 questions)

Results: 2 passed, 0 failed
```

---

## Adding Questions to the Bank

1. Open `http://localhost:8080/question-creator.html`
2. Author your questions using the visual editor
3. Click **⬇ Download JSON** — save the file inside `questions/<Class>/<Syllabus>/<Subject>/<Unit>/`
4. Add a corresponding entry to `questions/manifest.json`
5. Run `python validate_json.py` to confirm the file is valid
6. Reload `http://localhost:8080` — the new unit appears in the Question Bank dropdowns
