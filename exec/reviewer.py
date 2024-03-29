"""
Package rawspec_testing

Review the results of runner.py activities.

* cd <trial diretcory>
* For each .tbldat file in the <trial directory>, do the following:
    - Optional: Compare   <.tbldat file> to counterpart in the baseline
    - Compare   <.tblhdr file> to counterpart in the baseline
    - Compare   <.tbldsel file> to counterpart in the baseline
    - Compare   <.tblnpols file> to counterpart in the baseline
* In all cases, report SUCCESS or FAILURE.
"""

MY_NAME = "reviewer"

import sys
import os
import glob
from argparse import ArgumentParser

# Helper functions:
from site_parameters import BASELINE_DIR, RAWSPECTEST_TBL, \
                            RUN_TURBO_SETI, TRIAL_DIR
from common import MY_VERSION, oops, logger
from compare_2_csvs import compare_tbldat, compare_tblhdr, compare_tblnpols, compare_tbldsel


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

    # Initialise error count to zero.
    n_errors = 0

    # On the right system?
    osinfo = os.uname()
    logger(MY_NAME, "O/S name = {}, release = {}, version = {}"
                .format(osinfo.sysname, osinfo.release, osinfo.version))
    logger(MY_NAME, "Node name = {}, CPU type = {}, HOME = {}"
                .format(osinfo.nodename, osinfo.machine, os.environ["HOME"]))

    # BASELINE_DIR exist?
    if not os.path.exists(BASELINE_DIR):
        oops("Trial directory ({}) does NOT exist !!".format(BASELINE_DIR))

    # TRIAL_DIR exist?
    if not os.path.exists(TRIAL_DIR):
        oops("Trial directory ({}) does NOT exist !!".format(TRIAL_DIR))

    # For each unique .tbldat file in BASELINE_DIR,
    # compare it to its counterpart in TRIAL_DIR.
    if RUN_TURBO_SETI:
        for baseline_file in sorted(glob.glob("{}/*.tbldat".format(BASELINE_DIR))):
            basename = os.path.basename(baseline_file)
            logger(MY_NAME, "Compare baseline and trial for {} .....".format(basename))
            trial_file = os.path.join(TRIAL_DIR, basename)
            if os.path.isfile(trial_file): # If nonexistent, then it was commented out in site_parameters.py
                n_errors += compare_tbldat(baseline_file, trial_file)

    # For each unique .tblhdr file in BASELINE_DIR,
    # compare it to its counterpart in TRIAL_DIR.
    for baseline_file in sorted(glob.glob("{}/*.tblhdr".format(BASELINE_DIR))):
        basename = os.path.basename(baseline_file)
        logger(MY_NAME, "Compare baseline and trial for {} .....".format(basename))
        trial_file = os.path.join(TRIAL_DIR, basename)
        if os.path.isfile(trial_file): # If nonexistent, then it was commented out in site_parameters.py
            n_errors += compare_tblhdr(baseline_file, trial_file)

    # For each unique .tbldsel file in BASELINE_DIR,
    # compare it to its counterpart in TRIAL_DIR.
    for baseline_file in sorted(glob.glob("{}/*.tbldsel".format(BASELINE_DIR))):
        basename = os.path.basename(baseline_file)
        logger(MY_NAME, "Compare baseline and trial for {} .....".format(basename))
        trial_file = os.path.join(TRIAL_DIR, basename)
        if os.path.isfile(trial_file): # If nonexistent, then it was commented out in site_parameters.py
            n_errors += compare_tbldsel(baseline_file, trial_file)

    # Compare trial to baseline versions o0f rawspectest .tblnpols files.
    logger(MY_NAME, "Compare baseline and trial for {} .....".format(RAWSPECTEST_TBL))
    baseline = BASELINE_DIR + RAWSPECTEST_TBL
    trial = TRIAL_DIR + RAWSPECTEST_TBL
    n_errors += compare_tblnpols(baseline, trial)

    # Bye-bye.
    if n_errors > 0:
        logger(MY_NAME, "*FAILURE* - Number of errors reported = {}".format(n_errors))
    else:
        logger(MY_NAME, "*SUCCESS* - No errors reported.")
    sys.exit(n_errors)


if __name__ == "__main__":
    main()
