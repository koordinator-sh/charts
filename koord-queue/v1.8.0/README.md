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
| v0.1.0  | 2022年10月15日 | Koord-queue应用上线                                                                                                                    |
| v0.1.1  | 2023年1月10日  | Koord-queue多队列版本上线                                                                                                                 |
| v0.1.2  | 2023年1月12日  | 修复Koord-queue偶尔长时间无法出队的Bug                                                                                                         |
| v0.1.3  | 2023年1月12日  | 修复Koord-queue偶尔丢失QueueUnit的Bug                                                                                                     |
| v0.1.4  | 2023年2月14日  | 修复Koord-queue偶尔QueueUnit出队后Used信息丢失的Bug                                                                                            |
| v0.1.5  | 2023年2月28日  | 修复Koord-queue偶尔删除任务失败的Bug                                                                                                          |
| v0.1.6  | 2023年3月15日  | 修复TFJOB不显示State的Bug                                                                                                               |
| v0.1.8  | 2023年4月25日  | 增加严格优先级出队功能                                                                                                                       |
| v0.1.9  | 2023年5月16日  | 增加长时间Pending任务重新入队功能以及多队列公平调度                                                                                                     |
| v0.1.10 | 2023年6月14日  | koord-queue-controller, tf-operator-extension以及pytorch-operator-extension支持ARM架构                                                   |
| v0.1.11 | 2023年6月30日  | 任务更新时同步更新Queueunit状态                                                                                                              |
| v0.1.12 | 2023年7月20日  | Koord-queue支持在队列级别配置队列阻塞功能开关，支持通过将extension中的timeout参数配置成0来关闭重新入队功能                                                                |
| v0.1.13 | 2023年7月26日  | 修复更新时缺少LastUpdateTime可能导致组件无法工作的问题                                                                                                |
| v0.2.0  | 2023年8月29日  | 1. 支持通过Arena提交MPI Job排队；2. 支持Argo Workflow排队；3. 优化队列出队失败时的日志提示；4. 在ElasticQuotaTree中使用koord-queue/max-jobs作为资源名可以实现对同时出队的Job数量进行限制 |
| v0.2.1  | 2023年8月31日  | 修复Template中的NodeSelector导致在Worker节点上无法调度的问题                                                                                       |
| v0.2.2  | 2023年9月4日   | 新增对Kubernetes原生Job类型的支持                                                                                                           |
| v0.3.0  | 2023年9月13日  | 新增对在Queue中透出任务排队序列信息                                                                                                              |
| v0.3.1  | 2023年9月13日  | 修复删除QueueUnit时偶尔导致队列错误的问题                                                                                                         |
| v0.3.3  | 2023年12月26日 | 通过环境变量设置全局阻塞队列时将会全局刷新所有Queue的阻塞队列模式                                                                                               |
| v0.3.4  | 2024年1月4日   | 修复Block模式下删除队头任务时偶尔导致队头阻塞的问题                                                                                                      |
| v0.4.0  | 2024年2月1日   | 支持SparkApplication排队，需要与ACK应用市场中的Spark-Operator同时使用                                                                               |
| v1.21.1  | 2024年6月18日   | Queue中支持配置AdmissionCheck；Koord Queue默认安装ProvReq AdmissionCheck Controller；Job Extensions会在QueueUnits中传递PodSet|
| v1.21.2  | 2024年7月16日   | 修复ChartTempalte中Resource渲染错误的问题 |
| v1.22.2 | 2025年7月24日 | Koord Queue支持任务扩缩以及任务重启（需要结合调度器）；Koord Queue支持waiting-for-pods-ready特性 |

## ProReq Admission Check Controller
| 版本号 | 变更时间      | 变更内容                                                                      |
|-----|-----------|---------------------------------------------------------------------------|
|v1.0.0-aliyun-3e867557   | 2024年6月27日 | 支持ProReq Admission Check，支持通过--enable-reservation=true与资源预留结合 |

## Job Extensions Release Note
| 版本号 | 变更时间      | 变更内容                                                                      |
|-----|-----------|---------------------------------------------------------------------------|
| v0.4.0-aliyun-64d96075   | 2024年2月1日 | 同时支持PytorchJob、TfJob、MPIJob、BatchJob以及SparkApplication，通过Deployment启动参数控制 |
|v0.4.1-aliyun-4aa6611c| 2024年2月2日 | 支持超时重新入队功能，修复tfjob出队问题                                                    |
|v0.4.6-aliyun-0f09a156| 2024年6月18日 | 支持在QueueUnits中传递PodSet                                                    |

## Pytorch Operator Extension Release Note
| 版本号 | 变更时间        | 变更内容           |
| ------ |-------------|-------------------|
| v1 |  | 1. 支持通过Arena提交的Pytorch Job的入队排队 |
| v1.7.1 | 2023年8月29日 | 1. 支持感知Scheduled状态，Job可以通过此状态表示一个任务的Pod已有Nodename；2. Job排队时将给Job新增Queuing状态 |
| v1.7.2 | 2023年9月4日 | 新增在QueueUnit中传递Job的Label和Annotation信息 |
| v1.7.3 | 2023年10月13日 | QueueUnit出队后将Queuing状态设置为False |

## Tf Operator Extension Release Note
| 版本号 | 变更时间        | 变更内容           |
| ------ |-------------|-------------------|
| v1 |  | 1. 支持通过Arena提交的Tf Job的入队排队 |
| v1.7.1 | 2023年8月29日 | 1. 支持感知Scheduled状态，Job可以通过此状态表示一个任务的Pod已有Nodename；2. Job排队时将给Job新增Queuing状态 |
| v1.7.2 | 2023年9月4日 | 新增在QueueUnit中传递Job的Label和Annotation信息 |
| v1.7.3 | 2023年10月13日 | QueueUnit出队后将Queuing状态设置为False |

## MPI Operator Extension Release Note
| 版本号 | 变更时间        | 变更内容           |
| ------ |-------------|-------------------|
| v0.0.1 | 2023年8月29日 | 1. 支持通过Arena提交的MPI Job的入队排队，默认不开启，可通过将extension.mpi.enable置为true的方式启用 |
| v0.1.0 | 2023年9月4日 | 新增在QueueUnit中传递Job的Label和Annotation信息 |

## Argo Operator Extension Release Note
| 版本号 | 变更时间        | 变更内容           |
| ------ |-------------|-------------------|
| v0.1.0 | 2023年8月29日 | 1. 支持Argo Workflow以整体进行任务排队，可通过将extension.argo.enable置为true的方式启用 |
| v0.1.1 | 2023年9月4日 | 新增在QueueUnit中传递Job的Label和Annotation信息 |

## Batch Job Operator Extension Release Note
| 版本号 | 变更时间        | 变更内容           |
| ------ |-------------|-------------------|
| v0.1.0 | 2023年8月29日 | 1. 支持以Kubernetes原生Job类型进行任务排队，可通过将extension.batchjob.enable置为true的方式启用 |
| v0.1.1 | 2023年10月8日 | 1. 新增通过--qps以及--burst设置组件的客户端qps；2. 新增在Job未达到终态时对Job每30s进行一次同步 |
