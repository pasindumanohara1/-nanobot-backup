"""
Islamic Post Template Renderer
Usage:
  python render_template.py <template_number>     — Generate image from template
  python render_template.py all                   — Generate all 10 templates
  python render_template.py list                  — List available templates

Edit content in each template file (TITLE_TEXT, ARABIC_TEXT, MAIN_TEXT, etc.)
"""

import sys
import os
import importlib.util

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

TEMPLATE_FILES = {
    "1": ("template_01_classic.py", "Classic Elegance — Navy + Gold"),
    "2": ("template_02_dark_gold.py", "Dark Gold Luxury — Black + Gold"),
    "3": ("template_03_green_nature.py", "Green Nature — Green + Leaves"),
    "4": ("template_04_purple_elegance.py", "Purple Elegance — Purple + Crescent"),
    "5": ("template_05_teal_modern.py", "Teal Modern — Teal + Geometric"),
    "6": ("template_06_maroon_warmth.py", "Maroon Warmth — Maroon + Gold"),
    "7": ("template_07_sunrise.py", "Sunrise Gradient — Orange/Pink/Purple"),
    "8": ("template_08_minimalist_white.py", "Minimalist White — Clean + Teal"),
    "9": ("template_09_geometric_islamic.py", "Geometric Islamic — Stars + Emerald"),
    "10": ("template_10_calligraphy.py", "Calligraphy Style — Parchment + Gold"),
}


def load_and_run(template_file, output_path=None):
    """Load a template module and run its generate() function."""
    spec = importlib.util.spec_from_file_location("template", os.path.join(TEMPLATES_DIR, template_file))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.generate(output_path)


def main():
    if len(sys.argv) < 2 or sys.argv[1].lower() == "list":
        print("Available Templates:")
        print("=" * 55)
        for num, (fname, desc) in TEMPLATE_FILES.items():
            print("  {:>2}. {}".format(num, desc))
        print("\nUsage: python render_template.py <number|all>")
        return

    arg = sys.argv[1].lower()

    if arg == "all":
        print("Generating all 10 templates...\n")
        for num, (fname, desc) in TEMPLATE_FILES.items():
            try:
                path = load_and_run(fname)
                print("  [{}] {}".format(num, desc))
                print("       -> {}".format(path))
            except Exception as e:
                print("  [{}] ERROR: {}".format(num, e))
        print("\nDone! All images saved.")
    elif arg in TEMPLATES_DIR or arg.isdigit() and arg in TEMPLATE_FILES:
        num = arg if arg.isdigit() else None
        if num is None:
            # Try to match filename
            for n, (f, _) in TEMPLATE_FILES.items():
                if f == arg:
                    num = n
                    break
        if num and num in TEMPLATE_FILES:
            fname, desc = TEMPLATE_FILES[num]
            print("Rendering: {}".format(desc))
            path = load_and_run(fname)
            print("Saved: {}".format(path))
        else:
            print("Unknown template: {}".format(arg))
    else:
        print("Unknown argument: {}".format(arg))
        print("Use a number 1-10, 'all', or 'list'")


if __name__ == "__main__":
    main()
