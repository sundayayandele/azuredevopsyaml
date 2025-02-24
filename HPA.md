When configuring Horizontal Pod Autoscalers (HPA) in OpenShift (or Kubernetes), the ratio of resources.requests to resources.limits for CPU is an important factor because it directly influences:

1. Pod scheduling behavior: Kubernetes schedules pods based on resources.requests, ensuring enough CPU is available.


2. Autoscaling responsiveness: HPA relies on metrics such as CPU usage compared to the requests value.



Here’s what you need to consider to determine the best ratio:


---

General Best Practices for CPU Ratio

1. Ratio Between Requests and Limits:

The recommended starting point is 1:1 or slightly below that (e.g., resources.requests should be at least 70%-100% of resources.limits).

If your CPU limit is 3000m, a reasonable request value might range from 2100m to 3000m.



2. Why?

Too low requests (e.g., 1000m with a 3000m limit):

The HPA will consider the pod as underutilized, making scaling decisions inaccurate.

May lead to under-scheduled resources during sudden spikes.


Too high requests (e.g., close to 3000m):

Leaves little room for bursting and could reduce overall node utilization.

Could result in unnecessary throttling if pods exceed the CPU requests for short bursts.




3. Choose Based on Workload Characteristics:

Burstable Workloads: Workloads with frequent spikes benefit from a lower ratio (e.g., 70%-80% of the limit), allowing burstable performance.

Steady-State Workloads: If your application has consistent and predictable CPU usage, a higher ratio closer to 1:1 works well.





---

Example Based on 3000m CPU Limit

Burstable workload:

resources.requests: 2100m

resources.limits: 3000m

This allows up to ~40% additional CPU usage during spikes while keeping HPA responsive to sustained usage patterns.


Steady workload:

resources.requests: 2700m

resources.limits: 3000m

This minimizes overcommitment and throttling while still allowing some flexibility.




---

Testing and Monitoring

The "best" ratio ultimately depends on observing your application’s behavior under load. You can:

1. Start with a 70%-80% request-to-limit ratio.


2. Use OpenShift’s built-in monitoring tools to observe:

Average CPU utilization compared to requests and limits.

Pod scaling behavior (ensuring it's scaling as intended).



3. Tune iteratively to meet your workload's demands.




Would you like details on HPA CPU target utilization setup or monitoring strategies?

