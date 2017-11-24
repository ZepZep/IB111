import pickle
import matplotlib.pyplot as plt
import numpy as np

with open("people.pickle", "rb") as f:
    people = pickle.load(f)

print(len(people))

monthDays = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
names = list(range(1, 13))

nobelCounts = [0]*12

for person in people:
    bdate = person["bdate"]
    if bdate is not None:
        l = bdate.split("-")
        if len(l) == 3:
            month = int(l[1])
            nobelCounts[month-1] += 1

insurence = [0] * 12
with open("insurence.txt", "r") as f:
    for line in f.readlines():
        l = line.split(" ")
        month = int(l[0][:2])
        count = int(l[1])

        insurence[month-1] += count

chessCounts = [0] * 12
with open("chess.txt", "r") as f:
    for line in f.readlines():
        l = line.split("-")
        if len(l) >= 2:
            month = int(l[1])
            chessCounts[month - 1] += 1

soccer = [924, 785, 802, 761, 772, 679, 736, 805, 792, 842, 727, 735]


def getNormalized(months):
    global monthDays
    monthsum = sum(months)
    return [mc/monthDays[i]*365.25/12/monthsum*100 for i, mc in enumerate(months)]


normNobel = getNormalized(nobelCounts)
normInsurence = getNormalized(insurence)
normChess = getNormalized(chessCounts)
normSoc = getNormalized(soccer)

print("Birth ", normInsurence)
print("Nobel ", normNobel)
print("Chess ", normChess)
print("Soccer", normSoc)

print(np.corrcoef(normInsurence, normNobel))

plt.subplot(2,2,1).set_title("birth")
plt.bar(names, normInsurence)
plt.subplot(2,2,2).set_title("nobel")
plt.bar(names, normNobel)
plt.subplot(2,2,3).set_title("chess")
plt.bar(names, normChess)
plt.subplot(2,2,4).set_title("soccer")
plt.bar(names, normSoc)

plt.show()
