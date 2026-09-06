# CAPD continuum backend build

This is a build record for the local C++ backend used by the adjacent
continuum-endpoint certificate runner. It records a dependency build only and
contains no certificate result or research verdict.

## Pinned source and local prefix

- Official repository: <https://github.com/CAPDGroup/CAPD>
- Release tag: `v6.0.0`
- Checked-out revision: `693998cd6d73a0c4e1b141bfb79fcad1c40c3cbe`
- Local cache prefix: `/home/lagyeongjun/.cache/ice-capd/693998cd6d73a0c4e1b141bfb79fcad1c40c3cbe`

The cache prefix is outside this repository and is not a `pyproject.toml` or
`uv.lock` dependency. It is a task-specific, user-local installation. A
different machine may choose another cache root, but must use the pinned source
revision, configuration, and recorded hashes below before accepting a helper
binary as equivalent.

## Build environment

- Compiler: `c++ (Debian 14.2.0-19) 14.2.0` at `/usr/bin/c++`
- Make: GNU Make 4.4.1
- CMake: 4.4.3 at
  `/home/lagyeongjun/.cache/uv/archive-v0/4nN1Zt-a7GLK58yg/cmake/data/bin/cmake`
- CAPD configuration: Release, C++17, tests OFF, examples OFF,
  `CAPD_ENABLE_MULTIPRECISION=OFF`

The host had MPFR and GMP shared libraries but lacked their development
headers, so this build uses CAPD's rigorous binary64 interval types and does
not claim MPFR multiprecision support.

For a portable reconstruction, set a task-specific prefix such as:

```bash
capd_cache_prefix=/home/lagyeongjun/.cache/ice-capd/693998cd6d73a0c4e1b141bfb79fcad1c40c3cbe
git clone --depth 1 --branch v6.0.0 https://github.com/CAPDGroup/CAPD.git "$capd_cache_prefix/source"
git -C "$capd_cache_prefix/source" rev-parse HEAD
mkdir -p "$capd_cache_prefix/build"
```

The `rev-parse` output must be
`693998cd6d73a0c4e1b141bfb79fcad1c40c3cbe`. Configure, build, and install
under the same user-local prefix:

```bash
/path/to/cmake -S "$capd_cache_prefix/source" -B "$capd_cache_prefix/build" \
  -DCAPD_ENABLE_MULTIPRECISION=OFF \
  -DCAPD_BUILD_TESTS=OFF \
  -DCAPD_BUILD_EXAMPLES=OFF \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$capd_cache_prefix/install"
make -C "$capd_cache_prefix/build" -j2
make -C "$capd_cache_prefix/build" install
```

## Helper compilation and linkage

The compiled source is
[`starobinsky_continuum_endpoint_certificate.cpp`](../../cpt_temporal_folded_susy/starobinsky_continuum_endpoint_certificate.cpp).
Its compile command is:

```bash
mkdir -p "$capd_cache_prefix/ice-helper"
c++ -std=c++17 -D__USE_FILIB__ -O2 -frounding-math -DFILIB_EXTENDED -DHAVE_SSE \
  -I"$capd_cache_prefix/install/include" \
  cpt_temporal_folded_susy/starobinsky_continuum_endpoint_certificate.cpp \
  -L"$capd_cache_prefix/install/lib" -lcapd -lfilib \
  -o "$capd_cache_prefix/ice-helper/starobinsky_continuum_endpoint_certificate"
```

The helper links `libcapd.a` and `libfilib.a` statically. Its observed dynamic
dependencies are the host C++ runtime, `libm`, `libgcc_s`, `libc`, and the ELF
loader; no CAPD shared object is loaded.

## Recorded hashes

| Object | SHA-256 |
|---|---|
| CMake cache | `421632833c663712f536d6e74f88ecbc6284d6d0dbf2184b0293366a2b435144` |
| `install/lib/libcapd.a` | `10aaa2b78fbb54f8258e8a9d790b37f790565d79270c2cbfeb00dbdbefb2741e` |
| `install/lib/libfilib.a` | `90a1d0c3919f3739f4b189f7e662fb1a3dd79050df124504dd5411bdbbccea71` |
| helper source | `e10661f470dce792390e38dc5411420c3237b0f9d9e4500429a632337a833575` |
| helper binary | `39809e3c4fd5c24a8992e432230427d8df921f6a745a2d1e53e7484f588eee9f` |

CAPD's `capd-config` wrapper was installed, but this host lacks `pkg-config`.
The explicit compiler and linker command above is therefore the recorded build
interface.

## Validated API boundary checked in the pinned source

`capdDynSys/include/capd/diffAlgebra/SolutionCurve.h` specializes
`SolutionCurve<CurveT,true>` for intervals. Its `eval` locates the first and
last overlapping pieces, evaluates each on the intersecting time interval,
and applies `intervalHull`. Thus evaluation on `[0,1]` covers every saved
validated step, including intermediate times. The helper's positive-scale
check uses that full tube, not just the final state. `TimeMap_template.h`
appends the solver curve when advancing the same set with `stopAfterStep`.
These API facts support a domain enclosure; the actual numerical positivity
and C1 control results belong to the separate certificate result.
