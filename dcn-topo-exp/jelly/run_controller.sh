#!/bin/bash
./pox/pox.py riplpox.riplpox --topo=jelly,seed=0,switches=16,nodes=4,ports_per_switch=4,hosts_per_switch=1 --routing=kshortest --mode=reactive
