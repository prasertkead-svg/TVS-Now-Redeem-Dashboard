# TVS Now Redeem Dashboard — Shop by WW

Dashboard ติดตามการ Redeem TVS Now (Redeem-Yes / Redeem-No) · ธีมชมพู–ขาว · Region: BMA / UPC I / UPC II (อ้างอิง MAN LIST)

- รหัส Admin: `ADMIN5555` · รหัส User: `WW5555` (เป็นการกั้นหน้าจอเท่านั้น ไม่ใช่การเข้ารหัสข้อมูล)
- เปิดผ่าน GitHub Pages: `https://prasertkead-svg.github.io/tvs-now-redeem-dashboard/`

## ตั้งค่าครั้งแรก (ทำครั้งเดียว)
1. **Settings → Pages → Build and deployment → Source: `GitHub Actions`**
2. ไปที่ **Actions** → `Update data & deploy dashboard` → **Run workflow** (หรือ push อะไรก็ได้) รอ ~1 นาที

## อัปเดตข้อมูล — Dashboard อัปเดตเองอัตโนมัติ
หน้าเว็บเช็คข้อมูลใหม่ทุก 1 นาที (และทุกครั้งที่กลับมาที่แท็บ) — ไม่ต้องรีเฟรชเอง

**วิธี A — อัปโหลด Excel ผ่าน GitHub (ไม่ต้องมี Token)**
1. เปิดโฟลเดอร์ `input/redeem/` (ไฟล์ TVS NOW REDEEM) หรือ `input/master/` (ไฟล์ MAN&SHOPLIST)
2. **Add file → Upload files** → ลากไฟล์ Excel (ชื่ออะไรก็ได้) → Commit
3. GitHub Actions แปลงไฟล์ล่าสุดเป็น `data/*.json` แล้ว deploy ให้เอง (~1–2 นาที)

**วิธี B — อัปโหลดผ่านหน้า Admin ของ Dashboard**
1. Login ด้วย `ADMIN5555` → แท็บ ⚙ Admin → การ์ด **เชื่อมต่อ GitHub** ใส่ Fine-grained Token
   (Repository access: เฉพาะ repo นี้ · Permissions: **Contents → Read and write**) → บันทึก → ทดสอบ
2. ลากไฟล์ Excel ลงช่องอัปโหลด → **บันทึก & เผยแพร่ให้ทุกคน** (Commit ขึ้น GitHub ให้ทันที)

## โครงสร้าง
| ไฟล์ | รายละเอียด |
|---|---|
| `index.html` | Dashboard (Login, Dashboard, By Staff, By Campaign, Admin) |
| `data/redeem.json`, `data/master.json` | ข้อมูลที่หน้าเว็บอ่าน |
| `data/version.json` | ตัวบอกเวอร์ชันข้อมูล ใช้ตรวจว่ามีข้อมูลใหม่ |
| `input/redeem/`, `input/master/` | วางไฟล์ Excel ใหม่ที่นี่ (ระบบใช้ไฟล์ที่ commit ล่าสุด) |
| `scripts/convert.py` | แปลง Excel → JSON (หา Sheet ให้อัตโนมัติ ไม่ยึดชื่อไฟล์) |
| `.github/workflows/deploy.yml` | แปลงข้อมูล + deploy GitHub Pages อัตโนมัติ |

เปิดในเครื่อง: `python3 -m http.server` แล้วเข้า `http://localhost:8000`

> ⚠️ ข้อมูลมีเบอร์โทรลูกค้า — Repo/Pages แบบ Public ทุกคนบนอินเทอร์เน็ตเข้าถึงได้
