"""유어데이 샘플 의류 일러스트를 생성한다 (실제 상품 사진이 아님)."""
from pathlib import Path
import cairosvg
root = Path(__file__).resolve().parent.parent / 'theme/yourday/assets'
shapes = {
'knit': '<path d="M215 180 L160 200 80 340 145 380 190 300 180 610 Q300 640 420 610 L410 300 455 380 520 340 440 200 385 180 Q360 235 300 235 Q240 235 215 180Z"/><path d="M218 182 Q232 255 300 255 Q368 255 382 182 M185 580 Q300 604 415 580 M190 594 Q300 618 410 594" class="seam"/>',
'cardigan':'<path d="M230 165 L165 195 95 520 165 540 202 315 190 620 Q300 640 410 620 L398 315 435 540 505 520 435 195 370 165 300 290Z"/><path class="seam" d="M230 165 300 290 300 630 M370 165 300 290 M210 460 265 460 265 515 210 515 M335 460 390 460 390 515 335 515"/><g fill="#837c6b"><circle cx="300" cy="355" r="5"/><circle cx="300" cy="415" r="5"/><circle cx="300" cy="475" r="5"/><circle cx="300" cy="535" r="5"/></g>',
'blazer':'<path d="M230 155 160 185 90 570 160 585 205 325 192 640 408 640 395 325 440 585 510 570 440 185 370 155 300 275Z"/><path class="seam" d="M230 155 207 255 260 275 240 310 300 390 300 640 M370 155 393 255 340 275 360 310 300 390 M215 480 265 480 M335 480 385 480"/><circle fill="#605a4e" cx="300" cy="470" r="7"/>',
'shirt':'<path d="M240 165 170 195 80 510 150 535 205 315 195 615 Q300 650 405 615 L395 315 450 535 520 510 430 195 360 165 300 205Z"/><path class="seam" d="M240 165 270 240 300 205 330 240 360 165 M300 210 300 632 M340 300 390 300 390 355 340 355Z M90 480 158 506 M442 506 510 480"/><g fill="#c5c2b7"><circle cx="300" cy="290" r="4"/><circle cx="300" cy="350" r="4"/><circle cx="300" cy="410" r="4"/><circle cx="300" cy="470" r="4"/><circle cx="300" cy="530" r="4"/></g>',
'pants':'<path d="M200 155 Q300 145 400 155 L420 640 325 650 300 325 275 650 180 640Z"/><path class="seam" d="M200 185 400 185 M300 155 300 325 M240 190 225 630 M360 190 375 630 M205 193 235 193 235 250 M365 250 365 193 395 193"/>',
'dress':'<path d="M230 150 185 180 150 300 205 320 230 255 240 340 145 650 Q300 690 455 650 L360 340 370 255 395 320 450 300 415 180 370 150 Q350 205 300 205 Q250 205 230 150Z"/><path class="seam" d="M240 340 Q300 355 360 340 M220 160 Q240 220 300 220 Q360 220 380 160 M230 400 200 640 M370 400 400 640"/>',
'bag':'<path fill="none" stroke-width="20" d="M230 350 V220 Q230 135 300 135 Q370 135 370 220 V350"/><path d="M180 300 Q300 330 420 300 L445 580 Q300 650 155 580Z"/><path class="seam" d="M190 330 175 565 Q300 620 425 565 L410 330 M230 320 230 420 M370 320 370 420"/>',
'coat':'<path d="M225 130 160 160 75 550 145 575 195 310 170 675 430 675 405 310 455 575 525 550 440 160 375 130 300 250Z"/><path class="seam" d="M225 130 205 245 260 260 240 290 300 370 300 675 M375 130 395 245 340 260 360 290 300 370 M200 435 260 435 260 500 200 500 M340 435 400 435 400 500 340 500 M190 380 410 380"/><circle fill="#746651" cx="300" cy="430" r="6"/><circle fill="#746651" cx="300" cy="510" r="6"/>'
}
colors = {'knit':'#c5bba3','cardigan':'#868a7b','blazer':'#a79e89','shirt':'#efede3','pants':'#666861','dress':'#b7b0a0','bag':'#6c5743','coat':'#c0ae90'}
for name, shape in shapes.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="750" viewBox="0 0 600 750"><defs><linearGradient id="bg" x2="0" y2="1"><stop stop-color="#ebe9e2"/><stop offset="1" stop-color="#f2f0e9"/></linearGradient><linearGradient id="fabric" x2="1" y2=".2"><stop stop-color="{colors[name]}"/><stop offset=".5" stop-color="{colors[name]}"/><stop offset="1" stop-color="#77786b" stop-opacity=".3"/></linearGradient><filter id="shadow"><feDropShadow dx="8" dy="15" stdDeviation="13" flood-color="#4b493f" flood-opacity=".17"/></filter><pattern id="rib" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M2 0V7" stroke="#fff" opacity=".09"/></pattern></defs><rect width="600" height="750" fill="url(#bg)"/><ellipse cx="300" cy="690" rx="150" ry="12" fill="#555345" opacity=".04"/><g fill="url(#fabric)" stroke="{colors[name]}" stroke-width="2" filter="url(#shadow)">{shape}</g><style>.seam{{fill:none;stroke:#595c50;stroke-width:2;opacity:.28}}</style><text x="300" y="717" text-anchor="middle" font-family="Georgia,serif" font-size="10" letter-spacing="4" fill="#7f8275">YOURDAY · SAMPLE</text></svg>'''
    path = root / f'{name}.svg'
    path.write_text(svg)

for name in shapes:
    cairosvg.svg2png(url=str(root / f'{name}.svg'), write_to=str(root / f'{name}.png'))
print('8개 샘플 의류 일러스트 생성 완료')
