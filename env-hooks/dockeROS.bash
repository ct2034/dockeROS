#!/bin/bash
function dockeROS() {
  local workspace=$(roscd && cd .. && pwd)
  local package=$(rospack find dockeros)
  case $1 in
  b|build)
    shift
    python2 $package/src/dockeros_ui.py build $@
    ;;
  r|run)
    shift
    python2 $package/src/dockeros_ui.py run $@
    ;;
  p|push)
    shift
    python2 $package/src/dockeros_ui.py push $@
    ;;
  *)
    python2 $package/src/dockeros_ui.py
    ;;
  esac
}

function complete_dockeROS() {
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local cmd="${COMP_WORDS[1]}"

  case "${COMP_CWORD}" in
	1)
    COMPREPLY=( $(compgen -W "b build r run p push" -- $cur) )
    ;;
	2)
    case "${cmd}" in
    b|build)
      shift
      echo "to be implemented"
      ;;
    r|run)
      shift
      echo "to be implemented"
      ;;
    p|push)
      shift
      echo "to be implemented"
      ;;
    esac
    ;;
	*)
    COMPREPLY=""
    ;;
  esac
}

complete -F complete_dockeROS dockeROS
