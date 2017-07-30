# coding: utf-8
from scene import *
from map_man import Game
from in_app import InApp

if __name__ == '__main__':
    
    InApp.initialize()
    game = Game()

    main_view = ui.View()
    scene_view = SceneView(frame=main_view.bounds, flex='WH')
    main_view.add_subview(scene_view)
    scene_view.scene = game
    main_view.present(hide_title_bar=True, animated=False)

