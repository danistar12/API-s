from sqlalchemy import create_engine, MetaData, Table, select


engine = create_engine('sqlite:///books.db')

# Create a metadata instance
metadata = MetaData()

# Reflect the book table from the database
book_table = Table('book', metadata, autoload_with=engine)

# Create a select statement to query the title column in alphabetical order
stmt = select(book_table.c.title).order_by(book_table.c.title)

# Execute the statement and fetch all results
with engine.connect() as connection:
    results = connection.execute(stmt).fetchall()

# Print the titles
for row in results:
    print(row.title)