# Metrics Dashboard

Metrics Dashboard is a project that implements microservices observability using the Prometheus-Grafana-Jaeger stack. This is a project for the Udacity's Cloud Native Application Architecture Nanodegree.

## Table of Contents

+ [Table of Contents](#table-of-contents)
+ [Main steps](#main-steps)
+ [Verify the monitoring installation](#verify-the-monitoring-installation)
+ [Setup the Jaeger and Prometheus source](#setup-the-jaeger-and-prometheus-source)
+ [Create a basic dashboard](#create-a-basic-dashboard)
+ [Describe SLO/SLI](#describe-slosli)
+ [Creating SLI metrics](#creating-sli-metrics)
+ [Create a dashboard to measure our SLIs](#create-a-dashboard-to-measure-our-slis)
+ [Tracing our Flask app](#tracing-our-flask-app)
+ [Jaeger in dashboards](#jaeger-in-dashboards)
+ [Report error](#report-error)
+ [Creating SLIs and SLOs](#creating-slis-and-slos)
+ [Building KPIs for our plan](#building-kpis-for-our-plan)
+ [Final dashboard](#final-dashboard)

## Main steps

1. Deploy a sample application in your Kubernetes cluster.
2. Use Prometheus to monitor the various metrics of the application.
3. Use Jaeger to perform traces on the application.
4. Use Grafana in order to visualize these metrics in a series of graphs that can be shared with other members on your team.
5. Document the project in a README.

## Verify the monitoring installation

![Cluster resources](./docs/images/monitoringInstallation.png)

## Setup the Jaeger and Prometheus source

![Grafana](./docs/images/grafana.png)

## Create a basic dashboard

![Prometheus Dashboard](./docs/images/prometheusDashboard.png)

## Describe SLO/SLI

Suppose that these are our SLOs for *monthly uptime* and *request response time*:
1. 99.99% uptime in the year.
2. 95% of requests completed in < 100 ms.

We can describe SLIs as:
1. We got 99.98% uptime in the current year.
2. 94% of the requests were completed in < 100 ms.

## Creating SLI metrics

1. **Number of error responses in a period of time** - This metric could help us to identify possible bootlenecks and bugs.
2. **The average time taken to return a request** - This metric could help us to identify opportunities to tune our services performance.
3. **The average time taken recover a service if it goes down** - This metric could help us to measure our capacity to recover possible failovers.
4. **Percentage of uptime in a period of time** - This metric could help us to measure the health of our services.
5. **Average percentage of memory or CPU used by a service in a period of time** - This metric could help us to measure the impact of our services in the costs of maintaining a system and look for efficient services.

## Create a dashboard to measure our SLIs

![HTTP errors panel](./docs/images/httpErrorsPanel.png)

## Tracing our Flask app

![Jaeger UI](./docs/images/backendTracing.png)

## Jaeger in dashboards

![Grafana tracing panel](./docs/images/tracingPanel.png)

## Report error

```markdown
**TROUBLE TICKET**

**Name**: Franky River
**Date**: 09/27/2021 5:15:10 PM
**Subject**: Front-end service is creating many 40x and 50x errors
**Affected Area**: API requests
**Severity**: High

**Description**:
The `static/js/click.js` file is not handling clicks correctly and requests can not be processed because the
fetch url are not right.
```

## Creating SLIs and SLOs

SLO: 99.95% uptime per month.

Our SLO corresponds to the following periods of allowed downtime/unavailability:
* Daily: 43s
* Weekly: 5m 2s
* Monthly: 21m 54s
* Quarterly: 1h 5m 44s
* Yearly: 4h 22m 58s

SLIs:
1. We got less than 21 minutes of downtime in the last month.
2. We got 2 minutes downtime in the past week for the current month.

## Building KPIs for our plan

1. Network pressure
2. Cluster usage
3. CPU usage

## Final dashboard

![KPI monitoring dashboard](./docs/images/kpiDashboard.png)

1. The Network I/O Pressure panel displays information about the amount of data received and sent from the cluster.
2. The Total usage group of panels display information about the memory usage, the CPU usage and the filesystem usage in the cluster. It displays metrics in GiB.
3. The Containers CPU usage displays the amount cores used by all the containers in our cluster.
