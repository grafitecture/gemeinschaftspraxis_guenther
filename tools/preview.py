import sys, os, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
async def main(files, out, width=1400):
    css = f"""@font-face{{font-family:'Fira Sans';src:url('file://{ROOT}/assets/fonts/fira-sans-Light.woff');font-weight:300}}
@font-face{{font-family:'Fira Sans';src:url('file://{ROOT}/assets/fonts/fira-sans-Regular.woff');font-weight:400}}
@font-face{{font-family:'Fira Sans';src:url('file://{ROOT}/assets/fonts/fira-sans-Medium.woff');font-weight:500}}
@font-face{{font-family:'Fira Sans';src:url('file://{ROOT}/assets/fonts/fira-sans-SemiBold.woff');font-weight:600}}
body{{margin:0;display:flex;flex-wrap:wrap;gap:16px;padding:16px;background:#ddd}} .c{{background:#fff;width:{int(sys.argv[3]) if len(sys.argv)>3 else 640}px}} svg{{display:block;width:100%;height:auto}}"""
    body = "".join(f'<div class="c">{open(os.path.join(ROOT,"assets/img",f)).read()}</div>' for f in files)
    html = f"<html><head><style>{css}</style></head><body>{body}</body></html>"
    p = os.path.join(ROOT, 'tools', '_prev.html'); open(p,'w').write(html)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width': width, 'height': 900})
        await pg.goto('file://' + p); await pg.wait_for_timeout(400)
        await pg.screenshot(path=out, full_page=True); await b.close()
asyncio.run(main(sys.argv[1].split(','), sys.argv[2]))
