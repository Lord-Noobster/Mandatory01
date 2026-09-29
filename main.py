import pandas as pd
import json

try:
    with open("incident.json", "r") as f:
        data = json.load(f)

    alerts = data["alerts"]

    entity_config = [
        ("domains", "alerts_domains.csv"),
        ("fileHashes", "alerts_fileHashes.csv"),
        ("ips", "alerts_ips.csv"),
        ("processes", "alerts_processes.csv"),
    ]

    for entity_field, output_file in entity_config:
        rows = []

        for alert in alerts:
            rows.append(
                {
                    "alertId": alert["alertId"],
                    "machineId": alert.get("machineId", ""),
                    "firstActivity": alert.get("firstActivity", ""),
                    entity_field: alert["entities"].get(entity_field, []),
                }
            )

        df = pd.DataFrame(rows)
        df = df.explode(entity_field, ignore_index=True)
        df.to_csv(output_file, index=False)
        print(f"{output_file}")
except FileNotFoundError:
    print("Error: incident.json file not found.")
except json.JSONDecodeError:
    print("Error: file not a valid JSON")
except Exception as e:
    print(f"Error: {e}")
