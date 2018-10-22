# Multipoint sender

```
usage: smt [-h] (-sf FILE NAME | -stdi | -s) [-df FILE NAME]
           [-H IP:PORT [IP:PORT ...]] [-m MSS] [-p PORT] [-fs MB] [-st]

Simple multipoint transmission.

optional arguments:
  -h, --help            show this help message and exit
  -sf FILE NAME, --sfile FILE NAME
                        path to source file
  -stdi, --std-input    use standard input as input (pipe before s required)
  -s, --server          use input socket as input
  -m MSS, --mss MSS     max segment size
  -p PORT, --port PORT  Port address to receive data from remote host
  -fs MB, --filesize MB
                        Size of transmitted data
  -st, --statistics     Show statistics and progress

possible actions (at least one is required):
  -df FILE NAME, --dfile FILE NAME
                        path to destination file
  -H IP:PORT [IP:PORT ...], --hosts IP:PORT [IP:PORT ...]
                        destination hosts
```

## Four-step chain
One producer which reads the data from a file and send it throug the network to another hosts in a chain manner. Relay host get the packet, write it on the disk and forward it to the second host.  
<p align="center">
    <img src="https://mntw.github.io/multipoint-sender/demo-chain.svg">
</p>

One producer which sends data to many consumers. Consumer could be another multisend process or nc as in the demo.
<p align="center">
    <img src="https://mntw.github.io/multipoint-sender/demo-multipoint.svg">
</p>
