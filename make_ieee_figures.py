"""Build the ImageGen-assisted, vector-annotated IEEE figure set."""

from __future__ import annotations

from figure_v3_common import MANIFEST, OUT, write_manifest
from figure_v3_overview import build_fig01, build_fig02, build_fig03
from figure_v3_architectures import (
    build_fig04,
    build_fig05,
    build_fig06,
    build_fig07,
    build_fig08,
)
from figure_v3_evidence import build_fig09, build_fig10, build_fig11


def main() -> None:
    MANIFEST.clear()
    for builder in (
        build_fig01,
        build_fig02,
        build_fig03,
        build_fig04,
        build_fig05,
        build_fig06,
        build_fig07,
        build_fig08,
        build_fig09,
        build_fig10,
        build_fig11,
    ):
        builder()
    write_manifest()
    print(f"Created {len(MANIFEST)} ImageGen-assisted IEEE figure plates in {OUT}")


if __name__ == "__main__":
    main()
