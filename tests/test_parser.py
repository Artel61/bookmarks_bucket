from bookmarks_bucket.context.parser import OpenGraphParser


def test_parse_html_with_opengraph_markup(fxt_opengraph_raw_html):
    parser = OpenGraphParser()
    parser.feed(fxt_opengraph_raw_html)
    assert parser.opengraph_markup


def test_parse_html_without_opengraph_markup(fxt_raw_html):
    parser = OpenGraphParser()
    parser.feed(fxt_raw_html)
    assert not parser.opengraph_markup


def test_parse_corrupted_html(fxt_corrupted_raw_html, fxt_text_instead_of_html):
    parser = OpenGraphParser()

    parser.feed(fxt_corrupted_raw_html)
    assert not parser.opengraph_markup

    parser.feed(fxt_text_instead_of_html)
    assert not parser.opengraph_markup
