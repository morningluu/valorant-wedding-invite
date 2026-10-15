# 生成分享卡片（微信 og:image 1200x630）与二维码 PNG
# 字体使用系统宋体（SimSun），零网络依赖
from PIL import Image, ImageDraw, ImageFont
import qrcode

FONT = "C:/Windows/Fonts/simsun.ttc"
RED = "#A11228"
GOLD = "#EAC381"
GOLD_DIM = "#C89B5E"
INK = "#F6E7C9"

def font(size):
    return ImageFont.truetype(FONT, size, index=0)

# ---------- 分享卡片 1200x630（红纸底烫金字，与页面一致） ----------
W, H = 1200, 630
img = Image.new("RGB", (W, H), RED)
d = ImageDraw.Draw(img)
# 金线双层框
d.rectangle([30, 30, W-30, H-30], outline=GOLD, width=4)
d.rectangle([46, 46, W-46, H-46], outline=GOLD_DIM, width=1)
# 中心标题：烫金 + 纸色副题
d.text((W/2, 200), "打瓦请柬", font=font(160), fill=GOLD, anchor="mm")
d.text((W/2, 396), "LET'S PLAY A VALORANT", font=font(44), fill=INK, anchor="mm")
d.text((W/2, 476), "2026.10.15  20:00  莲花古城卷帘门", font=font(36), fill="#E2C79E", anchor="mm")
img.save("assets/share-card.jpg", quality=90)

# ---------- 二维码 ----------
URL = "https://morningluu.github.io/valorant-wedding-invite/"
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
qr.add_data(URL)
qr.make(fit=True)
q = qr.make_image(fill_color="#1A1A1A", back_color="white").convert("RGB")

pad, label_h = 64, 120
c = Image.new("RGB", (q.width + 2*pad, q.height + 2*pad + label_h), "white")
c.paste(q, (pad, pad))
d2 = ImageDraw.Draw(c)
d2.rectangle([pad-12, pad-12, q.width+pad+11, q.height+pad+11], outline=RED, width=6)
d2.text((c.width/2, q.height + 2*pad + 34), "打瓦请柬 · 扫码上号", font=font(38), fill=RED, anchor="mm")
c.save("assets/qr.png")

print("share-card.jpg:", img.size)
print("qr.png:", c.size)
