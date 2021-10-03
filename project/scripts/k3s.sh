#!/bin/bash
echo "**** Begin installing k3s"

# Install k3s and allow Rancher to access to the cluster
curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" sh -

echo "**** End installing k3s"
