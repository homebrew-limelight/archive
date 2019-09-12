import api

# print(s)
# print()
# print(s.dict())
# print()
# print(s.dict(skip_defaults=True))
# print()

s = api.Settings(morph=api.Settings.Morph(enable=True, erode=999))

print()
print(s)
print()
print(s.dict())
print()
print(s.dict(skip_defaults=True))
print()
