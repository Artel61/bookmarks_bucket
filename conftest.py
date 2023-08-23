import pytest


@pytest.fixture
def fxt_opengraph_raw_html():
    return '''<html prefix="og: https://ogp.me/ns#">
<head>
<title>The Rock (1996)</title>
<meta property="og:title" content="The Rock" />
<meta property="og:type" content="video.movie" />
<meta property="og:url" content="https://www.imdb.com/title/tt0117500/" />
<meta property="og:image" content="https://ia.media-imdb.com/images/rock.jpg" />
...
</head>
...
</html>'''


@pytest.fixture
def fxt_raw_html():
    return '''<html><head><title>Test</title></head><body><h1>Parse me!</h1></body></html>'''


@pytest.fixture
def fxt_corrupted_raw_html():
    return '''<html><head><body</html>'''


@pytest.fixture
def fxt_text_instead_of_html():
    return 'This text will kill you, Parser!'
