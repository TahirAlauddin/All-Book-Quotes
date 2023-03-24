import json
import unicodedata

csv_file = "data.txt"
json_file = "books_data.json"

data = []
with open(csv_file, encoding="utf-8") as file:
    reader = file.readlines()
    for row in reader:
        row = row.split("|")
        # split the facebook, twitter, and mail links by ~
        quotes = row[6].split("~")
        cleaned_quotes = []
        for quote in quotes:
            clean_quote = unicodedata.normalize('NFKD', quote).encode('ascii', 'ignore').decode('utf-8')
            cleaned_quotes.append(clean_quote)

        # create a dictionary for the row
        row_dict = {
            "image_src": row[0],
            "book_name": row[1],
            "author": row[2],
            "pages": row[3],
            "rating": row[4],
            "votes": row[5],
            "quotes": cleaned_quotes,
        }
        data.append(row_dict)

# write the JSON data to a file
with open(json_file, 'w') as outfile:
    json.dump(data, outfile)
