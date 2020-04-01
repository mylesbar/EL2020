#!/bin/bash
clear

#echo "Script start: "
monday="VLSI & Blockchain"
tuesday="Language Processing Lecture & Lab"
wednesday="VLSI Lab & Embedded Linux"
thursday="VLSI"
friday="Language Processing"

dayString=$(date +%A)
echo "Today is" ${dayString}
echo "Today's clases are:"

case ${dayString} in
	"Monday")
		echo $monday
	;;
	"Wednesday")
		echo $wednesday
	;;
	"Tuesday")
		echo $Tuesday
	;;
	"Thursday")
		echo $Thursday
	;;
	"Friday")
		echo $Friday
	;;

esac

echo "done"


