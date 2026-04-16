# Koord-queue

Koord-queue manages AI/ML and batch workloads in Kubernetes. It allows system administrators to customize job queue management for queues, providing flexibility and fairness across different queues. Combined with a quota system (similar to Kubernetes ResourceQuota), Koord-queue automates and optimizes workload and resource quota management to maximize cluster resource utilization.

## Architecture

![Architecture](https://raw.githubusercontent.com/koord-queue/koord-queue/main/doc/img/architecture-updated.jpg)

## Key Features

- Job queueing based on workload priority, creation time, and quota
- Support for dynamic priority adjustment of jobs within queues
- Provides fairness across queues

## Release Note

| Version | Date | Changes |
|---------|------|---------|
| v1.8.0 | April 24, 2026 | Koord-Queue v1.8.0 released, supports ElasticQuotaV2 mode, integrated with Koordinator ecosystem |