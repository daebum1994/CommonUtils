import os
import time
import argparse
import shutil

from config.setting import ROOT_DIR
from config.logger import ml_logger


def dir_copy(src_path, dest_path, dest_dir):
    try:
        shutil.copytree(src_path, dest_path)
        ml_logger.info(f"복사 완료: {src_path} -> {dest_path}")
        shutil.rmtree(src_path)
        ml_logger.info(f"원본 삭제: {src_path}")

    except PermissionError:
        ml_logger.info(f"권한 오류: {src_path}에 접근할 수 없습니다.")
    except FileNotFoundError:
        ml_logger.info(
            f"파일 없음 오류: {src_path} 또는 {dest_path}가 존재하지 않습니다."
        )
    except OSError as e:
        ml_logger.info(f"OS 오류 발생: {e}")
    except Exception as e:
        ml_logger.info(f"파일 처리 중 알 수 없는 오류 발생: {e}")


def monitor_and_copy(src_dir, dest_dir, interval):
    copied_files = set()

    while True:
        file_list = os.listdir(src_dir)
        for dir_name in file_list:
            src_path = os.path.join(src_dir, dir_name)
            dest_path = os.path.join(dest_dir, dir_name)

            if not os.path.isdir(src_path):
                continue

            # 파일이 새롭게 발견되었고, 아직 복사되지 않았는지 확인
            if dir_name not in copied_files:
                dir_copy(src_path, dest_path, dest_dir)
                copied_files.add(dir_name)

        # 지정된 시간 동안 대기 (5분)
        time.sleep(interval)


def main(args):
    for dir_path in [args.source_dir, args.destination_dir]:
        if not os.path.isdir(dir_path):
            ml_logger.info(f"Path Check : {dir_path}")
            raise ValueError(f"Path Check : {dir_path}")

        total, used, free = shutil.disk_usage(dir_path)
        ml_logger.info(f"경로: {dir_path}")
        ml_logger.info(f"전체 용량: {total // (2**30)} GB")
        ml_logger.info(f"사용된 용량: {used // (2**30)} GB")
        ml_logger.info(f"남은 용량: {free // (2**30)} GB\n")

    monitor_and_copy(src_dir=args.source_dir, dest_dir=args.destination_dir, interval=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Backup", description="Auto Backup")
    args = parser.add_argument_group("Common Parameter")
    args.add_argument("--check_time", type=int, default=500, required=False)
    args.add_argument(
        "--source_dir",
        type=str,
        default=os.path.join(ROOT_DIR, "gemma-2-9b-it-FT/"),
        required=False,
    )
    args.add_argument(
        "--destination_dir",
        type=str,
        default="/home/data/backup_0924_MRC_gemma_tuning",
        required=False,
    )
    main(parser.parse_args())
