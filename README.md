# Video Tools

Docker 기반 비디오 처리 CLI 도구 모음

## 요구사항

- Docker
- Docker Compose

## 기능

### 오디오 제거 (remove-audio)

비디오 파일에서 오디오 트랙을 제거합니다.

```bash
# 기본 사용 (input_noaudio.mp4 출력)
docker compose run --rm remove-audio input.mp4

# 출력 파일 지정
docker compose run --rm remove-audio input.mp4 -o output.mp4

# 여러 파일 처리
docker compose run --rm remove-audio video1.mp4 video2.mp4
```

**옵션:**

| 옵션 | 설명 |
|------|------|
| `input` | 입력 비디오 파일 (여러 개 가능) |
| `-o, --output` | 출력 파일 경로 (단일 파일만) |

**출력:**

- 기본: `{원본파일명}_noaudio.{확장자}`
- `-o` 옵션 사용시 지정된 경로로 출력
