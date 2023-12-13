# II. Evaluation - System Limits Analysis


Ping reference

c1 -> r0  => 0.092 ms  0% packet loss

ASIA ->
    c1 -> r1 => 38.074 ms 1% packet loss
    c1 -> h1 => 69.084 ms 9% packet loss
    c1 -> h2 => 67.94 ms 11% packet loss

EMEA -> 
    c1 -> r2 => 0.118 ms 0% packet loss
    c1 -> h3 => 77.75 ms 0% packet loss
    c1 -> h4 => 68.387 ms 0% packet loss

US -> 
    c1 -> r3 => 20.493 ms 0% packet loss
    c1 -> h5 => 92.876 ms 0% packet loss
    c1 -> h6 => 98.613 ms 6% packet loss


#        a) How many requests can be handled by a single machine?
I managed to add a new function to test.py "test_max_nr_request" which is sending 
continousely requests from source to destination and outputs a succes message after
each one. I tested sending requests from the client to h1 and after the 306 request
I waited for several minutes but the request 307 was not completed. So in conclusion
the maximum number of requests that a machine can process is 306.

#        b) What is the latency of each region?

ASIA -> Average latency of 68,084 ms
EMEA -> Average latency of 73.0685
US -> Average latency of 95.7445


#        c) What is the server path with the smallest response time? But the slowest?

The fastest server path is c1 -> h2 with a lattency of 67.94 ms while
the slowest one is c1 -> h6 with a latency of 98.613 ms


#        d) What is the path that has the greatest loss percentage?

The path with the greatest loss percentage is c1 -> h2 with a 11% packet loss

#        e) What is the latency introduced by the first router in our path?

The latency of the first router is of 0.092 ms

#        f) Is there any bottleneck in the topology? How would you solve this issue?

        Based on the provided latency and packet loss data, there are indications of potential bottlenecks in the network topology. Here's an analysis of potential bottlenecks and how to address them:

    Latency Bottleneck: The US region exhibits the highest average latency, with an average latency of approximately 95.7445 ms. This suggests that there may be a latency bottleneck when communicating with the US region. To address this, the following solutions can be considered:
        Optimized Routing: Analyze and optimize the routing paths to reduce latency. This may involve choosing more efficient routes, optimizing the configuration of routers, or implementing Quality of Service (QoS) to prioritize traffic.
        Increased Bandwidth: Upgrade the network infrastructure to provide higher bandwidth, especially for the US region, to reduce congestion and decrease latency.
        Content Distribution: Implement content distribution networks (CDNs) or edge computing to bring content closer to end-users in the US region, reducing the need for data to traverse long distances.

    Packet Loss Bottleneck: The communication path to host h2 in the ASIA region experiences a high packet loss rate of 11%. This indicates a potential bottleneck in terms of packet loss. To mitigate packet loss, consider the following solutions:
        Network Monitoring: Implement network monitoring tools to identify and address the specific cause of packet loss, whether it's due to network congestion, hardware issues, or other factors.
        Quality of Service (QoS): Implement QoS policies to prioritize critical traffic and reduce packet loss for important applications.
        Redundancy: Introduce redundancy in network paths to ensure that if one path experiences packet loss, traffic can be rerouted through an alternate path.

    Load Distribution Bottleneck: The varying latencies and packet loss rates suggest an imbalance in load distribution across the network components. To address load distribution issues:
        Load Balancing: Implement load balancing mechanisms to evenly distribute traffic across network paths and prevent overloading of specific components.
        Capacity Planning: Conduct capacity planning to ensure that network components can handle the expected traffic load, especially during peak usage times.

    Scaling Bottleneck: As the network grows, it may face scalability challenges. To ensure scalability:
        Scalable Architecture: Design the network with scalability in mind, allowing for easy expansion by adding additional routers, switches, and capacity as needed.
        Traffic Engineering: Continuously monitor traffic patterns and adjust network configurations to accommodate increased demand.


#        g) What is your estimation regarding the latency introduced?
        
    The estimation of latency introduced within the network can be derived from the ping times observed during communication between the client (c1) and various network components. Here is a detailed analysis:

    First Hop Latency to Router r0: The initial ping from c1 to router r0 exhibits a minimal latency of 0.092 ms. This latency represents the baseline for communication originating from c1.

    Latency in the ASIA Region: When communicating with the ASIA region, the latency to router r1 is significantly higher at 38.074 ms. This implies that the path from c1 to r1 introduces an additional latency of approximately 37.982 ms (38.074 ms - 0.092 ms from r0). This increase in latency could be attributed to factors such as geographical distance, intermediate networking devices, or potential network congestion.

    Latency in the EMEA Region: In contrast, communication with the EMEA region shows a latency of 0.118 ms to router r2. This latency is nearly identical to the baseline latency, indicating that the path from c1 to r2 introduces a negligible additional latency of approximately 0.026 ms.

    Latency in the US Region: Communication with the US region results in a latency of 20.493 ms to router r3. Consequently, the path from c1 to the US region introduces an additional latency of approximately 20.401 ms (20.493 ms - 0.092 ms from r0).

    In summary, the latency introduced within the network varies significantly across regions. The ASIA region experiences the highest additional latency, primarily due to factors beyond the initial router, while the EMEA region demonstrates minimal latency increase. These estimations provide insights into the network's performance and can guide optimization efforts.

#        h) What downsides do you see in the current architecture design?

The current architecture design shows some potential downsides:

    Single Points of Failure: If any of the routers (r1, r2, r3) or switches (s1, s2, s3) fails, the respective regional network could become completely isolated from the rest of the network.

    High Latency in Certain Paths: The latency is quite high when reaching the hosts in the US region compared to others, which could indicate either a longer physical distance or less efficient routing. This could affect the performance of applications that require real-time data exchange.

    Packet Loss: There is packet loss noted in communication with some hosts, particularly h1 and h2 in the ASIA region, and h6 in the US region. This could be due to network congestion, poor quality links, or issues with the hosts themselves.

    Scalability Issues: As the network grows, the current design may not scale well, especially if more hosts are added to a region without consideration for the capacity of the routers and switches.

    Load Distribution: There seems to be an imbalance in load distribution, as indicated by the different latencies and packet loss rates. Some paths are experiencing higher loads, leading to increased latency and packet loss.

    Potential Bottlenecks: The connection to the ASIA region shows the highest latency and packet loss, suggesting a bottleneck. This could be due to insufficient bandwidth, poor quality of service (QoS) settings, or simply because the traffic is too high for the current infrastructure.

To address these downsides, one could consider implementing redundant paths to avoid single points of failure, upgrading the infrastructure to handle higher loads, optimizing routing to reduce latency, and using quality of service (QoS) to manage traffic effectively. Additionally, regularly monitoring network traffic and performance can help identify and alleviate bottlenecks before they impact users significantly.
