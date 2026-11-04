# Koordinator v1.8.0

## Configuration

Note that installing this chart directly means it will use the default template values for Koordinator.

You may have to set your specific configurations if it is deployed into a production cluster, or you want to configure feature-gates.

### Optional: chart parameters

The following table lists the configurable parameters of the chart and their default values.

| Parameter                                          | Description                                                      | Default                         |
|----------------------------------------------------|------------------------------------------------------------------|---------------------------------|
| `manager.enabled` | Install manager and its component-specific resources | `true` |
| `scheduler.enabled` | Install scheduler and its component-specific resources | `true` |
| `descheduler.enabled` | Install descheduler and its component-specific resources | `true` |
| `koordlet.enabled` | Install koordlet and its component-specific resources | `true` |
| `deviceDaemon.enabled` | Install deviceDaemon and its component-specific resources | `true` |
| `koordlet.extraArgs` | Additional flags as a map of names to scalar values | `{}` |
| `featureGates`                                     | Feature gates for Koordinator, empty string means all by default | ` `                             |
| `installation.namespace`                           | namespace for Koordinator installation                           | `koordinator-system`            |
| `installation.createNamespace`                     | Whether to create the installation.namespace                     | `true`                          |
| `imageRepositoryHost`                              | Image repository host                                            | `ghcr.io`                       |
| `manager.log.level`                                | Log level that koord-manager printed                             | `4`                             |
| `manager.replicas`                                 | Replicas of koord-manager deployment                             | `2`                             |
| `manager.image.repository`                         | Repository for koord-manager image                               | `koordinator-sh/koord-manager`  |
| `manager.image.tag`                                | Tag for koord-manager image                                      | `v1.8.0`                        |
| `manager.resources.limits.cpu`                     | CPU resource limit of koord-manager container                    | `1000m`                         |
| `manager.resources.limits.memory`                  | Memory resource limit of koord-manager container                 | `1Gi`                           |
| `manager.resources.requests.cpu`                   | CPU resource request of koord-manager container                  | `500m`                          |
| `manager.resources.requests.memory`                | Memory resource request of koord-manager container               | `256Mi`                         |
| `manager.metrics.port`                             | Port of metrics served                                           | `8080`                          |
| `manager.webhook.port`                             | Port of webhook served                                           | `9876`                          |
| `manager.healthProbe.port`                         | Port of health probe served                                      | `8000`                          |
| `manager.nodeAffinity`                             | Node affinity policy for koord-manager pod                       | `{}`                            |
| `manager.nodeSelector`                             | Node labels for koord-manager pod                                | `{}`                            |
| `manager.tolerations`                              | Tolerations for koord-manager pod                                | `[]`                            |
| `manager.resyncPeriod`                             | Resync period of informer koord-manager, defaults no resync      | `0`                             |
| `manager.hostNetwork`                              | Whether koord-manager pod should run with hostnetwork            | `false`                         |
| `scheduler.log.level`                              | Log level that koord-scheduler printed                           | `4`                             |
| `scheduler.replicas`                               | Replicas of koord-scheduler deployment                           | `2`                             |
| `scheduler.image.repository`                       | Repository for koord-scheduler image                             | `koordinator-sh/koord-scheduler` |
| `scheduler.image.tag`                              | Tag for koord-scheduler image                                    | `v1.8.0`                        |
| `scheduler.resources.limits.cpu`                   | CPU resource limit of koord-scheduler container                  | `1000m`                         |
| `scheduler.resources.limits.memory`                | Memory resource limit of koord-scheduler container               | `1Gi`                           |
| `scheduler.resources.requests.cpu`                 | CPU resource request of koord-scheduler container                | `500m`                          |
| `scheduler.resources.requests.memory`              | Memory resource request of koord-scheduler container             | `256Mi`                         |
| `scheduler.port`                                   | Port of metrics served                                           | `10251`                         |
| `scheduler.nodeAffinity`                           | Node affinity policy for koord-scheduler pod                     | `{}`                            |
| `scheduler.nodeSelector`                           | Node labels for koord-scheduler pod                              | `{}`                            |
| `scheduler.tolerations`                            | Tolerations for koord-scheduler pod                              | `[]`                            |
| `scheduler.monitorEnabled`                         | Whether to enable PodMonitor for koord-scheduler                 | `false`                         |
| `scheduler.hostNetwork`                            | Whether koord-scheduler pod should run with hostnetwork          | `false`                         |
| `koordlet.log.level`                               | Log level that koordlet printed                                  | `4`                             |
| `koordlet.image.repository`                        | Repository for koordlet image                                    | `koordinator-sh/koordlet`       |
| `koordlet.image.tag`                               | Tag for koordlet image                                           | `v1.8.0`                        |
| `koordlet.resources.limits.cpu`                    | CPU resource limit of koordlet container                         | `200m`                          |
| `koordlet.resources.limits.memory`                 | Memory resource limit of koordlet container                      | `256Mi`                         |
| `koordlet.resources.requests.cpu`                  | CPU resource request of koordlet container                       | `0`                             |
| `koordlet.resources.requests.memory`               | Memory resource request of koordlet container                    | `0`                             |
| `koordlet.nodeAffinity`                            | Node affinity policy for koordlet pod                            | `{}`                            |
| `koordlet.runtimeClassName`                        | RuntimeClassName for koordlet pod                                | ` `                             |
| `koordlet.enableServiceMonitor`                    | Whether to enable ServiceMonitor for koordlet                    | `false`                         |
| `koordlet.metrics.port`                            | Port of metrics served                                           | `9316`                          |
| `scheduler.featureGates`                           | Feature gates for koord-scheduler                                | ` `                             |
| `scheduler.enableJobPreemption`                    | Whether to enable job preemption in koord-scheduler              | `true`                          |
| `scheduler.deviceShare.gpuShareUnsupportedModels`  | GPU vendor-model pairs that do not support GPU sharing (e.g. vNPU). Pods requesting `gpu.shared` will be filtered out from nodes matching any of these models. | `[{vendor: huawei, model: Ascend-310P3-300I-DUO}]` |
| `descheduler.log.level`                            | Log level that koord-descheduler printed                         | `4`                             |
| `descheduler.replicas`                             | Replicas of koord-descheduler deployment                         | `2`                             |
| `descheduler.image.repository`                     | Repository for koord-descheduler image                           | `koordinator-sh/koord-descheduler` |
| `descheduler.image.tag`                            | Tag for koord-descheduler image                                  | `v1.8.0`                        |
| `descheduler.resources.limits.cpu`                 | CPU resource limit of koord-descheduler container                | `1000m`                         |
| `descheduler.resources.limits.memory`              | Memory resource limit of koord-descheduler container             | `1Gi`                           |
| `descheduler.resources.requests.cpu`               | CPU resource request of koord-descheduler container              | `500m`                          |
| `descheduler.resources.requests.memory`            | Memory resource request of koord-descheduler container           | `256Mi`                         |
| `descheduler.port`                                 | Port of metrics served                                           | `10251`                         |
| `descheduler.featureGates`                         | Feature gates for koord-descheduler                              | ` `                             |
| `descheduler.nodeAffinity`                         | Node affinity policy for koord-descheduler pod                   | `{}`                            |
| `descheduler.nodeSelector`                         | Node labels for koord-descheduler pod                            | `{}`                            |
| `descheduler.tolerations`                          | Tolerations for koord-descheduler pod                            | `[]`                            |
| `descheduler.monitorEnabled`                       | Whether to enable PodMonitor for koord-descheduler               | `false`                         |
| `descheduler.hostNetwork`                          | Whether koord-descheduler pod should run with hostnetwork        | `false`                         |
| `deviceDaemon.log.level`                           | Log level that koord-device-daemon printed                       | `4`                             |
| `deviceDaemon.image.repository`                    | Repository for koord-device-daemon image                         | `koordinator-sh/koord-device-daemon` |
| `deviceDaemon.image.tag`                           | Tag for koord-device-daemon image                                | `v1.8.0`                        |
| `deviceDaemon.resources.limits.cpu`                | CPU resource limit of koord-device-daemon container              | `200m`                          |
| `deviceDaemon.resources.limits.memory`             | Memory resource limit of koord-device-daemon container           | `256Mi`                         |
| `deviceDaemon.resources.requests.cpu`              | CPU resource request of koord-device-daemon container            | `0`                             |
| `deviceDaemon.resources.requests.memory`           | Memory resource request of koord-device-daemon container         | `0`                             |
| `deviceDaemon.nodeAffinity`                        | Node affinity policy for koord-device-daemon pod                 | `{}`                            |
| `webhookConfiguration.failurePolicy.pods`          | The failurePolicy for pods in mutating webhook configuration     | `Ignore`                        |
| `webhookConfiguration.failurePolicy.elasticquotas` | The failurePolicy for elasticQuotas in all webhook configuration | `Ignore`                        |
| `webhookConfiguration.failurePolicy.nodeStatus`    | The failurePolicy for node.status in all webhook configuration   | `Ignore`                        |
| `webhookConfiguration.failurePolicy.nodes`         | The failurePolicy for nodes in all webhook configuration         | `Ignore`                        |
| `webhookConfiguration.failurePolicy.reservations`  | The failurePolicy for reservations in all webhook configuration  | `Ignore`                        |
| `webhookConfiguration.timeoutSeconds`              | The timeoutSeconds for all webhook configuration                 | `30`                            |
| `crds.managed`                                     | Koordinator will not install CRDs with chart if this is false    | `true`                          |
| `imagePullSecrets`                                 | The list of image pull secrets for koordinator image             | `false`                         |

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install` or `helm upgrade`.

### Optional: feature-gate

Feature-gate controls some influential features in Koordinator:

| Name                      | Description                                                       | Default | Effect (if closed)                     |
| ------------------------- | ----------------------------------------------------------------  | ------- | -------------------------------------- |
| `PodMutatingWebhook`      | Whether to open a mutating webhook for Pod **create**             | `true`  | Don't inject koordinator.sh/qosClass, koordinator.sh/priority and don't replace koordinator extend resources ad so on |
| `PodValidatingWebhook`    | Whether to open a validating webhook for Pod **create/update**    | `true`  | It is possible to create some Pods that do not conform to the Koordinator specification, causing some unpredictable problems |

If you want to configure the feature-gate, just set the parameter when install or upgrade. Such as:

```bash
$ helm install koordinator https://... --set featureGates="PodMutatingWebhook=true\,PodValidatingWebhook=true"
```

If you want to enable all feature-gates, set the parameter as `featureGates=AllAlpha=true`.

### Optional: install or upgrade specific CRDs

If you want to skip specific CRDs during the installation or the upgrade, you can set the parameter `crds.<crdPluralName>` to `false` and install or upgrade them manually.

```bash
# skip install the CRD noderesourcetopologies.topology.node.k8s.io
$ helm install koordinator https://... --set crds.managed=true,crds.noderesourcetopologies=false
# only upgrade specific CRDs
$ helm upgrade koordinator https://... --set crds.managed=true,crds.recommendations=true,crds.clustercolocationprofiles=true,crds.elasticquotaprofiles=true,crds.elasticquotas=true,crds.devices=true,crds.podgroups=true,crds.podmigrationjobs=true,crds.clusternetworktopologies=true,crds.scheduleexplanations=true
```

### Optional: the local image for China

If you are in China and have problem to pull image from official DockerHub, you can use the registry hosted on Alibaba Cloud:

```bash
$ helm install koordinator https://... --set imageRepositoryHost=registry.cn-beijing.aliyuncs.com
```


### Optional components

All components remain enabled by default. Set `manager.enabled`,
`scheduler.enabled`, `descheduler.enabled`, `koordlet.enabled`, or
`deviceDaemon.enabled` to `false` to omit that component. Its workload and
component-specific ServiceAccounts, RBAC, ConfigMaps, Services, Secrets, webhook
configurations and monitors are omitted together. Monitor settings have no effect
when their component is disabled. The GPU shared resource templates ConfigMap
belongs to the scheduler; the SLO controller ConfigMap belongs to the manager.

The installation Namespace, PriorityClasses and CRDs are shared and remain
independent of component enablement. Use the existing `crds.managed` and per-CRD
settings to manage CRDs separately. Disabling components does not automatically
disable any CRD. The device daemon is independently optional and shares device
information with koordlet through a host directory; it does not use koordlet's
ServiceAccount.

For example, to install only koordlet:

```yaml
manager:
  enabled: false
scheduler:
  enabled: false
descheduler:
  enabled: false
deviceDaemon:
  enabled: false
```

These settings control chart resources, not application feature dependencies.
Without the manager, its controllers and admission webhooks are unavailable;
provide any required NodeSLO or other policy resources separately. Disable
features that require omitted components or provide those dependencies externally.
Disabling components on an existing Helm release removes their chart-managed
resources during upgrade; review the rendered changes first.

### Additional koordlet arguments

`koordlet.extraArgs` is a map of flag names **without leading dashes** to strings,
booleans or numbers. Each entry becomes one quoted `--name=value` argument in
sorted key order. Empty strings, `false` and `0` are preserved. Lists, objects and
null values are unsupported; repeated flags are unsupported. For example:

```yaml
koordlet:
  extraArgs:
    enable-node-metric-report: false
    node-topology-sync-interval: 0s
    runtime-hooks-network: unix
```

The chart rejects arguments it already generates, avoiding duplicate flags:
`addr` (use `koordlet.metrics.port`), `feature-gates` (use `koordlet.features`),
`runtime-hooks-host-endpoint` (use `koordlet.hostDirs.koordletSockDir`), `v` (use
`koordlet.log.level`), and the fixed `cgroup-root-dir` and `logtostderr` flags.
Additional arguments must be supported by the selected koordlet image. Setting
extra arguments does not add or change host mounts, RBAC, or other pod settings.

### Render regression tests

From the repository root, with Helm and Python 3 installed:

```sh
python3 -m pip install PyYAML
python3 scripts/test-koordinator.py
```

The tests render locally and do not connect to a Kubernetes cluster. They compare
default resources with chart 1.8.0, exercise component combinations and monitor
dependencies, and check additional argument serialization and validation.
