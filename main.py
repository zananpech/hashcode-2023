import collections
import csv
import heapq
from Destination import Destination
from Group import Group

map = collections.defaultdict(list)
groups = {}
destinations_category_map  = collections.defaultdict(list)
destinations_name_map = {}


with open('production/Map.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        from_, to, dist = row
        from_key = row[from_]
        to_key = row[to]
        dist_key = row[dist]
        map[from_key.strip()].append([float(dist_key), to_key.strip()])
        map[to_key.strip()].append([float(dist_key), from_key.strip()])

with open('production/Groups.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        size, time, identifier = row
        size_key = row[size]
        time_key = row[time]
        identifier_key = row[identifier]
        groups[identifier_key] = Group(int(size_key), float(time_key), identifier_key)
       
with open('production/Interests.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        category, interest, group_id = row
        category_key = row[category]
        group_id_key = row[group_id]
        group = groups[row[group_id]]
        group.interest[category_key.strip()] = 1 + group.interest.get(category_key.strip(), 0)

with open('production/Destinations.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name, category, rating, duration, price = row
        category_key = row[category]
        name_key = row[name]
        rating_key = row[rating]
        duration_key = row[duration]
        price_key = row[price]
        heapq.heappush(destinations_category_map[category_key.strip()], [-1 * float(rating_key), float(duration_key), float(price_key), name_key.strip()])
        destinations_name_map[name_key.strip()] = Destination(category_key, float(rating_key), float(duration_key), float(price_key), name_key.strip())
        
# print(map)

output = []

for group_id in groups:
    group = groups[group_id]
    
    #sort group based on number of vote, pick the most voted one
    group_interest = sorted(group.interest.items(), key=lambda x: -x[1])
    start_category = None
    
    #find category in group interest that exist in destionation list
    for interest  in group_interest:
        current_category, vote = group_interest.pop(0)

        if not current_category in destinations_category_map:
            continue
        #when the first one is found, break
        else:
            start_category = current_category
            break

    start_destination = destinations_category_map[start_category][0]
    rating, time, price, name = start_destination
    
    min_heap = [[0, name]]
    visit = set()
    visit.add(name)
    
    #start djikstra's algorithm
    while min_heap and group.time > 0:  
        
        current_distance, current_destination_name = heapq.heappop(min_heap)
        current_destination = destinations_name_map[current_destination_name]
       
        # We need to check if current destionation category is in group interest
        if current_destination.category in group.interest:
            group.time -= current_destination.duration
            output.append([current_destination.name, current_destination.category, str(current_destination.duration), group_id])
        # Loop through neighboring places and check if it's already visited or not in the map
        for distance, next_destination_name in map[current_destination.name]:
            if next_destination_name in visit or next_destination_name not in destinations_name_map:
                continue
            heapq.heappush(min_heap, [current_distance + distance, next_destination_name])
            visit.add(next_destination_name)

with open('output.csv', 'w', newline='') as output_file:
    # create the csv writer
    writer = csv.writer(output_file)
    writer.writerow(["Name Destination", "Category", "Time Spent", "Group"])
    for row in output:
        writer.writerow(row)
        
print("Write success!")