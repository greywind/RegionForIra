# -*- coding: utf-8
__author__ = 'brezickiy.sa'
from grab import Grab
from lxml.html import fromstring

LETTERS_COUNT = 1
current_letter = 1

result = {}
resultFile = open('C:\\MoscowStreets.csv', 'w')

g = Grab()
g.setup(user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')

while current_letter <= LETTERS_COUNT:
    resp = g.go('http://mosopen.ru/streets/letter/'+str(current_letter))
    htmlLetter = fromstring(resp.body)
    streetURLs = [a.get('href') for a in htmlLetter.xpath('//div[@class="double_part"]/descendant::a')]

    for streetURL in streetURLs:
        resp = g.go(streetURL)
        htmlStreet = fromstring(resp.body)
        houseURLs = [a.get('href') for a in htmlStreet.xpath('//*[@id="content"]/p[3]/a')]

        for houseURL in houseURLs:
            resp = g.go(houseURL)
            htmlHouse = fromstring(resp.body)

            ao = htmlHouse.xpath('//dt[text()="Округ:"]/following-sibling::dd/a')[0].text_content()
            region = htmlHouse.xpath('//dt[text()="Район:"]/following-sibling::dd/a')[0].text_content()
            index = htmlHouse.xpath('//dt[text()="Индекс:"]/following-sibling::dd/a')[0].text_content()

            result[ao] = result.get(ao, {})
            result[ao][region] = result[ao].get(region, [])
            result[ao][region].append(index)
            print(ao+'\t'+region+'\t'+index)

    current_letter += 1

for ao in result:
    for region in result[ao]:
        for index in result[ao][region]:
            resultFile.write(ao+'\t'+region+'\t'+index+'\n')