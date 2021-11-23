# Package rawspec_testing
# Execute testing.
# Prerequisite: xprep.sh
#

HERE=`pwd`
LOG=${HERE}/`basename $0`.log
> $LOG # Make the log nil.
set -e
set -o pipefail

function oops {
	echo
	echo '*** Oops *** '$1' !! ***' 2>&1 | tee -a $LOG
	echo
	exit 86
}

function check_gpu_id {
    case "$1" in
        (*[!0-9]*)
            oops 'The specified GPU ID is not numeric: '$1
    esac
    if [ "$1" -gt 3 ]; then
        MSG='The specified GPU ID must be 0, 1, 2, or 3 but I saw '$1
        echo $MSG  2>&1 | tee -a $LOG
    fi
 }

# One command line argument (optional): GPU ID.

NARGS=$#
[ $NARGS -ne 1 ] && oops '1 argument must be supplied: GPU ID (0, 1, 2, or 3)'
GPU_ID=$1
Q_USE_H5=$2

check_gpu_id $GPU_ID

export PATH=$HOME/rawspec:$PATH
export LD_LIBRARY_PATH=$HOME/rawspec

cd $HOME/rawspec_testing/exec

# SIGPROC Filterbank testing.
echo 2>&1 | tee -a $LOG
echo ================= 2>&1 | tee -a $LOG
echo Issue \#39 Testing 2>&1 | tee -a $LOG
echo ================= 2>&1 | tee -a $LOG

for ndx in 1 2 3
do
    echo 2>&1 | tee -a $LOG
    echo ----- Begin ndx=$ndx ------------------------- 2>&1 | tee -a $LOG
    python3 runner.py -g $GPU_ID 2>&1 | tee -a $LOG
    if [ $? -eq 0 ]; then
        python3 reviewer.py 2>&1 | tee -a $LOG
        if [ $? -ne 0 ]; then
            oops Exit status $?
        fi
    fi
    echo ----- End ndx=$ndx ------------------------- 2>&1 | tee -a $LOG
done

echo 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo FINISHED 2>&1 | tee -a $LOG
echo ======== 2>&1 | tee -a $LOG
echo There is a log of this session in $LOG

