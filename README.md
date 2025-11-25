Quickbase Pipeline Slug Updater

A cross-platform, open-source tool for bulk-updating Quickbase Pipeline YAML files during realm migrations.
This utility reads exported Pipeline YAML, replaces old account slugs using a simple mapping file, and writes updated versions into a clean output directory.

Works on Windows, macOS, and Linux.
Requires Python 3.8+ and no external dependencies.

🚀 Features

🔄 Batch update hundreds of Pipeline YAML files at once

🔧 Simple mapping format — old_slug=new_slug

🖥️ Cross-platform (Windows, Mac, Linux)

📁 Keeps folder structure when rewriting updated YAML files

⚠️ Dry-run mode to preview changes

🧩 No third-party packages (standard library only)

📁 Project Structure
Yaml Slug Update/
  slug_map.env          ← old_slug=new_slug mappings
  Exported Yaml/        ← original pipeline YAML files
  Updated Yaml/         ← auto-generated updated YAML files
  Code/
    requirements.txt
    update_quickbase_slugs.py
    run_slug_update.py

🔧 Mapping File Format (slug_map.env)

A simple, platform-friendly text file:

# slug_map.env
# Format: old_slug=new_slug

jnG1ypk=NEWslug01
abc1234=NEWslug02
sampleOld=sampleNew


One mapping per line

Lines starting with # are comments

Whitespace is trimmed

No quotes, no CSV, no headers

📦 Installation
1. Install Python

Make sure Python 3.8+ is installed.

Windows: https://www.python.org/downloads/

macOS: brew install python or use system Python

Linux: Your package manager (Ubuntu: sudo apt install python3)

2. Install requirements

Even though the tool uses only built-in modules, this keeps the workflow standard:

cd "Yaml Slug Update/Code"
python -m pip install -r requirements.txt

▶️ Usage
Recommended: Use the one-command runner

From the Code/ directory:

Dry run (preview changes)
python run_slug_update.py --dry-run

Execute and write updated YAML files
python run_slug_update.py


This automatically uses:

../slug_map.env

../Exported Yaml/

../Updated Yaml/

Manual CLI (custom paths)

You can also call the core script directly:

python update_quickbase_slugs.py ../slug_map.env "../Exported Yaml" "../Updated Yaml"


Add --dry-run to preview changes.

🛠 How It Works

Loads all slug mappings from slug_map.env

Recursively scans the input folder (Exported Yaml) for .yaml / .yml files

Replaces any occurrence of:

quickbase[old_slug]


with:

quickbase[new_slug]


Writes updated files while preserving folder structure into Updated Yaml/

💡 Example

Before:

- TRIGGER quickbase[jnG1ypk] record on_update -> a:


After:

- TRIGGER quickbase[NEWslug01] record on_update -> a:

🧪 Future Enhancements (Planned)

Mapping for table IDs (e.g., <bqr9x7pve> → new IDs)

Automatic detection of slugs used in YAMLs

Web UI wrapper for non-technical users

Automated Quickbase API import/export integration

🤝 Contributing

Contributions are welcome!

Open an issue for bugs or enhancement ideas

Fork the repo and create a PR for code improvements

Keep code cross-platform and dependency-free whenever possible

📜 License

MIT License — free to use, modify, and distribute.
