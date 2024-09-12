import mysql.connector

def db_connection():
    return mysql.connector.connect(
        host="localhost",  # or your MySQL server host
        user="root",
        password="seyi123",
        database="bincom_test"
    )


def display_polling_unit_results(polling_unit_uniqueid):
    connection = db_connection()
    cursor = connection.cursor()

    query = """
    SELECT party_abbreviation, party_score
    FROM announced_pu_results
    WHERE polling_unit_uniqueid = %s
    """

    cursor.execute(query, (polling_unit_uniqueid,))
    results = cursor.fetchall()

    if results:
        print(f"Results for Polling Unit {polling_unit_uniqueid}:")
        for row in results:
            print(f"Party: {row[0]}, Score: {row[1]}")
    else:
        print(f"No results found for Polling Unit {polling_unit_uniqueid}")

    cursor.close()
    connection.close()


# Example Usage:
#polling_unit_uniqueid = int(input("Enter Polling Unit Unique ID: "))
#display_polling_unit_results(polling_unit_uniqueid)


def display_lga_results(lga_id):
    connection = db_connection()
    cursor = connection.cursor()

    query = """
    SELECT apr.party_abbreviation, SUM(apr.party_score) AS total_score
    FROM polling_unit pu
    JOIN announced_pu_results apr ON pu.polling_unit_id = apr.polling_unit_uniqueid
    WHERE pu.lga_id = %s
    GROUP BY apr.party_abbreviation
    """

    cursor.execute(query, (lga_id,))
    results = cursor.fetchall()

    if results:
        print(f"Summed Results for LGA {lga_id}:")
        for row in results:
            print(f"Party: {row[0]}, Total Score: {row[1]}")
    else:
        print(f"No results found for LGA {lga_id}")

    cursor.close()
    connection.close()


# Example Usage:
#lga_id = int(input("Enter LGA ID: "))
#display_lga_results(lga_id)

def add_polling_unit_results():
    connection = db_connection()
    cursor = connection.cursor()

    polling_unit_uniqueid = input("Enter Polling Unit Unique ID: ")

    party_results = []
    while True:
        party_abbreviation = input("Enter Party Abbreviation (or 'q' to quit): ")
        if party_abbreviation.lower() == 'q':
            print('Program Successfully quit')
            break
        else:
           party_score = input(f"Enter score for {party_abbreviation}: ")
           party_results.append((polling_unit_uniqueid, party_abbreviation, party_score))

    # Insert results into the database
    for polling_unit_uniqueid, party_abbreviation, party_score in party_results:
        query = """
        INSERT INTO announced_pu_results (polling_unit_uniqueid, party_abbreviation, party_score)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (polling_unit_uniqueid, party_abbreviation, party_score))

    connection.commit()
    print("Results added successfully!")

    cursor.close()
    connection.close()

# Example Usage:
#add_polling_unit_results()

def main():
    while True:
        print("\nElection Results Management System")
        print("1. Display Polling Unit Results")
        print("2. Display Summed Total Results for an LGA")
        print("3. Add Results for a New Polling Unit")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            polling_unit_uniqueid = int(input("Enter Polling Unit Unique ID: "))
            display_polling_unit_results(polling_unit_uniqueid)
        elif choice == '2':
            lga_id = int(input("Enter LGA ID: "))
            display_lga_results(lga_id)
        elif choice == '3':
            add_polling_unit_results()
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
