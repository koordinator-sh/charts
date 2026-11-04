#!/usr/bin/env python3
"""Offline render regression tests. Requires Helm and PyYAML."""
import itertools
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
CHART = ROOT / "charts/koordinator"
BASELINE = ROOT / "versions/v1.8.0"
COMPONENTS = ("manager", "scheduler", "descheduler", "koordlet", "deviceDaemon")
MONITORS = {
    "koordlet": {("Service", "koordlet-service"),
                ("ServiceMonitor", "koordlet-service-monitor")},
    "scheduler": {("PodMonitor", "koord-scheduler-metrics-podmonitor")},
    "descheduler": {("PodMonitor", "koord-descheduler-metrics-podmonitor")},
}
OWNED = {
    "manager": {
        ("Deployment", "koord-manager"), ("ServiceAccount", "koord-manager"),
        ("ClusterRole", "koord-manager-role"),
        ("ClusterRoleBinding", "koord-manager-rolebinding"),
        ("Role", "koord-leader-election-role"),
        ("RoleBinding", "koord-leader-election-rolebinding"),
        ("Service", "koordinator-webhook-service"),
        ("Secret", "koordinator-webhook-certs"),
        ("ConfigMap", "slo-controller-config"),
        ("MutatingWebhookConfiguration", "koordinator-mutating-webhook-configuration"),
        ("ValidatingWebhookConfiguration", "koordinator-validating-webhook-configuration"),
    },
    "scheduler": {
        ("Deployment", "koord-scheduler"), ("ServiceAccount", "koord-scheduler"),
        ("ClusterRole", "koord-scheduler-role"),
        ("ClusterRoleBinding", "koord-scheduler-rolebinding-custom"),
        ("ClusterRoleBinding", "koord-scheduler-rolebinding"),
        ("ClusterRoleBinding", "koord-scheduler-rolebinding-volume"),
        ("ConfigMap", "koord-scheduler-config"),
        ("ConfigMap", "gpu-shared-resource-templates"),
    },
    "descheduler": {
        ("Deployment", "koord-descheduler"),
        ("ServiceAccount", "koord-descheduler"),
        ("ClusterRole", "koord-descheduler-role"),
        ("ClusterRoleBinding", "koord-descheduler-rolebinding"),
        ("ConfigMap", "koord-descheduler-config"),
    },
    "koordlet": {
        ("DaemonSet", "koordlet"), ("ServiceAccount", "koordlet"),
        ("ClusterRole", "koordlet-role"),
        ("ClusterRoleBinding", "koordlet-rolebinding"),
    },
    "deviceDaemon": {("DaemonSet", "koord-device-daemon")},
}


def render(values=None, chart=CHART, kube="1.30.0", success=True):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "values.json"
        path.write_text(json.dumps(values or {}))
        result = subprocess.run(
            [os.environ.get("HELM", "helm"), "template", "test", str(chart),
             "--namespace", "koordinator-system", "--kube-version", kube,
             "-f", str(path)], text=True, capture_output=True, check=False,
        )
    if not success:
        if result.returncode == 0:
            raise AssertionError("Expected template rendering to fail")
        return result.stderr
    if result.returncode:
        raise AssertionError(result.stderr)
    docs = [doc for doc in yaml.safe_load_all(result.stdout) if doc]
    resources = {(doc["kind"], doc["metadata"]["name"]): doc for doc in docs}
    if len(resources) != len(docs):
        raise AssertionError("Duplicate resource identity")
    return resources


class KoordinatorRenderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = render(chart=BASELINE)

    def check_dependencies(self, resources):
        for (kind, _), resource in resources.items():
            if kind in ("Deployment", "DaemonSet"):
                pod = resource["spec"]["template"]["spec"]
                if "serviceAccountName" in pod:
                    self.assertIn(("ServiceAccount", pod["serviceAccountName"]), resources)
                for volume in pod.get("volumes", []):
                    if "configMap" in volume:
                        self.assertIn(("ConfigMap", volume["configMap"]["name"]), resources)
            if kind in ("ClusterRoleBinding", "RoleBinding"):
                ref = resource["roleRef"]
                if not ref["name"].startswith("system:"):
                    self.assertIn((ref["kind"], ref["name"]), resources)
                for subject in resource.get("subjects", []):
                    if subject["kind"] == "ServiceAccount":
                        self.assertIn(("ServiceAccount", subject["name"]), resources)
            if kind.endswith("WebhookConfiguration"):
                for webhook in resource["webhooks"]:
                    self.assertIn(("Service", webhook["clientConfig"]["service"]["name"]), resources)

    def test_default_parity(self):
        for kube in ("1.20.0", "1.22.0", "1.30.0"):
            with self.subTest(kube=kube):
                self.assertEqual(render(chart=BASELINE, kube=kube), render(kube=kube))

    def test_all_component_combinations_with_monitors(self):
        shared = {key: value for key, value in self.baseline.items()
                  if key not in set().union(*OWNED.values())}
        self.assertEqual({kind for kind, _ in shared},
                         {"Namespace", "PriorityClass", "CustomResourceDefinition"})
        for enabled in itertools.product((True, False), repeat=len(COMPONENTS)):
            values = {c: {"enabled": flag} for c, flag in zip(COMPONENTS, enabled)}
            values["koordlet"]["enableServiceMonitor"] = True
            values["scheduler"]["monitorEnabled"] = True
            values["descheduler"]["monitorEnabled"] = True
            with self.subTest(enabled=enabled):
                actual = render(values)
                expected = set(shared)
                for component, flag in zip(COMPONENTS, enabled):
                    if flag:
                        expected |= OWNED[component] | MONITORS.get(component, set())
                        for key in OWNED[component]:
                            self.assertEqual(actual.get(key), self.baseline[key])
                self.assertEqual(set(actual), expected)
                for key, value in shared.items():
                    self.assertEqual(actual[key], value)
                self.check_dependencies(actual)

    def test_monitor_parity(self):
        values = {"koordlet": {"enableServiceMonitor": True},
                  "scheduler": {"monitorEnabled": True},
                  "descheduler": {"monitorEnabled": True}}
        self.assertEqual(render(values, chart=BASELINE), render(values))

    def test_koordlet_only_without_crds(self):
        values = {c: {"enabled": c == "koordlet"} for c in COMPONENTS}
        values["crds"] = {"managed": False}
        actual = render(values)
        self.assertEqual(set(actual), OWNED["koordlet"] | {
            ("Namespace", "koordinator-system"),
            *[("PriorityClass", "koord-" + p) for p in ("batch", "free", "mid", "prod")],
        })
        self.check_dependencies(actual)

    def test_per_crd_selection(self):
        actual = render({"crds": {"nodeslos": False}})
        expected = dict(self.baseline)
        del expected[("CustomResourceDefinition", "nodeslos.slo.koordinator.sh")]
        self.assertEqual(actual, expected)

    def test_extra_args(self):
        extra = {"runtime-hooks-network": "unix", "enable-node-metric-report": False,
                 "node-topology-sync-interval": "0s", "test-zero": 0,
                 "test-empty": "", "test-true": True, "test-decimal": 1.5,
                 "cpu-burst-excluded-namespaces": "system-a,system-b",
                 "test-quoted": 'spaces: "quotes" # and = signs'}
        actual = render({"koordlet": {"extraArgs": extra}})
        expected = dict(self.baseline)
        daemon = actual[("DaemonSet", "koordlet")]
        args = daemon["spec"]["template"]["spec"]["containers"][0]["args"]
        baseline_args = self.baseline[("DaemonSet", "koordlet")]["spec"]["template"]["spec"]["containers"][0]["args"]
        serialized = [f"--{key}={str(value).lower() if isinstance(value, bool) else value}"
                      for key, value in sorted(extra.items())]
        self.assertEqual(args, baseline_args + serialized)
        self.assertEqual(len({arg.lstrip('-').split('=')[0] for arg in args}), len(args))
        # Removing extra arguments restores every baseline resource and field.
        del args[len(baseline_args):]
        self.assertEqual(actual, expected)

    def test_managed_args_rejected(self):
        for flag in ("addr", "cgroup-root-dir", "feature-gates",
                     "runtime-hooks-host-endpoint", "logtostderr", "v"):
            with self.subTest(flag=flag):
                self.assertIn(f"{flag} is managed by the chart", render(
                    {"koordlet": {"extraArgs": {flag: "value"}}}, success=False))

    def test_invalid_extra_args(self):
        for extra in ([], "--flag=value", {"--flag": True}, {"flag=value": True},
                      {"": True}, {"flag": []}, {"flag": {}}, {"flag": None}):
            with self.subTest(extra=extra):
                self.assertIn("koordlet.extraArgs", render(
                    {"koordlet": {"extraArgs": extra}}, success=False))

    def test_existing_koordlet_settings(self):
        values = {"koordlet": {"features": "AllAlpha=false,CPUBurst=true",
                              "metrics": {"port": 9999}, "log": {"level": "2"},
                              "hostDirs": {"koordletSockDir": "/custom/koordlet"},
                              "extraArgs": {"enable-node-metric-report": False}}}
        args = render(values)[("DaemonSet", "koordlet")]["spec"]["template"]["spec"]["containers"][0]["args"]
        self.assertIn("-feature-gates=AllAlpha=false,CPUBurst=true", args)
        self.assertIn("-addr=:9999", args)
        self.assertIn("--v=2", args)
        self.assertIn("-runtime-hooks-host-endpoint=/custom/koordlet/koordlet.sock", args)
        self.assertIn("--enable-node-metric-report=false", args)


if __name__ == "__main__":
    unittest.main(verbosity=2)
