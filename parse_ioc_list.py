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
        
        if '†' in genus:
            is_extinct = True
            genus = genus.replace('†', '').strip()

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
        
        # Add everything to the row
        name_parts = filter(lambda x: x != None and x != '', [last_genus, last_species, subspecies])
        fullName = ' '.join(name_parts)
        scientificName = (fullName +  ' ' + row['Authority']).strip() # strip just in case
        row['Full Name'] = fullName
        [row['Infraclass'], row['Parvclass'], row['Order'], row['Family (Scientific)'], row['Family (English)'], row['Genus'], row['Species (Scientific)'], row['Canonical Scientific Name'], row['Full Scientific Name']] = [last_infraclass, last_parvclass, last_order, last_family, last_english_family, last_genus, last_species, fullName, scientificName]
        row["Comment"] = row["Comment"].strip()
        row["Extinct"] = is_extinct

        new_rows.append(row)

    # Write the new rows to a new CSV file
    print('Writing new CSV file...')
    with open(path.join(csvDir, csvFile.replace('.csv', '_cleaned.csv')), 'w', encoding='utf8', newline='', errors='ignore') as new_file:
        fieldnames = list(row.keys())

        def move_item(lst, old_index, new_index):
            item = lst.pop(old_index)
            lst.insert(new_index, item)
            return lst
        fieldnames = move_item(fieldnames, fieldnames.index('Canonical Scientific Name'), fieldnames.index('Authority') + 1)
        fieldnames = move_item(fieldnames, fieldnames.index('Full Scientific Name'), fieldnames.index('Authority') + 2)

        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in new_rows:
            writer.writerow(row)

print('All done...')


        