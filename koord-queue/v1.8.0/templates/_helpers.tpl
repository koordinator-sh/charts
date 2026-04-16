{{/*
Expand the name of the chart.
*/}}
{{- define "koord-queue.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "koord-queue.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "koord-queue.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "koord-queue.labels" -}}
helm.sh/chart: {{ include "koord-queue.chart" . }}
{{ include "koord-queue.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "koord-queue.selectorLabels" -}}
app.kubernetes.io/name: {{ include "koord-queue.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "koord-queue.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "koord-queue.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "koord-queue.imagePrefix" -}}
{{- if or (eq (.Values.global.clusterType | default "Default") "ExternalKubernetes") (eq (.Values.global.clusterProfile | default "Default") "Edge")}}
{{- .Values.global.imagePrefix }}
{{- else if .Values.global.pullImageByVPCNetwork }}
{{- .Values.global.imagePrefix }}
{{- else }}
{{- .Values.global.imagePrefix }}
{{- end }}
{{- end }}
