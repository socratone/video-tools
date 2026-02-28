#!/usr/bin/env python3
"""
Video Audio Remover CLI
비디오 파일에서 오디오 트랙을 제거하는 CLI 도구
"""

import argparse
import subprocess
import sys
from pathlib import Path


def remove_audio(input_path: Path, output_path: Path) -> bool:
    """
    FFmpeg를 사용하여 비디오에서 오디오를 제거합니다.

    Args:
        input_path: 입력 비디오 파일 경로
        output_path: 출력 비디오 파일 경로

    Returns:
        성공 여부
    """
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-c:v", "copy",  # 비디오 코덱 복사 (재인코딩 없음)
        "-an",           # 오디오 스트림 제거
        "-y",            # 출력 파일 덮어쓰기
        str(output_path)
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return False

        return True

    except FileNotFoundError:
        print("Error: FFmpeg가 설치되어 있지 않습니다.", file=sys.stderr)
        print("Docker를 사용하거나 FFmpeg를 설치해주세요.", file=sys.stderr)
        return False


def generate_output_path(input_path: Path) -> Path:
    """입력 파일명에 _noaudio 접미사를 붙인 출력 경로 생성"""
    return input_path.parent / f"{input_path.stem}_noaudio{input_path.suffix}"


def main():
    parser = argparse.ArgumentParser(
        description="비디오 파일에서 오디오를 제거합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s input.mp4                    # input_noaudio.mp4 출력
  %(prog)s input.mp4 -o output.mp4      # 출력 파일 지정
  %(prog)s video1.mp4 video2.mp4        # 여러 파일 처리
        """
    )

    parser.add_argument(
        "input",
        nargs="+",
        help="입력 비디오 파일 (여러 개 가능)"
    )

    parser.add_argument(
        "-o", "--output",
        help="출력 파일 경로 (단일 파일 처리시에만 사용 가능)"
    )

    args = parser.parse_args()

    input_files = [Path(f) for f in args.input]

    # 출력 옵션 검증
    if args.output and len(input_files) > 1:
        print("Error: -o/--output 옵션은 단일 파일 처리시에만 사용 가능합니다.", file=sys.stderr)
        sys.exit(1)

    # 입력 파일 존재 여부 확인
    for input_file in input_files:
        if not input_file.exists():
            print(f"Error: 파일을 찾을 수 없습니다: {input_file}", file=sys.stderr)
            sys.exit(1)

    success_count = 0
    fail_count = 0

    for input_file in input_files:
        if args.output:
            output_file = Path(args.output)
        else:
            output_file = generate_output_path(input_file)

        print(f"처리 중: {input_file} -> {output_file}")

        if remove_audio(input_file, output_file):
            print(f"완료: {output_file}")
            success_count += 1
        else:
            print(f"실패: {input_file}", file=sys.stderr)
            fail_count += 1

    # 결과 요약
    if len(input_files) > 1:
        print(f"\n결과: {success_count}개 성공, {fail_count}개 실패")

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
