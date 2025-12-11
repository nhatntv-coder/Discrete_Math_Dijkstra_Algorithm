Minh họa cho thuật toán Dijkstra

## Hướng dẫn chạy code

### Yêu cầu
- Python **3.9 hoặc cao hơn**

---

### Step 0: Tải code

```bash
git clone https://github.com/zombieTDV/Discrete_Math_Dijkstra_Algorithm.git
```

```bash
cd Discrete_Math_Dijkstra_Algorithm
```

### Step 1: Tạo môi trường ảo Python

```bash
python -m venv .venv
```

Sử dụng môi trường ảo:

- Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

---

### Step 2: Tải các thư viện cần thiết

```bash
pip install -r requirements.txt
```

---

### Step 3: Chạy chương trình

```bash
python src/app.py
```

## Cấu trúc dự án

```bash
project/
│
├── app.py
├── requirements.txt
│
├── algorithms/
│   ├── __init__.py
│   ├── dijkstra.py
│   ├── bfs.py
│   ├── dfs.py
│   └── multipoint.py
│
├── grid/
│   ├── __init__.py
│   └── grid.py
│
├── utils/
│   ├── __init__.py
│   ├── parsing.py
│   └── helpers.py
│
└── templates/
    └── index.html
```
