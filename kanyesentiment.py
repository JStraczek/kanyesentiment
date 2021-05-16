import json
import requests


def get_quotes(how_many):
    quote_list = []
    for i in range(how_many):
        url = 'https://api.kanye.rest'
        try:
            res = requests.get(url)
            quote = json.loads(res.text)['quote']
            if quote in quote_list:
                i -= 1
                continue
            quote_list.append(quote)
        except Exception:
            print('Could not get quote from %s' % url)

    return quote_list


def read_sentiment(quote):
    url = 'https://sentim-api.herokuapp.com/api/v1/'
    headers = {'Accept': "application/json",
               "Content-Type": "application/json"}
    payload = {"text": quote}
    try:
        res = requests.post(url, headers=headers, data=json.dumps(payload))
        # We only care about the overall result not the evaluation of specific sentences
        result = json.loads(res.text)['result']

        sentiment = result['type']
        polarity = result['polarity']
    except:
        print('Could not get sentiment from %s' % url)
        return None

    return sentiment, polarity


def solve():
    quote_list = get_quotes(amount)

    extreme_quote = quote_list[0]
    extreme_sentiment, extreme_polarity = read_sentiment(quote_list[0])
    has_extreme = False
    tmp = extreme_polarity

    count_dict = {'positive': 0, 'negative': 0, 'neutral': 0}

    print('Kanye quotes with sentiment evalutation: ')
    for i, quote in enumerate(quote_list):
        print(str(i+1) + '.', quote)
        quote_sentiment, quote_polarity = read_sentiment(quote)
        count_dict[quote_sentiment] += 1

        if quote_polarity != tmp:
            has_extreme = True
        tmp = quote_polarity

        if abs(quote_polarity) > abs(extreme_polarity):
            extreme_polarity = quote_polarity
            extreme_sentiment = quote_sentiment
            extreme_quote = quote

        print(
            f'This quote is {quote_sentiment} and it\'s polarity is: {quote_polarity}\n')

    print(f'Positive quotes: {count_dict["positive"]}')
    print(f'Negative quotes: {count_dict["negative"]}')
    print(f'Neutral quotes: {count_dict["neutral"]}\n')

    if has_extreme:
        print(
            f'The most extreme quote is: \n{extreme_quote} \nwith {extreme_sentiment} polarity of: {extreme_polarity}')
    else:
        print(
            f'All quotes are equally polarizing')


print('How many Kanye quotes do you want to evaluate?: (Give a number from 5 to 20)')
amount = int(input())
while not 5 <= amount <= 20:
    print('Number you provided is incorrect, please provide a number from 5 to 20')
    amount = int(input())

solve()
