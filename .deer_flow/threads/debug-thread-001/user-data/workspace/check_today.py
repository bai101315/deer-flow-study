import datetime

# Current timestamp from the system
current_ts = 1776633600  # approximate for 2026-04-19

# Today's date
today = datetime.date(2026, 4, 19)
today_start = datetime.datetime(2026, 4, 19, 0, 0, 0)
today_start_ts = int(today_start.timestamp())

print(f"Today: {today}")
print(f"Today start timestamp: {today_start_ts}")

# Submission timestamps from the data
submissions = [
    (719494295, 1776601291, "Multi Source Flood Fill"),
    (719494245, 1776601279, "Smallest Stable Index II"),
    (719494222, 1776601273, "Smallest Stable Index I"),
    (719421197, 1776586318, "Maximum Distance Between a Pair of Values"),
    (719416859, 1776585616, "Maximum Distance Between a Pair of Values"),
    (719414196, 1776585190, "Maximum Distance Between a Pair of Values"),
    (719412541, 1776584890, "Maximum Distance Between a Pair of Values"),
    (719272761, 1776522014, "Subarray Sum Equals K"),
    (719272653, 1776521987, "Subarray Sum Equals K"),
    (719269532, 1776521237, "Longest Substring Without Repeating Characters"),
    (719221842, 1776508285, "Mirror Distance of an Integer"),
    (719060936, 1776435625, "Trapping Rain Water"),
    (719052740, 1776433764, "3Sum"),
    (719051591, 1776433495, "3Sum"),
    (719047082, 1776432449, "Container With Most Water"),
]

print("\nToday's submissions (2026-04-19):")
print("-" * 60)

today_subs = []
for sub_id, ts, title in submissions:
    if ts >= today_start_ts:
        dt = datetime.datetime.fromtimestamp(ts)
        today_subs.append((dt, title, sub_id))
        print(f"{dt.strftime('%H:%M:%S')} - {title} (ID: {sub_id})")

print(f"\nTotal: {len(today_subs)} submissions today")