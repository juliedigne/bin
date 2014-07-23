#!/bin/bash
set -e
# Usage : buffalogetfiles.sh <filelist> <dst_folder>
# This script will read from <filelist> a list of file which are supposed to
# be present on the buffalo and scp them to the directory <dst_folder>


print_usage()
{
  echo "Usage : $0 <filelist> <dst_folder>"
}

# sends files with ftp script generated by gen_ftp_script
ftp_send_files()
{
  ftp -v buffalo < $FTP_SCRIPT
}


# ftp every files listed in the file to DST
gen_ftp_script()
{
  cd $DST
  echo "ascii" > $FTP_SCRIPT
  while read line; do
    folder=`dirname ${line#/mnt}`
    file=`basename $line`
    echo "cd $folder" >> $FTP_SCRIPT
    echo "get \"$file\"" >> $FTP_SCRIPT
  done < $FILE_LIST.tmp
  echo "exit" >> $FTP_SCRIPT
}

# scp every files listed in the file to DST
scp_files()
{
  while read line
  do
    if [ -n $line ]; then
      cmd="scp admin@buffalo:\"$line\" $DST"
      eval $cmd
    fi
  done < $FILE_LIST.tmp
}

FTP_SCRIPT=`mktemp /tmp/FTP_SCRIPT.XXXX`
FILE_LIST=$1
DST=$2

# check arguments are given
if [ -z $DST ]; then
  echo "Error : Missing destination folder argument"
  print_usage
  exit 1
fi

if [ -z $FILE_LIST ]; then
  echo "Error : Missing destination folder argument"
  print_usage
  exit 1
fi

# check filelist exists
if [ ! -f $FILE_LIST ]; then
  echo "Error : $FILE_LIST does not exist"
  exit 1
fi

# check output dir exists
if [ ! -d $DST ]; then
  echo "Error : $DST is not a valid directory"
  exit 1
fi

# remove blank lines
sed '/^\s*$/d' $FILE_LIST > $FILE_LIST.tmp

gen_ftp_script
ftp_send_files

rm $FILE_LIST.tmp