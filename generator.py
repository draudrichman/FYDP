import csv
import json

# Define input file paths
video_id = "V048"
csv_file = "v048.csv"  # Replace with actual path
text_file = "actions.txt"  # Replace with actual path

# Load predefined action labels
action_labels = {}
next_action_id = 0

with open(text_file, "r") as f:
    for line in f:
        line = line.strip()
        if line:
            action_id, action_desc = line.split(" ", 1)
            action_labels[action_desc] = action_id
            action_num = int(action_id[1:])  # Extract number from "cXXX"
            next_action_id = max(next_action_id, action_num)

# Prepare data from CSV
annotations = []
new_actions = []
with open(csv_file, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)  # Skip header row

    for row in reader:
        if len(row) < 5:  # Ensure row has enough columns
            continue  

        _, video_file, start_time, end_time, metadata = row

        try:
            start_time, end_time = float(start_time), float(end_time)
        except ValueError:
            # print(f"Skipping row with invalid timestamps: {row}")
            continue

        action_desc = json.loads(metadata)["subtitle"]

        # Assign existing action ID or generate a new one
        if action_desc in action_labels:
            action_id = action_labels[action_desc]
        else:
            next_action_id += 1
            action_id = f"c{next_action_id:03d}"
            action_labels[action_desc] = action_id
            new_actions.append(f"{action_id} {action_desc}")

        annotations.append(f"{action_id} {start_time:.2f} {end_time:.2f}")

# Update actions.txt with new actions
if new_actions:
    with open(text_file, "a") as f:  # Append mode
        f.write("\n".join(new_actions) + "\n")

# Generate the final output string
manual_placeholder = ""  # This will be manually added later
formatted_string = f'{video_id},"{manual_placeholder}",' + ";".join(annotations) + f",{end_time:.2f}"

print(formatted_string)
