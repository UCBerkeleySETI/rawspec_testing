"""
Package rawspec_testing
Site parameters.

The following definitions reflect the UC Berkeley data centre compute nodes.
"""

TESTING_NODE = "any"

# The root of all rawspec_testing artifacts.
RAWSPEC_TESTING_DIR = "/mnt_blpd20/scratch/rawspec_testing/"

# List of file stems used.
# SELECTED and RAWSPEC_OPTS are 1-to-1.
SELECTED = [ 
    "blc13_guppi_57991_49836_DIAG_FRB121102_0010",
    "blc17_guppi_57991_49318_DIAG_PSR_J0332+5434_0008",
    "ATA_guppi_59229_47368_006379_40blocks",
    "ATA_guppi_59229_47368_006379_40blocks",
    "ATA_guppi_59811_38723_118314086_AzEl_0001-beam0001",
    ]

# The rawspec command-line options that are paired to the corresponding entry in SELECTED.
# SELECTED and RAWSPEC_OPTS are 1-to-1.
RAWSPEC_OPTS = [
    "-f 1048576  -t 51",
    "-f 1048576,8,1024 -t 51,128,3072",
    "-f 8192 -t 2 -i '1.0'",
    "-f 8192 -t 2 -S",
    "-f 1 -t 32",
    ]

# Baseline directory for measuring trial results to.
BASELINE_DIR = RAWSPEC_TESTING_DIR + "baseline/"

# The trial directory.
TRIAL_DIR = RAWSPEC_TESTING_DIR + "trial/"

# The table name for storing rawspectest results.
RAWSPECTEST_TBL = "rawspectest.tblnpols"

# Not using turbo_seti.
RUN_TURBO_SETI = False
