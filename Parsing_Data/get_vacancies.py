from urllib.request import urlopen


def get_dict():
    url = "https://www.naumen.ru/career/trainee/"

    page = urlopen(url)
    html = page.read().decode("utf-8")

    def find_all(html, start_string, end_string):
        ans_list = []
        start = 0
        while True:
            start = html.find(start_string, start)
            if start == -1:
                break
            end = html.find(end_string, start + len(start_string))
            if end == -1:
                break
            ans_list.append(html[start + len(start_string):end])
            start = end + len(end_string)
        return ans_list

    href_start = "href=\"/career/trainee/"
    href_end = "\">"
    hrefs = find_all(html, href_start, href_end)
    # print(hrefs)

    towns = ["moscow", "ekb", "spb", "tver", "chlb", "krasnodar"]
    town_names = {"moscow": "Москва",
                  "ekb": "Екатеринбург",
                  "spb": "Санкт-Петербург",
                  "tver": "Тверь",
                  "chlb": "Челябинск",
                  "krasnodar": "Краснодар"}
    town_to_links = {}
    links = []
    for town in towns:
        town_to_links[town] = []

    for href in hrefs:
        for town in towns:
            if town in href:
                links.append(href)
                town_to_links[town].append(href)

    # print(links)
    links = list(set(links))
    link_to_utility = dict.fromkeys(links)
    for link in links:
        link_to_utility[link] = []

    ret_dict = {}
    for link in links:
        url = "https://www.naumen.ru/career/trainee/" + link
        # print(url)
        page = urlopen(url)
        html = page.read().decode("utf-8")
        title = find_all(html, "<title>", "</title>")[0]
        title = title[title.rfind("|", ) + 2:].capitalize()
        information = find_all(html[:html.find("Этапы отбора")], "<li>", "</li>")
        # information_titles = find_all(html, '<h2 class="title -small">', "</h2>")
        # print(information_titles)
        new_information = []
        for info in information:
            if "<strong>" not in info and "a class=" not in info:
                new_information.append(info)
        information = []
        for el in new_information:
            if not el:
                continue
            el = el.replace("</li>", "").replace("<li>", "").replace('\n', "").replace('\r', "").replace('\t',
                                                                                                         "").replace(
                ".", "").replace(";", "").replace("&nbsp", " ").replace("&mdash", " ").replace("<nobr>", "") \
                .replace("</nobr>", "").replace("&laquo", " ").replace("&hellip", " "). \
                replace("&raquo", " ").replace("  ", " ").strip()
            while el.find('<') != -1:
                f = el.find('<')
                s = el.find('>', f)
                el = el[:f] + el[(s + 1):]
            information.append(el.capitalize())
        link_to_utility[link] = (title, information)

    for town_id, town in town_names.items():
        ret_dict[town] = {}
        for link in town_to_links[town_id]:
            title, information = link_to_utility[link]
            ret_dict[town][title] = information

    # Индексация словаря(для использования в callback_data, так как не передает длинные строки)
    last_idx = 0
    new_dict = dict()
    for city in ret_dict.keys():
        if len(ret_dict[city]) > 0:
            new_dict['{},{}:'.format(last_idx, last_idx+len(ret_dict[city])) + city] = ret_dict[city]
            last_idx += len(ret_dict[city])
        else:
            new_dict['{},{}:'.format("#", '#') + city] = ret_dict[city]
    ret_dict = new_dict.copy()
    idx = 1
    final_dict = dict()
    for city in ret_dict.keys():
        new_dict = dict()
        for vac in ret_dict[city].keys():
            new_dict['{}:'.format(idx) + vac] = ret_dict[city][vac]
            idx += 1
        final_dict[city] = new_dict

    return final_dict


if __name__ == '__main__':
    res = get_dict()

    print(list(res.values()))