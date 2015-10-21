###### ALL CREDIT GOES TO STANLEY FOR THIS ONE. I WAS ABSENT WHEN WE COVERED THIS AND I REALLY COULDN'T
###### FIGURE IT OUT WITHOUT THIS CODE

import sys

class Assembler:

    def __init__(self):
        self.graph = {}
        self.counts = {}
        self.edge_count = 0

        self.non_branching = set()
        self.contigs = []

    def load_kmers(self, kmers, k):
        all_kmers = []
        for kmer in kmers:
            kmer_comp = sorted([kmer[pos:pos+k] for pos in range(len(kmer)) if len(kmer[pos:pos+k]) == k])
            all_kmers += kmer_comp

        for kmer in all_kmers:
            left = kmer[:-1]
            right = kmer[1:]
            self.edge_count += 1

            if left in self.graph:
                self.graph[left].append(right)
            else:
                self.graph[left] = [right]

            if left in self.counts:
                self.counts[left][1] += 1
            else:
                self.counts[left] = [0, 1]

            if right in self.counts:
                self.counts[right][0] += 1
            else:
                self.counts[right] =[1, 0]

    def get_contig(self, start, g):

        path = [start]
        cur_node = start

        while len(cur_node) > 0:
            next_node = g[cur_node][0]
            del g[cur_node][0]

            self.edge_count -= 1

            if next_node in self.non_branching:
                path.append(next_node)
                cur_node = next_node
                continue
            else:
                path.append(next_node)
                break

        return path

    def merge_nodes(self, nodes):
        contig = nodes[0]
        for i in range(1, len(nodes)):
            contig += nodes[i][-1]
        return contig

    def has_outgoing(self, node):
        if len(g[node]) > 0:
            return True
        else:
            return False

    def find_all_contigs(self, kmers, k):
        self.load_kmers(kmers, k)
        for key, item in self.counts.iteritems():
            if item[0] == 1 and item[1] == 1:
                self.non_branching.add(key)
        start = self.graph.keys()[0]

        while self.edge_count > 0:
            for i in self.graph.keys():
                if i in self.non_branching or len(self.graph[i]) == 0:
                    continue
                start = i
                break
            c = self.get_contig(start, self.graph)
            self.contigs.append(c)

        for contig in self.contigs:
            print self.merge_nodes(contig),

if __name__ == "__main__":
    kmers = []
    with open(sys.argv[1]) as fh:
        for line in fh:
            if not line[0] == ">":
                kmers.append(line.strip())

    assembler = Assembler()

    assembler.find_all_contigs(kmers, 10)