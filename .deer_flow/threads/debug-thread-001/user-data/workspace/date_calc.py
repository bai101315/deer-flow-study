from datetime import datetime, timedelta

# 获取当前时间
now = datetime.now()
today = now.date()

# 一天前
one_day_ago = today - timedelta(days=1)

# 一周前
one_week_ago = today - timedelta(weeks=1)

# 一个月前（使用30天近似）
one_month_ago = today - timedelta(days=30)

# 输出结果
print("=== 当前时间 ===")
print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"当前日期: {today}")

print("\n=== 一天前 ===")
print(f"一天前: {one_day_ago.strftime('%Y-%m-%d')} 00:00 至 {one_day_ago.strftime('%Y-%m-%d')} 23:59")

print("\n=== 一周前 ===")
print(f"一周前: {one_week_ago.strftime('%Y-%m-%d')} 00:00 至 {one_week_ago.strftime('%Y-%m-%d')} 23:59")

print("\n=== 一个月前 ===")
print(f"一个月前: {one_month_ago.strftime('%Y-%m-%d')} 00:00 至 {one_month_ago.strftime('%Y-%m-%d')} 23:59")

print("\n=== 汇总 ===")
print(f"一天前: {one_day_ago.strftime('%Y-%m-%d')} 00:00 至 {one_day_ago.strftime('%Y-%m-%d')} 23:59")
print(f"一周前: {one_week_ago.strftime('%Y-%m-%d')} 00:00 至 {one_week_ago.strftime('%Y-%m-%d')} 23:59")
print(f"一个月前: {one_month_ago.strftime('%Y-%m-%d')} 00:00 至 {one_month_ago.strftime('%Y-%m-%d')} 23:59")