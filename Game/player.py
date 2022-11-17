import arcade
import constants

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.scale = constants.CHARACTER_SCALING
        self.textures = []

        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        texture = arcade.load_texture("duck2.png")
        self.textures.append(texture)
        texture = arcade.load_texture("duck2.png",
                                      flipped_horizontally=True)
        self.textures.append(texture)

        # By default, face right.
        self.texture = texture

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[constants.TEXTURE_RIGHT]
        elif self.change_x > 0:
            self.texture = self.textures[constants.TEXTURE_LEFT]