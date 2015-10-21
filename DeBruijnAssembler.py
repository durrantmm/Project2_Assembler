'''
Created on Oct 8, 2015

@author: ErikCR
'''

import sys


inFile = open(sys.argv[1],'r') #inEulerianCycle.txt
outFile = open(sys.argv[2],'w')
k = int(sys.argv[3])
errorChecking = int(sys.argv[4])

def merge_nodes( nodes ):
    contig = nodes[ 0 ]
    for i in range( 1, len( nodes ) ):
        contig += nodes[ i ][ -1 ]
    return contig

def makeDebruijnGraph(kmerList,counts):
    deBrujinGraph = {}

    for kmer in kmerList:
    #print kmer
        left = kmer[ : -1 ]
        right = kmer[ 1 : ]

        if left in deBrujinGraph:
            deBrujinGraph[ left ].append( right )
        else:
            deBrujinGraph[ left ] = [ right ]
    
        if left in counts:
            counts[ left ][ 1 ] += 1
        else:
            counts[ left ] = [ 0, 1 ]

        if right in counts:
            counts[ right ][ 0 ] += 1
        else:
            counts[ right ] =[ 1, 0 ]

    return deBrujinGraph

def makeNonBranchingPath(startNode,deBrujinGraph,contigList):
    
    currentNode = startNode
    while len(deBrujinGraph) > 0:
        #print contigList[-1]
        contigList[-1].append(deBrujinGraph[currentNode][0]) # not possible for non branching path to have mutiple edges
        #print deBrujinGraph[currentNode]
        if deBrujinGraph[currentNode][0] in non_branching: # non_branching is global
            del deBrujinGraph[currentNode]
        else:
            del deBrujinGraph[currentNode]
            break
        currentNode = contigList[-1][-1]
        

def makeContig(deBrujinGraph, non_branching):

    contigList = []
    
    while len(deBrujinGraph) >0:
        
            for node in deBrujinGraph:
            
                nodeVisit = [node]
                currentNode = node
                nSize = len(deBrujinGraph[currentNode])
                nodeVisit.append(deBrujinGraph[currentNode][0]) # grabbing first adjacent node

                if node in non_branching: # or outdegree is 1 and indegree is atleast one
                    continue
        
                elif len(deBrujinGraph[currentNode]) > 1 : # if multiple edge pick first one to remove leave rest
                    #print deBrujinGraph[currentNode][nSize-1:]
                    deBrujinGraph[currentNode] = deBrujinGraph[currentNode][nSize-1:]
                    break
                        
                else:
                    del deBrujinGraph[currentNode]
                    break   
            
                if nodeVisit[-1] in deBrujinGraph: # check to see if you've visited this edge of Node if you haven't follow it
                    currentNode = nodeVisit[-1]
                else:
                    break
                    #print nodeVisit

            contigList.append(nodeVisit)
            if nodeVisit[-1] in non_branching:
                makeNonBranchingPath(nodeVisit[-1],deBrujinGraph,contigList)
    return contigList

kmerDict = {}
nodeDegreeDict = {}
kmerSet = set()

for seq in inFile:
    seq = seq.strip()
    if seq[0] != ">":
        for i in range(len(seq)):
            if i + k < len(seq) + 1:
                kmer = seq[i:i+k]
                kmerDict[kmer] = kmerDict[kmer] + 1 if kmerDict.has_key(kmer) else 1
                if errorChecking > 0: # means no checking for errors
                    if kmerDict[kmer] > errorChecking:
                        kmerSet.add(kmer)
                else:
                    kmerSet.add(kmer)
#print kmerDict

deBrujinGraph = makeDebruijnGraph(kmerSet, nodeDegreeDict)
#print deBrujinGraph

non_branching = set()
contigs = []

for key, item in nodeDegreeDict.iteritems():
    if item[ 0 ] == 1 and item[ 1 ] == 1:
        non_branching.add( key ) 
        
contigs = makeContig(deBrujinGraph, non_branching)

strContigList = ""
for contig in contigs:
    strContigList += merge_nodes(contig) + "\n"

outFile.write(strContigList)


inFile.close()
outFile.close()
