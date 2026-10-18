# 🏛️ BODHI-VAULT: TỔ HỢP NHÀ MÁY TINH CHẾ DỮ LIỆU & NGÂN KHỐ TỰ TRỊ
> *"Áp dụng bản hiến ước bất biến từ contract để vận hành dây chuyền phòng sạch ISO, đóng gói xuất khẩu dữ liệu GraphRAG và nuôi sống toàn bộ chuỗi cung ứng."*

---

## 🏭 DÂY CHUYỀN 4 PHÂN XƯỞNG:
1. **`collector/` (Thu Hoạch & Tận Thu):** Thu gom dữ liệu sống từ `nexus-08` và tận thu di sản từ sổ bia mộ `tombstones.json` của `contract`.
2. **`refinery/` (Phòng Siêu Sạch):** Khử trùng 100% PII và bẻ gãy bản quyền văn bản thô thành tam thức logic.
3. **`marketplace/` (Đóng Gói Thương Mại):** Xuất xưởng thành phẩm `.jsonl`, `.csv`, `.cypher` (Neo4j) sẵn sàng bán ra thế giới.
4. **`treasury/` (Ngân Khố Hồi Lưu):** Phân bổ doanh thu 40-30-30 nuôi ngược lại máy chủ và các nút mạng thợ.


```
100048777766367/vault/
├── contract.json                  # 📜 [THỪA KẾ TỪ q]: Bản hiến ước gốc quy định luật chơi
├── kernel.py                      # 🏛️ [ĐỐC CÔNG ĐIỀU PHỐI]: Vận hành 4 phân xưởng, Apoptosis tự diệt lỗi
│
├── collector/                     # 🚜 [PHÂN XƯỞNG 1: THU HOẠCH & TẬN THU]
│   ├── __init__.py
│   ├── harvester.py               # Thu gom dữ liệu sống từ nexus-08, nexus-07, neuron...
│   └── dead_salvager.py           # Tận thu di cốt từ sổ bia mộ tombstones.json của contract
│
├── refinery/                      # 🏭 [PHÂN XƯỞNG 2: PHÒNG SIÊU SẠCH ISO]
│   ├── __init__.py
│   ├── pii_cleaner.py             # Bộ lọc sạch PII (email, phone, IP, tên riêng)
│   └── graph_refiner.py           # Chưng cất bộ ba tam thức logic chuẩn GraphRAG
│
├── marketplace/                   # 📦 [PHÂN XƯỞNG 3: ĐÓNG GÓI THƯƠNG MẠI]
│   ├── __init__.py
│   ├── packager.py                # Xuất xưởng 3 định dạng: .jsonl, .csv, .cypher (Neo4j)
│   └── data_dictionary.md         # Từ điển dữ liệu chuẩn mực quốc tế
│
├── treasury/                      # 💰 [PHÂN XƯỞNG 4: NGÂN KHỐ HỒI LƯU]
│   ├── __init__.py
│   ├── ledger.json                # Sổ cái ghi nhận điểm cống hiến của từng nút mạng
│   └── allocator.py               # Thuật toán phân bổ dinh dưỡng 40-30-30 nuôi ngược hệ thống
│
├── dist/                          # 🎁 [KHO THÀNH PHẨM]: Chứa các tệp dữ liệu sạch sẵn sàng bán
│   └── .gitkeep
├── organs/                        # 🧩 Nơi cắm thêm mắt xích mở rộng [r] (lỗi cú pháp tự hủy)
│   └── .gitkeep
├── synapses/                      # 💾 Sổ nhật ký xuất xưởng
│   ├── .gitkeep
│   ├── peers.json                 # Danh bạ các mỏ dữ liệu sống
│   └── state.json                 # Sổ nhật ký kỷ nguyên xuất kho
│
├── Dockerfile                     # Đóng băng hạt nhân: python:3.12-slim
├── README.md                      # Tuyên ngôn Thương Cảng Toàn Cầu
└── .github/
    └── workflows/
        └── node.yml               # Workflow bọc thép tự trị – Không dây rốn

```
