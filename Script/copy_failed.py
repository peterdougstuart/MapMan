from scene import *
from map_man import Game

if __name__ == '__main__':
    
    game = Game(copy_failed=True)

    main_view = ui.View()
    scene_view = SceneView(frame=main_view.bounds, flex='WH')
    main_view.add_subview(scene_view)
    scene_view.scene = game
    main_view.present(hide_title_bar=True, animated=False)
