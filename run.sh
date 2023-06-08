#!/bin/bash

start(){
	nohup python run_byfastapi.py > run.log 2>&1 &
}

stop(){
	ps -aux|grep run_byfastapi.py|grep -v grep|awk '{print $2}'|xargs -i kill {}
}

status(){
	flag=`ps -aux|grep run_byfastapi.py|wc -l`
	if [ "$flag" == 2 ];then
		echo -e "process is \033[32mup\033[0m"
	else
		echo -e "process is \033[31mdown\033[0m"
	fi

}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  status)
    status
    ;;
  *)
    echo "Usage: $0 {start|stop|status}"
esac
