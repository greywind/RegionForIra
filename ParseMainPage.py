# -*- coding: utf-8
__author__ = 'brezickiy.sa'
from grab import Grab
from lxml.html import fromstring
from time import sleep

current_letter = 33
LETTERS_COUNT = current_letter + 1

GET_URL_MAX_COUNT = 10;


g = Grab()
g.setup(
    user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')

while current_letter < LETTERS_COUNT:
    current_letter += 1
    result = {}
    errors = [];

    print('LETTER: '+str(current_letter)+'/'+str(LETTERS_COUNT))

    tryNumber = 1
    while tryNumber <= GET_URL_MAX_COUNT:
        try:
            resp = g.go('http://mosopen.ru/streets/letter/' + str(current_letter))
            break
        except Exception:
            tryNumber += 1
    if tryNumber == GET_URL_MAX_COUNT:
        errors.append('http://mosopen.ru/streets/letter/' + str(current_letter))
        continue

    htmlLetter = fromstring(resp.body)
    streetURLs = [a.get('href') for a in htmlLetter.xpath('//div[@class="double_part"]/descendant::a')]
    streetIndex = 0
    streetCount = len(streetURLs)

    for streetURL in streetURLs:
        streetIndex += 1
        print('STREET: '+str(streetIndex)+'/'+str(streetCount))
        tryNumber = 1
        while tryNumber <= GET_URL_MAX_COUNT:
            try:
                resp = g.go(streetURL)
                break
            except Exception:
                tryNumber += 1
        if tryNumber == GET_URL_MAX_COUNT:
            errors.append(streetURL)
            continue

        htmlStreet = fromstring(resp.body)
        houseURLs = [a.get('href') for a in
                     htmlStreet.xpath('//*[@id="content"]/p[3]/descendant::a[not(contains(@href, "javascript"))]')]

        houseIndex = 0
        houseCount = len(houseURLs)

        for houseURL in houseURLs:
            houseIndex += 1
            print('HOUSE: '+str(houseIndex)+'/'+str(houseCount))
            tryNumber = 1
            while tryNumber <= GET_URL_MAX_COUNT:
                try:
                    resp = g.go(houseURL)
                    break
                except Exception:
                    tryNumber += 1
            if tryNumber == GET_URL_MAX_COUNT:
                errors.append(houseURL)
                continue

            htmlHouse = fromstring(resp.body)

            aoNodes = htmlHouse.xpath('//dt[text()="Округ:"]/following-sibling::dd/a')
            regionNodes = htmlHouse.xpath('//dt[text()="Район:"]/following-sibling::dd/a')
            indexNodes = htmlHouse.xpath('//dt[text()="Индекс:"]/following-sibling::dd/a')

            if len(aoNodes) == 0 or len(regionNodes) == 0 or len(indexNodes) == 0:
                continue

            ao = aoNodes[0].text_content()
            region = regionNodes[0].text_content()
            index = indexNodes[0].text_content()

            result[ao] = result.get(ao, {})
            result[ao][region] = result[ao].get(region, set())

            result[ao][region].add(index)

    resultFile = open('O:\\Cloud@Mail.Ru\\\MoscowStreets'+str(current_letter)+'.csv', 'a')

    for ao in result:
        for region in result[ao]:
            for index in result[ao][region]:
                resultFile.write(ao + '\t' + region + '\t' + index + '\n')

    resultFile.write(str(current_letter) + '\t' + str(current_letter) + '\t' + str(current_letter) + '\n')

    resultFile.close()

    errorsFile = open('O:\\Cloud@Mail.Ru\\MoscowStreets_ERRORS.csv', 'a')

    for e in errors:
        errorsFile.write(e+'\n')

    errorsFile.close()
