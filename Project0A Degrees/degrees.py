import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    If no possible path, returns None.
    """
    if source == target:
        return []
    
    path_front = QueueFrontier()
    path_front.add([(None, source)])
    path_back = QueueFrontier()
    path_back.add([(None, target)])
    cost = {source:(1, None), target: (-1, None)}

    while not path_front.empty() or not path_back.empty():
        if path_front.empty():
            continue
        path = path_front.remove()
        current = path[-1][1]
        for movie in people[current]["movies"]:
            for person in movies[movie]["stars"]:
                foundValue, foundPath = cost.get(person, (0, None))
                if foundValue == -1:
                    if foundPath == None:
                        return path[1:] + [(movie, person)]
                    else:
                        return path[1:] + [(movie, person)] + foundPath[1:][::-1]
                elif foundValue == 0:
                    copyPath = []
                    for node in path:
                        copyPath.append(node)
                    copyPath.append((movie, person))
                    cost[person] = (1, copyPath)
                    path_front.add(copyPath)
        if path_back.empty():
            continue
        path = path_back.remove()
        current = path[-1][1]
        for movie in people[current]["movies"]:
            for person in movies[movie]["stars"]:
                foundValue, foundPath = cost.get(person, (0, None))
                if foundValue == 1:
                    if foundPath == None:
                        return [(movie, current)] + path[1:][::-1]
                    else:
                        return foundPath[1:] + [(movie, current)] + path[1:][::-1]
                elif foundValue == 0:
                    copyPath = []
                    for node in path:
                        copyPath.append(node)
                    copyPath.append((movie, current))
                    cost[person] = (-1, copyPath)
                    path_back.add(copyPath)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


if __name__ == "__main__":
    main()
