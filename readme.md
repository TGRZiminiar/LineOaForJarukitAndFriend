https://developers.line.biz/console/

login line สร้าง provider

เลือกสร้าง messaging api


tab messaging api
    เปิดให้เป้นปุ่มเขียว Use webhook 
    Auto-reply messages disabled
    ปิด Auto-response messages
    กดรับ issue แล้วเอาไปใส่ env

https://formulae.brew.sh/cask/ngrok

รันแยก terminal

python3 main.py
ngrok http 5000

เอา Url Forwarding ไปใส่ webhook

เช่น https://db8d-101-108-198-141.ngrok-free.app/webhook