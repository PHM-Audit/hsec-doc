FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动
CMD ["gunicorn", "app:app", "--timeout", "120", "--workers", "2", "--bind", "0.0.0.0:5000"]
