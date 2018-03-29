# coding: utf-8
from scene import *
from map_man import Game
from in_app import InApp
from rate import Rater

def start_game(simulate_tilt=False):
    
    Rater.initialize()
    InApp.initialize()
    
    game = Game(simulate_tilt=simulate_tilt)

    main_view = ui.View()
    scene_view = SceneView(frame=main_view.bounds, flex='WH')
    main_view.add_subview(scene_view)
    scene_view.scene = game
    main_view.present(hide_title_bar=True, animated=False)
    
if __name__ == '__main__':
    
    start_game()

