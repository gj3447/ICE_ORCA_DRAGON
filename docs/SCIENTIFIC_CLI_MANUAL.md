# Scientific CLI manual

이 문서는 2026-08-16 현재 이 호스트에 실제로 설치된 과학 계산 도구의 버전별 진입점과
자주 쓰는 명령을 한곳에 모은 로컬 안내서다. 전체 옵션은 각 도구의 내장 `--help`가
정본이고, API 세부사항은 아래의 공식 문서 링크 또는 내려받은 오프라인 매뉴얼을 사용한다.

어떤 도구도 물리 가설을 자동으로 증명하지 않는다. 중요한 부호·관성·제약대수 결과는 서로
다른 엔진으로 교차검산하고, 수치 계산은 차원과 오차를 함께 추적한다.

## 1. 설치 상태와 가장 짧은 진입 명령

| 도구 | 설치 버전 | 바로 시작 | 전체 도움말 |
|---|---:|---|---|
| Cadabra | 2.5.14 | `cadabra2` | `cadabra2 --help` |
| JupyterLab | 4.6.3 | `jupyter-lab` | `jupyter-lab --help-all` |
| marimo | 0.23.16 | `marimo edit` | `marimo --help`, `marimo COMMAND --help` |
| Snakemake | 9.25.1 | `snakemake --cores all` | `snakemake --help` |
| uv | 0.12.3 | `uv run python script.py` | `uv help`, `uv help COMMAND` |
| Lean | 4.33.0 | `lean Main.lean` | `lean --help` |
| Lake | 5.0.0 | `lake build` | `lake help`, `lake help COMMAND` |
| elan | 4.2.3 | `elan show` | `elan help`, `elan help SUBCOMMAND` |
| Julia | 1.12.7 | `julia` | `julia --help`와 `julia --help-hidden` |
| Juliaup | 1.21.0 | `juliaup status` | `juliaup help`, `juliaup help COMMAND` |

로컬에 `man` 페이지는 없다. 특히 다음 차이를 기억한다.

- JupyterLab의 전체 설정은 `--help`가 아니라 `--help-all`이다.
- marimo와 Snakemake에는 `--help-all`이 없다. marimo는 하위 명령별 `--help`, Snakemake는
  루트 `--help`가 전체 CLI 참조다.
- Lean에는 `--help-hidden`이 없다. Julia의 `--help-hidden`은 기본 도움말의 대체물이 아니라
  숨은 옵션만 별도로 보여 주므로 둘 다 확인한다.
- Lake는 `lake help build`, elan은 `elan help toolchain`, Juliaup은
  `juliaup help override`처럼 재귀적으로 도움말을 연다.

## 2. Python 환경은 두 개다

### 저장소 잠금 환경

저장소 계산은 기본적으로 아래처럼 실행한다.

```bash
uv sync
uv run python path/to/check.py
uv run python -c 'import sympy, scipy; print(sympy.__version__, scipy.__version__)'
```

현재 저장소 `.venv`는 Python 3.13.5, NumPy 2.5.2, SciPy 1.18.0, SymPy 1.14.0,
mpmath 1.3.0을 사용한다. `uv.lock`을 재현해야 하는 계산에는 이 환경을 쓴다.

### JupyterLab 격리 도구 환경

`jupyter-lab`은 `uv tool`로 분리 설치되어 저장소의 `uv.lock`을 바꾸지 않는다. 현재 커널은
Python 3.11.15이며 NumPy 2.4.6, SciPy 1.17.1, SymPy 1.14.0, pandas 3.0.5,
Matplotlib 3.11.1, mpmath 1.3.0, NetworkX 3.6.1, ipykernel 7.3.0,
python-flint 0.9.0, Astropy 8.0.1, Pint 0.25.3, uncertainties 3.2.3,
z3-solver 5.1.0을 포함한다.

```bash
jupyter-lab
jupyter-lab --no-browser --ServerApp.port=8888
jupyter-lab paths
/home/lagyeongjun/.local/share/uv/tools/jupyterlab/bin/jupyter server list
/home/lagyeongjun/.local/share/uv/tools/jupyterlab/bin/jupyter kernelspec list
```

현재 PATH에는 `jupyter-lab`만 노출되고 범용 `jupyter` wrapper는 노출되지 않는다. 그래서
`jupyter server ...`나 `jupyter kernelspec ...`은 위의 전체 경로를 사용한다.

동일한 격리 환경에서 노트북 없이 스크립트를 실행하려면:

```bash
/home/lagyeongjun/.local/share/uv/tools/jupyterlab/bin/python check.py
```

## 3. Cadabra 2.5.14

Cadabra는 텐서, vielbein, gamma matrix, Grassmann 변수, Fierz 변환처럼 일반 CAS가
쉽게 망가뜨리는 장론 문법에 우선 사용한다.

```bash
cadabra2                 # 대화형 CLI
cadabra2 calculation.cdb # 스크립트 실행
cadabra2 -i calculation.cdb
cadabra2 -q calculation.cdb
cadabra2 --version
cadabra2 --help
```

중요 옵션:

- `-i`: 스크립트 실행 뒤 같은 Python 문맥에서 대화형 모드 유지
- `-l`: 입력을 대화형처럼 한 줄씩 실행
- `-f`: `SystemExit` 발생 시 다음 스크립트로 진행하지 않음
- `-q`: 시작 배너 숨김
- `-w`: 색상 출력 비활성화
- `-V`: 디버그 출력

Cadabra에서는 `-v`가 version이고 `-V`가 verbose다. 임베디드 Python은 3.10.12로,
저장소와 Jupyter의 Python과 또 다른 런타임이다.

연구에서는 BGG 원문의 connection/curvature를 Cadabra의 source-order index 규칙으로 만들고,
동일한 결과를 SymPy나 FLINT에서 독립적으로 재구성한다. 한 엔진의 자동 단순화만 믿지 않는다.

공식 참조: [Cadabra reference](https://cadabra.science/man.html),
[help/book](https://cadabra.science/help.html).

## 4. JupyterLab 4.6.3

```bash
jupyter-lab                        # 현재 디렉터리를 루트로 실행
jupyter-lab notebooks/             # 특정 디렉터리에서 실행
jupyter-lab --no-browser
jupyter-lab --ServerApp.ip=127.0.0.1 --ServerApp.port=8888
jupyter-lab path                   # application 경로
jupyter-lab paths                  # data/config/runtime 경로
jupyter-lab workspace --help-all
jupyter-lab --generate-config
```

서버를 외부 인터페이스에 노출할 때는 token과 방화벽을 먼저 확인한다. 연구 notebook은 입력,
출력, 패키지 버전을 함께 남기되 최종 exact identity는 독립 스크립트나 테스트로 옮긴다.

공식 문서: [JupyterLab 4.6.x](https://jupyterlab.readthedocs.io/en/4.6.x/),
[user guide](https://jupyterlab.readthedocs.io/en/4.6.x/user/).

## 5. marimo 0.23.16

marimo notebook은 Python 파일로 저장되고 반응형 dependency graph를 갖는다.

```bash
marimo tutorial intro
marimo tutorial --help
marimo edit
marimo edit notebook.py
marimo edit notebook.py --headless --port 2718
marimo run notebook.py
marimo check notebook.py
marimo check --fix notebook.py
marimo convert old.ipynb -o notebook.py
marimo export html notebook.py -o notebook.html
marimo export ipynb notebook.py -o notebook.ipynb
marimo export pdf notebook.py -o notebook.pdf  # nbformat/nbconvert 필요
marimo env
```

Jupyter 변환 후에는 cell 실행순서에 의존하던 mutation을 고쳐야 할 수 있다. 원격 notebook을
호스트에서 실행할 때 `--trusted`를 무심코 쓰지 않는다.

공식 문서: [marimo CLI reference](https://docs.marimo.io/cli/),
[scripts](https://docs.marimo.io/guides/scripts/),
[export](https://docs.marimo.io/guides/exporting/).

## 6. Snakemake 9.25.1

Cadabra, SymPy, Julia, plotting을 하나의 재현 가능한 계산 DAG로 묶을 때 쓴다.

```bash
snakemake --help
snakemake -n --cores all           # 반드시 먼저 dry-run
snakemake --cores all
snakemake target/file --cores 4
snakemake --printshellcmds
snakemake --lint
snakemake --dag | dot -Tpdf > dag.pdf
snakemake --summary
snakemake --report report.html
snakemake --rerun-incomplete --cores all
snakemake --unlock
```

`--delete-all-output`, `--delete-temp-output`, `--cleanup-metadata`는 삭제성 명령이다. 대상과
dry-run을 먼저 확인한다.

공식 문서: [Snakemake 9.25.1](https://snakemake.readthedocs.io/en/v9.25.1/),
[CLI reference](https://snakemake.readthedocs.io/en/v9.25.1/executing/cli.html).

## 7. uv 0.12.3

```bash
uv sync                              # lock에 맞춰 환경 동기화
uv lock                              # lock 갱신
uv run python calculation.py
uv run --with sympy python check.py  # 일회성 격리 dependency
uv add sympy
uv remove sympy
uv tree
uv tool list
uv tool install PACKAGE
uv tool run --from PACKAGE COMMAND
uv python list --only-installed
uv cache dir
uv help run
```

저장소 계산에 `uv pip install`을 습관적으로 쓰면 `pyproject.toml`/`uv.lock`과 실제 환경이
어긋날 수 있다. 프로젝트 dependency는 `uv add`, 일회성 검산은 `uv run --with`를 우선한다.

공식 문서: [uv CLI reference](https://docs.astral.sh/uv/reference/cli/).

## 8. Python 과학 라이브러리

### SymPy 1.14.0

정확한 Hessian과 관성을 구성하는 최소 예:

```python
import sympy as sp

dX, dT, dY = sp.symbols("dX dT dY", real=True)
lam = sp.symbols("lambda", positive=True)
L = lam * (-dX**2 + dT**2 + dY**2) / 2
G = sp.hessian(L, (dX, dT, dY))
assert G == sp.diag(-lam, lam, lam)
assert sp.factor(G.det()) == -lam**3
```

도움말:

```bash
python -m pydoc sympy
python -c 'import sympy as s; help(s.hessian)'
```

공식 문서: [SymPy 1.14](https://docs.sympy.org/).

### python-flint 0.9.0

```python
from flint import fmpz, fmpq, fmpz_poly, arb

assert fmpq(1, 3) + fmpq(1, 6) == fmpq(1, 2)
x = fmpz_poly([0, 1])
print((x**4 - 1).factor())
print(arb(2).sqrt())  # rigorous ball arithmetic
```

FLINT는 exact integer/rational/polynomial 계산과 Arb ball arithmetic 교차검산에 쓴다.
현재 hosted `latest` 문서는 0.8.0이므로 설치본 0.9.0과 차이가 있을 수 있다.

공식 문서: [python-flint](https://python-flint.readthedocs.io/en/latest/).

### SciPy

저장소 환경은 1.18.0, Jupyter 도구 환경은 1.17.1이다.

```python
import numpy as np
from scipy.integrate import solve_ivp

def rhs(t, y):
    return [y[1], -y[0]]

sol = solve_ivp(rhs, (0.0, 20.0), [1.0, 0.0], rtol=1e-10, atol=1e-12)
assert sol.success
```

공식 문서: [SciPy user guide](https://docs.scipy.org/doc/scipy/tutorial/).

### Astropy 8.0.1

```python
from astropy import units as u
from astropy.cosmology import Planck18

length = (3.0 * u.kpc).to(u.m)
age_z10 = Planck18.age(10)
print(length, age_z10)
```

공식 문서: [Astropy 8.0.1](https://docs.astropy.org/en/v8.0.1/).

### Pint 0.25.3와 uncertainties 3.2.3

```python
from pint import UnitRegistry
from uncertainties import ufloat

ureg = UnitRegistry()
H = 70 * ureg.kilometer / ureg.second / ureg.megaparsec
print(H.to(1 / ureg.second))

x = ufloat(2.0, 0.1)
y = x**2
print(y.nominal_value, y.std_dev)
```

Pint는 차원 오류를 막고, uncertainties는 선형화된 오차 전파와 상관관계를 추적한다.
큰 비선형성·비가우시안 분포에서는 Monte Carlo와 비교한다.

공식 문서: [Pint 0.25.3](https://pint.readthedocs.io/en/0.25.3/),
[uncertainties](https://uncertainties.readthedocs.io/en/stable/).

### Z3 5.1.0

```python
from z3 import Real, Solver, sat

x, y = Real("x"), Real("y")
s = Solver()
s.add(x + y == 1, x > 0, y > 0)
assert s.check() == sat
print(s.model())
```

Z3는 finite side condition, sign case, constraint consistency를 검사하는 보조 도구다. 연속
함수해석이나 물리적 Hilbert-space domain을 SMT 결과로 대체하지 않는다.

공식 문서: [Online Z3 Guide](https://microsoft.github.io/z3guide/),
[API](https://z3prover.github.io/api/html/).

## 9. Julia 1.12.7, Juliaup 1.21.0

```bash
julia
julia script.jl arg1 arg2
julia --project=. script.jl
julia --project=@temp
julia -e 'using Pkg; Pkg.status()'
julia -t auto script.jl
juliaup status
juliaup list
juliaup add 1.12
juliaup default 1.12
juliaup update
```

REPL 모드:

- `?name`: 도움말
- `]`: Pkg 모드 (`status`, `add`, `update`, `instantiate`, `precompile`)
- `;`: shell 모드
- Backspace: 특수 모드 종료

프로젝트 dependency를 재현하려면 `Project.toml`과 `Manifest.toml`을 함께 둔다. 현재
Symbolics/OrdinaryDiffEq는 저장소가 아니라 `~/.julia/environments/v1.12/`의 홈 기본
환경에 설치되어 있으므로, 연구 계산을 고정할 때는 저장소 안에 Julia project와 manifest를
새로 만드는 편이 안전하다.

공식 문서: [Julia 1.12 manual](https://docs.julialang.org/en/v1.12/),
[Pkg](https://pkgdocs.julialang.org/v1/).

## 10. Symbolics.jl 7.36.0과 OrdinaryDiffEq.jl 7.6.0

```julia
using Symbolics

@variables x y
expr = expand((x + y)^3)
@assert substitute(expr, Dict(x => 1, y => 2)) == 27
```

```julia
using OrdinaryDiffEq

f(u, p, t) = u
prob = ODEProblem(f, 1.0, (0.0, 1.0))
sol = solve(prob, Tsit5(); reltol=1e-10, abstol=1e-12)
@assert abs(sol(1.0) - exp(1)) < 1e-8
```

설치본의 정확한 버전 확인:

```bash
julia --startup-file=no -e 'using Pkg; Pkg.status()'
julia --startup-file=no -e 'using Symbolics; println(pkgversion(Symbolics))'
julia --startup-file=no -e 'using OrdinaryDiffEq; println(pkgversion(OrdinaryDiffEq))'
```

현재 stable hosted 문서는 각각 Symbolics 7.31.0, OrdinaryDiffEq 7.1.1로 빌드되어 설치본보다
뒤처져 있다. API가 의심스러우면 Julia REPL `?name`, `methods(name)`, 설치된 package source를
우선 확인한다.

공식 문서: [Symbolics](https://docs.sciml.ai/Symbolics/stable/),
[OrdinaryDiffEq](https://docs.sciml.ai/OrdinaryDiffEq/stable/).

## 11. Lean 4.33.0, Lake 5.0.0, elan 4.2.3

단일 파일 검사:

```lean
theorem add_zero_nat (n : Nat) : n + 0 = n := by
  simp
```

```bash
lean Main.lean
lean --json Main.lean
lean --profile Main.lean
```

프로젝트:

```bash
lake new MyProof math
cd MyProof
lake update
lake build
lake lean MyProof/Basic.lean
lake lint
lake test
lake env lean --version
```

도구 버전 관리:

```bash
elan show
elan toolchain list
elan default leanprover/lean4:v4.33.0
elan override set leanprover/lean4:v4.33.0
elan which lean
```

Lean은 수식과 가정이 고정된 뒤의 대수 정리에 쓴다. formal proof가 source convention의
물리적 정당성이나 자연의 모형 선택을 대신하지 않는다.
현재 elan default는 움직이는 `stable` channel이므로 실제 연구 프로젝트에는
`lean-toolchain` 파일로 `leanprover/lean4:v4.33.0`을 고정한다. Juliaup도 현재 `release`
channel이므로 실행 기록에는 해석된 Julia 1.12.7을 함께 남긴다.

공식 문서: [Lean 4.33 reference](https://lean-lang.org/doc/reference/4.33.0/),
[Lake](https://lean-lang.org/doc/reference/4.33.0/Build-Tools-and-Distribution/Lake/),
[Elan](https://lean-lang.org/doc/reference/4.33.0/Build-Tools-and-Distribution/Managing-Toolchains-with-Elan/).

## 12. 내려받은 오프라인 매뉴얼

PDF는 모두 열기·텍스트 추출·첫/중간/마지막 페이지 렌더링 검사를 통과했다.
대용량 PDF/ZIP 본체는 이 checkout의 로컬 reference cache이며 Git에는 넣지 않는다.
공식 URL, version caveat, SHA-256과 문서 색인은 `output/manual-bundles/`의 추적 가능한
텍스트 파일에 남긴다.

| 로컬 파일 | 내용 | 버전 주의 |
|---|---|---|
| [`cadabra-2-book-2025.pdf`](../output/pdf/tool-manuals/cadabra-2-book-2025.pdf) | The Cadabra Book, 117쪽 | Cadabra 2.5.14 시점 |
| [`cadabra-writing-algorithms.pdf`](../output/pdf/tool-manuals/cadabra-writing-algorithms.pdf) | Cadabra2 algorithm 작성, 12쪽 | 공식 보조 문서 |
| [`cadabra-introduction-paper.pdf`](../output/pdf/tool-manuals/cadabra-introduction-paper.pdf) | Cadabra tutorial/reference paper, 116쪽 | 역사적 문서 |
| [`sympy-1.14.0-documentation.pdf`](../output/pdf/tool-manuals/sympy-1.14.0-documentation.pdf) | SymPy 전체 문서, 3,622쪽 | 설치본과 정확히 일치 |
| [`julia-1.12.6-documentation.pdf`](../output/pdf/tool-manuals/julia-1.12.6-documentation.pdf) | Julia 언어 문서, 1,897쪽 | 설치 1.12.7보다 patch 하나 이전; 1.12.7 PDF 링크는 현재 404 |
| [`uncertainties-documentation.pdf`](../output/pdf/tool-manuals/uncertainties-documentation.pdf) | uncertainties 문서, 36쪽 | PDF는 3.2.2, 설치본은 3.2.3 |
| [`lean4-language-paper.pdf`](../output/pdf/tool-manuals/lean4-language-paper.pdf) | Lean 4 system description, 11쪽 | CLI reference는 온라인 4.33 문서 사용 |

추가 오프라인 묶음:

| 로컬 파일 | 내용 |
|---|---|
| [`sympy-1.14.0-html-docs.zip`](../output/manual-bundles/sympy-1.14.0-html-docs.zip) | SymPy 1.14 exact HTML 전체 |
| [`scipy-1.17.0-html-docs.zip`](../output/manual-bundles/scipy-1.17.0-html-docs.zip) | SciPy 1.17.0 HTML; Jupyter의 1.17.1과 patch 차이 |
| [`z3-5.1.0-api-docs.zip`](../output/manual-bundles/z3-5.1.0-api-docs.zip) | Z3 5.1.0 release API docs |
| [`uncertainties-3.2.2-docs.zip`](../output/manual-bundles/uncertainties-3.2.2-docs.zip) | uncertainties 3.2.2 static docs |
| [`marimo-doc-index.txt`](../output/manual-bundles/marimo-doc-index.txt) | 공식 marimo 전체 문서 URL 색인 |
| [`uv-doc-index.txt`](../output/manual-bundles/uv-doc-index.txt) | 공식 uv 문서 URL 색인 |
| [`SHA256SUMS`](../output/manual-bundles/SHA256SUMS) | 내려받은 모든 오프라인 파일의 무결성 목록 |
| [`SOURCES.md`](../output/manual-bundles/SOURCES.md) | 각 로컬 파일의 공식 다운로드 URL과 version caveat |

JupyterLab, marimo, Snakemake, python-flint, Astropy, Pint, Symbolics, OrdinaryDiffEq의 공식
사이트는 현재 versioned PDF를 제공하지 않는다. 위의 exact HTML 링크와 내장 도움말을 사용한다.

## 13. 이 연구에서의 권장 순서

1. BGG 한 출처의 action, connection, curvature convention을 그대로 옮긴다.
2. Cadabra로 index order와 fermionic/tensor algebra를 계산한다.
3. SymPy로 FLRW/Bianchi-I 축약, endpoint 제거, Hessian, Legendre transform을 계산한다.
4. FLINT로 핵심 exact coefficient와 polynomial identity를 독립 검산한다.
5. Pint/Astropy units로 차원을 검사한다.
6. 살아남은 방정식만 SciPy/OrdinaryDiffEq로 수치 적분한다.
7. Snakemake로 각 엔진과 산출물의 dependency를 묶는다.
8. 오랫동안 유지될 핵심 대수 정리만 Lean으로 고정한다.

이 순서는 계산을 재현 가능하게 만들지만, “빅뱅 전 시간가지가 superpartner sector다”라는
물리적 동일시에는 별도의 nonzero physical charge, relational branch projector,
cross-branch observable이 여전히 필요하다.
