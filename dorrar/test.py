from bs4 import BeautifulSoup


# Example usage:
html_example = """
وكَذَا، فإنْ كُنْتِ بَرِيئَةً، فَسَيُبَرِّئُكِ اللَّهُ، وإنْ كُنْتِ <a class="hist-link" href="/ghreeb/12617" target="_blank">ألْمَمْتِ</a> بذَنْبٍ، فَاسْتَغْفِرِي اللَّهَ وتُوبِي إلَيْهِ، فإنَّ العَبْدَ إذَا اعْتَرَفَ ثُمَّ تَابَ، <a class="hist-link" href="/ghreeb/6967">
"""

cleaned_text = remove_html_tags(html_example)
print(cleaned_text)
