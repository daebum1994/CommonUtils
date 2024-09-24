#!/bin/bash

# 사용법을 출력하는 함수
usage() {
  echo "Usage: $0 <PID>"
  echo "Find out which Docker container is running the process with the given PID."
  echo "Example: $0 1234"
}

# PID를 입력으로 받지 않았을 경우 사용법을 출력하고 스크립트를 종료
if [ $# -ne 1 ]; then
  usage
  exit 1
fi

# 호스트 시스템에서의 PID
HOST_PID=$1

# 모든 실행 중인 Docker 컨테이너에 대하여 루프
for CONTAINER_ID in $(docker ps -q); do
  # 컨테이너 내에서 실행 중인 프로세스의 PID 목록 가져오기
  PIDS_IN_CONTAINER=$(docker top "$CONTAINER_ID" -eo pid | tail -n +2)

  # 주어진 PID가 컨테이너 내 프로세스 목록에 있는지 확인
  if echo "$PIDS_IN_CONTAINER" | grep -q -w "$HOST_PID"; then
    # 컨테이너의 이름 가져오기
    CONTAINER_NAME=$(docker inspect --format '{{.Name}}' "$CONTAINER_ID" | sed 's|/||')

    # 결과 출력
    echo "The process with PID $HOST_PID is running inside the Docker container:"
    echo "Container ID: $CONTAINER_ID"
    echo "Container Name: $CONTAINER_NAME"
    exit 0
  fi
done

# PID가 어떤 Docker 컨테이너에서도 실행되고 있지 않다면 메시지 출력
echo "The process with PID $HOST_PID is not running inside any Docker container on this host."