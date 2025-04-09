# book_name_translation = {
#     'Genesis':'Gen',
#     'Exodus' :
#
#
# }


books = ['Genesis',
'Exodus',
'Leviticus',
'Numbers',
'Deuteronomy',
'Joshua',
'Judges',
'Ruth',
'1 Samuel',
'2 Samuel',
'1 Kings',
'2 Kings',
'1 Chronicles',
'2 Chronicles',
'Ezra',
'Nehemiah',
'Esther',
'Job',
'Psalms',
'Proverbs',
'Ecclesiastes',
'Song of Solomon',
'Isaiah',
'Jeremiah',
'Lamentations',
'Ezekiel',
'Daniel',
'Hosea',
'Joel',
'Amos',
'Obadiah',
'Jonah',
'Micah',
'Nahum',
'Habakkuk',
'Zephaniah',
'Haggai',
'Zechariah',
'Malachi',
'Matthew',
'Mark',
'Luke',
'John',
'Acts',
'Romans',
'1 Corinthians',
'2 Corinthians',
'Galatians',
'Ephesians',
'Philippians',
'Colossians',
'1 Thessalonians',
'2 Thessalonians',
'1 Timothy',
'2 Timothy',
'Titus',
'Philemon',
'Hebrews',
'James',
'1 Peter',
'2 Peter',
'1 John',
'2 John',
'3 John',
'Jude',
'Revelation']



def generate_abreviations():
    abreviation = []
    for book in books:
        book = book.replace(' ','')
        if len(book) < 4:
            abreviation.append(book)
        else:
            abreviation.append(book[0:3])

    return abreviation