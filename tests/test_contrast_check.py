"""Tests for consistent-web-ui/scripts/contrast_check.py (standard library only)."""
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "consistent-web-ui", "scripts", "contrast_check.py")
spec = importlib.util.spec_from_file_location("contrast_check", SCRIPT)
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)


def hexof(value, scheme="light"):
    color = cc.parse_color(value, scheme)
    return None if color is None else cc.to_hex(color)


def run(argv):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = cc.main(argv)
    return code, buffer.getvalue()


class Formula(unittest.TestCase):
    def ratio(self, a, b):
        return round(cc.contrast(cc.parse_color(a), cc.parse_color(b)), 2)

    def test_reference_ratios(self):
        self.assertEqual(self.ratio("#000", "#fff"), 21.0)
        self.assertEqual(self.ratio("#767676", "#ffffff"), 4.54)
        self.assertEqual(self.ratio("#777777", "#ffffff"), 4.48)
        self.assertEqual(self.ratio("#ff0000", "#ffffff"), 4.0)
        self.assertEqual(self.ratio("#ffffff", "#ffffff"), 1.0)


class Parsing(unittest.TestCase):
    def test_hex_named_and_transparent(self):
        self.assertEqual(hexof("#abc"), "#aabbcc")
        self.assertAlmostEqual(cc.parse_color("#aabbcc80")[3], 128 / 255)
        self.assertEqual(hexof("RebeccaPurple"), "#663399")
        self.assertEqual(cc.parse_color("transparent")[3], 0.0)
        self.assertIsNone(cc.parse_color("#abcde"))
        self.assertIsNone(cc.parse_color("currentColor"))

    def test_functional_notations(self):
        self.assertEqual(hexof("rgb(255, 0, 0)"), "#ff0000")
        self.assertEqual(hexof("rgb(100% 0% 0% / 50%)"), "#ff0000")
        self.assertEqual(hexof("hsl(222.2 47.4% 11.2%)"), "#0f172a")
        self.assertEqual(hexof("hsla(0, 100%, 50%, .5)"), "#ff0000")
        self.assertEqual(hexof("hwb(120 0% 0%)"), "#00ff00")
        self.assertEqual(hexof("oklch(21% 0.034 264.665)"), "#101828")
        self.assertEqual(hexof("oklch(54.6% 0.245 262.881)"), "#155dfc")
        self.assertEqual(hexof("oklab(0.628 0.2249 0.1258)"), "#ff0000")
        self.assertEqual(hexof("lab(54.29% 80.81 69.89)"), "#ff0000")
        self.assertEqual(hexof("lch(54.29% 106.84 40.85)"), "#ff0000")

    def test_light_dark_color_mix_and_bare_channels(self):
        self.assertEqual(hexof("light-dark(#fff, #000)"), "#ffffff")
        self.assertEqual(hexof("light-dark(#fff, #000)", "dark"), "#000000")
        self.assertEqual(hexof("color-mix(in srgb, #000 50%, #fff)"), "#808080")
        self.assertEqual(hexof("color-mix(in oklab, #ff0000, #0000ff)"), "#8c53a2")
        self.assertEqual(hexof("0 0% 100%"), "#ffffff")
        self.assertEqual(hexof("18, 18, 18"), "#121212")

    def test_var_substitution_with_fallback_and_cycles(self):
        tokens = {"--a": "var(--b)", "--b": "#123456", "--loop": "var(--loop)",
                  "--hsl": "222.2 47.4% 11.2%", "--wrapped": "hsl(var(--hsl))"}
        self.assertEqual(cc.substitute("var(--a)", tokens), "#123456")
        self.assertEqual(cc.substitute("var(--missing, #fff)", tokens), "#fff")
        self.assertIsNone(cc.substitute("var(--loop)", tokens))
        self.assertIsNone(cc.substitute("var(--missing)", tokens))
        self.assertEqual(hexof(cc.substitute("var(--wrapped)", tokens)), "#0f172a")


CSS = """
@custom-variant dark (&:is(.dark *));
:root { --bg: #ffffff; --fg: #111111; --muted: #777777; --brand: #0a66c2; --on-brand: #ffffff;
        --overlay: rgba(0, 0, 0, .5); }
@theme inline { --color-bg: var(--bg); }
[data-theme="dark"] { --bg: #0b0b0b; --fg: #f5f5f5; --muted: #8a8a8a; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #101010; --fg: #eeeeee; } }
@media (min-width: 900px) { :root { --bg: #ff00ff; } }
.card { --bg: #00ff00; }
.dark { --bg: #000000; --fg: #ffffff; }
"""


class Themes(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="cc-")
        self.css = os.path.join(self.dir, "theme.css")
        with open(self.css, "w") as handle:
            handle.write(CSS)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_theme_detection_ignores_component_and_breakpoint_scopes(self):
        themes, raw, _ = cc.load_themes([self.css])
        self.assertEqual(set(themes), {"base", "dark", "dark (system)"})
        self.assertEqual(themes["base"]["--bg"], "#ffffff")
        self.assertEqual(themes["dark"]["--bg"], "#000000")  # .dark declared last wins over [data-theme]
        self.assertEqual(themes["dark (system)"]["--bg"], "#101010")
        self.assertEqual(themes["base"]["--color-bg"], "var(--bg)")
        self.assertEqual(themes["dark"]["--brand"], "#0a66c2")  # inherited from base

    def test_pairs_file_large_text_and_exit_codes(self):
        pairs = os.path.join(self.dir, "pairs.json")
        with open(pairs, "w") as handle:
            json.dump({"pairs": [{"fg": "--fg", "bg": "--bg", "use": "body"},
                                 {"fg": "--muted", "bg": "--bg", "use": "large muted", "large": True},
                                 {"fg": "--on-brand", "bg": "--brand", "use": "button"}]}, handle)
        code, out = run(["--css", self.css, "--pairs", pairs, "--theme", "base"])
        self.assertEqual(code, 0, out)
        code, out = run(["--css", self.css, "--pairs", pairs, "--json"])
        data = json.loads(out)
        self.assertEqual(data["summary"]["FAIL"], 0)
        self.assertEqual(len(data["results"]), 9)

    def test_failure_unresolved_and_alpha(self):
        code, out = run(["--css", self.css, "--pair", "--muted", "--bg", "--theme", "base"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        code, out = run(["--css", self.css, "--pair", "--nope", "--bg", "--theme", "base"])
        self.assertEqual(code, 1)
        self.assertIn("UNRESOLVED", out)
        code, out = run(["--css", self.css, "--pair", "--overlay", "--bg", "--theme", "base", "--json"])
        row = json.loads(out)["results"][0]
        self.assertEqual(row["fg_hex"], "#808080")
        self.assertIn("foreground alpha composited", row["notes"])

    def test_token_names_with_or_without_dashes(self):
        code, out = run(["--css", self.css, "--pair", "--fg", "--bg", "--theme", "base"])
        self.assertEqual(code, 0, out)
        code, out = run(["--css", self.css, "--pair", "fg", "bg", "--theme", "base"])
        self.assertEqual(code, 0, out)
        self.assertEqual(run(["--pair", "#000"])[0], 2)

    def test_list_themes_and_literal_pairs(self):
        code, out = run(["--css", self.css, "--list-themes"])
        self.assertEqual(code, 0)
        self.assertIn("dark (system)", out)
        code, out = run(["--pair", "#767676", "white"])
        self.assertEqual(code, 0)
        self.assertIn("4.54:1", out)


class Suggestions(unittest.TestCase):
    def test_naming_conventions_and_alias_deduplication(self):
        tokens = {"--background": "#fff", "--foreground": "#000", "--card": "#fafafa",
                  "--card-foreground": "#111", "--color-card": "var(--card)",
                  "--color-card-foreground": "var(--card-foreground)", "--primary": "#0a66c2",
                  "--on-primary": "#fff", "--danger-bg": "#fee", "--danger-text": "#900"}
        pairs = {(p["fg"], p["bg"]) for p in cc.suggest_pairs(tokens)}
        self.assertIn(("--card-foreground", "--card"), pairs)
        self.assertIn(("--on-primary", "--primary"), pairs)
        self.assertIn(("--danger-text", "--danger-bg"), pairs)
        self.assertIn(("--foreground", "--background"), pairs)
        self.assertNotIn(("--color-card-foreground", "--color-card"), pairs)


if __name__ == "__main__":
    unittest.main()
