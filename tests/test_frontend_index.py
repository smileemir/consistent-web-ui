"""Tests for consistent-web-ui/scripts/frontend_index.py (standard library only).

Run from the repository root:  python3 -m unittest discover -s tests -v
"""
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "consistent-web-ui", "scripts", "frontend_index.py")
spec = importlib.util.spec_from_file_location("frontend_index", SCRIPT)
fi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fi)


class Fixture:
    def __init__(self):
        self.root = tempfile.mkdtemp(prefix="fi-")

    def add(self, rel, content=""):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        return self

    def scan(self):
        return fi.scan(os.path.realpath(self.root), 4000, [])

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)


def routes(result):
    return {r["route"] for r in result["routes"]["items"]}


def by_file(result):
    return {r["file"]: r["route"] for r in result["routes"]["items"]}


class RouteDetection(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()

    def tearDown(self):
        self.fx.cleanup()

    def test_next_pages_router(self):
        (self.fx.add("package.json", json.dumps({"dependencies": {"next": "15.0.0", "react": "19"}}))
         .add("src/pages/index.tsx").add("src/pages/products.tsx").add("src/pages/product/[id].tsx")
         .add("src/pages/checkout/success.tsx").add("src/pages/_app.tsx").add("src/pages/404.tsx")
         .add("src/pages/api/orders.ts").add("src/components/Button.js"))
        r = self.fx.scan()
        self.assertEqual(routes(r), {"/", "/products", "/product/[id]", "/checkout/success"})
        self.assertIn("next", r["detected"]["frameworks"])
        self.assertTrue(any(s["file"] == "src/pages/_app.tsx" for s in r["shells"]))
        self.assertTrue(any(s["file"] == "src/pages/404.tsx" for s in r["states"]))
        self.assertNotIn("src/pages/api/orders.ts", by_file(r))

    def test_next_app_router_groups_slots_and_states(self):
        (self.fx.add("app/page.tsx").add("app/layout.tsx").add("app/not-found.tsx")
         .add("app/(shop)/products/[id]/page.tsx").add("app/@modal/login/page.tsx")
         .add("app/api/orders/route.ts").add("app/[locale]/about/page.tsx"))
        r = self.fx.scan()
        self.assertEqual(routes(r), {"/", "/products/[id]", "/login", "/[locale]/about"})
        self.assertTrue(r["i18n_route_param"])
        self.assertTrue(any(s["source"] == "next-app not-found" for s in r["states"]))

    def test_nuxt_and_astro(self):
        self.fx.add("package.json", json.dumps({"dependencies": {"nuxt": "^3"}}))
        self.fx.add("pages/index.vue").add("pages/cart.vue").add("pages/product/[slug].vue")
        self.fx.add("site/src/pages/about.astro").add("site/src/pages/_draft.astro")
        r = self.fx.scan()
        self.assertTrue({"/", "/cart", "/product/[slug]", "/about"} <= routes(r))
        self.assertIn("nuxt", r["detected"]["frameworks"])

    def test_astro_underscore_files_are_not_routes(self):
        self.fx.add("src/pages/index.astro").add("src/pages/_draft.astro").add("src/pages/_parts/x.astro")
        self.assertEqual(routes(self.fx.scan()), {"/"})

    def test_sveltekit(self):
        (self.fx.add("src/routes/+page.svelte").add("src/routes/+layout.svelte")
         .add("src/routes/+error.svelte").add("src/routes/(shop)/cart/+page.svelte")
         .add("src/routes/cart/+page.server.ts").add("src/routes/api/+server.ts"))
        r = self.fx.scan()
        self.assertEqual(routes(r), {"/", "/cart"})
        self.assertTrue(any(s["source"] == "sveltekit error" for s in r["states"]))

    def test_remix_flat_routes(self):
        (self.fx.add("package.json", json.dumps({"dependencies": {"@remix-run/react": "2"}}))
         .add("app/routes/_index.tsx").add("app/routes/products.$id.tsx").add("app/routes/_auth.tsx")
         .add("app/routes/_auth.login.tsx").add("app/routes/dashboard/route.tsx")
         .add("app/routes/dashboard/Card.tsx").add("app/root.tsx"))
        r = self.fx.scan()
        self.assertEqual(routes(r), {"/", "/products/:id", "/login", "/dashboard"})
        self.assertTrue(any(s["file"] == "app/routes/_auth.tsx" for s in r["shells"]))

    def test_router_config_in_plain_js(self):
        (self.fx.add("src/App.js", 'import {createBrowserRouter} from "react-router-dom";\n'
                     'const r = createBrowserRouter([{path: "/", element: null}, {path: "/cart"},'
                     ' {path: "/product/:id"}, {path: "*"}]);')
         .add("src/Routes.jsx", '<Routes><Route path="/checkout" element={<C/>}/></Routes>')
         .add("src/config.js", 'export default { path: "/tmp/cache" }'))
        r = self.fx.scan()
        self.assertEqual(routes(r), {"/", "/cart", "/product/:id", "/checkout"})
        self.assertTrue(any(s["route"] == "*" for s in r["states"]))

    def test_shopify_theme(self):
        (self.fx.add("layout/theme.liquid").add("templates/product.json").add("templates/product.alt.json")
         .add("templates/customers/account.json").add("templates/404.json")
         .add("sections/header.liquid").add("snippets/card.liquid"))
        r = self.fx.scan()
        self.assertIn("shopify-theme", r["detected"]["platforms"])
        self.assertEqual(routes(r), {"/products/{handle}", "/products/{handle} [alt]", "/account", "(not found)"})

    def test_wordpress_and_woocommerce(self):
        (self.fx.add("style.css", "/*\nTheme Name: Demo\n*/\nbody{color:#111}")
         .add("functions.php").add("index.php").add("front-page.php").add("single.php").add("page-about.php")
         .add("header.php").add("woocommerce/single-product.php").add("woocommerce/cart/cart.php")
         .add("woocommerce/loop/price.php")
         .add("page-templates/landing.php", "<?php /* Template Name: Landing */ ?>"))
        r = self.fx.scan()
        found = routes(r)
        self.assertTrue({"(index)", "(front-page)", "(single)", "(page-about)", "(product page)", "(cart)",
                         "(template: Landing)"} <= found)
        self.assertNotIn("woocommerce/loop/price.php", by_file(r))
        self.assertTrue(any(s["file"] == "header.php" for s in r["shells"]))

    def test_server_views(self):
        (self.fx.add("app/views/products/show.html.erb").add("app/views/products/_card.html.erb")
         .add("app/views/layouts/application.html.erb")
         .add("resources/views/shop/index.blade.php").add("resources/views/components/btn.blade.php")
         .add("Pages/Index.cshtml").add("Pages/Cart.cshtml").add("Pages/_ViewStart.cshtml"))
        found = routes(self.fx.scan())
        self.assertTrue({"products#show", "view:shop.index", "/", "/Cart"} <= found)
        self.assertFalse(any("_card" in x or "btn" in x for x in found))

    def test_plain_html_skips_partials(self):
        self.fx.add("index.html").add("about/index.html").add("partials/footer.html").add("404.html")
        r = self.fx.scan()
        self.assertEqual(routes(r), {"/", "/about"})
        self.assertTrue(any(s["file"] == "404.html" for s in r["states"]))


class ScanBoundaries(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()

    def tearDown(self):
        self.fx.cleanup()

    def test_generated_vendor_backend_and_hidden_folders_are_not_entered(self):
        for folder in ("node_modules/x", "dist", ".next", ".git", "server", "api", "vendor"):
            self.fx.add(folder + "/a.css", "a{color:#123456}")
        self.fx.add("src/app.css", "a{color:#abcdef}")
        r = self.fx.scan()
        self.assertEqual(r["analyzed_files"], 1)
        self.assertEqual(r["colors"]["raw_hex"], 1)

    def test_symlink_outside_root_is_ignored(self):
        outside = tempfile.mkdtemp(prefix="outside-")
        try:
            with open(os.path.join(outside, "secret.css"), "w") as handle:
                handle.write("a{color:#000}")
            os.symlink(os.path.join(outside, "secret.css"), os.path.join(self.fx.root, "link.css"))
            self.fx.add("ok.css", "a{color:#fff}")
            self.assertEqual(self.fx.scan()["analyzed_files"], 1)
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    def test_min_test_and_story_files_are_skipped(self):
        self.fx.add("a.min.css").add("b.test.tsx").add("c.stories.tsx").add("d.d.ts").add("e.tsx")
        self.assertEqual(self.fx.scan()["analyzed_files"], 1)

    def test_text_output_and_cli(self):
        self.fx.add("index.html", "<p style='color:#f00'>x</p>")
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            fi.main(["--root", self.fx.root])
        text = buffer.getvalue()
        self.assertIn("Routes: 1", text)
        self.assertIn("Inline styles: 1", text)
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            fi.main(["--root", self.fx.root, "--json"])
        self.assertEqual(json.loads(buffer.getvalue())["routes"]["count"], 1)


class TokensColoursValues(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()

    def tearDown(self):
        self.fx.cleanup()

    def test_token_definitions_usage_and_gaps(self):
        (self.fx.add("styles/theme.css", ":root{--color-bg:#ffffff;--color-fg:#111111;--space-2:8px;--unused:1px}"
                     "[data-theme=dark]{--color-bg:#0b0b0b}")
         .add("styles/other.css", ":root{--color-bg:#fafafa}")
         .add("components/card.css", ".card{background:var(--color-bg);color:var(--color-fg);"
                                     "border-color:var(--color-border);outline-color:var(--ring, #00f)}")
         .add("components/Card.jsx", "el.style.setProperty('--card-w', '10px'); x = s.getPropertyValue('--space-2');"
                                     "<div style={{'--accent':'red'}} className='a'/>"))
        t = self.fx.scan()["tokens"]
        self.assertEqual([x[0] for x in t["undefined_without_fallback"]], ["--color-border"])
        self.assertEqual(t["undefined_with_fallback_count"], 1)
        self.assertIn("--unused", t["possibly_unused"])
        self.assertNotIn("--space-2", t["possibly_unused"])  # read from JS
        self.assertIn(["--color-bg", 2], t["defined_in_several_files"])
        self.assertTrue(all(x[0] not in ("--card-w", "--accent") for x in t["undefined_without_fallback"]))

    def test_tailwind_v4_theme_tokens_and_namespaces(self):
        (self.fx.add("package.json", json.dumps({"devDependencies": {"tailwindcss": "^4.1.0"}}))
         .add("app.css", '@import "tailwindcss";\n@theme { --color-brand: #0a66c2; --font-display: Inter; }')
         .add("Page.tsx", "<div className='bg-brand p-[13px] text-[#333] animate-pulse'"
                          " style={{color:'var(--color-red-500)'}}/>"))
        r = self.fx.scan()
        self.assertIn("tailwind-v4", r["detected"]["styling"])
        self.assertEqual(r["tokens"]["possibly_unused"], [])
        self.assertEqual(r["tokens"]["undefined_without_fallback"], [])
        self.assertEqual(r["utility_arbitrary_values"]["count"], 2)
        self.assertEqual(r["motion"]["looping_animation_files"], [["Page.tsx", 1]])
        self.assertTrue(r["theme_sources"][0]["file"] == "app.css")

    def test_colour_literals_skip_anchors_selectors_and_token_definitions(self):
        (self.fx.add("index.html", '<a href="#add">x</a><a href="#cafe">y</a>'
                                   '<style>#faded{color:#fff} .x{border:1px solid #CCC}</style>')
         .add("theme.scss", "$brand: #ff0000;\n$muted: #777777;\n$line: #e5e5e5;\n.btn{color:#333}")
         .add("tailwind.config.js", "module.exports={theme:{colors:{brand:'#123456'}}}"))
        c = self.fx.scan()["colors"]
        self.assertEqual(c["raw_hex"], 3)  # #fff, #CCC, #333
        self.assertEqual(c["in_token_or_theme_definitions"], 4)
        self.assertIn(["#cccccc", 1], c["most_used_raw_hex"])

    def test_near_duplicate_colours(self):
        self.fx.add("a.css", ".a{color:#1f2937}.b{color:#1e293b}.c{color:#ff0000}")
        near = self.fx.scan()["colors"]["near_duplicate_raw_hex"]
        self.assertEqual(near, [["#1f2937", "#1e293b"]])

    def test_value_census(self):
        (self.fx.add("a.css", ".a{margin:16px 12px;padding:var(--space-2);gap:13px;z-index:9999;"
                              "font-size:clamp(1rem,2vw,2rem);transition:opacity .3s ease, transform 200ms}"
                              ".b{z-index:10;animation:spin 1s infinite linear;will-change:transform}"
                              "@media (prefers-reduced-motion: reduce){.b{animation:none}}")
         .add("B.jsx", "<div style={{marginTop: 12, zIndex: 50, fontSize: '14px'}}/>"))
        r = self.fx.scan()
        spacing = r["values"]["spacing"]
        self.assertEqual(spacing["declarations"], 4)
        self.assertEqual(spacing["tokenized"], 1)
        self.assertEqual(dict(spacing["top_raw_values"]), {"12px": 2, "16px": 1, "13px": 1})
        self.assertEqual(dict(r["values"]["z-index"]["top_raw_values"]), {"9999": 1, "10": 1, "50": 1})
        durations = dict(r["values"]["duration"]["top_raw_values"])
        self.assertEqual(durations, {"300ms": 1, "200ms": 1, "1000ms": 1})
        self.assertEqual(dict(r["values"]["font-size"]["top_raw_values"]), {"clamp(...)": 1, "14px": 1})
        self.assertEqual(r["motion"]["looping_animation_files"], [["a.css", 1]])
        self.assertEqual(r["motion"]["will_change_files"], [["a.css", 1]])
        self.assertEqual(r["motion"]["reduced_motion_guards"], 1)

    def test_inline_style_values_stop_at_the_attribute_boundary(self):
        self.fx.add("index.html", '<h2 style="font-size:26px;margin:24px 0 13px">Hi</h2>'
                                  '<img width="220" height="160"><p>Only 3 left! 02:00:00</p>')
        values = self.fx.scan()["values"]
        self.assertEqual(dict(values["font-size"]["top_raw_values"]), {"26px": 1})
        self.assertEqual(dict(values["spacing"]["top_raw_values"]), {"24px": 1, "13px": 1})

    def test_platform_consumed_tokens_are_not_reported_unused(self):
        (self.fx.add("layout/theme.liquid", "<style>:root{--shopify-account-radius:4px;--own-unused:1px}</style>")
         .add("templates/index.json", "{}"))
        unused = self.fx.scan()["tokens"]["possibly_unused"]
        self.assertEqual(unused, ["--own-unused"])

    def test_tailwind_entry_is_a_theme_source_and_utility_motion_counts(self):
        (self.fx.add("app/globals.css", '@import "tailwindcss";')
         .add("app/page.tsx", "<div className='transition-opacity duration-300'/>"))
        r = self.fx.scan()
        self.assertEqual(r["theme_sources"][0]["file"], "app/globals.css")
        self.assertEqual(r["motion"]["files_with_motion"], 1)

    def test_locales_and_theme_modes(self):
        (self.fx.add("locales/en.json", "{}").add("locales/de-DE.json", "{}").add("locales/index.js")
         .add("a.css", "@media (prefers-color-scheme: dark){:root{--bg:#000}} .dark .x{color:var(--bg)}"))
        r = self.fx.scan()
        self.assertEqual(r["locales"], ["de-DE", "en"])
        self.assertEqual(r["theme_mode_signals"], {"prefers-color-scheme": 1, ".dark class": 1})


if __name__ == "__main__":
    unittest.main()
