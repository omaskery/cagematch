"""this file describes an entity and a container that manages a group of entities"""


class Entity(object):
    """describes a basic entity"""

    def __init__(self):
        """constructor for an entity"""
        self._alive = True
        # callback can be set to alert someone to an entity dying
        self._death_callback = lambda this: None

    def set_death_callback(self, callback):
        """sets the death callback so you can be alerted of this entity's death"""
        self._death_callback = callback

    def is_alive(self):
        """returns whether this entity is still alive"""
        return self._alive

    def render(self, bounds, dest):
        """causes this entity to render to the screen if applicable"""
        pass

    def think(self, dt):
        """causes this entity to update it's simulation/model state"""
        pass

    def die(self):
        """sets this entity's alive flag to false"""
        if self._alive:
            self._death_callback(self)
            self._alive = False


class EntityContainer(Entity):
    """a container for entities, which can also be treated as an entity (composite pattern)"""

    def __init__(self, die_on_empty=True):
        """constructor"""
        super().__init__()
        self._entities = []
        self._die_on_empty=die_on_empty

    def is_alive(self):
        """containers live forever unless die_on_empty is set, in which case when all entities are dead they die"""
        result = self._alive
        if self._die_on_empty and self._alive:
            result = any([entity.is_alive() for entity in self._entities])
            if not result:
                self.die()
        return result

    def render(self, bounds, dest):
        """renders all entities within the container"""
        list(map(lambda entity: entity.render(bounds, dest), self._entities))

    def think(self, dt):
        """updates the simulation/model state of all entities inside the container"""
        self._entities = list(filter(lambda entity: EntityContainer._update_entity(entity, dt), self._entities))

    def add(self, entity):
        """adds an entity to the collection"""
        self._entities.append(entity)

    def remove(self, entity):
        """removes an entity from the collection"""
        self._entities.remove(entity)

    def check_collisions(self, other_container, callback):
        """checks every entity for collision with every entity in a given container,
        calling the given callback with the each entity as the arguments - note that
        this function assumes both containers only have entities with a valid _rect
        property"""
        my_ents = self._entities
        other_ents = other_container._entities
        for me in my_ents:
            for oe in other_ents:
                if me._rect.colliderect(oe._rect):
                    callback(me, oe)
                    break

    def check_collision_single(self, other_entity, callback):
        """checks every entity for collision with the given entity, calling the given
        callback with the each entity as the arguments - note that this function assumes
        both the entities in the container and the other entity have a valid _rect
        property"""
        my_ents = self._entities
        for me in my_ents:
            if me._rect.colliderect(other_entity._rect):
                callback(me, other_entity)
                break

    @staticmethod
    def _update_entity(entity, dt):
        """updates a single entity (if it is alive) and returns whether it is still alive afterwards"""
        if entity.is_alive():
            entity.think(dt)
        return entity.is_alive()
