# Linkora

Linkora is a **Domain-Specific Language (DSL)** for creating customizable
profile pages, similar to Link-in-Bio platforms such as Zlink.

Instead of hand-writing HTML and CSS, you describe the structure and content of
your page in a single `.lkr` source file. The Linkora compiler validates the
file and generates a complete, self-contained, mobile-first static HTML page.

```lkr
Page {

    Link {
        title: "GitHub"
        url: "https://github.com"
    }

    Link { title: "Portfolio", url: "https://example.com" }

}
```

## Features

- Clean, human-readable declarative syntax
- `Page` block as the root container of every document
- Schema-driven semantic validation (types, enums, colors, URLs, required properties)
- Static HTML + CSS generation, mobile-first and responsive
- Deterministic error messages with line and column information
- Easy to extend: adding a new block requires no grammar or parser changes

## Requirements

- Python 3.10 or newer
- Java 11+ (only needed to regenerate the parser from the grammar)

## Installation

Create a virtual environment (optional but recommended) and install the
runtime dependency:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

For development (running the test suite), install the development
dependencies instead:

```bash
pip install -r requirements-dev.txt
```

## Usage

Compile a Linkora source file into a static page:

```bash
python main.py <source.lkr>
```

By default the generated page is written to `output/index.html`. Use `--out`
to choose a different directory:

```bash
python main.py examples\sample.lkr --out my-site
```

Then open the generated file in a browser:

```bash
start output\index.html       # Windows
open output/index.html        # macOS
```

The output is a single self-contained HTML file with the CSS embedded, so it
can be hosted anywhere or opened directly.

### Exit codes

- `0` — compilation succeeded and the page was generated.
- `1` — compilation failed. All errors are printed to stderr in the format:

```
Semantic Error
Unknown property 'fontSize' inside block 'Link'.
Line 12, Column 5.
```

## Project Structure

```
grammar/Linkora.g4          ANTLR4 grammar (lexer + parser)
tools/generate_parser.bat   Regenerates the parser from the grammar
compiler/
  generated/                ANTLR-generated Python parser (do not edit)
  ast.py                    Intermediate representation
  build_ast.py              Parse tree -> AST
  schema.py                 Block and property definitions (the language spec)
  validator.py              Semantic validation and default resolution
  codegen/                  HTML and CSS generation
  pipeline.py               End-to-end compilation
main.py                     Command-line interface
docs/                       Language specification and block reference
tests/                      Test suite
examples/                   Sample .lkr files
```

## Language

A Linkora document is a single `Page` block that contains all other blocks.

The full language reference will be available in the
[`docs/language/LinkoraLanguageSpecification.md`](docs/language/LinkoraLanguageSpecification.md) in the future.
Blocks implemented so far:

| Block | Documentation |
|-------|---------------|
| `Page` | [`docs/language/Page.md`](docs/language/Page.md) |
| `Link` | [`docs/language/Link.md`](docs/language/Link.md) |

## Status

🚧 Under development.
