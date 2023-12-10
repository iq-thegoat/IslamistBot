from islamway import Parser

p = Parser()

d = p.Books.search_book("التوحيد", limit=2)
print(d)
