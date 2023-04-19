import math
import sys

outputs = sys.argv[0]
targets = sys.argv[1]


###wypisuje tez inne liczby
# worst_case = 0
# for (o, t) in zip(outputs, targets):
#     best_dist = math.inf
#     for j in o:
#         dist = abs(int(j[4:]) - int(t))
#         # dist = abs(int(j[4:]) - 789)
#         # print(j, t, dist)
#         if best_dist > dist:
#             best_dist = dist
#     # print('----', best_dist)
#     # if worst_case < best_dist:
#     #     worst_case = best_dist
#     worst_case += best_dist


worst_case = 0
for (o, t) in zip(outputs, targets):
    best_dist = math.inf
    bad_output = 0
    found = False
    for j in o:
        dist = abs(int(j[4:]) - int(t))
        # dist = abs(int(j[4:]) - 789)
        # print(j, t, dist)
        if best_dist > dist:
            best_dist = dist
        if abs(int(j[4:]) - int(t)) != 0:
            bad_output += 0.1
        else:
            found = True
    if found:
        best_dist = bad_output
    # if worst_case < best_dist:
    #     worst_case = best_dist
    worst_case += best_dist


### wypisuje tylko odpowiednia liczbe
# worst_case = -math.inf
# for (o, t) in zip(outputs, targets):
#     best_dist = math.inf
#     bad_output = 0
#     found = False
#     for j in o:
#         dist = abs(int(j[4:]) - int(t))
#         # dist = abs(int(j[4:]) - 789)
#         # print(j, t, dist)
#         if best_dist > dist:
#             best_dist = dist
#         if abs(int(j[4:]) - int(t)) != 0:
#             bad_output += 0.1
#         else:
#             found = True
#     if found:
#         best_dist = bad_output
#     if worst_case < best_dist:
#         worst_case = best_dist


sys.argv = [worst_case]
