
# FEYNMAN DIAGRAM PROJECT: Feynman Diagram Validator and Generator

The **FEYNMAN DIAGRAM PROJECT** is a Python-based tool that takes a particle physics reaction (e.g. `e+ e- -> mu+ mu-`), checks whether the process is physically allowed, and generates a LaTeX TikZ-Feynman diagram if it is.


## Features

- **Input Parsing**: Accepts simple text reactions and normalizes them.
- **Validity Checking**: Verifies conservation of charge, lepton/baryon number, and known interaction vertices.
- **Diagram Generation**: Outputs a valid TikZ-Feynman diagram in LaTeX.
- **Optional Rendering**: Compiles TikZ into PDF or image format.
- **Extensible**: Easily add more particles, forces, or topologies.


## Getting Started

### Prerequisites

- Python 3.9+
- LaTeX with `TikZ-Feynman` package installed
- (Optional) `pdflatex` or `latexmk` for diagram rendering

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

(write how the output works)




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

Contributions are welcome! If you’d like to add new interactions (e.g. QCD, weak), open an issue or fork the repo and submit a pull request.

## License

MIT License


## Acknowledgments

•	TikZ-Feynman for LaTeX diagram generation  
•	SymPy for symbolic math (planned)

---