import argparse
import re
from pathlib import Path


def load_slug_map(mapping_path: Path) -> dict:
    """
    Load old->new slug mappings from a simple KEY=VALUE text file.

    Expected format:
        # slug_map.env
        # old_slug=new_slug
        jnG1ypk=NEWslug01
        abc1234=NEWslug02
    """
    slug_map: dict[str, str] = {}

    for raw_line in mapping_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise ValueError(f"Invalid mapping line (no '='): {raw_line!r}")

        old_slug, new_slug = line.split("=", 1)
        old_slug = old_slug.strip()
        new_slug = new_slug.strip()

        if not old_slug or not new_slug:
            raise ValueError(f"Empty slug in line: {raw_line!r}")

        slug_map[old_slug] = new_slug

    if not slug_map:
        raise ValueError("No slug mappings loaded. Check your mapping file.")
    return slug_map


def process_file(path: Path, slug_map: dict[str, str]) -> tuple[str, int]:
    """
    Read a YAML file, replace all quickbase[old_slug] with quickbase[new_slug]
    according to slug_map, and return (new_text, total_replacements).
    """
    text = path.read_text(encoding="utf-8")
    total_replacements = 0

    for old_slug, new_slug in slug_map.items():
        pattern = re.compile(rf"quickbase\[{re.escape(old_slug)}\]")
        replacement = f"quickbase[{new_slug}]"
        text, count = pattern.subn(replacement, text)
        total_replacements += count

    return text, total_replacements


def update_directory(
    mapping_file: Path, input_dir: Path, output_dir: Path, dry_run: bool = False
) -> None:
    if not mapping_file.is_file():
        raise SystemExit(f"Mapping file not found: {mapping_file}")

    if not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Using mapping file: {mapping_file}")
    print(f"Input directory:   {input_dir}")
    print(f"Output directory:  {output_dir}")
    print(f"Dry run:           {dry_run}")
    print("-" * 60)

    slug_map = load_slug_map(mapping_file)
    print(f"Loaded {len(slug_map)} slug mappings.")
    total_files = 0
    total_replacements = 0

    yaml_extensions = {".yaml", ".yml"}

    for path in sorted(input_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in yaml_extensions:
            total_files += 1
            new_text, replacements = process_file(path, slug_map)
            total_replacements += replacements

            rel_path = path.relative_to(input_dir)
            out_path = output_dir / rel_path
            out_path.parent.mkdir(parents=True, exist_ok=True)

            if dry_run:
                print(f"[DRY RUN] {rel_path} -> {replacements} replacements")
            else:
                out_path.write_text(new_text, encoding="utf-8")
                print(f"Updated {rel_path} ({replacements} replacements)")

    print(
        f"\nProcessed {total_files} file(s), {total_replacements} total replacement(s)."
    )
    if dry_run:
        print("Dry run complete. No files were written.")


def cli():
    """
    CLI entry point.

    Defaults (based on this file's location):

        repo_root/
          slug_map.env
          Exported Yaml/
          Updated Yaml/
          Code/
            update_quickbase_slugs.py  ← this file
    """
    code_dir = Path(__file__).resolve().parent
    repo_root = code_dir.parent

    default_mapping = repo_root / "slug_map.env"
    default_input = repo_root / "Exported Yaml"
    default_output = repo_root / "Updated Yaml"

    parser = argparse.ArgumentParser(
        description="Update Quickbase account slugs in Pipeline YAML files."
    )
    parser.add_argument(
        "--mapping-file",
        type=Path,
        default=None,
        help=f"Mapping file (default: {default_mapping})",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=None,
        help=f"Input directory with original YAML (default: {default_input})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=f"Output directory for updated YAML (default: {default_output})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write files, just print what would change.",
    )

    args = parser.parse_args()

    mapping_file = args.mapping_file or default_mapping
    input_dir = args.input_dir or default_input
    output_dir = args.output_dir or default_output

    update_directory(mapping_file, input_dir, output_dir, args.dry_run)


if __name__ == "__main__":
    cli()
