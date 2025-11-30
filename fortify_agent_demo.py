#!/usr/bin/env python
# coding: utf-8

# ============================================================
# Simulated Sequential Agent for Jenkins + Fortify SSC Check
# Local Version (No Kaggle, No Cloud Needed)
# ============================================================

import random
import pandas as pd
from datetime import datetime


# ------------------------------------------------------------
# 1. Simulated Jenkins Pipeline Stage
# ------------------------------------------------------------

class MockJenkins:
    
    def __init__(self):
        """
        Simulate Jenkins pipeline stages and their execution times.
        """
        self.pipeline_data = {
            "service-A": random.randint(5, 25),
            "service-B": random.randint(5, 25),
            "service-C": random.randint(5, 25),
            "service-D": random.randint(5, 25),
        }
    
    def get_scan_duration(self, service_name):
        return self.pipeline_data.get(service_name, None)


# ------------------------------------------------------------
# 2. Simulated Fortify SSC System
# ------------------------------------------------------------

class MockFortifySSC:
    
    def __init__(self):
        self.ssc_status_data = {
            "service-A": random.choice(["Pending Approval", "Approved", "In Progress"]),
            "service-B": random.choice(["Pending Approval", "Approved", "In Progress"]),
            "service-C": random.choice(["Pending Approval", "Approved", "In Progress"]),
            "service-D": random.choice(["Pending Approval", "Approved", "In Progress"]),
        }
    
    def get_project_status(self, service_name):
        return self.ssc_status_data.get(service_name, None)


# ------------------------------------------------------------
# 3. Sequential Agent Logic
# ------------------------------------------------------------

class FortifyApprovalAgent:
    
    def __init__(self, jenkins, ssc, threshold_minutes=15):
        self.jenkins = jenkins
        self.ssc = ssc
        self.threshold = threshold_minutes
        self.log = []
    
    def run_check(self):
        print("=== Sequential Agent Execution Started ===")
        print(f"Threshold: {self.threshold} minutes\n")

        for service in self.jenkins.pipeline_data.keys():
            duration = self.jenkins.get_scan_duration(service)
            print(f"Checking Jenkins scan time for {service} → {duration} mins")

            if duration > self.threshold:
                print(f"⛔ {service}: Scan exceeded {self.threshold} mins – Checking SSC...")

                status = self.ssc.get_project_status(service)
                print(f"SSC Status for {service}: {status}")

                if status == "Pending Approval":
                    print(f"⚠️  Logging: {service} is stuck in Pending Approval\n")
                    self.log.append({
                        "service": service,
                        "scan_duration": duration,
                        "ssc_status": status,
                        "timestamp": datetime.now()
                    })
                else:
                    print(f"✔ SSC status OK for {service}\n")
            else:
                print(f"✔ {service}: Scan time OK\n")

        print("=== Agent Execution Complete ===")

    def get_log_dataframe(self):
        if not self.log:
            return pd.DataFrame(columns=["service", "scan_duration", "ssc_status", "timestamp"])
        return pd.DataFrame(self.log)


# ------------------------------------------------------------
# 4. Run the Simulation
# ------------------------------------------------------------

if __name__ == "__main__":
    jenkins = MockJenkins()
    ssc = MockFortifySSC()
    agent = FortifyApprovalAgent(jenkins, ssc)

    agent.run_check()

    # ------------------------------------------------------------
    # 5. Display Results
    # ------------------------------------------------------------

    df_logs = agent.get_log_dataframe()

    print("\n\n==================== LOGGED SERVICES ====================")
    if df_logs.empty:
        print("No services exceeded threshold *and* were pending approval.")
    else:
        print(df_logs.to_string(index=False))
