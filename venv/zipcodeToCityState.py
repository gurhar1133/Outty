from uszipcode import SearchEngine


def get_citystate_data(zip):
    # set simple_zipcode=False to use rich info database
    search = SearchEngine(simple_zipcode=True)
    zipcode = search.by_zipcode(zip)
    return [zipcode.major_city, zipcode.state]
