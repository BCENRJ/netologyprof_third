from my_fun import formate_habr, last_page, my_re, headers


def main():
    print(*formate_habr(last_page, my_re, headers), sep='\n')


if __name__ == '__main__':
    main()
