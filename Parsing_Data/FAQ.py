from urllib.request import urlopen


def make_faq():
    url = "https://www.naumen.ru/career/trainee/"

    page = urlopen(url)
    html = page.read().decode("utf-8")

    def find_between(html, start, last):
        ans_list = {}
        while True:
            start = html.find("<h2>", start)
            if start == -1 or start > last:
                break
            end = html.find("</h2>", start + 4)
            question = html[start + 4:end]
            start = end + 5

            start = html.find("<p>", start)
            end = html.find("</p>", start + 3)
            answer = html[start + 3:end].replace("&nbsp;", " ").replace("<nobr>", "").replace("</nobr>", " ")
            while answer.find("<") != -1:
                pos = answer.find("<")
                pos1 = answer.find(">", pos)
                answer = answer[:pos] + answer[(pos1 + 1):]

            start = end + 4

            ans_list[question] = answer
        return ans_list

    begin = html.find("F.A.Q.")
    end = html.find("Связаться с нами")

    dictionary = find_between(html, begin, end)
    for key in dictionary.keys():
        dictionary[key] = dictionary[key].replace('&mdash;', ' - ')

    return dictionary


if __name__ == '__main__':
    dictionary = make_faq()
    for key in dictionary.keys():
        print(dictionary[key])
