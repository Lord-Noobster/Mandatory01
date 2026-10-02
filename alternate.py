import json
import csv


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
    field_names = ["alertId", "machineId", "firstActivity", entity_field]

    with open(output_file, "w", newline="", encoding="utf-8") as out_f:
        writer = csv.DictWriter(out_f, fieldnames=field_names, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for alert in alerts:
            alert_id = alert["alertId"]
            machine_id = alert.get("machineId", "")
            first_activity = alert.get("firstActivity", "")
            entities_list = alert.get("entities", {}).get(entity_field, [])

            if not entities_list:
                writer.writerow(
                    {
                        "alertId": alert_id,
                        "machineId": machine_id,
                        "firstActivity": first_activity,
                        entity_field: "",
                    }
                )
            else:
                for item in entities_list:
                    writer.writerow(
                        {
                            "alertId": alert_id,
                            "machineId": machine_id,
                            "firstActivity": first_activity,
                            entity_field: item,
                        }
                    )

    print(f"{output_file}")
