#!/bin/bash

USAGE="
USAGE:  bash $0 in_dir/ out.bam 
EXAMPLE: bash $0 ./outputs/TmapMergeActor-00  TargetSeq_Exome_Merged.bam

WARNING: All BAM files should have same header!
"

SRC_DIR=$1
OUTPUT_MERGED_BAM=$2

if [ $# -lt 2 ];then
     echo "$USAGE"
     exit
fi

if [ ! -d "$SRC_DIR" ];then
     echo "Error: Input Directory Does not exist!"
     echo "$USAGE"
     exit
fi

ENV_FILE=/share/apps/IR/ionreporter40/bin/lscope-setenv.sh
if [ ! -f "$ENV_FILE" ];then
    ENV_FILE=/share/apps/IR/ionreporter42/bin/lscope-setenv.sh
fi
source $ENV_FILE
INPUT_BAM=$SRC_DIR/*bam

## If separate header generating needed.
#
#HEADER_SRC=`echo ${SRC_DIR} | sed s@/@_@g`
#HEADER=/tmp/${HEADER_SRC}.sam
#samtools view -H `echo $INPUT_BAM | cut -f1 -d" "` > $HEADER
#samtools merge -h $HEADER $OUTPUT_MERGED_BAM $INPUT_BAM
#

echo " *** Merging Bam"
samtools merge - $INPUT_BAM | samtools sort - $OUTPUT_MERGED_BAM
