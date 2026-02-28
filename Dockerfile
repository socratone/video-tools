FROM python:3.11-alpine

# FFmpeg 설치
RUN apk add --no-cache ffmpeg

# 작업 디렉토리 설정
WORKDIR /app

# 소스 코드 복사
COPY src/ /app/

# 기본 명령어
ENTRYPOINT ["python", "remove_audio.py"]
