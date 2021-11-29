import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def cowBullGame():
    while 1:
        print ("Player 1, enter a 4 lettered word with 1 vowel and 3 different consonants only: ")
        a = input().upper()
        word = list(a)
        n=0
        q = a.isalpha()

        if q!=1:
            print ("Only Alphabets allowed !!\n")
            continue
        elif len(word)!=4:
            print ("Please enter a word of length only of 4 characters\n")
            continue
        elif word[0]==word[1] or word[0]==word[2] or word[0]==word[3] or word[1]==word[2] or word[1]==word[3] or word[2]==word[3]:
            print("You have repeated letters in your word. Please try again.. \n")
            continue
        
        for i in range(4):
            if word[i] in ['A', 'E', 'I', 'O', 'U']:
                n = n+1
        if n!=1:
            print ("You have entered a word with ", n, " vowels. Only 1 vowel is allowed !!\n")
            continue
    
        break

    clearConsole()
    print ("Player 2, kindly note you have only 15 tries to guess the right word. All the best !!\n\n")
    t=1
    flag = 0

    while 1:
        print ("Try #", t, " :")
        print ("Enter a word of only 4 alphabets")
        r = input().upper()
        resp = list(r)
        q = r.isalpha()
        
        if len(resp)!=4:
            print ("Please enter a word of length only of 4 alphabets\n")
            continue
        elif q!=1:
            print ("Only Alphabets allowed !!\n")
            continue

        b = 0
        c = 0

        for j in range(4):
            if resp[j]==word[j]:
                b = b+1
        if b==4:
            print ("\n\n\n\nCongratulations!! You have guessed the correct word!!")
            print ("The word was ", a)
            print ("You guessed the correct word in ", t, " tries.")
            break

        for n1 in range(4):
            for n2 in range(n1+1,4):
                if resp[n1]==word[n2] or resp[n2]==word[n1]:
                    if resp[n1]==word[n2] and resp[n2]==word[n1]:
                        c=c+2
                    else:
                        c = c+1
        
        print("                                                           ", r, ": ", b, "B, ", c, "C")

        if t>14:
            flag = 1
            break
        t = t+1

    if flag==1:
        print ("\n\nWell played! The correct word was ", a, ". Better luck next time!")

if __name__ == "__main__":
    cowBullGame()