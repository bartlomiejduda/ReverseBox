# TODO - refactor this
# fmt: off
def unswizzle_psvita(writebuf, readbuf, writeoffset, segwidth, segheight, datawidth):
    global readoffset, buffer
    xy = False  # set to false for yx swizzle order
    if segwidth == 2 and segheight == 2:
        if xy:
            writebuf[writeoffset:writeoffset + 2] = readbuf[readoffset:readoffset + 2]
            writebuf[writeoffset + datawidth:writeoffset + datawidth + 2] = readbuf[readoffset + 2:readoffset + 4]
        else:
            writebuf[writeoffset] = readbuf[readoffset]
            writebuf[writeoffset + datawidth] = readbuf[readoffset + 1]
            writebuf[writeoffset + 1] = readbuf[readoffset + 2]
            writebuf[writeoffset + datawidth + 1] = readbuf[readoffset + 3]
        readoffset += 4
    else:
        if xy:
            unswizzle_psvita(writebuf, readbuf, writeoffset, segwidth // 2, segheight // 2, datawidth)
            unswizzle_psvita(writebuf, readbuf, writeoffset + segwidth // 2, segwidth // 2, segheight // 2, datawidth)
            unswizzle_psvita(writebuf, readbuf, writeoffset + datawidth * (segheight // 2), segwidth // 2, segheight // 2, datawidth)
            unswizzle_psvita(writebuf, readbuf, writeoffset + datawidth * (segheight // 2) + segwidth // 2, segwidth // 2, segheight // 2, datawidth)
        else:
            unswizzle_psvita(writebuf, readbuf, writeoffset, segwidth // 2, segheight // 2, datawidth)
            unswizzle_psvita(writebuf, readbuf, writeoffset + datawidth * (segheight // 2), segwidth // 2, segheight // 2, datawidth)
            unswizzle_psvita(writebuf, readbuf, writeoffset + segwidth // 2, segwidth // 2, segheight // 2, datawidth)
            unswizzle_psvita(writebuf, readbuf, writeoffset + datawidth * (segheight // 2) + segwidth // 2, segwidth // 2, segheight // 2, datawidth)
# fmt: on
