# 第一阶段：测试
FROM python:3.10-slim as test

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY tests/ ./tests/
COPY src/ ./src/
COPY prompts/ ./prompts/
COPY content/ ./content/
COPY pytest.ini .

# 创建日志目录
RUN mkdir -p logs

# 安装 Python 依赖（包括测试依赖）
RUN pip install --no-cache-dir -r requirements.txt pytest pytest-cov pytest-mock

# 运行测试
RUN pytest

# 第二阶段：生产环境
FROM python:3.10-slim as prod

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY src/ ./src/
COPY prompts/ ./prompts/
COPY content/ ./content/

# 创建日志目录
RUN mkdir -p logs

# 安装 Python 依赖（仅生产依赖）
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 7860

# 设置启动命令
CMD ["python", "src/main.py"] 