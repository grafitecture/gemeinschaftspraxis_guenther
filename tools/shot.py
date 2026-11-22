import sys, asyncio, os
from playwright.async_api import async_playwright
async def main(url, out, w, h, full):
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type in ('error','warning') else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(url)
        if os.environ.get('SCROLL'):
            h = await pg.evaluate('document.body.scrollHeight')
            for y in range(0, h, 600):
                await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(60)
            await pg.evaluate('window.scrollTo(0,0)')
        await pg.wait_for_timeout(int(os.environ.get("WAIT","900")))
        await pg.screenshot(path=out, full_page=full)
        print('errors:', errs)
        await b.close()
url, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
asyncio.run(main(url, out, w, h, len(sys.argv) > 5))
