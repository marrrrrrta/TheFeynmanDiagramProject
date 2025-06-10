
# FEYNMAN DIAGRAM PROJECT: Feynman Diagram Validator and Generator

The **FEYNMAN DIAGRAM PROJECT** is a Python-based tool that takes a particle physics reaction (e.g. `e+ e- -> mu+ mu-`), checks whether the process is physically allowed, and generates a Feynman diagram if it is.


## Features

- **Input Parsing**: Accepts simple text reactions and normalizes them.
- **Validity Checking**: Verifies conservation of charge, lepton/baryon number, and known interaction vertices.
- **Reaction Identifier**: Identifies the type of interaction(s) that happen in the reaction (strong, weak, electromagnetic, or flavor change).

#### In progress ⚙️ :
- **Diagram Generation**: Outputs a valid TikZ-Feynman diagram in LaTeX.
- **Optional Rendering**: Compiles TikZ into PDF or image format.
- **GUI Interface**: A simple GUI for inputting reactions and viewing diagrams.
- **Extensible**: Easily add more particles, forces, or topologies.


## Getting Started

### Prerequisites

- Python 3.9+
- LaTeX with `TikZ-Feynman` package installed
- `pdflatex` or `latexmk` for diagram rendering

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/feyndiag.git
   cd feyndiag

	2.	Create a virtual environment and install dependencies:

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt


## Usage

Run the main script and follow the prompts:

```bash
python main.py
```
You will be prompted to enter a particle reaction in the form of `particle1 particle2 -> particle3 particle4`. The script will validate the reaction and generate a Feynman diagram if valid.



## Project Structure

    feyndiag_project/
    ├── main.py               # CLI entry point
    ├── data/                 # Particle definitions
    ├── src/                  # Core logic
    ├── tests/                # Unit tests
    ├── output/               # Generated diagrams
    ├── requirements.txt
    └── README.md



## Contributing

Contributions are welcome! The project is in early stages, so feel free to suggest features, report bugs, or submit pull requests.

## License

MIT License

---