"""
Package rawspec_testing

* Create <trial directory> tree under /tmp.
* cd <trial diretcory>
* For each .raw file in the <baseline directory>, do the following:
    - rawspec   -f 1048576   -t 51  --dest .   <full path of the .raw file prefix>
* For each ext = .fil or .h5 file in the <trial directory> produced by rawspec, do the following:
    - turboSETI   -n 64   -s 10   -g y   -d <GPU_ID>   <0000.ext file>
    - Create a .tbldat file.
    - Create a .tblhdr file.
    - Create a .tbldsel file.
* rawspectest stdout --> <.tblnpols file>
* Cleanup: rm *.fil, *.h5, *.dat, *.log
"""

MY_NAME = "runner"

import sys
import os
import glob
import time
import shutil
import stat
from datetime import timedelta
import logging
from argparse import ArgumentParser

# Helper functions:
from common import BASELINE_DIR, MY_VERSION, RAWSPECTEST_TBL, \
                   TRIAL_DIR, TS_SNR_THRESHOLD, oops, run_cmd, set_up_logger
import dat2tbl
import hdr2tbl
import npols2tbl
import dsel2tbl


def main(args=None):
    """
    Parameters
    ----------
    args : Namespace
        Command-line parameters. The default is None.

    Returns
    -------
    None.

    """

    # Create an option parser to get command-line input/arguments
    parser = ArgumentParser(description="installer version {}."
                                        .format(MY_VERSION))
    parser.add_argument("-g", "--gpu_id",
                        dest="gpu_id",
                        type=int,
                        required=True,
                        help="GPU device ID (0-3) to use in rawspec and turbo_seti")
    parser.add_argument("--h5",
                        dest="flag_h5",
                        default=True,
                        action="store_true",
                        help="Rawspec will produce .h5 files instead of .fil files.")
    parser.add_argument("-S", "--skip_cleanup",
                        dest="flag_skip_cleanup",
                        default=False,
                        action="store_true",
                        help="Skip removing the files generated by rawspec and turbo_seti after the tables are produced.")
    parser.add_argument("-v", "--version",
                        dest="show_version",
                        default=False,
                        action="store_true",
                        help="Flag: Show the installer version and exit")

    # Validate arguments.
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    if args.show_version:
        print("installer: {}".format(MY_VERSION))
        sys.exit(0)

    # Set up logging.
    logger = set_up_logger(MY_NAME)

    # TEMPORARY WARNING about the --h5 option.
    if args.flag_h5:
        logging.warning("Currently, the --h5 flag is ignored.")

    # Show system information.
    osinfo = os.uname()
    logger.info("O/S name = {}, release = {}, version = {}"
                .format(osinfo.sysname, osinfo.release, osinfo.version))
    logger.info("Node name = {}, CPU type = {}, HOME = {}"
                .format(osinfo.nodename, osinfo.machine, os.environ["HOME"]))

    # Take a timestamp
    time1 = time.time()

    # TRIAL_DIR still exist?  If so, remove it.
    if os.path.exists(TRIAL_DIR): # Yes, it exists.
        try:
            shutil.rmtree(TRIAL_DIR, ignore_errors=True)
        except:
            oops("shutil.rmtree({}) FAILED !!".format(TRIAL_DIR))

    # Create TRIAL_DIR.
    try:
        os.mkdir(TRIAL_DIR)
        mode = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO
        os.chmod(TRIAL_DIR, mode=mode)
        logger.info("Created directory {} with mode={}."
              .format(TRIAL_DIR, oct(mode)))
    except:
        oops("os.mkdir/os.chmod({}, mode={}) FAILED !!"
             .format(TRIAL_DIR, oct(mode)))

    # Go to TRIAL_DIR.
    try:
        os.chdir(TRIAL_DIR)
        logger.debug("Current directory is now {}".format(TRIAL_DIR))
    except:
        oops("os.chdir({}) FAILED !!".format(TRIAL_DIR))

    # For each unique file stem, run rawspec.
    # Note: If a rawspec file is X.0000.raw then its rawstem is X.
    for one_raw_file in sorted(glob.glob("{}/*.0000.raw".format(BASELINE_DIR))):
        rawstem = one_raw_file[0:-9]
        cmd = "rawspec  -f 1048576  -t 51  -g {}  -d {}  {}" \
              .format(args.gpu_id, TRIAL_DIR, rawstem)
        run_cmd(cmd, logger)

    # For each unique 0000.fil, run turbo_seti, dat2tbl, and hdr2tbl.
    for filfile in sorted(glob.glob("*.fil")):
        cmd = "turboSETI  --snr {}  --gpu y  --gpu_id {}  --n_coarse_chan 64  {}" \
              .format(TS_SNR_THRESHOLD, args.gpu_id, filfile)
        run_cmd(cmd, logger)
        dat_name = filfile.split("/")[-1].replace(".fil", ".dat")
        tbldat_name = filfile.split("/")[-1].replace(".fil", '.tbldat')
        try:
            dat2tbl.main([dat_name, tbldat_name])
        except:
            oops("dat2tbl.main({}, {}) FAILED !!".format(dat_name, tbldat_name))
        h5_name = filfile.split("/")[-1].replace(".fil", ".h5")
        tblhdr_name = filfile.split("/")[-1].replace(".fil", ".tblhdr")
        try:
            hdr2tbl.main([h5_name, tblhdr_name])
        except:
            oops("hdr2tbl.main({}, {}) FAILED !!".format(h5_name, tblhdr_name))
        tbldsel_name = filfile.split('/')[-1].replace(".fil", ".tbldsel")
        try:
            dsel2tbl.main([h5_name, tbldsel_name])
        except:
            oops("dsel2tbl.main({}, {}) FAILED !!".format(h5_name, tbldsel_name))

        logger.info("Created post-turbo_seti tables for {}.".format(filfile))

    # rawspectest cases.
    tblnpols_name = TRIAL_DIR + RAWSPECTEST_TBL
    npols2tbl.main([tblnpols_name])

    # Do post-run cleanup.
    if args.flag_skip_cleanup:
        logger.info("Skipping post-run cleanup at the operator's request")
    else:
        cmd = "rm *.dat *.fil *.h5 *.log"
        run_cmd(cmd, logger)

    # Bye-bye.
    time2 = time.time()
    time_delta = timedelta(seconds=(time2 - time1))
    logger.info("Bye-bye, elapsed hh:mm:ss = {}".format(time_delta))


if __name__ == "__main__":
    main()
