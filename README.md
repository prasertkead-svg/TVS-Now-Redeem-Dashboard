# TVS Now Redeem Dashboard — Shop by WW

Dashboard ติดตามการ Redeem TVS Now (Redeem-Yes / Redeem-No) ธีมชมพู–ขาว

## โครงสร้าง
| ไฟล์ | รายละเอียด |
|---|---|
| `index.html` | ตัว Dashboard (Login, Dashboard, By Staff, By Campaign, Admin) |
| `data/redeem.json` | ข้อมูล TVS NOW REDEEM (เข้ารหัสแบบ dictionary ต่อคอลัมน์) |
| `data/master.json` | ข้อมูล MAN LIST + SHOP LIST |

## การใช้งาน
- รหัส Admin: `ADMIN5555` · รหัส User: `WW5555` (เป็นการกั้นหน้าจอเท่านั้น ไม่ใช่การเข้ารหัสข้อมูล)
- Region (BMA / UPC I / UPC II) อ้างอิงจาก MAN LIST (แถว RRH ที่ดูแลแต่ละ Area)
- เปิดดูในเครื่อง: `python3 -m http.server` แล้วเข้า `http://localhost:8000`
  (ต้องเปิดผ่าน web server เพราะหน้าเว็บโหลดไฟล์ `data/*.json`)

## อัปเดตข้อมูล
หน้า Admin รองรับการอัปโหลดไฟล์ Excel ใหม่ (ไม่ยึดชื่อไฟล์) เมื่อเปิดบน claude.ai จะบันทึกให้ทุกคนได้
หากเปิดจาก GitHub Pages / เครื่องตัวเอง การอัปโหลดจะแสดงผลเฉพาะเครื่องนั้น — ให้แทนที่ไฟล์ `data/*.json` แล้ว commit แทน

> ⚠️ `data/redeem.json` มีเบอร์โทรลูกค้า — ควรเก็บ Repo เป็น Private
