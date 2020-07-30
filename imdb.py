import pandas
import requests

from bs4 import BeautifulSoup


def load_imdb(chart='top rated') -> pandas.DataFrame:
    """
    Returns selected chart from IMDb website.


    Parameters
    ----------
    chart : str, default: 'top'
        IMDb chart to load. Possible values: 'box office', 'most popular',
        'top rated', 'top rated english', 'most popular tv', 'top tv',
        'lowest rated'.


    Returns
    -------
    pandas.DataFrame
        DataFrame with the selected chart sorted according to the parameters.
    """
    charts = {
        'box office': 'boxoffice',
        'most popular': 'moviemeter',
        'top rated': 'top',
        'top rated english': 'top-english-movies',
        'most popular tv': 'tvmeter',
        'top tv': 'toptv',
        'lowest rated': 'bottom'
    }
    tv_charts = {'most popular tv', 'top tv'}
    tv = chart in tv_charts

    if chart not in charts:
        raise ValueError(
            f'Invalid argument for IMDb chart: {chart}. See the docs.')

    # downloading the content
    url = 'https://www.imdb.com/chart/' + charts[chart]
    tree = BeautifulSoup(requests.get(url).content, 'html.parser')

    # extracting all the rows from the chart
    rows = tree.find('tbody').find_all('tr')

    # TV AND BOX OFFICE CHARTS ARE DIFFERENT FROM THE REST
    # m is short for movie

    # extracting the links and the names of directors and stars
    # for tv shows where there were no names had to use 'try except'
    links = ('https://www.imdb.com' +
             m.find('td', 'titleColumn').a['href'] for m in rows)
    if not tv:
        names = [m.find('td',
                        'titleColumn'
                        ).a['title'].partition(' (dir.), ') for m in rows]
        directors = (name[0] for name in names)
        stars = (name[2] for name in names)
    else:
        stars = []
        for m in rows:
            try:
                stars.append(m.find('td', 'titleColumn').a['title'])
            except KeyError:
                stars.append(None)

    # box office chart doesn't provide usual fields, title path is different
    if chart == 'box office':
        titles = (m.find('td', 'titleColumn').text.strip() for m in rows)
        weekend = (m.find('td', 'ratingColumn').text.strip() for m in rows)
        gross = (m.find('span').text.strip() for m in rows)
        weeks = (m.find('td', 'weeksColumn').text.strip() for m in rows)

        return pandas.DataFrame({'Title': titles,
                                 'Weekend': weekend,
                                 'Gross': gross,
                                 'Weeks': weeks,
                                 'Director': directors,
                                 'Stars': stars,
                                 'Link': links})

    # for all but box office
    titles = (m.find('td', 'titleColumn').a.text for m in rows)
    years = (m.find('span', 'secondaryInfo').text.strip('()') for m in rows)

    # generator comprehension is too messy here because of the missing ratings
    # in several charts
    ratings = []
    votes = []
    for m in rows:
        rate = m.find('strong')
        if rate:
            ratings.append(rate.text)
            votes.append(rate['title'].split()[-3].replace(',', ''))
        else:
            ratings.append(None)
            votes.append(None)

    if tv:
        return pandas.DataFrame({'Title': titles,
                                 'Year': years,
                                 'Rating': ratings,
                                 'Votes': votes,
                                 'Stars': stars,
                                 'Link': links})
    return pandas.DataFrame({'Title': titles,
                             'Year': years,
                             'Rating': ratings,
                             'Votes': votes,
                             'Director': directors,
                             'Stars': stars,
                             'Link': links})
