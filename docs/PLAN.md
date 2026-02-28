# Video Audio Remover CLI 구현 계획

## 개요
비디오 파일에서 오디오 트랙을 제거하는 Python CLI 프로그램.
Docker Compose를 통해 FFmpeg 의존성 없이 어디서든 실행 가능.

## 기술 스택
- **언어**: Python 3.11+
- **비디오 처리**: FFmpeg (Docker 컨테이너 내 설치)
- **CLI 프레임워크**: `argparse` (표준 라이브러리)
- **Docker**: Alpine 기반 경량 이미지
- **실행 환경**: Docker Compose

## 프로젝트 구조
```
video-tools/
├── src/
│   └── remove_audio.py      # 메인 CLI 스크립트
├── docs/
│   └── PLAN.md              # 구현 계획 문서
├── Dockerfile               # Docker 이미지 정의
├── docker-compose.yml       # 실행 설정
└── README.md                # 사용법 문서
```

## 구현 상세

### 1. CLI 인터페이스 (`src/remove_audio.py`)
```bash
# 사용 예시
docker compose run --rm remove-audio input.mp4                # 기본: input_noaudio.mp4 출력
docker compose run --rm remove-audio input.mp4 -o output.mp4  # 출력 파일 지정
docker compose run --rm remove-audio *.mp4                    # 여러 파일 처리
```

**기능:**
- 단일/다중 파일 처리
- 출력 파일명 자동 생성 (`_noaudio` 접미사)
- `-o/--output` 옵션으로 출력 경로 지정
- 에러 처리 및 메시지 출력

### 2. Docker 구성

**Dockerfile:**
- 베이스 이미지: `python:3.11-alpine`
- FFmpeg 설치
- 작업 디렉토리: `/app`

**docker-compose.yml:**
- 현재 디렉토리를 `/videos`로 마운트
- `remove-audio` 서비스로 실행

### 3. FFmpeg 명령어
```bash
ffmpeg -i input.mp4 -c:v copy -an output.mp4
```
- `-c:v copy`: 비디오 코덱 재인코딩 없이 복사 (빠름)
- `-an`: 오디오 스트림 제거

## 실행 방법

```bash
# 이미지 빌드
docker compose build

# 오디오 제거
docker compose run --rm remove-audio input.mp4
```

## 파일 목록

| 파일 | 설명 |
|------|------|
| `src/remove_audio.py` | 메인 CLI 스크립트 |
| `docs/PLAN.md` | 구현 계획 문서 |
| `Dockerfile` | Docker 이미지 빌드 설정 |
| `docker-compose.yml` | Docker Compose 실행 설정 |
| `README.md` | 사용법 문서 |

## 검증 방법
1. 샘플 비디오 파일 준비
2. Docker 이미지 빌드: `docker compose build`
3. 오디오 제거 실행: `docker compose run --rm remove-audio sample.mp4`
4. 출력 파일 확인: `ffprobe sample_noaudio.mp4`로 오디오 스트림 없음 확인
