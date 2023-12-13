import time
import threading


def test(net):

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

    # check_ping_latency(c1, r0)
    # check_ping_latency(c1, r1)
    # check_ping_latency(c1, r2)
    # check_ping_latency(c1, r3)

    # check_ping_latency(c1, h1)
    # check_ping_latency(c1, h2)
    # check_ping_latency(c1, h3)
    # check_ping_latency(c1, h4)
    # check_ping_latency(c1, h5)
    # check_ping_latency(c1, h6)
    
    # Start the HTTP server on h1
    h1.sendCmd("python3 -m http.server 9000 &")

    # Testing multiple requests
    test_multiple_urls(c1, h1)

    # Start the max number of requests
    # test_max_nr_request(c1, h1)
    

    print("Running base test with only one server")
    c1.sendCmd("python3 client.py -p http 10.10.101.2:9000")

    # Wait for the client command to finish and retrieve its output
    output = c1.waitOutput()
    print("Client output:")
    print(output)

    print("Done")
    print("hint:Quit and check client_log.txt")
    return

def check_ping_latency(source, destination):
    result = source.cmd('ping -c 3', destination.IP())
    print(result)
    return

def test_max_nr_request(source, destination):
    iter = 1
    while True:
        source.sendCmd(f"python3 client.py -p http {destination.IP()}:9000")
        output = source.waitOutput()  # Wait for each command to complete before the next
        print(f"Request finished succesfully: #{iter}")
        iter = iter + 1
    return

def test_multiple_urls(source, destination):
    request_url = destination.IP() + ":9000"
    all_requests = " ".join([request_url] * 100)
    c1_run = "python3 client.py -p http " + all_requests
    source.sendCmd(c1_run);
    output = source.waitOutput()
    print(output)
    return
