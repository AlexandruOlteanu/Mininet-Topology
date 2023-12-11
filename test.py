import time
import threading


def test(net):
    # Get hosts h1 and h2

    #command unit
    c1 = net.get("c1")

    #routers
    r0 = net.get("r0")
    r1 = net.get("r1")
    r2 = net.get("r2")
    r3 = net.get("r3")

    # hosts
    h1 = net.get("h1")
    h2 = net.get("h2")
    h3 = net.get("h3")
    h4 = net.get("h4")
    h5 = net.get("h5")
    h6 = net.get("h6")

    check_ping_latency(c1, r0)
    check_ping_latency(c1, r1)
    check_ping_latency(c1, r2)
    check_ping_latency(c1, r3)

    check_ping_latency(c1, h1)
    check_ping_latency(c1, h2)
    check_ping_latency(c1, h3)
    check_ping_latency(c1, h4)
    check_ping_latency(c1, h5)
    check_ping_latency(c1, h6)
    
    # Start the HTTP server on h1
    h1.sendCmd("python3 -m http.server 9000 &")

    # Start the client on c1
    c1 = net.get("c1")
    c1.sendCmd("python3 client.py -p http 10.10.101.2:9000 &")

    print("Running base test with only one server")
    time.sleep(4)

    # Wait for the client command to finish and retrieve its output
    output = net.get("c1").waitOutput()
    print("Client output:")
    print(output)

    print("Done")
    print("hint:Quit and check client_log.txt")
    return

def check_ping_latency(source, destination):
    result = source.cmd('ping -c 3', destination.IP())
    print(result)
    return
