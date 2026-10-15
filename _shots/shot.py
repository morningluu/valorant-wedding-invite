# 手机端截图 + 几何数据导出（本地预览用，不入库）
import json, pathlib
from playwright.sync_api import sync_playwright

url = pathlib.Path(r"C:/Users/Moringluu/valorant-wedding-invite/index.html").as_uri()
out = pathlib.Path(r"C:/Users/Moringluu/valorant-wedding-invite/_shots")

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, w, h in [("m390", 390, 844), ("s320", 320, 568)]:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        pg.goto(url)
        pg.wait_for_timeout(600)
        pg.screenshot(path=str(out / f"{name}-1-cover.png"))
        pg.click("#cover")
        pg.wait_for_timeout(1400)
        pg.screenshot(path=str(out / f"{name}-2-fold.png"))
        pg.screenshot(path=str(out / f"{name}-3-full.png"), full_page=True)
        geo = pg.eval_on_selector_all(".poster, .poster *", """
          els => els.map(e => {
            const r = e.getBoundingClientRect();
            const s = getComputedStyle(e);
            return {cls: e.className && String(e.className).split(" ")[0],
                    txt: (e.textContent||"").trim().slice(0,24),
                    x: Math.round(r.x), y: Math.round(r.y + scrollY),
                    w: Math.round(r.width), h: Math.round(r.height),
                    fs: s.fontSize, ta: s.textAlign};
          })
        """)
        (out / f"{name}-geo.json").write_text(json.dumps(geo, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{name}: saved, page_h={pg.evaluate('document.body.scrollHeight')}")
        pg.close()
    b.close()
print("DONE")
