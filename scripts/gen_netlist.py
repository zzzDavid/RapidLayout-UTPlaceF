class Netlist:
    instances = []
    connection = []

    bram_cols = [2*2, 3*2, 7*2, 12*2, 14*2, 19*2, 20*2, 25*2, 27*2, 32*2, 34*2, 41*2, 49*2, 50*2]
    height = 160  # 0, 2, 5, 7
    # how mamy BRAMs? 80 blocks * 8 each = 640
    # we have 14 columns, we can put 48 brams each.
    fixed_brams = []  # store bram names to fix
    locations = []  # corresponding locations for fixed_brams

    def fix_bram(self, name):
        # add bram's inst name
        self.fixed_brams.append(name)
        # find the next place to put it
        num = len(self.fixed_brams)-1  # the index of current bram to place
        col_idx = int(num / 48)
        col = self.bram_cols[col_idx]
        row = int( (num % 48) * 2.5)
        self.locations.append([col, row])

    def write_fixed_brams(self, filename):
        with open(filename, 'a+') as f:
            for idx, inst_name in enumerate(self.fixed_brams):
                [col, row] = self.locations[idx]
                f.write(inst_name + " " + str(col) + " " + str(row) + " 0 FIXED\n")


    def addInst(self, type):
        self.instances.append(type)
        return "inst_" + str(len(self.instances) - 1)

    def addConnection(self, inst, port, idx=-1):
        # inst and port are both string type
        if idx is -1:
            t = [inst, port]
            if len(self.connection) is 0:
                newlist = [t]
                self.connection.append(newlist)
            else:  # put it in the last list
                self.connection.append([])
                self.connection[-1].append(t)
            return len(self.connection) - 1
        else:  # we specify which list to put
            t = [inst, port]
            self.connection[idx].append(t)

    def addConnection2(self, srcInst, srcPort, dstInst, dstPort):
        t1 = [srcInst, srcPort]
        t2 = [dstInst, dstPort]
        if len(self.connection) is 0:
            newlist = [t1, t2]
            self.connection.append(newlist)
        else:  # put it in the last list
            self.connection.append([])
            self.connection[-1].append(t1)
            self.connection[-1].append(t2)
        return len(self.connection) - 1

    def write_insts(self, filename):
        with open(filename, 'a+') as f:
            for i, s in enumerate(self.instances):
                f.write("inst_" + str(i) + " " + s + "\n")

    def write_connection(self, filename):
        with open(filename, 'a+') as f:
            for i in range(len(self.connection)):
                f.write("net net_" + str(i) + " " + str(len(self.connection[i])) + "\n")
                for inst_port in self.connection[i]:
                    f.write("    " + inst_port[0] + " " + inst_port[1] + "\n")
                f.write("endnet\n\n")



def create_conv(netlist, clk_net_idx):
    # add all instances
    URAM1 = netlist.addInst("RAMB36E2")
    URAM2 = netlist.addInst("RAMB36E2")
    BRAM_1_1 = netlist.addInst("DSP48E2")
    BRAM_1_2 = netlist.addInst("DSP48E2")
    BRAM_1_3 = netlist.addInst("DSP48E2")
    BRAM_1_4 = netlist.addInst("DSP48E2")
    BRAM_2_1 = netlist.addInst("DSP48E2")
    BRAM_2_2 = netlist.addInst("DSP48E2")
    BRAM_2_3 = netlist.addInst("DSP48E2")
    BRAM_2_4 = netlist.addInst("DSP48E2")
    DSP_1_1 = netlist.addInst("DSP48E2")
    DSP_1_2 = netlist.addInst("DSP48E2")
    DSP_1_3 = netlist.addInst("DSP48E2")
    DSP_1_4 = netlist.addInst("DSP48E2")
    DSP_1_5 = netlist.addInst("DSP48E2")
    DSP_1_6 = netlist.addInst("DSP48E2")
    DSP_1_7 = netlist.addInst("DSP48E2")
    DSP_1_8 = netlist.addInst("DSP48E2")
    DSP_1_9 = netlist.addInst("DSP48E2")
    DSP_2_1 = netlist.addInst("DSP48E2")
    DSP_2_2 = netlist.addInst("DSP48E2")
    DSP_2_3 = netlist.addInst("DSP48E2")
    DSP_2_4 = netlist.addInst("DSP48E2")
    DSP_2_5 = netlist.addInst("DSP48E2")
    DSP_2_6 = netlist.addInst("DSP48E2")
    DSP_2_7 = netlist.addInst("DSP48E2")
    DSP_2_8 = netlist.addInst("DSP48E2")
    DSP_2_9 = netlist.addInst("DSP48E2")

    # add connections

    # connect clock
    netlist.addConnection(URAM1, "CLKARDCLK", clk_net_idx)
    netlist.addConnection(URAM1, "CLKBWRCLK", clk_net_idx)
    netlist.addConnection(URAM2, "CLKARDCLK", clk_net_idx)
    netlist.addConnection(URAM2, "CLKBWRCLK", clk_net_idx)
    insts = [BRAM_1_1, BRAM_1_2, BRAM_1_3, BRAM_1_4, BRAM_2_1, BRAM_2_2, BRAM_2_3, BRAM_2_4,
             DSP_1_1, DSP_1_2, DSP_1_3, DSP_1_4, DSP_1_5, DSP_1_6, DSP_1_7, DSP_1_7, DSP_1_8,
             DSP_1_9, DSP_2_1, DSP_2_2, DSP_2_3, DSP_2_4, DSP_2_5, DSP_2_6, DSP_2_7, DSP_2_8, DSP_2_9]
    for inst in insts:
        netlist.addConnection(inst, "CLK", clk_net_idx)

    # connect datapath
    for i in range(30):  # urams to brams
        netlist.addConnection2(URAM1, "DOUTADOUT[" + str(i) + "]", BRAM_1_1, "ACIN[" + str(i) + "]")
        netlist.addConnection2(URAM1, "DOUTBDOUT[" + str(i) + "]", BRAM_2_1, "ACIN[" + str(i) + "]")
        netlist.addConnection2(URAM1, "DOUTADOUT[" + str(i) + "]", BRAM_1_2, "ACIN[" + str(i) + "]")
        netlist.addConnection2(URAM1, "DOUTBDOUT[" + str(i) + "]", BRAM_2_2, "ACIN[" + str(i) + "]")
    for i in range(18):  # cascade brams
        netlist.addConnection2(BRAM_1_2, "BCOUT[" + str(i) + "]", BRAM_1_3, "BCIN[" + str(i) + "]")
        netlist.addConnection2(BRAM_1_3, "BCOUT[" + str(i) + "]", BRAM_1_4, "BCIN[" + str(i) + "]")
        netlist.addConnection2(BRAM_2_2, "BCOUT[" + str(i) + "]", BRAM_2_3, "BCIN[" + str(i) + "]")
        netlist.addConnection2(BRAM_2_3, "BCOUT[" + str(i) + "]", BRAM_2_4, "BCIN[" + str(i) + "]")
    for i in range(8):  # dsps
        netlist.addConnection2(BRAM_1_1, "PCOUT[" + str(i) + "]", DSP_1_1, "A[" + str(i) + "]")
        netlist.addConnection2(BRAM_1_2, "PCOUT[" + str(i) + "]", DSP_1_1, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_1_1, "ACOUT[" + str(i) + "]", DSP_1_2, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_1_1, "BCOUT[" + str(i) + "]", DSP_1_2, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_1_1, "P[" + str(i) + "]",     DSP_1_2, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_1_2, "ACOUT[" + str(i) + "]", DSP_1_3, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_1_2, "BCOUT[" + str(i) + "]", DSP_1_3, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_1_2, "P[" + str(i) + "]",     DSP_1_3, "C[" + str(i) + "]")
        netlist.addConnection2(BRAM_1_3, "PCOUT[" + str(i) + "]", DSP_1_4, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_1_3, "BCOUT[" + str(i) + "]", DSP_1_4, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_1_3, "P[" + str(i) + "]",     DSP_1_4, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_1_4, "ACOUT[" + str(i) + "]", DSP_1_5, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_1_4, "BCOUT[" + str(i) + "]", DSP_1_5, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_1_4, "P[" + str(i) + "]",     DSP_1_5, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_1_5, "ACOUT[" + str(i) + "]", DSP_1_6, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_1_5, "BCOUT[" + str(i) + "]", DSP_1_6, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_1_5, "P[" + str(i) + "]", DSP_1_6, "C[" + str(i) + "]")
        netlist.addConnection2(BRAM_1_4, "PCOUT[" + str(i) + "]", DSP_1_7, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_1_6, "BCOUT[" + str(i) + "]", DSP_1_7, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_1_6, "P[" + str(i) + "]", DSP_1_7, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_1_7, "ACOUT[" + str(i) + "]", DSP_1_8, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_1_7, "BCOUT[" + str(i) + "]", DSP_1_8, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_1_7, "P[" + str(i) + "]", DSP_1_8, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_1_8, "ACOUT[" + str(i) + "]", DSP_1_9, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_1_8, "BCOUT[" + str(i) + "]", DSP_1_9, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_1_8, "P[" + str(i) + "]", DSP_1_9, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_1_9, "P[" + str(i) + "]", URAM2, "DINADIN[" + str(i) + "]")

        netlist.addConnection2(BRAM_2_1, "PCOUT[" + str(i) + "]", DSP_2_1, "A[" + str(i) + "]")
        netlist.addConnection2(BRAM_2_2, "PCOUT[" + str(i) + "]", DSP_2_1, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_2_1, "ACOUT[" + str(i) + "]", DSP_2_2, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_2_1, "BCOUT[" + str(i) + "]", DSP_2_2, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_2_1, "P[" + str(i) + "]", DSP_2_2, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_2_2, "ACOUT[" + str(i) + "]", DSP_2_3, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_2_2, "BCOUT[" + str(i) + "]", DSP_2_3, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_2_2, "P[" + str(i) + "]", DSP_2_3, "C[" + str(i) + "]")
        netlist.addConnection2(BRAM_2_3, "PCOUT[" + str(i) + "]", DSP_2_4, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_2_3, "BCOUT[" + str(i) + "]", DSP_2_4, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_2_3, "P[" + str(i) + "]", DSP_2_4, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_2_4, "ACOUT[" + str(i) + "]", DSP_2_5, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_2_4, "BCOUT[" + str(i) + "]", DSP_2_5, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_2_4, "P[" + str(i) + "]", DSP_2_5, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_2_5, "ACOUT[" + str(i) + "]", DSP_2_6, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_2_5, "BCOUT[" + str(i) + "]", DSP_2_6, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_2_5, "P[" + str(i) + "]", DSP_2_6, "C[" + str(i) + "]")
        netlist.addConnection2(BRAM_2_4, "PCOUT[" + str(i) + "]", DSP_2_7, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_2_6, "BCOUT[" + str(i) + "]", DSP_2_7, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_2_6, "P[" + str(i) + "]", DSP_2_7, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_2_7, "ACOUT[" + str(i) + "]", DSP_2_8, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_2_7, "BCOUT[" + str(i) + "]", DSP_2_8, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_2_7, "P[" + str(i) + "]", DSP_2_8, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_2_8, "ACOUT[" + str(i) + "]", DSP_2_9, "A[" + str(i) + "]")
        netlist.addConnection2(DSP_2_8, "BCOUT[" + str(i) + "]", DSP_2_9, "B[" + str(i) + "]")
        netlist.addConnection2(DSP_2_8, "P[" + str(i) + "]", DSP_2_9, "C[" + str(i) + "]")
        netlist.addConnection2(DSP_2_9, "P[" + str(i) + "]", URAM2, "DINBDIN[" + str(i) + "]")


    # fix brams
    netlist.fix_bram(BRAM_1_1)
    netlist.fix_bram(BRAM_1_2)
    netlist.fix_bram(BRAM_1_3)
    netlist.fix_bram(BRAM_1_4)
    netlist.fix_bram(BRAM_2_1)
    netlist.fix_bram(BRAM_2_2)
    netlist.fix_bram(BRAM_2_3)
    netlist.fix_bram(BRAM_2_4)




if __name__ == "__main__":
    netsFile = "design.nets"
    nodesFile = "design.nodes"
    fixFile = "design.pl"
    netlist = Netlist()
    buffer = netlist.addInst("BUFGCE")
    clk_net_idx = netlist.addConnection(buffer, "O")
    for i in range(80):
        create_conv(netlist, clk_net_idx)
    netlist.write_insts(nodesFile)
    netlist.write_connection(netsFile)
    # netlist.write_fixed_brams(fixFile)

