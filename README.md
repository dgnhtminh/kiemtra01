# Hệ thống Microservices bằng FastAPI (Python)

Đây là một hệ thống microservices đơn giản bao gồm:
- **api-gateway**: API Gateway điều hướng request. Chạy cổng `8000`.
- **staff-service**: Quản lý nhân viên và thiết bị (sử dụng MySQL). Chạy cổng `8001`.
- **customer-service**: Quản lý khách hàng (sử dụng MySQL). Chạy cổng `8002`.
- **laptop-service**: Quản lý laptop (sử dụng PostgreSQL). Chạy cổng `8003`.
- **mobile-service**: Quản lý điện thoại di động (sử dụng PostgreSQL). Chạy cổng `8004`.

## 1. Yêu cầu và cài đặt môi trường
- Cài đặt Python 3.9+
- Cài đặt Docker và Docker Compose

Trước tiên, cài đặt các packages Python cần thiết:
```bash
pip install -r requirements.txt
```

## 2. Khởi chạy Databases
Hệ thống sử dụng Docker Compose để chạy database (MySQL và PostgreSQL).
Tại thư mục gốc, chạy lệnh sau:
```bash
docker-compose up -d
```
Bạn sẽ có:
- MySQL chạy trên cổng `3306` (user: `dbuser`, pass: `dbpassword`, db: `microservices_db`)
- PostgreSQL chạy trên cổng `5432` (user: `dbuser`, pass: `dbpassword`, db: `microservices_db`)

## 3. Khởi chạy các Services
Hãy mở 5 Terminal (cửa sổ dòng lệnh) khác nhau để chạy song song 5 service này:

**Terminal 1:** (Gateway)
```bash
cd api-gateway
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2:** (Staff Service)
```bash
cd staff-service
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 3:** (Customer Service)
```bash
cd customer-service
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

**Terminal 4:** (Laptop Service)
```bash
cd laptop-service
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

**Terminal 5:** (Mobile Service)
```bash
cd mobile-service
uvicorn main:app --host 0.0.0.0 --port 8004 --reload
```

## 4. Hướng dẫn sử dụng
Cấu trúc API Gateway điều hướng dựa trên path như sau:
- `/staff/...` -> Gọi đến staff-service
- `/customer/...` -> Gọi đến customer-service
- `/laptop/...` -> Gọi đến laptop-service
- `/mobile/...` -> Gọi đến mobile-service

**Tài liệu API Docs tự động (Swagger UI):**
Sau khi chạy các service, bạn có thể xem tài liệu chi tiết cấu trúc JSON tại:
- Staff Service Docs: http://localhost:8001/docs
- Khách hàng (Customer) Docs: http://localhost:8002/docs

**Ví dụ một số API (Gọi qua Gateway 8000):**
1. Thêm nhân viên:
`POST http://localhost:8000/staff/staffs/`
```json
{
  "name": "Nguyen Van A",
  "department": "IT",
  "position": "Developer"
}
```

2. Cấp phát/Nhập Item mới cho staff có ID=1:
`POST http://localhost:8000/staff/items/`
```json
{
  "name": "ThinkPad T14",
  "description": "Laptop cho lập trình viên",
  "serial_number": "SN-12345",
  "status": "Assigned",
  "staff_id": 1
}
```

3. Cập nhật Item (VD: Thu hồi thiết bị ID=1):
`PUT http://localhost:8000/staff/items/1`
```json
{
  "status": "Returned"
}
```
# kiemtra01
