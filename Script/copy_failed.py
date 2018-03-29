from scene import *

class CopyFailMenu(Scene):

	def setup(self):
		Scene.setup(self)
		self.add_label(self.size.h*0.75, 'could not expand files')
		self.add_label(self.size.h*0.50, 'try freeing up space')
		self.add_label(self.size.h*0.25, 'on your device')
		
	def add_label(self, y, text):
		label = LabelNode(parent=self)
		label.anchor_point = (0.5, 0.5)
		label.position = (self.size.w/2, y)
		label.text = text
		
if __name__ == '__main__':
    
    game = CopyFailMenu()

    main_view = ui.View()
    scene_view = SceneView(frame=main_view.bounds, flex='WH')
    main_view.add_subview(scene_view)
    scene_view.scene = game
    main_view.present(hide_title_bar=True, animated=False)
