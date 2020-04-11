# RapidLayout-UTPlaceF

## Introduction

This is the repository for UTPlaceF placement experiment with
our systolic convolution accelerator design. We use the 
publicly available UTPlaceF TCAD 2017 Version executable
from [here](http://wuxili.net/project/utplacef/).

## Run UTPlaceF

```bash
./UTPlaceF_TCAD17 -aux conv/design.aux -out conv.out
```

## Generate Netlist and Architecture Definition

We first introduce the extended bookshelf format used by UTPlaceF, then
we show how to generate the required files with Python scripts.

#### The Extended BookShelf format for FPGA Placement:
- `design.aux`: auxiliary file, it tells the executable the path of other required files for current design;
- `design.lib`: all library cells are defined in `design.lib`, a new addition to bookshelf format;
- `design.nets`: defines the nets that connect nodes;
- `design.nodes`: defines corresponding library cells for each instance;
- `design.pl`: fixed placements for certain instances;
- `design.scl`: defines the resource (instances) layout on FPGA.

#### Generating required files

We show how to generate `design.scl`, `design.nodes`, and `design.nets` with our Python scripts.

```bash
$ cd scripts
$ python gen_netlist.py
$ python gen_scl.py
```

Then we copy the three generated files to `conv` folder, the placement experiment is ready to run. 


## License

This tool is distributed under MIT license.

Copyright (c) 2020 Niansong Zhang, Nachiket Kapre

<div style="text-align: justify;">
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
<br><br>
</div>


<div style="text-align: justify;">
<b>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</b>
<br><br>
</div>


<div style="text-align: justify;">
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 </div>
