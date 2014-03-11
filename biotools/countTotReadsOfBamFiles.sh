#!/bin/bash

USAGE="
USAGE:  bash $0 1.bam [2.bam 3.bam ...] 
"

trgs=${@}

 
if [ $# -eq 0 ];then
     echo "$USAGE"
     exit
fi 
 
for bam in ${trgs}
do   
    if [ ! -f "$bam" ];then
     echo "Error: given bam file does not exist: ${bam}!"
     echo "$USAGE"
     exit 1
    fi 
done

ENV_FILE=/share/apps/IR/ionreporter40/bin/lscope-setenv.sh
if [ ! -f "$ENV_FILE" ];then
    ENV_FILE=/share/apps/IR/ionreporter42/bin/lscope-setenv.sh
fi
source $ENV_FILE

for bam in $(find . -name "*bam")
do
    echo "Counting... ${bam} "
    num=`samtools view -c $bam`
    echo " ** ${bam} $num" 
done

