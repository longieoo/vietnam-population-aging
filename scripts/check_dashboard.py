"""Exercise the shipped offline dashboard in Chromium (desktop and mobile)."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def check(browser_executable=None, screenshots=None):
    with sync_playwright() as playwright:
        launch = {"headless": True}
        if browser_executable:
            launch["executable_path"] = browser_executable
        browser = playwright.chromium.launch(**launch)
        try:
            for width, height in [(1440, 1000), (390, 844)]:
                page = browser.new_page(viewport={"width": width, "height": height}, accept_downloads=True)
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto((ROOT / "outputs/interactive/explorer.html").as_uri())
                page.wait_for_function("document.getElementById('chart-a').data?.length > 0")
                for view in ["overview", "aging", "economy", "labor"]:
                    page.locator(f"#tab-{view}").click()
                    page.wait_for_function("document.getElementById('chart-a').data?.length > 0")
                    assert page.locator(f"#tab-{view}").get_attribute("aria-selected") == "true"
                    assert len(page.locator("#kpis .kpi").all()) == 4
                    assert page.locator("#source-body tr").count() > 0
                    if screenshots:
                        target = Path(screenshots)
                        target.mkdir(parents=True, exist_ok=True)
                        page.screenshot(path=str(target / f"{view}-{width}.png"), full_page=True)
                # Native tab navigation keeps one tab stop and updates the active panel.
                page.locator("#tab-labor").focus()
                page.keyboard.press("Home")
                assert page.locator("#tab-overview").get_attribute("aria-selected") == "true"
                page.keyboard.press("End")
                assert page.locator("#tab-labor").get_attribute("aria-selected") == "true"
                page.locator("#tab-economy").click()
                first = page.locator("#source-body tr").first.inner_text()
                page.locator("#source-next").click()
                assert "Trang 2" in page.locator("#source-page").inner_text()
                assert page.locator("#source-body tr").first.inner_text() != first
                page.locator("#source-prev").click()
                assert page.locator("#source-body tr").first.inner_text() == first
                with page.expect_download() as info:
                    page.locator('[data-export="a"]').click()
                download = info.value
                assert download.suggested_filename.endswith(".csv")
                csv_text = Path(download.path()).read_text("utf-8-sig")
                assert len(csv_text.splitlines()) == 198  # 197 complete GDP-age pairs + header
                # An invalid rate interval is explicitly empty, not an invented zero rate.
                page.locator("#tab-aging").click()
                page.locator("#year").evaluate("element => element.value = 1991")
                page.locator("#year").dispatch_event("input")
                page.wait_for_function("document.getElementById('chart-b').layout?.annotations?.[0]?.text.includes('Không có dữ liệu')")
                assert page.locator("#source-prev").is_disabled()
                page.locator("#reset").click()
                assert page.locator("#year").input_value() == "2023"
                assert page.locator("#country").input_value() == "VNM"
                page.select_option("#region", index=1)
                assert "năm 2023" in page.locator("#scope").inner_text()
                page.select_option("#country", "JPN")
                assert "Nhật Bản" in page.locator("#scope").inner_text()
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"), "Page overflows viewport"
                assert not errors, errors
                page.close()
                print(f"Dashboard browser checks passed: {width}x{height}")
        finally:
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser-executable", type=str)
    parser.add_argument("--screenshots", type=Path)
    args = parser.parse_args()
    check(args.browser_executable, args.screenshots)

