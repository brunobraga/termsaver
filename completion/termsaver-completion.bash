_termsaver () {
  local cur prev opts
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"
  if [[ ${cur} == -* ]]; then
    opts="--help --verbose"
  else
    opts="asciiartfarts clock jokes4all matrix programmer quotes4all randtxt rfc rssfeed starwars sysmon urlfetcher"
  fi
  COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) ) && return 0
}
complete -F _termsaver termsaver
