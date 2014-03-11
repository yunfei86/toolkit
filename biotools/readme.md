
All tools:

 - `readUsageFile.sh`: In IR local, information of used storage of organization is stored in usage.dat
 - `countTotReadsOfBamFiles.sh`: If you have 10+ bam file and you would like to know reads count of them
 - `countTotReadsOfDirs.sh`: If you have 10+ directories that contain segmented bam files (such as exome data), and you would like to know reads count of all bam of each directory
 - `mergeBam.sh`: If you want to merge bam files

## Clone 
     git clone ssh://git@jira.itw:7999/swteam/swteam.git

## Usage

     $ bash readUsageFile.sh
     USAGE:  bash readUsageFile.sh usage.dat

     $ bash countTotReadsOfBamFiles.sh
     USAGE:  bash countTotReadsOfBamFiles.sh 1.bam [2.bam 3.bam ...]


     $ bash countTotReadsOfDirs.sh
     USAGE:  bash countTotReadsOfDirs.sh dir1/ [dir2/ dir3/ ...]

     $ bash mergeBam.sh
     USAGE:  bash mergeBam.sh in_dir/ out.bam
     EXAMPLE: bash mergeBam.sh ./outputs/TmapMergeActor-00  TargetSeq_Exome_Merged.bam
     WARNING: All BAM files should have same header!
     
    
