from html import escape
from pathlib import Path
import shutil
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
EXCLUDED_DIRS = {".git", ".github", ".vscode", "_site", "scripts"}
GENERATED_FILES = {"index.html", "menu.html", "index-example.html"}


def display_name(path: Path) -> str:
    name = path.stem.replace("_", " ").replace("-", " ")
    return " ".join(part.capitalize() for part in name.split())


def url_name(name: str) -> str:
    return quote(name, safe="")


def page_shell(title: str, body: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
    <style>
        :root {{ --ink: #17242b; --muted: #536b70; --paper: #f8fbf7; --cream: #e7f0ee; --sage: #a9d2c5; --tomato: #ef684f; --teal: #28666e; }}
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; min-height: 100vh; color: var(--ink); background: var(--cream); background-image: linear-gradient(rgba(40,102,110,.06) 1px, transparent 1px), linear-gradient(90deg, rgba(40,102,110,.06) 1px, transparent 1px); background-size: 42px 42px; font-family: Georgia, "Times New Roman", serif; }}
        body::before {{ content: ""; position: fixed; z-index: -1; width: 420px; height: 420px; top: -160px; right: -120px; border: 1px solid rgba(40,102,110,.24); border-radius: 50%; box-shadow: 0 0 0 26px rgba(40,102,110,.07), 0 0 0 52px rgba(40,102,110,.04); }}
        main {{ width: min(1080px, calc(100% - 36px)); margin: auto; padding: 68px 0; }}
        .eyebrow {{ color: var(--teal); font: bold 11px Arial, sans-serif; letter-spacing: .18em; text-transform: uppercase; }}
        h1 {{ margin: 12px 0 10px; font-size: clamp(3rem, 8vw, 6.5rem); line-height: .88; letter-spacing: -.06em; font-weight: 500; }}
        .intro {{ max-width: 560px; color: var(--muted); line-height: 1.6; }}
        .menu {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin: 42px 0 30px; }}
        .item {{ display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 20px; color: var(--ink); background: var(--paper); border-left: 4px solid var(--sage); text-decoration: none; box-shadow: 0 8px 22px rgba(23,36,43,.1); transition: transform .2s, border-color .2s, box-shadow .2s; }}
        .item:hover {{ transform: translateY(-4px); border-color: var(--tomato); box-shadow: 0 15px 30px rgba(23,36,43,.18); }}
        .item strong {{ font-size: 1.1rem; font-weight: 500; }}
        .item span {{ color: var(--tomato); font: 21px Arial, sans-serif; }}
        .back {{ color: var(--muted); font: bold 12px Arial, sans-serif; letter-spacing: .08em; text-decoration: none; text-transform: uppercase; }}
        .back:hover {{ color: var(--tomato); }}
        @media (max-width: 600px) {{ main {{ padding: 48px 0; }} .menu {{ grid-template-columns: 1fr; margin-top: 32px; }} }}
    </style>
</head>
<body><main>{body}</main></body>
</html>'''


def folder_menu(folder: Path, html_files: list[Path]) -> None:
    links = []
    for source in html_files:
        target = source.name
        if source.name.lower() == "index.html":
            target = "index-example.html"
        links.append(
            f'<a class="item" href="{escape(url_name(target))}">'
            f'<strong>{escape(display_name(source))}</strong><span>&rarr;</span></a>'
        )
    body = (
        '<div class="eyebrow">Training collection</div>'
        f'<h1>{escape(display_name(folder))}</h1>'
        '<p class="intro">Explore the HTML exercises in this folder.</p>'
        f'<nav class="menu" aria-label="{escape(display_name(folder))} files">'
        + "".join(links)
        + '</nav><a class="back" href="../index.html">&larr; Back to Main Menu</a>'
    )
    output_folder = SITE / folder.name
    output_folder.mkdir(parents=True, exist_ok=True)
    generated_menu = page_shell(
        f"{display_name(folder)} | Training Menu", body)
    for output_name in ("index.html", "menu.html"):
        (output_folder / output_name).write_text(generated_menu, encoding="utf-8")


def root_menu(folders: list[Path]) -> None:
    links = []
    for folder in folders:
        links.append(
            f'<a class="item" href="{escape(url_name(folder.name))}/menu.html">'
            f'<strong>{escape(display_name(folder))}</strong><span>&rarr;</span></a>'
        )
    body = (
        '<div class="eyebrow">NG 5.4 GCET / Training archive</div>'
        '<h1>Learn by building.</h1>'
        '<p class="intro">Browse every training folder and HTML exercise from one responsive explorer.</p>'
        '<nav class="menu" aria-label="Training folders">'
        + "".join(links)
        + "</nav>"
    )
    (SITE / "index.html").write_text(
        page_shell("NG 5.4 GCET | Training Explorer", body), encoding="utf-8"
    )


def main() -> None:
    if SITE.exists():
        if SITE.is_dir():
            shutil.rmtree(SITE)
        else:
            SITE.unlink()
    SITE.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT, SITE, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(*EXCLUDED_DIRS))

    folders = sorted(
        path for path in ROOT.iterdir()
        if path.is_dir() and not path.name.startswith(".") and path.name not in EXCLUDED_DIRS
    )
    for folder in folders:
        output_folder = SITE / folder.name
        source_index = folder / "index.html"
        if source_index.is_file():
            shutil.copy2(source_index, output_folder / "index-example.html")
        html_files = sorted(
            path for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() == ".html" and path.name.lower() not in GENERATED_FILES
        )
        folder_menu(folder, html_files)
    root_menu(folders)
    print(f"Generated {_site_summary(folders)}")


def _site_summary(folders: list[Path]) -> str:
    return f"site for {len(folders)} folder(s) at {SITE}"


if __name__ == "__main__":
    main()
