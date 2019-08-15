from random import randint
from graphviz import Digraph
import seaborn as sns

class RefGraphBuilder():

    def __init__(self):
        pass

    def referencepath(self,refpath):
        self.refpath = refpath
        p = Digraph(name='REFERENCE', node_attr={'shape': 'cds', 'color': 'black', 'fillcolor': 'grey', 'fixedsize':'true'}, format='png',graph_attr={'splines': 'spline', 'rankdir': 'LR'},engine='dot',edge_attr={'arrowhead': 'vee', 'arrowsize': '0.5', 'color': 'black','penwidth':'2'})
        nw = 0
        nodedata = {}
        for i in range(1, len(self.refpath) - 1):  # Has to start at one, else loopback in graph
            nw = (int(refpath[i+1][1]) - int(refpath[i][1])) / 10
            if nw < 1.2:
                nw = 1.2
            ##### Return a dictionary of node attr to work with - interactive plotting
            nodedata[str(self.refpath[i - 1][1] + self.refpath[i - 1][2])] = ["label", str(self.refpath[i - 1][0] + ' ' + self.refpath[i - 1][1] + ' ' + self.refpath[i - 1][2]), "width", str(nw)]
            #####
            p.node(self.refpath[i - 1][1] + self.refpath[i - 1][2],label=str(self.refpath[i - 1][0] + ' ' + self.refpath[i - 1][1] + ' ' + self.refpath[i - 1][2]), width = str(nw))
            #### NEED TO ADD FOR EDGES AS WELL
            p.edge(self.refpath[i - 1][1] + self.refpath[i - 1][2], self.refpath[i][1] + self.refpath[i][2])

        p.node(self.refpath[len(self.refpath) - 1][1] + self.refpath[len(self.refpath) - 1][2],label=str(self.refpath[len(self.refpath) - 1][0] + ' ' + self.refpath[len(self.refpath) - 1][1] + ' ' + self.refpath[len(self.refpath) - 1][2]))
        p.node(self.refpath[len(self.refpath) - 2][1] + self.refpath[len(self.refpath) - 2][2],label=str(self.refpath[len(self.refpath) - 2][0] + ' ' + self.refpath[len(self.refpath) - 2][1] + ' ' + self.refpath[len(self.refpath) - 2][2]))
        p.edge(self.refpath[len(self.refpath) - 2][1] + self.refpath[len(self.refpath) - 2][2],
               self.refpath[len(self.refpath) - 1][1] + self.refpath[len(self.refpath) - 1][2])

        p.node(str('REF'), label=str('Reference'),  width = '1.6')
        p.node(str('REF_'), label=str('Path'))
        p.edge('REF', 'REF_')

        #print(nodedata)
        return p, nodedata;

    def variantpath(self, output,graph,loci,refpath):

        self.output = output
        self.graph = graph
        self.loci =loci
        self.refpath = refpath

        colour = sns.color_palette("colorblind", desat=.5) + sns.color_palette("Set1", n_colors=8, desat=.5)
        del colour[7:9]
        colour = sns.color_palette(colour)
        colour = colour.as_hex()

        ## newvar
        allvar = {}
        testref = [list(elem) for elem in refpath]
        ## newvar

        for key in self.output:
            varpath = ()
            for i in self.output[key]:
                if i[0] == self.loci[0] and int(i[1]) >= self.loci[1] and int(i[1]) <= self.loci[2]:
                    varpath = sorted(
                        tuple(varpath) + (([i[0], i[1], i[3]]),))  # have to convert to int for sort - see refpath
                    varpath = sorted(varpath, key=lambda x: int(x[1]))
            ## newvar
            nw = 0
            temp = []
            matching = []
            ## newvar

            x = Digraph(name=key, node_attr={'shape': 'cds', 'color': colour[randint(0, len(colour) - 1)],'fillcolor': colour[randint(0, len(colour) - 1)]} , engine='dot',edge_attr={'arrowhead': 'vee', 'arrowsize': '0.5', 'color': colour[randint(0, len(colour) - 1)],'penwidth':'4'})  # colour can also be set to use x11 names 'red'

            for i in range(1, len(varpath) - 1):
                # if output[key][i][0] == loci[0] and int(output[key][i][1]) >= loci[1] and int(output[key][i][1]) <= loci[2]:

                nw = (int(varpath[i+1][1]) - int(varpath[i][1])) / 10
                if nw < 1.2: # have to include a maximum node size as well
                    nw = 1.2
                if varpath[i - 1] in testref:
                    x.node(varpath[i - 1][1] + varpath[i - 1][2],label=str(varpath[i - 1][0] + ' ' + varpath[i - 1][1] + ' ' + varpath[i - 1][2]), width=str(nw))
                    matching = list(filter(lambda k: varpath[i] in allvar[k], allvar.keys()))
                    if matching: # exit pathways to a reference node
                        matching.append(key)
                        x.edge(varpath[i - 1][1] + varpath[i - 1][2], varpath[i][1] + varpath[i][2], label=str(' - '.join(matching)), color='black', style='dotted')
                        matching = []
                    else:
                        x.edge(varpath[i - 1][1] + varpath[i - 1][2], varpath[i][1] + varpath[i][2], label=str(key))

                else:
                    x.node(varpath[i - 1][1] + varpath[i - 1][2],label=str(varpath[i - 1][0] + ' ' + varpath[i - 1][1] + ' ' + varpath[i - 1][2]),width=str(nw))
                    matching = list(filter(lambda k: varpath[i] in allvar[k], allvar.keys()))
                    if matching:  ####################
                        matching.append(key)

                        x.edge(varpath[i - 1][1] + varpath[i - 1][2], varpath[i][1] + varpath[i][2],label=str(' - '.join(matching)), color='black', style='dotted')
                        matching = []
                    else:
                        x.edge(varpath[i - 1][1] + varpath[i - 1][2], varpath[i][1] + varpath[i][2], label=str(key))


            x.node(varpath[len(varpath) - 1][1] + varpath[len(varpath) - 1][2], label=str(varpath[len(varpath) - 1][0] + ' ' + varpath[len(varpath) - 1][1] + ' ' + varpath[len(varpath) - 1][2]))
            x.node(varpath[len(varpath) - 2][1] + varpath[len(varpath) - 2][2], label=str(varpath[len(varpath) - 2][0] + ' ' + varpath[len(varpath) - 2][1] + ' ' + varpath[len(varpath) - 2][2]))
            x.edge(varpath[len(varpath) - 2][1] + varpath[len(varpath) - 2][2],varpath[len(varpath) - 1][1] + varpath[len(varpath) - 1][2])

            x.node(str(key), label=str(key))
            x.node(str(key + '_'), label=str('Path'))
            x.edge(str(key), str(key + '_'))

            temp = [_ for _ in varpath if _[2] != 'REF']
            allvar[key] = temp

            self.graph.subgraph(x)
        return graph