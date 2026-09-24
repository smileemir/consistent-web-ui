"""The shipped templates must be valid inputs for the shipped tools."""
import importlib.util
import io
import os
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, "..", "consistent-web-ui")


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SKILL, "scripts", name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Templates(unittest.TestCase):
    def test_template_theme_passes_template_pairs_in_every_theme(self):
        cc = load("contrast_check")
        templates = os.path.join(SKILL, "assets", "templates")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = cc.main(["--css", os.path.join(templates, "theme-tokens.css"),
                            "--pairs", os.path.join(templates, "contrast-pairs.json")])
        self.assertEqual(code, 0, buffer.getvalue())
        themes, _, _ = cc.load_themes([os.path.join(templates, "theme-tokens.css")])
        self.assertEqual(set(themes), {"base", "dark", "dark (system)"})
        self.assertEqual(themes["dark"], themes["dark (system)"], "dark blocks drifted apart")

    def test_inventory_flags_template_placeholders(self):
        fi = load("frontend_index")
        result = fi.scan(os.path.realpath(os.path.join(SKILL, "assets", "templates")), 100, [])
        reasons = " ".join(" ".join(s["reasons"]) for s in result["theme_sources"])
        self.assertIn("unfinished TODO(brand) values", reasons)

    def test_layer_scale_is_strictly_ordered(self):
        import re
        with open(os.path.join(SKILL, "assets", "templates", "theme-tokens.css"), encoding="utf-8") as handle:
            css = handle.read()
        order = ["base", "raised", "sticky", "dropdown", "drawer", "modal", "toast", "tooltip"]
        values = [int(re.search(r"--layer-%s:\s*(\d+)" % name, css).group(1)) for name in order]
        self.assertEqual(values, sorted(values))
        self.assertEqual(len(set(values)), len(values))

    def test_info_toggletip_markup_follows_the_help_rules(self):
        from html.parser import HTMLParser

        class Walker(HTMLParser):
            def __init__(self):
                super().__init__()
                self.stack, self.buttons, self.panels, self.order, self.titles = [], [], {}, [], 0
                self.hidden_text, self._in_hidden, self._current = {}, False, None

            def handle_starttag(self, tag, attrs):
                a = dict(attrs)
                if "title" in a:
                    self.titles += 1
                classes = (a.get("class") or "").split()
                if tag == "button" and "info__button" in classes:
                    self.buttons.append({"attrs": a, "in_label": "label" in self.stack})
                    self._current = a.get("popovertarget")
                    self.order.append(("button", a.get("popovertarget")))
                if "info__panel" in classes:
                    self.panels[a.get("id")] = a
                    self.order.append(("panel", a.get("id")))
                if "visually-hidden" in classes and self._current:
                    self._in_hidden = True
                if tag not in ("path", "circle", "svg", "input", "meta", "link", "br"):
                    self.stack.append(tag)

            def handle_endtag(self, tag):
                if tag in self.stack:
                    while self.stack and self.stack.pop() != tag:
                        pass
                if tag == "button":
                    self._current = None
                if tag == "span":
                    self._in_hidden = False

            def handle_data(self, data):
                if self._in_hidden and self._current:
                    self.hidden_text[self._current] = self.hidden_text.get(self._current, "") + data

        path = os.path.join(SKILL, "assets", "templates", "info-toggletip.html")
        with open(path, encoding="utf-8") as handle:
            html = handle.read()
        body = html.split("<body>", 1)[1]
        walker = Walker()
        walker.feed(body)
        self.assertGreaterEqual(len(walker.buttons), 3)
        for button in walker.buttons:
            target = button["attrs"].get("popovertarget")
            self.assertEqual(button["attrs"].get("type"), "button")
            self.assertIn(target, walker.panels, "button points to a missing panel")
            self.assertIn("popover", walker.panels[target])
            self.assertFalse(button["in_label"], "an (i) must never sit inside a label")
            self.assertTrue(walker.hidden_text.get(target, "").strip().startswith("About "))
        for index, (kind, ref) in enumerate(walker.order):
            if kind == "button":
                self.assertEqual(walker.order[index + 1], ("panel", ref), "the panel must follow its button")
        self.assertEqual(walker.titles, 0, "help never lives in a title attribute")
        self.assertIn("beforetoggle", html)

    def read_template(self, name):
        with open(os.path.join(SKILL, "assets", "templates", name), encoding="utf-8") as handle:
            return handle.read()

    def test_dialog_template_locks_the_page_and_sizes_to_content(self):
        import re
        html = self.read_template("dialog.html")
        for needle in ("html.is-scroll-locked { overflow: hidden; }", "overscroll-behavior: contain",
                       "showModal()", "returnFocusTo", "data-dialog-persistent", "prefers-reduced-motion"):
            self.assertIn(needle, html)
        self.assertRegex(html, r"\.dialog__media \{[^}]*max-block-size: \d+vh")
        body = html.split("<body>", 1)[1]
        for dialog in re.findall(r"<dialog[^>]*>", body):
            labelled = re.search(r'aria-labelledby="([^"]+)"', dialog)
            self.assertIsNotNone(labelled, dialog)
            self.assertRegex(body, r'id="%s" tabindex="-1"' % re.escape(labelled.group(1)))
        for close in re.findall(r'<button[^>]*class="dialog__close"[^>]*>', body):
            self.assertIn('aria-label="', close)
        self.assertRegex(html, r"\.dialog__close \{[^}]*inline-size: 36px")

    def test_toast_template_follows_the_notification_rules(self):
        html = self.read_template("toast.html")
        for needle in ('"alert" : "status"', "MAX_VISIBLE = 3", "error: 0", "pointer-events: none",
                       ":modal", "pointerenter", "focusin", "prefers-reduced-motion", "var(--layer-toast"):
            self.assertIn(needle, html)

    def test_controls_share_one_height(self):
        css = self.read_template("controls.html").split("/* ===== Form controls and buttons: copy from here ===== */", 1)[1]
        css = css.split("/* ===== Form controls and buttons: copy until here ===== */", 1)[0]
        for selector in (".control {", ".segmented {", ".btn {"):
            block = css.split(selector, 1)[1].split("}", 1)[0]
            self.assertIn("var(--control-height", block, selector)
        self.assertIn("@supports (appearance: base-select)", css)
        self.assertIn("--control-height: 40px;", self.read_template("theme-tokens.css"))

    def test_ui_check_script_is_valid(self):
        import shutil
        import subprocess
        path = os.path.join(SKILL, "scripts", "ui_check.js")
        with open(path, encoding="utf-8") as handle:
            source = handle.read()
        self.assertIn("window.uiCheck = function uiCheck()", source)
        for check in ("controls-height", "modal-scroll-lock", "modal-click-through", "overlay-opaque",
                      "modal-actions", "close-size", "sticky-opaque"):
            self.assertIn(check, source)
        node = shutil.which("node")
        if node:
            subprocess.run([node, "--check", path], check=True)

    def test_design_contract_ids_are_unique(self):
        import re
        with open(os.path.join(SKILL, "assets", "templates", "design-contract.md"), encoding="utf-8") as handle:
            ids = re.findall(r"^\| (DC-\d+) \|", handle.read(), re.M)
        self.assertGreater(len(ids), 20)
        self.assertEqual(len(ids), len(set(ids)), "duplicate DC ids")


class Package(unittest.TestCase):
    ROOT = os.path.join(HERE, "..")

    def read(self, *parts):
        with open(os.path.join(self.ROOT, *parts), encoding="utf-8") as handle:
            return handle.read()

    def test_license_travels_with_the_skill_folder(self):
        self.assertEqual(self.read("LICENSE"), self.read("consistent-web-ui", "LICENSE.txt"),
                         "LICENSE and consistent-web-ui/LICENSE.txt must stay identical")

    def test_skill_version_matches_latest_changelog_entry(self):
        import re
        skill = self.read("consistent-web-ui", "SKILL.md")
        version = re.search(r'^\s+version:\s*"?([0-9.]+)"?\s*$', skill, re.M)
        latest = re.search(r"^## ([0-9]+\.[0-9]+\.[0-9]+)", self.read("CHANGELOG.md"), re.M)
        self.assertIsNotNone(version, "SKILL.md metadata has no version")
        self.assertEqual(version.group(1), latest.group(1))

    def test_marketplace_entry_matches_the_skill(self):
        import json
        import re
        market = json.loads(self.read(".claude-plugin", "marketplace.json"))
        entry = market["plugins"][0]
        version = re.search(r'^\s+version:\s*"?([0-9.]+)"?\s*$', self.read("consistent-web-ui", "SKILL.md"), re.M).group(1)
        self.assertEqual(entry["version"], version, "marketplace.json and SKILL.md versions differ")
        self.assertEqual(entry["skills"], ["./consistent-web-ui"])
        self.assertEqual(entry["name"], "consistent-web-ui")

    def test_relative_links_resolve(self):
        import re
        broken = []
        for folder in ("consistent-web-ui", "."):
            base = os.path.join(self.ROOT, folder)
            names = []
            if folder == ".":
                names = [n for n in os.listdir(base) if n.endswith(".md")]
                names += [os.path.join("evals", n) for n in os.listdir(os.path.join(base, "evals")) if n.endswith(".md")]
            else:
                for root, _, files in os.walk(base):
                    names += [os.path.relpath(os.path.join(root, n), base) for n in files if n.endswith(".md")]
            for name in names:
                path = os.path.join(base, name)
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
                for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
                    if "://" in target or target.startswith("mailto:"):
                        continue
                    if not os.path.exists(os.path.join(os.path.dirname(path), target)):
                        broken.append(f"{folder}/{name} -> {target}")
        self.assertEqual(broken, [])


if __name__ == "__main__":
    unittest.main()
