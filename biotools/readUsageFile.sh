USAGE="USAGE:  bash $0 usage.dat
EXAMPLE: bash $0 usage.dat
"


x=$1

if [ $# -eq 0 ];then
     echo "$USAGE"
     exit
fi

if [ ! -f "$x" ];then
     echo "Error: Input file does not exist!"
     echo "$USAGE"
     exit
fi


echo -n $x
d=`dirname $1`
dn=`basename $d`
y=`hexdump -C  $x|head -1`
z=${y// }
w=`echo -n $z|cut -f1 -d\|`
echo -n " "
b=$((0x$w))
echo -n $b
echo -n " bytes "
echo -n $(($b/1024))
echo -n "K "
echo -n $(($b/1048576))
echo -n "M "
echo -n $(($b/1073741824))
echo G
