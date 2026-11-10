# TVS Now Redeem Dashboard — Shop by WW

Dashboard ติดตามการ Redeem TVS Now (Redeem-Yes / Redeem-No) · ธีมชมพู–ขาว · Region: BMA / UPC I / UPC II (อ้างอิงคอลัมน์ REGION ใน SHOP LIST)

- รหัส Admin: `ADMIN5555` · รหัส User: `WW5555` (เป็นการกั้นหน้าจอเท่านั้น ไม่ใช่การเข้ารหัสข้อมูล)
- เปิดผ่าน GitHub Pages: `https://prasertkead-svg.github.io/tvs-now-redeem-dashboard/`

## ตั้งค่า GitHub Pages
**Settings → Pages → Source: `Deploy from a branch` → Branch: `main` / `(root)`** (ตั้งไว้แล้ว)

## อัปเดตข้อมูล — Dashboard อัปเดตเองอัตโนมัติ
หน้าเว็บเช็คข้อมูลใหม่ทุก 15 วินาที (และทุกครั้งที่กลับมาที่แท็บ / กดปุ่ม 🔄) — ข้อมูลเปลี่ยนเองโดยไม่ต้องรีเฟรช

**วิธี A — อัปโหลด Excel ผ่าน GitHub (ไม่ต้องมี Token)**
1. **Add file → Upload files** → ลากไฟล์ Excel (ชื่อไฟล์/โฟลเดอร์อะไรก็ได้ แนะนำ `input/`) → Commit
2. ระบบดูหัวคอลัมน์เองว่าเป็นไฟล์ Redeem (STATUS_REDEEM + PARTNER_CODE) หรือ MAN&SHOPLIST (EMP_ID / SHOP CODE)
3. GitHub Actions แปลงเป็น `data/*.json` แล้ว deploy (~1 นาที) → หน้าจอทุกคนอัปเดตเอง

**วิธี B — อัปโหลดผ่านหน้า Admin ของ Dashboard**
1. Login ด้วย `ADMIN5555` → แท็บ ⚙ Admin → การ์ด **เชื่อมต่อ GitHub** ใส่ Fine-grained Token
   (Repository access: เฉพาะ repo นี้ · Permissions: **Contents → Read and write**) → บันทึก → ทดสอบ
2. ลากไฟล์ Excel ลงช่องอัปโหลด → ข้อมูลแสดงบนหน้าจอทันที (Mapping ใหม่) → กด **📢 เผยแพร่ให้ทุกคน** (Commit ขึ้น GitHub)

## โครงสร้าง
| ไฟล์ | รายละเอียด |
|---|---|
| `index.html` | Dashboard (Login, Dashboard, By Staff, By Campaign, Admin) |
| `data/redeem.json`, `data/master.json` | ข้อมูลที่หน้าเว็บอ่าน |
| `data/version.json` | ตัวบอกเวอร์ชันข้อมูล ใช้ตรวจว่ามีข้อมูลใหม่ |
| `input/` | ที่เก็บไฟล์ Excel ต้นฉบับ (อัปโหลดที่อื่นก็ได้) |
| `scripts/auto_update.py` | หาไฟล์ Excel ที่อัปโหลด แยกประเภทจากหัวคอลัมน์ แล้วแปลง |
| `scripts/convert.py` | แปลง Excel → JSON (หา Sheet ให้อัตโนมัติ ไม่ยึดชื่อไฟล์) |
| `.github/workflows/deploy.yml` | แปลงไฟล์ Excel ที่อัปโหลดเป็น `data/*.json` (Pages build ใหม่เอง) |

เปิดในเครื่อง: `python3 -m http.server` แล้วเข้า `http://localhost:8000`

> ⚠️ ข้อมูลมีเบอร์โทรลูกค้า — Repo/Pages แบบ Public ทุกคนบนอินเทอร์เน็ตเข้าถึงได้
