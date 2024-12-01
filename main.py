from parser import parse_data
from extract import extract_data

raw_filename = "test"
messenger = "Telegram"
output_dir = "."


parse_data(raw_filename, messenger, output_dir) 
data, fields = extract_data(output_dir + "/data.csv")
print(data, '\n\n', fields)



# Testing some stuff before making it clean
# TODO: make these separate functions
msg_counts = {user: 0 for user in fields["users"]}
for msg in data:
    msg_counts[msg["user"]] += 1
sorted_msg_counts = sorted(msg_counts.items(), key = lambda x: x[1], reverse = True)

print("\n\nAnalysis results")
print("---------------------------------------------")
print(f"\x1B[4mTotal messages: {sum(msg_counts.values())}\x1B[0m")

for user_stat in sorted_msg_counts:
    print(f"{user_stat[0]}: {user_stat[1]} ({user_stat[1] / sum(msg_counts.values()) * 100:.1f} %)")
    # print(f"{user}: {msg_counts[user]} ({msg_counts[user] / sum(msg_counts.values()) * 100:.1f} %)")


print("---------------------------------------------")
