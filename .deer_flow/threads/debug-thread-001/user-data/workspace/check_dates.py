import datetime

timestamps = [1776601291, 1776601279, 1776601273, 1776586318, 1776585616, 1776585190, 1776584890, 1776522014, 1776521987, 1776521237, 1776508285, 1776435625, 1776433764, 1776433495, 1776432449]

for ts in timestamps:
    dt = datetime.datetime.fromtimestamp(ts)
    print(f"{dt.strftime('%Y-%m-%d %H:%M:%S')} - {ts}")