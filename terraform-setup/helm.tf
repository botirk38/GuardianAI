provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)
    exec {
      api_version = "client.authentication.k8s.io/v1alpha1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
    }
  }
}

resource "helm_release" "redis" {
  name       = "redis"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "redis"
  namespace  = "default"

  set {
    name  = "global.storageClass"
    value = "gp2"
  }

  set {
    name  = "usePassword"
    value = "false"
  }
}

resource "helm_release" "zookeeper" {
  name       = "zookeeper"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "zookeeper"
  namespace  = "default"

  set {
    name  = "replicaCount"
    value = "3"
  }

  set {
    name  = "persistence.storageClass"
    value = "gp2"
  }
}

resource "helm_release" "kafka" {
  name       = "kafka"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "kafka"
  namespace  = "default"

  set {
    name  = "zookeeper.enabled"
    value = "false"
  }

  set {
    name  = "externalZookeeper.servers"
    value = "zookeeper.default.svc.cluster.local"
  }

  set {
    name  = "replicaCount"
    value = "3"
  }

  set {
    name  = "persistence.storageClass"
    value = "gp2"
  }
}


