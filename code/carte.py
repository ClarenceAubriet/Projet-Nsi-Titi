import pyscroll
import pytmx

from map import Map
from screen import Screen
from player import Player

class Carte:
    def __init__(self, screen: Screen):
        self.screen: Screen = screen
        self.map: Map = Map(self.screen)
        self.tmx_data: pytmx.TiledMap | None = None
        self.map_layer: pyscroll.BufferedRenderer | None = None
        self.group: pyscroll.PyscrollGroup | None = None
        self.player: Player | None = None

        self.zoom = self.screen.get_size()[0] / 1680
        self.zoom_step = 0.1
        self.min_zoom = self.screen.get_size()[0] / 1680
        self.max_zoom = 3.0
        self.camera_x = 0
        self.camera_y = 0
        self.map_data()
    
    def map_data(self):
        self.tmx_data = self.map.tmx_data
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.map_layer.zoom = self.zoom
        self.group.center(((self.screen.get_size()[0] / 2) / self.map_layer.zoom,(self.screen.get_size()[1] / 2) / self.map_layer.zoom))


    def screen_to_world(self, curseur_position):
        center_x = self.camera_x + (self.screen.get_size()[0] / 2) / self.map_layer.zoom
        center_y = self.camera_y + (self.screen.get_size()[1] / 2) / self.map_layer.zoom

        dx = curseur_position[0] - self.screen.get_size()[0] // 2
        dy = curseur_position[1] - self.screen.get_size()[1] // 2

        world_x = center_x + dx / self.map_layer.zoom
        world_y = center_y + dy / self.map_layer.zoom

        return (world_x, world_y)

    def update(self) -> None:
        self.group.update()
        self.group.draw(self.screen.get_display())