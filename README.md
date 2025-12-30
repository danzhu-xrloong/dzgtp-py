# dzgtp-py

一個用 Python 實現的 GTP (Go Text Protocol) 引擎。

## 描述

dzgtp-py 是一個輕量級的 Python 庫，用於實現 GTP 協議，這是圍棋引擎與圍棋界面之間的標準通信協議。該庫提供了基本的 GTP 引擎框架和響應解釋器，方便開發者構建自己的圍棋引擎。

## 功能

- GTP 協議版本 2 支持
- 輸入/輸出流處理
- 響應格式化（成功、失敗、恐慌）
- 簡單易用的 API

## 安裝

確保您有 Python 3.14 或更高版本，並已安裝 [uv](https://github.com/astral-sh/uv)。

```bash
uv pip install .
```

或者從源碼安裝：

```bash
git clone https://github.com/yourusername/dzgtp-py.git
cd dzgtp-py
uv pip install -e .
```

## 使用

### 基本使用

```python
from DanZhu.GTP.engine import GtpEngine
import io

# 創建輸入和輸出流
input_stream = io.StringIO("protocol_version\n")
output_stream = io.StringIO()

# 初始化引擎
engine = GtpEngine(input_stream, output_stream)

# 處理輸入
command = engine.input()
# 處理命令...

# 輸出響應
engine.output("=2\n")
```

### 響應解釋器

```python
from DanZhu.GTP.interpreter import interpretSuccess, interpretFailure

# 成功響應
response = interpretSuccess("2", id=1)  # "=1 2"

# 失敗響應
error = interpretFailure("unknown command", id=2)  # "?2 unknown command"
```

## 測試

運行測試：

```bash
uv run pytest
```

## 貢獻

歡迎貢獻！請提交 issue 或 pull request。

## 授權

此專案採用 Apache License 2.0 授權。詳見 [LICENSE](LICENSE) 文件。
