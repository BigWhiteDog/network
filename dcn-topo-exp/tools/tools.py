from mininet.topo import MultiGraph
from copy import deepcopy
import subprocess
import random
import re

def __xThrput(stream):
    while True:
        line = stream.readline()
        res = re.match(r"^.*?([0-9\.]*)\sMbits/sec.*", line)
        if res:
            return float(res.group(1))
            
"""
@param: net, Mininet Class
"""
def iperfTest(net, pairs = 1):
    print "iperfTest-------------------------------------------------START"
    hosts = net.hosts
    number = pairs
    server = random.sample(hosts, number)
    client = random.sample(filter(lambda x: x not in server, hosts), number)
    #server = hosts[0:2]
    #client = hosts[2:4]
    serverTasks = {}
    clientTasks = {}
    avgThrput = 0.0
    for s in server:
        serverTasks[s] = s.popen("iperf -s -u -f m", stdout=subprocess.PIPE, shell=True)
    for i in range(0, len(client)):
        c = client[i]
        s = server[i]
        print "C (%s) -----> S (%s)" % (c, s)
        clientTasks[c] = c.popen("iperf -c " + s.IP() + " -u -t 10 -b 100m -f m", stdout=subprocess.PIPE, shell=True)
    for h, t in clientTasks.iteritems():
        t.wait()
    for h, t in serverTasks.iteritems():
        thrput = __xThrput(t.stdout)
        avgThrput  += thrput / number
        print "S <%s> throughput: %.2f Mbps" % (h, thrput)
        t.kill()
    print "Average Throughput: %.2f Mbps" % avgThrput
    print "Aggregated Throughput: %.2f Mbps" % (avgThrput * number)
    print "iperfTest-------------------------------------------------FINISH"
        

"""
@param: mg, Topo.g (MultiGraph member of Topo Class)
"""
def minCut(mg):
    adjList = deepcopy(mg.edge)
    #remove all host related edge
    for k, v in adjList.items():
        if mg.node[k].get("isSwitch", False) == False:
            del adjList[k]
            continue
        for vert, attr in v.items():
            if mg.node[vert].get("isSwitch", False) == False:
                del adjList[k][vert]
    comb = {}
    mincut = 0xffffffff
    for i in range(0, len(adjList) - 1):
        s, t, ans = __contract(adjList, comb)
        comb[t] = 1
        if mincut > ans:
            mincut = ans
        if mincut == 0:
            break
        for vert, attr in adjList[t].iteritems():
            capa = attr[1].get("bw", 1)
            if not comb.get(vert):
                adjList[s].setdefault(vert, {1:{}})
                adjList[s][vert][1]["bw"] = adjList[s][vert][1].get("bw", 0) + capa
                adjList[vert][s] = adjList[s][vert]
    return mincut
    

def __contract(adjList, comb):
    visit = {}
    weight = {}
    s = t = None
    update = None
    for k1 in adjList:
            mmax = -1
            temp = None
            for k2 in adjList:
                if not comb.get(k2) and not visit.get(k2) and weight.get(k2, 0) > mmax:
                    temp = k2
                    mmax = weight.get(k2, 0)
            if temp == None:
                break
            s, t = t, temp
            update = mmax
            visit[t] = 1
            for vert, attr in adjList[t].iteritems():
                capa = attr[1].get("bw", 1)
                if not comb.get(vert) and not visit.get(vert):
                    weight[vert] = weight.get(vert, 0) + capa
    return s, t, update
