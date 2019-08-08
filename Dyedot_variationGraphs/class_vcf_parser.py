class Vcft():

    def __init__(self,data):
        self.data = data

    def list_positions(self):
        return [_[1] for _ in self.data]

    def list_refs(self):
        return [_[2] for _ in self.data]

    def list_alts(self):
        return [_[3] for _ in self.data]



class ReadVcfs():

    def __init__(self,path):
        self.path = path

    def variant_builder(self):
        #self.path = path
        import os
        vcfdata = {}
        filename = ''
        sample = ''
        for file in [_ for _ in os.listdir(self.path) if _.endswith('.vcf')]:
            filename = file
            sample = filename.split(sep='.')[0]
            print(f'Adding variants from: {filename}\n')
            vcfdata[sample] = VariantList(self.path, filename, sample)
        return vcfdata



class VariantList():


    def __init__(self,path,filename,sample):
        self.path = path
        self.filename = filename
        self.sample = sample


    def vcf_reader(self):
        vals_vcf = ((self.path),(self.sample))
        varnum = ''
        with open(self.path+self.filename, 'r') as f:
            print(f'Reading in variants from {self.filename}')

            for line in f:
                varnum = line.split(sep='\t')[1:2]
                #print(f"Adding variant {varnum}")
                if line.startswith('#'):
                    continue
                else:

                    line_input = ((line.split(sep='\t')[:2] + line.split(sep='\t')[3:5]),)
                    vals_vcf = vals_vcf + ((line.split(sep='\t')[:2] + line.split(sep='\t')[3:5]),)

            return vals_vcf


    def number_of_variants(self):
        numberofvariants = len(self.vcf_reader()) - 2
        return numberofvariants


    def inspect_varaint(self,num):
        self.num = num

        try:
            return self.vcf_reader()[num+1]
        except IndexError:

            print(f'{self.num} not in range. Number of variants {self.number_of_variants()}')


    def list_positions(self):
        return [_[:2] for _ in self.vcf_reader()[2:]]


    def list_refs(self):
        return [_[2] for _ in self.vcf_reader()[2:]]


    def list_alts(self):
        return [_[3] for _ in self.vcf_reader()[2:]]



class VarGraphCons():

    def __init__(self):
        pass


    def anchor_builder(self,dat):
        self.dat = dat
        anchor_string = []

        graphdb = {}

        for key in list(dat.keys()):  # This function adds REFERENCE anchors - allowing merging back to reference positions
            data = dat[key].vcf_reader()
            chromosomes = list(set([_[0] for _ in data[2:]]))  # need to split into chromosomes to add anchors. Could pull chr lengths in from gff?
            print('Finished')
            rebuild_genome = ()
            for i in chromosomes:
                temp = [tuple((_), ) for _ in data[2:] if _[0] == i]  # split per chromosome - needed to add anchors
                temp = (tuple([temp[0][0], str(int(temp[0][1]) - 1), ' ', 'REF'], ),) + tuple(temp)  # add chr start anchor
                temp = tuple(temp) + (tuple([temp[len(temp) - 1][0], str(int(temp[len(temp) - 1][1]) + 1), ' ','REF']),)  # add chr end anchor
                anchors = ()

                for k in range(1, len(temp) - 1):
                    if int(temp[k][1]) + 1 != int(temp[k + 1][1]) and int(temp[k][1]) - 1 != int(temp[k - 1][1]):
                        anchor_string = tuple([temp[k][0], str(int(temp[k][1]) - 1), ' ', 'REF'])
                        anchors = tuple(anchors) + (((anchor_string)),)


                anchors = tuple(anchors) + tuple(temp)
                anchors = sorted(anchors)
                rebuild_genome = tuple(rebuild_genome) + tuple(anchors)  # (((anchors)),)
                with open(str(key + '_' + 'graph_anchors'), 'w') as f:  # write to file as backup
                    for i in range(0, len(rebuild_genome) - 1):
                        f.write(str(''.join(
                            f'{rebuild_genome[i][0]}\t{rebuild_genome[i][1]}\t{rebuild_genome[i][2]}\t{rebuild_genome[i][3]}\n')))  # convert tuple to string and write to file
            graphdb[key] = rebuild_genome
        return graphdb


class RegionOfInterestGraph():

    def __init__(self, output, loci):
        self.output = output
        self.loci = loci


    def region(self):
        rangebreak = 0
        for key in list(self.output.keys()):
            if int(max(self.output[key], key=lambda x: int(x[1]))[1]) > rangebreak:
                rangebreak = int(max(self.output[key], key=lambda x: int(x[1]))[1])
            if rangebreak < int(self.loci[1]):
                print(f'Region of interest start ({self.loci[1]}) larger than variant input ({rangebreak}).')
                print(f'Modifying range parameters from: {self.loci[0]}":"{self.loci[1]}"-"{self.loci[2]}')
                if int(rangebreak) > 5000:
                    self.loci[1] = int(rangebreak) - 5000 # Hardcoding here - not cool man
                    self.loci[2] = rangebreak
                else:
                    self.loci[1] = 0
                    self.loci[2] = rangebreak
                print(f'To new range: {self.loci[0]}":"{self.loci[1]}"-"{self.loci[2]}')

        print(self.loci)

        if self.loci[0] == "DEFAULT":
            print(f"Using first chromosome element in graph data: {self.output[list(self.output.keys())[1]][0][0]}")
            self.loci[0] = self.output[list(self.output.keys())[1]][0][0]
        if self.loci[0] != "DEFAULT" and self.loci[0] in set([_[0] for _ in list(self.output.values())[0]]):
            print(f'Limiting graph area to: {self.loci}')
        else:
            print(f'Supplied chromosome not in any vcf: {self.loci[0]}\nAvailable options are: {set([_[0] for _ in list(self.output.values())[0]])}\nDefaulting to first element: {self.output[list(self.output.keys())[1]][0][0]}')

            self.loci[0] = self.output[list(self.output.keys())[1]][0][0]
            print(self.loci)


    def referencegr(self):
        refpath = ()
        buildfullref = ()
        for key in self.output:  # Create a merged reference path
            for i in self.output[key]:
                if i[3] == 'REF' and i[0] == self.loci[0] and int(i[1]) >= int(self.loci[1]) and int(i[1]) <= int(self.loci[2]):
                    refpath = tuple(refpath) + (([i[0], i[1], i[3]]),)
                if i[3] != "REF" and i[0] == self.loci[0] and int(i[1]) >= self.loci[1] and int(i[1]) <= self.loci[2]:
                    refpath = tuple(refpath) + (([i[0], i[1], 'REF']),)
            refpath = sorted(tuple(set(tuple(_) for _ in refpath))) # Get rid of duplicated nodes. Then convert back to tuple for indexing
            refpath = sorted(refpath, key=lambda x: int(x[1]))
        return refpath
