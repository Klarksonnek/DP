#!/bin/bash

EXIT_CODE=0

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
		EXIT_CODE=1
	fi

	#reset farby
	echo -n -e "\e[39m"
}

# 0 - nezobrazi sa debugovacie vypisy
# 1 - zobrazenie debug vypisov
SHOW_DEBUG_MSG=0

BIN=python3

# absolutna cesta do adresara, kde sa nachadza spustany script
# @see http://mywiki.wooledge.org/BashFAQ/028
ABS_PATH=${BASH_SOURCE%/*}
ABS_PATH+="/examples2"

cd ${ABS_PATH}

EXAMPLES=(
    "0000_db_tests/run.py"
    "0002_graph_example/run.py"
    "0100_open_close_all_graphs/run.py"
    "0101_shower_all_graphs/run.py"
    "0102_sh_diff_graphs_analysis/run.py"
    "0103_open_ventilation_length_detector/run.py"
    "0104_open_detector/run.py"
    "0105_shower_detector/run.py"
    "0200_open_close_all_graphs/run.py"
    "0201_co2_delays_histogram/run.py"
    "0202_open_detector/run_co2.py"
    "0202_open_detector/run_co2_t_h.py"
    "0202_open_detector/run_co2_t_h_out.py"
    "0203_open_ventilation_length_predictor/run.py"
)

if [[ `hostname` = *"travis"* ]]; then
	BIN=python
fi

for i in "${EXAMPLES[@]}"
do
	IFS='/' read -a myarray <<< "$i"
	cd ${myarray[0]}

	echo "description: "${i}

	if [ ${SHOW_DEBUG_MSG} -eq 1 ] ; then
		`time ${BIN} ${myarray[1]} >> /dev/null`
	else
		`time ${BIN} ${myarray[1]} &> /dev/null`
	fi

	check "OK"
	echo ""
	cd ..
done

sleep 1
exit ${EXIT_CODE}
