"""Normalize raw SHL scrape output into data/catalog/catalog_clean.json."""

from pathlib import Path


RAW_INPUT = Path("data/catalog/catalog_raw.json")
CLEAN_OUTPUT = Path("data/catalog/catalog_clean.json")


def main() -> None:
    if not RAW_INPUT.exists():
        raise FileNotFoundError(f"Missing raw scrape file: {RAW_INPUT}")

    raise NotImplementedError("Add normalization and taxonomy enrichment logic.")


if __name__ == "__main__":
    main()

