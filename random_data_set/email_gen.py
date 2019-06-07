import random
with open('random_data_set/english_word.csv','rt') as f:
    with open("random_data_set/email.csv","wt") as wf:
        words = f.readlines()
        counts = int(input("How many generate email? : "))
        for _ in range(counts):
            id,domain = random.choices(words,k=2)
            print("{}@{}.com".format(id.strip(),domain.strip()),file=wf)