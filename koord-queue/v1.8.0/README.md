# Koord-queue
Koord-queue用于管理Kubernetes中的AI/ML和批处理工作负载。它允许系统管理员为队列定制作业队列管理，以在不同队列之间提供灵活性和公平性。结合配额系统（类似于Kubernetes资源配额），Koord-queue自动化并优化工作负载和资源配额管理，以最大限度地提高集群资源利用率。

## 架构
![image.png](https://raw.githubusercontent.com/koord-queue/koord-queue/main/doc/img/architecture-updated.jpg)

## 关键功能
- 基于工作负载优先级、创建时间和配额的作业队列
- 支持队列中作业优先级的动态调整
- 在队列之间提供公平性

## Release Note
| 版本号     | 变更时间        | 变更内容                                                                                                                              |
|---------|-------------|-----------------------------------------------------------------------------------------------------------------------------------|
| v1.8.0  | 2026年4月24日 | Koord-Queue v1.8.0 正式发布，支持 ElasticQuotaV2 模式，集成 Koordinator 生态                                                                 |
