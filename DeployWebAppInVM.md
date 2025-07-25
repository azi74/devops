# Setup Monitoring on Azure VM with Docker, Prometheus, and Grafana

## ⚙️ 1. Provision Azure VM

* **Portal** : Used Azure Portal to create a Virtual Machine
* **Image** : Selected Ubuntu Server (e.g., Ubuntu 20.04 LTS)
* **Size** : Picked a VM size (e.g., B1s for low-cost dev/testing)
* **Authentication** : Configured SSH public key or password
* **Networking** :
* Allowed inbound ports:  **22 (SSH)** ,  **3000 (Grafana)** ,  **9090 (Prometheus)** , **9100 (Node Exporter)**
* Attached a public IP

## 🔐 2. Connect to VM via SSH

```bash
ssh azureuser@<vm-public-ip>
```

## 🐳 3. Install Docker

```bash
# Update
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh

# Add user to Docker group
sudo usermod -aG docker $USER
newgrp docker
```

## 🧱 4. Create Docker Network (Optional but Recommended)

```bash
docker network create monitoring-net
```

This allows Prometheus, Grafana, and Node Exporter to talk to each other via internal DNS names (`prometheus`, `node-exporter`, etc.).

## 📦 5. Run Prometheus in Docker

### Create `prometheus.yml` configuration file:

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

### Run Prometheus container:

```bash
docker run -d \
  --name=prometheus \
  --network=monitoring-net \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

## 🧾 6. Run Node Exporter in Docker

```bash
docker run -d \
  --name=node-exporter \
  --network=monitoring-net \
  -p 9100:9100 \
  prom/node-exporter
```

* `prometheus` will now scrape system metrics from `node-exporter` via `http://node-exporter:9100/metrics`

## 📊 7. Run Grafana in Docker

```bash
docker run -d \
  --name=grafana \
  --network=monitoring-net \
  -p 3000:3000 \
  grafana/grafana
```

## 🔑 8. Access Prometheus and Grafana in Browser

* **Prometheus** : `http://<vm-public-ip>:9090`
* **Grafana** : `http://<vm-public-ip>:3000`
* Default login: `admin / admin`

## 📈 9. Add Prometheus as Grafana Data Source

1. Open Grafana (`:3000`)
2. Go to **Settings → Data Sources → Add data source**
3. Choose **Prometheus**
4. Set URL to: `http://prometheus:9090`
   (This works because all containers are in the same Docker network: `monitoring-net`)
5. Click **Save & Test**

## 📂 10. Import Dashboard in Grafana

1. Go to **+ → Import**
2. Paste a dashboard ID from Grafana Dashboards
   * For Node Exporter: `1860` (Node Exporter Full)
3. Choose Prometheus as the data source
4. Import

## 🔎 11. Test Metric Collection

* Visit Prometheus → `http://<vm-ip>:9090/targets`
  * ✅ Ensure both `prometheus` and `node-exporter` targets are **UP**
* Visit Grafana dashboards
  * ✅ System metrics like CPU, Memory, Disk should show up

## 🧹 12. Optional: Enable Docker Compose

To make managing containers easier in the future:

```bash
sudo apt install docker-compose -y
```

You can then define all services in a `docker-compose.yml`.

## ⚠️ Final Notes on Costs

| Action                              | Incur Charges? |
| ----------------------------------- | -------------- |
| VM running                          | ✅ Yes         |
| VM stopped from inside OS           | ✅ Yes         |
| VM**deallocated from Portal** | ❌ No CPU cost |
| OS Disk attached (even if stopped)  | ✅ Yes         |
| Public IP (static)                  | ✅ Yes         |

## ✅ Summary

You have successfully:

* Created an Azure VM
* Installed Docker
* Setup Prometheus + Node Exporter for monitoring
* Installed and configured Grafana
* Connected everything inside a Docker network
* Visualized system metrics on Grafana dashboard
