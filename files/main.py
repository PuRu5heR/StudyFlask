def main():
    inp = open("test.txt", "r")
    out = open("answer.txt", "a")
    text = inp.read()
    inp.close()
    answer = eval(text)
    out.write(str(answer))

main()
