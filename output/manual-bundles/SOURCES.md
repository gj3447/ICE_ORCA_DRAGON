# Offline manual sources

Retrieved from official project domains on 2026-08-16 UTC.

| Local file | Official source |
|---|---|
| `../pdf/tool-manuals/cadabra-2-book-2025.pdf` | <https://cadabra.science/the_cadabra_book.pdf> |
| `../pdf/tool-manuals/cadabra-writing-algorithms.pdf` | <https://cadabra.science/writing_algorithms.pdf> |
| `../pdf/tool-manuals/cadabra-introduction-paper.pdf` | <https://cadabra.science/static/pdf/cadabra.pdf> |
| `../pdf/tool-manuals/sympy-1.14.0-documentation.pdf` | <https://github.com/sympy/sympy/releases/download/1.14.0/sympy-docs-pdf-1.14.0.pdf> |
| `sympy-1.14.0-html-docs.zip` | <https://github.com/sympy/sympy/releases/download/1.14.0/sympy-docs-html-1.14.0.zip> |
| `scipy-1.17.0-html-docs.zip` | <https://docs.scipy.org/doc/scipy-1.17.0/scipy-html-1.17.0.zip> |
| `z3-5.1.0-api-docs.zip` | <https://github.com/Z3Prover/z3/releases/download/z3-5.1.0/z3doc.zip> |
| `../pdf/tool-manuals/julia-1.12.6-documentation.pdf` | <https://raw.githubusercontent.com/JuliaLang/docs.julialang.org/assets/julia-1.12.6.pdf> |
| `../pdf/tool-manuals/uncertainties-documentation.pdf` | <https://lmfit.github.io/uncertainties/uncertainties.pdf> |
| `uncertainties-3.2.2-docs.zip` | <https://lmfit.github.io/uncertainties/uncertainties_doc.zip> |
| `../pdf/tool-manuals/lean4-language-paper.pdf` | <https://lean-lang.org/papers/lean4.pdf> |
| `marimo-doc-index.txt` | <https://docs.marimo.io/llms.txt> |
| `uv-doc-index.txt` | <https://docs.astral.sh/uv/llms.txt> |

Version caveats:

- installed Julia is 1.12.7, but the official 1.12.7 PDF link advertised by the HTML manual returned
  HTTP 404 and the official assets branch contained PDFs only through 1.12.6;
- installed Jupyter SciPy is 1.17.1 and repository SciPy is 1.18.0; the offline SciPy bundle is 1.17.0;
- installed uncertainties is 3.2.3; the static PDF/zip identifies itself as 3.2.2;
- all exact and nearest-version distinctions are recorded in `../../docs/SCIENTIFIC_CLI_MANUAL.md`.
