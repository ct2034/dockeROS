#!/bin/bash
function dr() {
  local workspace=$(roscd && cd .. && pwd)
  local package=$(rospack find dockeros)
  case $1 in
  b|build)
    shift
    python2 $package/src/dockeros/cli.py build $@
    ;;
  r|run)
    shift
    python2 $package/src/dockeros/cli.py run $@
    ;;
  p|push)
    shift
    python2 $package/src/dockeros/cli.py push $@
    ;;
  *)
    python2 $package/src/dockeros/cli.py $@
    ;;
  esac
}

function _complete_dr() {
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local drcmd="${COMP_WORDS[1]}"
  local package=$(rospack find dockeros)
  local allowed_roscommands=$(python2 $package/src/dockeros/cli.py _get_allowed_roscommands)
  local roscmd="${COMP_WORDS[2]}"
	local packages=$(rospack list-names 2>/dev/null)

  case "${COMP_CWORD}" in
	1)
    COMPREPLY=( $(compgen -W "b build r run p push" -- $cur) )
    ;;
	2)
    case "${drcmd}" in
    b|build)
      shift
      COMPREPLY=( $(compgen -W "$allowed_roscommands" -- $cur) )
      ;;
    r|run)
      shift
      COMPREPLY=( $(compgen -W "$allowed_roscommands" -- $cur) )
      ;;
    p|push)
      shift
      echo "to be implemented"
      ;;
    esac
    ;;
	3)
    case "${roscmd}" in
    *)
      shift
      COMPREPLY=( $(compgen -W "$packages" -- $cur) )
      ;;
    esac
    ;;
	4)
    local package_dir="$(rospack find ${COMP_WORDS[3]})"
    case "${roscmd}" in
    roslaunch)
      shift
			local launchfiles=$(find "$package_dir" -name '*.launch' -type f -printf "%f\n")
      COMPREPLY=( $(compgen -W "${launchfiles}" -- $cur) )
      ;;
    rosrun)
      shift
      COMPREPLY=""
      ;;
    esac
    ;;
	*)
    COMPREPLY=""
    ;;
  esac
}

complete -F _complete_dr dr
