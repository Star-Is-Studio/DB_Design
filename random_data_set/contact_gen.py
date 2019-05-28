import random
r = random.randint
cases = int(input("how many generate contacts? : "))
with open("random_data_set/contact.csv","wt") as f:
    for _ in range(cases):
        print("010-{:04d}-{:04d}".format(r(0,9999),r(0,9999)), file=f)