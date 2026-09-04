# Linkora

Linkora is a **Domain-Specific Language (DSL)** for creating customizable
profile pages, similar to Link-in-Bio platforms such as Zlink.

Instead of hand-writing HTML and CSS, you describe the structure and content of
your page in a single `.lkr` source file. The Linkora compiler validates the
file and generates a complete, self-contained, mobile-first static HTML page.

```lkr
Profile {
    Name { title: "Seyyedeh Fargol Nazemzadeh", subtitle: "Developer" }
    Logo { image: "./assets/logo.jpg" }
    Bio { text: "Building cool stuff" }
}

Title {
    title: "My Links"
}

Link { title: "GitHub", url: "https://github.com/Fargolnz" }

Link { title: "Portfolio", url: "https://example.com" }
```

## Features

- Clean, human-readable declarative syntax
- Profile container block with Name, Logo, Bio, and Cover children
- Schema-driven semantic validation (types, enums, colors, URLs, required properties)
- Static HTML + CSS generation, mobile-first and responsive
- Local image file copying to output directory
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
examples/                   Sample .lkr files and assets
```

## Language

A Linkora document is a sequence of top-level blocks.

The full language reference will be available in the
[`docs/language/LinkoraLanguageSpecification.md`](docs/language/LinkoraLanguageSpecification.md) in the future.
Blocks implemented so far:

| Block | Documentation |
|-------|---------------|
| `Profile` | [`docs/language/Profile.md`](docs/language/Profile.md) |
| `Name` | Part of [`docs/language/Profile.md`](docs/language/Profile.md) |
| `Bio` | Part of [`docs/language/Profile.md`](docs/language/Profile.md) |
| `Logo` | Part of [`docs/language/Profile.md`](docs/language/Profile.md) |
| `Cover` | Part of [`docs/language/Profile.md`](docs/language/Profile.md) |
| `Link` | [`docs/language/Link.md`](docs/language/Link.md) |
| `Title` | [`docs/language/Title.md`](docs/language/Title.md) |
| `Text` | [`docs/language/Text.md`](docs/language/Text.md) |
| `SocialMedia` | [`docs/language/SocialMedia.md`](docs/language/SocialMedia.md) |
| `SocialMediaItem` | Part of [`docs/language/SocialMedia.md`](docs/language/SocialMedia.md) |
| `SocialNetwork` | [`docs/language/SocialNetwork.md`](docs/language/SocialNetwork.md) |
| `SocialNetworkItem` | Part of [`docs/language/SocialNetwork.md`](docs/language/SocialNetwork.md) |
| `Contact` | [`docs/language/Contact.md`](docs/language/Contact.md) |
| `ContactItem` | Part of [`docs/language/Contact.md`](docs/language/Contact.md) |
| `Address` | [`docs/language/Address.md`](docs/language/Address.md) |
| `AddressItem` | Part of [`docs/language/Address.md`](docs/language/Address.md) |
| `Image` | [`docs/language/Image.md`](docs/language/Image.md) |
| `ImageItem` | Part of [`docs/language/Image.md`](docs/language/Image.md) |
| `Banner` | [`docs/language/Banner.md`](docs/language/Banner.md) |
| `BannerItem` | Part of [`docs/language/Banner.md`](docs/language/Banner.md) |
| `Video` | [`docs/language/Video.md`](docs/language/Video.md) |
| `FAQ` | [`docs/language/FAQ.md`](docs/language/FAQ.md) |
| `FAQItem` | Part of [`docs/language/FAQ.md`](docs/language/FAQ.md) |

## Status

🚧 Under development.
