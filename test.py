import time

def test(net):
    # on first server start the listener
    net.get("h1").sendCmd("python3 -m http.server 9000 &")
    
    # Start the client
    net.get("c1").sendCmd("python3 client.py -p http 10.10.101.2:9000 &")

    print("Running base test with only one server")

    time.sleep(4)
    
    # Wait for the client command to finish and retrieve its output
    output = net.get("c1").waitOutput()
    print("Client output:")
    print(output)

    print("Done")
    print("hint:Quit and check client_log.txt")
    return
