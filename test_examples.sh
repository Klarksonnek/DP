#!/bin/bash

check () {
	ERR=$?
	ERR_CODE=$ERR
	OK=0

	#zistenie ci je vysledok programu Ok/ERR
	if [ $ERR -eq 0 ] ; then
		OK=1
	fi

	#zelenou sa potvrdi spravny exit code
	#cercenou je chybny navratovy kod
	if [ "$1" == "OK"  ] && [  $OK -eq 1 ] ; then
		echo -ne "\e[92m"
	elif  [ "$1" == "ERR"  ] && [  $OK -eq 0 ] ; then
		echo -ne "\e[92m"
	else
		echo -ne "\e[31m"
		ERROR=$((ERROR + 1)) #pocet chyb
	fi

	#vypis vysledku
	if [ $ERR -eq 0 ] ; then
		echo "OK"
	else
		echo "ERROR"
	fi

	#reset farby
	echo -n -e "\e[39m"
}

# 0 - nezobrazi sa debugovacie vypisy
# 1 - zobrazenie debug vypisov
SHOW_DEBUG_MSG=0

# absolutna cesta do adresara, kde sa nachadza spustany script
# @see http://mywiki.wooledge.org/BashFAQ/028
ABS_PATH=${BASH_SOURCE%/*}
ABS_PATH+="/examples"

cd ${ABS_PATH}

GIT_BRANCH=`git branch | grep \* | cut -d ' ' -f2`

#() konvertuju jeden string to array
EXAMPLES=`git ls-tree -r ${GIT_BRANCH} --name-only -d`

# odstranenie prvych 3 znakov, ktore reprezentuju aktualny adresar
EXAMPLES=${EXAMPLES#???}
EXAMPLES=(${EXAMPLES})

for i in "${EXAMPLES[@]}"
do
	cd $i
	echo $i

	if [ ${SHOW_DEBUG_MSG} -eq 1 ] ; then
		`python3 run.py >> /dev/null`
	else
		`python3 run.py &> /dev/null`
	fi

	check "OK"
	echo ""

	cd ..
done
