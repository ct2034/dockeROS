#!/bin/bash
function dockeROS() {
  local workspace=$(roscd && cd .. && pwd)
  case $1 in
  b|build)
    shift
    WORKSPACE=$workspace rosrun striml_docker build_images $1
    ;;
  l|launch)
    shift
    echo "to be implemented"
    ;;
  s|set_ros_master)
    shift
    local ip=$(docker inspect --format "{{ .NetworkSettings.IPAddress }}" $1)
    export ROS_MASTER_URI=http://$ip:11311
    local ros_ip=$(sed 's/\.[0-9]$/.1/g' <<< $ip)
    export ROS_IP=$ros_ip
    ;;
	*)
    echo "A tool to use the docker environment ..."
    echo "----------------------"
    echo "Usage:"
    echo " dockeROS <subcommand>"
    echo "----------------------"
    echo "Available subcommands:"
    echo " build: to be implemented"
    echo " launch: to be implemented"
    echo " set_ros_master_uri: sets the ROS_MASTER_URI to the ip of the rocon_hub container"
    ;;
  esac
}

function complete_dockeROS() {
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local cmd="${COMP_WORDS[1]}"

  case "${COMP_CWORD}" in
	1)
    COMPREPLY=( $(compgen -W "b build l launch s set_ros_master" -- $cur) )
    ;;
	2)
    case "${cmd}" in
    b|build)
      shift
      COMPREPLY=( $(compgen -W "binary source update all" -- $cur) )
      ;;
    l|launch)
      shift
      echo "to be implemented"
      ;;
    s|set_ros_master)
      shift
      local images=$(docker ps --format "{{.Names}}")
		  COMPREPLY=( $(compgen -W "${images}" -- $cur) )
      ;;
    esac
    ;;
	*)
    COMPREPLY=""
    ;;
  esac
}

complete -F complete_dockeROS dockeROS
