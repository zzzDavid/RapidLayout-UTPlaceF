"""
 generate architecture file: design.scl

"""


def write_site(filename, sitename, primitive, quantity):
    with open(filename, 'a+') as f:
        f.write("SITE " + sitename + "\n")
        f.write("  " + primitive + " " + str(quantity) + "\n")
        f.write("END SITE\n\n")

def write_sites(filename, sitename, primitives, quantities):
    with open(filename, 'a+') as f:
        f.write("SITE " + sitename + "\n")
        for i, p in enumerate(primitives):
            quantity = quantities[i]
            f.write("  " + p + " " + str(quantity) + "\n")
        f.write("END SITE\n\n")


def write_resources(filename):
    with open(filename, 'a+') as f:
        f.write("RESOURCES\n")
        f.write("  LUT LUT1 LUT2 LUT3 LUT4 LUT5 LUT6\n")
        f.write("  FF  FDRE\n")
        f.write("  CARRY8 CARRY8\n")
        f.write("  DSP48E2 DSP48E2\n")
        f.write("  RAMB36E2 RAMB36E2\n")
        # f.write("  URAM288 URAM288\n")
        f.write("  IO IBUF OBUF BUFGCE\n")
        f.write("END RESOURCES\n\n")


def write_sitemap(filename):
    """
        SLICE = 0, DSP (DSP48E2 and RAMB18E2) = 1, BRAM (URAM288) = 2, IO = 3
    """
    # DSP48E2 and BRAM18E2
    DSP = [1, 4, 5, 6, 8, 10, 11, 13, 15, 16, 17, 18, 21, 22, 24, 26, 28, 30,
           31, 33, 35, 37, 38, 39, 40, 42,44, 45, 46, 47, 48, 51, 2, 3, 7, 12,
           14, 19, 20, 25, 27, 32, 34, 41, 49, 50]
    sorted(DSP)
    # URAM288
    BRAM = [9, 23, 29, 36, 43]

    for i, v in enumerate(DSP): DSP[i] = v * 2
    for i, v in enumerate(BRAM): BRAM[i] = v * 2
    IO = [0, 51]

    # how many elements in each column we need?
    # we need 5 * 32 = 160 URAMs
    height = 160
    label = []
    length = max(DSP) + 1
    for i in range(length):
        if i in DSP:
            label.append(1)
        elif i in BRAM:
            label.append(2)
        elif i in IO:
            label.append(3)
        else:
            label.append(0)

    with open(filename, 'a+') as f:
        f.write("SITEMAP " + str(length) + " " + str(height) + "\n")
        for i in range(length):
            # i is column index
            if label[i] is 0:
                # print a column of SLICE
                for j in range(height):
                    f.write(str(i) + " " + str(j) + " SLICE\n")

            elif label[i] is 1:
                # print a column of DSP
                for j in range(0, height, 10):
                    f.write(str(i) + " " + str(j) + " DSP\n")
                    f.write(str(i) + " " + str(j + 2) + " DSP\n")
                    f.write(str(i) + " " + str(j + 5) + " DSP\n")
                    f.write(str(i) + " " + str(j + 7) + " DSP\n")

            elif label[i] is 2:
                # print a column of BRAM
                for j in range(0, height, 5):
                    f.write(str(i) + " " + str(j) + " BRAM\n")

            else:
                # print a column of IO
                for j in range(0, height, 60):
                    f.write(str(i) + " " + str(j) + " IO\n")

        f.write("END SITEMAP\n\n")

if __name__ == "__main__":
    f = "design.scl"
    write_sites(f, "SLICE", ["LUT", "FF", "CARRY8"], [16, 16, 1])
    write_site(f, "DSP", "DSP48E2", 1)
    write_site(f, "BRAM", "RAMB36E2", 1)
    write_site(f, "IO", "IO", 64)
    write_resources(f)
    write_sitemap(f)
