test = "1 hr. 40 min."
# test = "40 min."
# if minute in test:
#     print("hi")

# if hour in test:
#     print("bye")

# if (hour in test) and (minute in test):
#     print("bruh")

# split = test.split('hr')
# print(split)

split = test.rstrip('.').split('.')
hour = 0
min = 0
if len(split) == 2:
    hour = int(split[0].split()[0])
    min = int(split[1].split()[0])
else:
    min = int(split[0].split()[0])

duration = (hour * 60) + min
print(hour)
print(min)
print(f"duration: {duration}")