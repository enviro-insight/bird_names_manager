# parse the list, drop subspecies, remove extinction symbols (add a column)
import csv
from os import path

csvDir = r'D:\Enviro Insight\Data'
csvFile = 'master_ioc_list_v15.1.csv'

# the IOC list only records genus and species names for the first entry of those names, the following rows are blank
# for those cells, so we need to fill in the genus as we go. 
# If the species name is blank, we need to skip that row
# Otherwise use the last genus name we saw the species, and the english name
print('Parsing IOC list...')
with open(path.join(csvDir, csvFile), 'r', encoding='utf-8-sig', errors='ignore') as file:
    reader = csv.DictReader(file)
    
    last_infraclass = None
    last_parvclass = None
    last_order = None
    last_family = None
    last_english_family = None
    last_genus = None
    last_species = None

    new_rows = []

    for row in reader:
        is_extinct = False
        infraclass = row['Infraclass']
        parvclass = row['Parvclass']
        order = row['Order']
        family = row['Family (Scientific)']
        english_family = row['Family (English)']
        genus = row['Genus']
        species = row['Species (Scientific)']
        if '†' in species:
            is_extinct = True
            species = species.replace('†', '').strip()

        subspecies = row['Subspecies']
        if '†' in subspecies:
            is_extinct = True
            subspecies = subspecies.replace('†', '').strip()

        if infraclass:
            last_infraclass = infraclass
        if parvclass:
            last_parvclass = parvclass
        if order:
            last_order = order
        if family:
            last_family = family
            last_english_family = english_family
        if genus:
            last_genus = genus
        if species:
            last_species = species
            
        # If the species name is blank, skip this row
        if not species and not subspecies:
            continue

        # Remove the extinction symbols
        genus = genus.replace('†', '').strip()
        species = species.replace('†', '').strip()
        subspecies = subspecies.replace('†', '').strip()
        
        # Add the genus and species name to the row
        [row['Infraclass'], row['Parvclass'], row['Order'], row['Family (Scientific)'], row['Family (English)'], row['Genus'], row['Species (Scientific)']] = [last_infraclass, last_parvclass, last_order, last_family, last_english_family, last_genus, last_species]
        row["Comment"] = row["Comment"].strip()
        row["Extinct"] = is_extinct

        new_rows.append(row)

    # Write the new rows to a new CSV file
    print('Writing new CSV file...')
    with open(path.join(csvDir, csvFile.replace('.csv', '_cleaned.csv')), 'w', encoding='utf8', newline='', errors='ignore') as new_file:
        fieldnames = reader.fieldnames.copy()  # make a copy to avoid modifying the original
        if 'Extinct' not in fieldnames:
            fieldnames.append('Extinct')
        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in new_rows:
            writer.writerow(row)

print('All done...')


        