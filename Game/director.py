import constants
import arcade
import player

class Director(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None
        self.player_sprite_list = None

        # Our physics engine
        self.physics_engine = None

        # A Camera that can be used for scrolling the screen
        self.camera = None

        # Load sounds
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        arcade.set_background_color(arcade.csscolor.BLACK)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = "map1..tmj"

        # Layer specific options are defined based on Layer names in a dictionary

        layer_options = {
            constants.LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },

            constants.LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, constants.TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.player_sprite_list = arcade.SpriteList()

        self.scene.add_sprite_list_after("Player", constants.LAYER_NAME_FOREGROUND)



        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = player.Player()
        self.player_sprite.center_x = constants.PLAYER_START_X
        self.player_sprite.center_y = constants.PLAYER_START_Y
        self.player_sprite_list.append(self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite)


        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=constants.GRAVITY,
            walls=self.scene[constants.LAYER_NAME_BOUNDARY],
            platforms=self.scene[constants.LAYER_NAME_PLATFORMS],
        )

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        arcade.start_render()

        # Activate the game camera
        self.camera.use()

        # Draw our Scene
        self.scene.draw()
        self.player_sprite_list.draw()

        
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = constants.PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -constants.PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = constants.PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x =  -(self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()
        self.player_sprite_list.update()


        if arcade.check_for_collision_with_list(
                self.player_sprite, self.scene[constants.LAYER_NAME_DONT_TOUCH]
            ):
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.center_x = constants.PLAYER_START_X
                self.player_sprite.center_y = constants.PLAYER_START_Y

                arcade.play_sound(self.game_over)
                self.setup()

        # Position the camera
        self.center_camera_to_player()