"""this file describes an entity and a container that manages a group of entities"""


class Entity(object):
    """describes a basic entity"""

    def __init__(self):
        """constructor for an entity"""
        self._alive = True

    def is_alive(self):
        """returns whether this entity is still alive"""
        return self._alive

    def render(self, bounds, dest):
        """causes this entity to render to the screen if applicable"""
        pass

    def think(self, dt):
        """causes this entity to update it's simulation/model state"""
        pass

    def _die(self):
        """sets this entity's alive flag to false"""
        self._alive = False


class EntityContainer(Entity):
    """a container for entities, which can also be treated as an entity (composite pattern)"""

    def __init__(self):
        """constructor"""
        super().__init__()
        self._entities = []

    def is_alive(self):
        """an entity container is alive as long as it contains a living entity inside it"""
        return any([entity.is_alive() for entity in self._entities])

    def render(self, *args):
        """renders all entities within the container"""
        list(map(lambda entity: entity.render(*args), self._entities))

    def think(self, *args):
        """updates the simulation/model state of all entities inside the container"""
        self._entities = list(filter(lambda entity: EntityContainer._update_entity(entity, args), self._entities))

    def add(self, entity):
        """adds an entity to the collection"""
        self._entities.append(entity)

    def remove(self, entity):
        """removes an entity from the collection"""
        self._entities.remove(entity)

    @staticmethod
    def _update_entity(entity, *args):
        """updates a single entity (if it is alive) and returns whether it is still alive afterwards"""
        if entity.is_alive():
            entity.think(*args)
        return entity.is_alive()
