#!/usr/bin/env python3
#
#  prjpeppercorn -- GateMate FPGAs Bitstream Documentation and Tools
#
#  Copyright (C) 2024  The Project Peppercorn Authors.
#
#  Permission to use, copy, modify, and/or distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import os, time
from os import path
from string import Template
import html_tilegrid
import shutil

GM_DOCS_INDEX = """
<html>
<head>
<title>Project Peppercorn HTML Documentation</title>
</head>
<body>
<h1>Project Peppercorn HTML Documentation</h1>
<p>Project Peppercorn is a project to document the GateMate bitstream and internal architecture.</p>
<p>This repository contains HTML documentation automatically generated from the
<a href="https://github.com/YosysHQ/prjpeppercorn">Project Peppercorn</a> database.
Data generated includes tilemap data and bitstream data for many tile types. Click on any tile to see its bitstream
documentation.
</p>
<hr/>
$docs_toc
<hr/>
<p>Licensed under a very permissive <a href="COPYING">CC0 1.0 Universal</a> license.</p>
</body>
</html>
"""

def main():
    shutil.rmtree("work_html", ignore_errors=True)
    os.mkdir("work_html")
    commit_hash = "" #database.get_db_commit()
    build_dt = time.strftime('%Y-%m-%d %H:%M:%S')

    docs_toc = ""
    family = "CCGM1"
    print("Family: " + family)
    docs_toc += f"<h3>{family.upper()} Family</h3>"
    docs_toc += "<h4>Bitstream Documentation</h4>"
    docs_toc += "<ul>"
    for device in ["A1"]:
        print("Device: " + device)
        docs_toc += f'<li><a href="{device}.html">{device} Documentation</a></li>'
        html_tilegrid.main(["html_tilegrid", family,  device, path.join("work_html",device + ".html")])
    docs_toc += "</ul>"
    index_html = Template(GM_DOCS_INDEX).substitute(
        datetime=build_dt,
        commit=commit_hash,
        docs_toc=docs_toc
    )
    with open(path.join("work_html", "index.html"), 'w') as f:
        f.write(index_html)
if __name__ == "__main__":
    main()
