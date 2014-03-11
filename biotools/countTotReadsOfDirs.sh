#!/bin/bash

USAGE="
USAGE:  bash $0 dir1/ [dir2/ dir3/ ...] 
"

trgs=${@}
 
if [ $# -lt 1 ];then
     echo "$USAGE"
     exit
fi 
 
for dir in ${trgs}
do   
    if [ ! -d "$dir" ];then
     echo "Error: Input directory does not exist: ${dir}!"
     echo "$USAGE"
     exit 1
    fi 
done

ENV_FILE=/share/apps/IR/ionreporter40/bin/lscope-setenv.sh
if [ ! -f "$ENV_FILE" ];then
    ENV_FILE=/share/apps/IR/ionreporter42/bin/lscope-setenv.sh
fi
source $ENV_FILE

for dir in ${trgs}
do
    echo "Counting... ${dir} "
    tot=0
    for bam in $(ls ${dir}/*bam)
    do
        num=`samtools view -c $bam`
        tot=$((tot+num))
        echo "  * $bam ${num}" 1>&2
    done
    
    echo " ** ${dir} $tot"
    echo
done
