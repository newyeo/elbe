#!/usr/bin/env python
#
# ELBE - Debian Based Embedded Rootfilesystem Builder
# Copyright (C) 2013  Linutronix GmbH
#
# This file is part of ELBE.
#
# ELBE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ELBE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ELBE.  If not, see <http://www.gnu.org/licenses/>.

import os

from optparse import OptionParser

from elbepack.elbexml import ElbeXML, ValidationError
from elbepack.filesystem import TargetFs
from elbepack.asciidoclog import ASCIIDocLog

def run_command( argv ):

    oparser = OptionParser( usage="usage: %prog hdimg --target <dir> --output <out> <xmlfile>")
    oparser.add_option( "--target", dest="target",
                        help="target directory",
                        metavar="FILE" )
    oparser.add_option( "-o", "--output", dest="output",
                        help="name of logfile" )
    oparser.add_option( "--buildtype", dest="buildtype",
                        help="Override the buildtype" )
    oparser.add_option( "--skip-validation", action="store_true",
                        dest="skip_validation", default=False,
                        help="Skip xml schema validation" )
    oparser.add_option( "--skip-grub", action="store_true",
                        dest="skip_grub", default=False,
                        help="Skip grub install" )

    (opt,args) = oparser.parse_args(argv)

    if len(args) != 1:
        print "Wrong number of arguments"
        oparser.print_help()
        sys.exit(20)

    if not opt.target:
        print "No directory specified!"
        oparser.print_help()
        sys.exit(20)

    if not opt.output:
        print "No Log output"
        oparser.print_help()
        sys.exit(20)

    opt.target = os.path.abspath(opt.target)

    if opt.buildtype:
        buildtype = opt.buildtype
    else:
        buildtype = None

    try:
        xml = ElbeXML( args[0], buildtype=buildtype, skip_validate=opt.skip_validation )
    except ValidationError:
        print "xml validation failed. Bailing out"
        sys.exit(20)

    outf = ASCIIDocLog(opt.output)

    target = os.path.join(opt.target, "target")
    targetfs = TargetFs(target, clean=False)

    targetfs.part_target(opt.target, opt.skip_grub)

