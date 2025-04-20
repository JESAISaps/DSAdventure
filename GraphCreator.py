from Map import Map
from Room import Room
from queue import Queue

def CreateGraph(depart:Room, file):
    file.write("digraph g {\n")
    queue = Queue()
    world = set()
    queue.put(item=depart)

    while queue.qsize() != 0:
        actualRoom:Room = queue.get()
        if not actualRoom in world:
            world.add(actualRoom)            
            for nextRoom in actualRoom.GetVoisinsAsList():
                file.write(f'"{actualRoom.GetName()}" -> "{nextRoom.GetName()}";\n')
                queue.put(item=nextRoom)

    file.write("}")

if __name__ == "__main__":
    start = Map().shop
    with open("map.dot", "w") as file:
        CreateGraph(start, file)


