#!/bin/bash

# 캐시 파일 삭제할 루트 디렉토리 설정 (기본값은 현재 디렉토리)
root_dir=${1:-.}

# __pycache__ 디렉토리와 .pyc 파일 삭제
find "$root_dir" -type d -name "__pycache__" -exec rm -r {} + -o -type f -name "*.pyc" -exec rm -f {} +

echo "Python cache files and directories have been removed."