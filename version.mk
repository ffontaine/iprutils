# (C) Copyright 2000, 2009
# International Business Machines Corporation and others.
# All Rights Reserved. This program and the accompanying
# materials are made available under the terms of the
# Common Public License v1.0 which accompanies this distribution.

IPR_MAJOR_RELEASE=2
IPR_MINOR_RELEASE=2
IPR_FIX_LEVEL=16
IPR_RELEASE=1
IPR_FIX_DATE=(August 14, 2009)

IPR_VERSION_STR=$(IPR_MAJOR_RELEASE).$(IPR_MINOR_RELEASE).$(IPR_FIX_LEVEL) $(IPR_FIX_DATE)

IPR_DEFINES = -DIPR_MAJOR_RELEASE=$(IPR_MAJOR_RELEASE) \
		 -DIPR_MINOR_RELEASE=$(IPR_MINOR_RELEASE) \
		 -DIPR_FIX_LEVEL=$(IPR_FIX_LEVEL) \
		 -DIPR_FIX_DATE='"$(IPR_FIX_DATE)"' \
		 -DIPR_VERSION_STR='"$(IPR_VERSION_STR)"' \
		 -DIPR_RELEASE=$(IPR_RELEASE)
