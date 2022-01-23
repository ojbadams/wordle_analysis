import itertools
import pandas as pd
import os

## Export five letter words, there are some issues with the csv so we can't used pandas
five_letter_words = []

for filei in os.listdir("files"): 
    with open("files//" + filei, encoding="utf8", errors='ignore') as f:
        for wordi in f.readlines():
            wordi = wordi.strip()
            if len(wordi) == 5 and wordi.isalnum():
                five_letter_words.append(wordi)

## Collect tuples of each letter with location of each letter 
dist = []

for wordi in five_letter_words:
    counter = 0
    for letteri in wordi:
        dist.append((letteri, counter))
        counter += 1

## Convert this letter, position list into a dataframe then count the occurences 
df = pd.DataFrame(dist, columns = ["Letter", "Position"])
df = df.value_counts().to_frame().reset_index()
df.to_csv("letter_quantity_distributions.csv", index = False)

## Now we know the most popular letters and in which positions
## n being the highest no of letters for each position
n = 30
pop_char = []
for index in range(0, 5):
    pop_char.append(list(df[df["Position"] == index]["Letter"].values[:n]))

## Use the itertools package, this is an implementation of cartesian product
## between each collection of elements
combos = list(itertools.product(pop_char[0], pop_char[1], pop_char[2], pop_char[3], pop_char[4]))

## We now have a list of combination of characters based on popularity distributions
## However, Wordle only considers proper words so we check if each word is in our original list
## We also remove words that have multiple letters, why? We want to identify the letters as 
## quick as possible.  
def letters_used(used_letters, current_word):
    for li in current_word:
        if li in used_letters:
            return False
    return True


valid_words = []
used_letters = []
for i in combos:
    if "".join(i) in five_letter_words \
        and sum(list(pd.DataFrame(i).value_counts())) == 5 \
            and "".join(i) not in valid_words \
                and letters_used(used_letters, "".join(i)):
        valid_words.append("".join(i))
        for j in "".join(i): 
            if j not in used_letters: 
                used_letters.append(j)

print(valid_words)
pd.DataFrame(valid_words).to_csv("best_words.csv", index = False)
