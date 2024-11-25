# FastAPI-Project

gunluk-calisma-api/
│
├── main.py                # Ana uygulama dosyası
├── models/                # Veritabanı modelleri ve tablolar
│   └── task_model.py
├── routes/                # API endpoint'leri
│   └── task_routes.py
├── database/              # Veritabanı bağlantısı ve işlemleri
│   └── connection.py
├── schemas/               # Veri doğrulama ve şemalar
│   └── task_schema.py
├── requirements.txt       # Gerekli kütüphaneler
└── tasks.db               # SQLite veritabanı (otomatik oluşturulacak)
