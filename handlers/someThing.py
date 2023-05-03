for a in range(1, 151):
    for b in range(1, 151):
        for c in range(1, 151):
            for d in range(1, 151):
                for e in range(1, 151):
                    print(f"{a}-{b}-{c}-{d}-{e}")
                    if a**5 + b**5 == e ** 5 - d ** 5 - c**5:
                        print(a + b + c + d + e)
                        break