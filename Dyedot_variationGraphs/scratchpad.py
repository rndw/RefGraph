nodedata = {}
for i in range(1, len(refpath) - 1):  # Has to start at one, else loopback in graph
    nw = (int(refpath[i + 1][1]) - int(refpath[i][1])) / 10
    if nw < 1.2:
        nw = 1.2

    nodedata[str(refpath[i - 1][1] + refpath[i - 1][2])] = ["label", str(refpath[i - 1][0] + ' ' + refpath[i - 1][1] + ' ' + refpath[i - 1][2]), "width", str(nw)]
    #p.edge(self.refpath[i - 1][1] + self.refpath[i - 1][2], self.refpath[i][1] + self.refpath[i][2])
