import re

print(re.findall("\w\w", "AV did idic didn"))
print(re.findall("@\w+.\w+","@example@gmail.com, example@mail.ru, example@yandex.by"))
result = re.sub (r'Good', 'Cool', 'Why Python is a Good Programming Language? ')
print(result)
result = re.findall(r'\b\w.', 'AV is largest Analytics community of India')
print(result)
result = re.search(r'(?:@\w+.\w+)', 'abc.test@gmail.com, xyz@test.in, test.first@analyticsvidhya.com, first.test@rest.biz')
print(result.groups())

