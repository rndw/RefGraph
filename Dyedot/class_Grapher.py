from random import randint
from graphviz import Digraph
import seaborn as sns

class RefGraphBuilder():
    '''
    PRIMARY DOT FILE CONSTRUCTOR
    INPUT: REFERENCEPATH OBJECT LIMITED BY RANGE; DICT KEY:VALUE (+ ANCHORS) PAIRS FOR VARIANTS
    OUTPUT: GRAPH STRUCTURE IN DOT FORMAT
    '''

    def __init__(self):
        pass

    def referencepath(self, refpath):
        '''

        :param refpath:
        :return:
        '''
        self.refpath = refpath

        #CONSTRUCT BASE GRAPH ATTRIBUTES
        #COLOUR SET TO GREY/BLACK - HARD CODED
        p = Digraph(name='REFERENCE', node_attr={'shape': 'box', 'color': 'black', 'fillcolor': 'grey'}, format='png', graph_attr={'splines': 'spline', 'rankdir': 'LR'}, edge_attr={'arrowhead': 'vee', 'arrowsize': '0.5', 'color': 'black'})
        p.graph_attr['rankdir'] = 'LR'

        for i in range(1, len(self.refpath) - 1):  # Has to start at one, else loopback in graph

            #ADD NODES FOR EACH POSITION, AVOIDING INDEXING ERROR. BIND NODES WITH EDGES.
            p.node(self.refpath[i - 1][1] + self.refpath[i - 1][2],
                   label=str(self.refpath[i - 1][0] + ':' + self.refpath[i - 1][1] + ' ' + self.refpath[i - 1][2]))
            p.edge(self.refpath[i - 1][1] + self.refpath[i - 1][2], self.refpath[i][1] + self.refpath[i][2])

        #SPECIAL CASE NODES AND EDGES
        p.node(self.refpath[len(self.refpath) - 1][1] + self.refpath[len(self.refpath) - 1][2],
               label=str(self.refpath[len(self.refpath) - 1][0] +':' + self.refpath[len(self.refpath) - 1][1] + ' ' + self.refpath[len(self.refpath) - 1][2]))
        p.node(self.refpath[len(self.refpath) - 2][1] + self.refpath[len(self.refpath) - 2][2],
               label=str(self.refpath[len(self.refpath) - 2][0] +':' + self.refpath[len(self.refpath) - 2][1] + ' ' + self.refpath[len(self.refpath) - 2][2]))
        p.edge(self.refpath[len(self.refpath) - 2][1] + self.refpath[len(self.refpath) - 2][2],
               self.refpath[len(self.refpath) - 1][1] + self.refpath[len(self.refpath) - 1][2])

        #ADD COLOUR REFERENCE TO START OF PATH
        p.node(str('REF'), label=str('Reference'))
        p.node(str('REF_'), label=str('Path'))
        p.edge('REF', 'REF_')

        return p

    def variantpath(self, output, graph, loci):
        '''
        #SAME AS REFERENCE PATH. ADDITIONALLY, REQUIRES LOCI RANGE SPECIFICATION OBJECT TO LIMIT GRAPHS
        :param output:
        :param graph:
        :param loci:
        :return:
        '''

        self.output = output
        self.graph = graph
        self.loci = loci

        #COLOURBLIND PALETTE CONSTRUCTED. DESATURATED.
        colour = sns.color_palette("colorblind", desat=.5) + sns.color_palette("Set1", n_colors=8, desat=.5)
        del colour[7:9] #REMOVE YELLOW. TERRIBLE COLOUR. REMOVE GREY, CONFUSION WITH REFERENCE.
        colour = sns.color_palette(colour)
        colour = colour.as_hex()

        for key in self.output:

            varpath = ()

            for i in self.output[key]:

                if i[0] == self.loci[0] and int(i[1]) >= self.loci[1] and int(i[1]) <= self.loci[2]:
                    varpath = sorted(
                        tuple(varpath) + (([i[0], i[1], i[3]]),))  # have to convert to int for sort - see refpath
                    varpath = sorted(varpath, key=lambda x: int(x[1])) #INPUT NEEDS TO BE SORTED ACCORDING TO POSITION

            #CONSTRUCT BASE VARIANT PATH ATTRIBUTES.
            #COLOURSCHEME CHOSEN AT RANDOM. NB! THERE IS A CHANCE THAT PATHS WOULD HAVE SIMILAR SCHEMES - OR SCHEMES DIFFICULT TO DIFFERENTIATE FROM EACH OTHER.
            #THIS IS A MAJOR CONCERN - NEEDS ATTENTION.
            #COULD USE SET.SEED AND BUILD SCHEME WITH MAXIMAL DIVERGENCE
            #PRE-ALLOCATE COLOUR SCHEME AND CHECK IF OVERLAP, IF OVERLAP, PRODUCE NEW SCHEME, ELSE, BREAK AND LIMIT SAMPLES?
            x = Digraph(name=key, node_attr={'shape': 'box', 'color': colour[randint(0, len(colour) - 1)], 'fillcolor': colour[randint(0, len(colour) - 1)]}, edge_attr={'arrowhead': 'vee', 'arrowsize': '0.5', 'color': colour[randint(0, len(colour) - 1)]})  # colour can also be set to use x11 names 'red'
            x.graph_attr['rankdir'] = 'LR'

            for i in range(1, len(varpath) - 1):

                x.node(varpath[i - 1][1] + varpath[i - 1][2],
                       label=str(varpath[i - 1][0] + ':' + varpath[i - 1][1] + ' ' + varpath[i - 1][2]))
                x.edge(varpath[i - 1][1] + varpath[i - 1][2], varpath[i][1] + varpath[i][2])

            x.node(varpath[len(varpath) - 1][1] + varpath[len(varpath) - 1][2], label=str(varpath[len(varpath) - 1][0] +':' + varpath[len(varpath) - 1][1] +' ' + varpath[len(varpath) - 1][2]))
            x.node(varpath[len(varpath) - 2][1] + varpath[len(varpath) - 2][2], label=str(varpath[len(varpath) - 2][0] +':' + varpath[len(varpath) - 2][1] +' ' + varpath[len(varpath) - 2][2]))
            x.edge(varpath[len(varpath) - 2][1] + varpath[len(varpath) - 2][2], varpath[len(varpath) - 1][1] + varpath[len(varpath) - 1][2])

            x.node(str(key), label=str(key))
            x.node(str(key + '_'), label=str('Path'))
            x.edge(str(key), str(key + '_'))

            self.graph.subgraph(x)
        return graph
