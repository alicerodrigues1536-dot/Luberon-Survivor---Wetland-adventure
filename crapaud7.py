import arcade
import math
import time
import ctypes


# ---------------- CONSTANTES ----------------

# Récupérer la taille de l’écran (Windows)
user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)

SCREEN_TITLE = "Luberon survivor - Wetland adventures"
TILE_SIZE = 64


# Values - parchemins
class Value(arcade.Sprite):
    def __init__(self, rolled_image, opened_image, text, scale=1):
        super().__init__(rolled_image, scale=scale)
        self.opened_texture = arcade.load_texture(opened_image)
        self.info_text = text
        self.active = True
        self.float_angle = 0
        self.collected_time = None  # moment où on a ramassé la value
        self.base_y = None  # position de base pour le flottement

    def update_float(self):
        if self.base_y is None:
            self.base_y = self.center_y
        self.float_angle += 0.05
        self.center_y = self.base_y + math.sin(self.float_angle) * 6


# Flottement des proies
class Prey(arcade.Sprite):
    def __init__(self, image_path, scale=0.5):
        super().__init__(image_path, scale=scale)
        self.base_y = None
        self.float_angle = 0

    def update_float(self):
        if self.base_y is None:
            self.base_y = self.center_y
        self.float_angle += 0.05
        self.center_y = self.base_y + math.sin(self.float_angle) * 6


# Home page

class HomeView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        if not self.window.main_theme_player:
            self.window.main_theme_player = arcade.play_sound(
                self.window.main_theme,
                volume=0.6,
                looping=True
            )


    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Luberon survivor - Wetland adventures",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            arcade.color.WHITE,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            "Appuie sur ENTRÉE pour commencer",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 40,
            arcade.color.LIGHT_GRAY,
            28,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            self.window.show_view(HeroView())

# Personnage principal
class HeroView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)
        self.texture = arcade.load_texture("Images/crapaud1.png")

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Joueur",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 60,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "Pélobate cultripède",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 120,
            arcade.color.LIGHT_GRAY,
            20,
            anchor_x="center"
        )

        arcade.draw_texture_rectangle(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            self.texture.width * 5,
            self.texture.height * 5,
            self.texture
        )

        arcade.draw_text(
            "Appuie sur ESPACE",
            SCREEN_WIDTH / 2,
            40,
            arcade.color.LIGHT_GRAY,
            16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(PreysView())


# Proies
class PreysView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_OLIVE_GREEN)

        # Liste des proies comme sprites
        self.prey_sprites = arcade.SpriteList()

        positions = [(650, 700), (650, 500), (650, 300)]
        images = ["Images/Lombric.png", "Images/Larve_coleo.png", "Images/Scarabe.png"]
        names = ["Lombric", "Larve de coléoptère", "Scarabée"]

        self.preys = []

        for i, img in enumerate(images):
            prey = Prey(img, scale=5)
            prey.center_x, prey.center_y = positions[i]
            self.prey_sprites.append(prey)
            self.preys.append((names[i], prey))

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Proies",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 90,
            arcade.color.WHITE,
            52,
            anchor_x="center"
        )

        for i, (name, sprite) in enumerate(self.preys):
            # Nom fixe
            y_text = 700 - i * 200  # coordonnées fixes pour le texte
            arcade.draw_text(
                f"{name} :",
                180,
                y_text,
                arcade.color.WHITE,
                28,
                anchor_x="left",
                anchor_y="center"
            )

            # Sprite flottant
            sprite.draw()

    def on_update(self, delta_time):
        for _, prey in self.preys:
            prey.update_float()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(EnemiesView())


# Ennemis
class EnemiesView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_RED)

        self.enemies = [
            ("Héron cendré", "Images/Heron_cendre_Standing.png", 1),
            ("Corbeau", "Images/raven.png", 0.10),  # plus petit pour correspondre à l’échelle relative
            ("Chat domestique", "Images/catwalk1.png",3),
            ("Chouette effraie des clochers", "Images/chouette1.png",2),
            ("Écrevisse de Louisiane", "Images/Ecrevisse_Walk1.png", 2)
        ]


    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Les ennemis",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 70,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        start_y = SCREEN_HEIGHT - 150

        for i, (name, path, scale) in enumerate(self.enemies):
            y = start_y - i * 120
            tex = arcade.load_texture(path)

            arcade.draw_text(
                name,
                200,
                y,
                arcade.color.WHITE,
                18,
                anchor_x="left",
                anchor_y="center"
            )

            # Décalage spécifique pour la chouette
            if "Chouette" in name:
                x_offset = 150
            else:
                x_offset = 0

            arcade.draw_texture_rectangle(
                500 + x_offset,  # ← applique le décalage ici
                y,
                tex.width * scale,
                tex.height * scale,
                tex
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(ValuesView())


# Parchemins
class ValuesView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BEIGE)

        # liste des valeurs
        self.values = [
            Value("Images/03_scroll.png", "Images/01_papers.png", "Enroulé", scale=1),
            Value("Images/01_papers.png", "Images/01_papers.png", "Déroulé", scale=1),
        ]

        # position initiale côte à côte
        start_x = SCREEN_WIDTH / 2 - 150  # gauche pour le premier
        spacing_x = 300                   # distance entre les deux
        y_pos = SCREEN_HEIGHT / 2         # même hauteur pour les deux

        for i, value in enumerate(self.values):
            value.center_x = start_x + i * spacing_x
            value.center_y = y_pos
            value.base_y = value.center_y  # pour le texte

    def on_draw(self):
        arcade.start_render()

        # TITRE
        arcade.draw_text(
            "Parchemins",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 70,
            arcade.color.BLACK,
            32,
            anchor_x="center"
        )

        # Dessin des parchemins et texte dessous
        for value in self.values:
            value.draw()
            arcade.draw_text(
                value.info_text,
                value.center_x,
                value.center_y - value.height / 2 - 20,  # juste en dessous de l'image
                arcade.color.BLACK,
                14,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        for value in self.values:
            value.update_float()  # fait flotter uniquement les images

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(MapView())

# ---------------- MAP ----------------
class MapView(arcade.View):
    def __init__(self):
        super().__init__()

        # Grande carte (à gauche)
        self.main_map_texture = arcade.load_texture("Images/d.png")

        # Petites cartes (à droite)
        self.side_maps = [
            arcade.load_texture("Images/map1.png"),
            arcade.load_texture("Images/map2.png"),
            arcade.load_texture("Images/map3.png"),
            arcade.load_texture("Images/map4.png"),
        ]

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        # =====================
        # TITRE
        # =====================
        arcade.draw_text(
            "MAP",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 70,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        # =====================
        # GRANDE CARTE (GAUCHE)
        # =====================
        main_width = 600
        main_height = 400

        arcade.draw_texture_rectangle(
            SCREEN_WIDTH * 0.32,
            SCREEN_HEIGHT / 2,
            main_width,
            main_height,
            self.main_map_texture
        )

        # =====================
        # CARTES À DROITE
        # =====================
        mini_width = 220  # plus grandes
        mini_height = 130

        start_x = SCREEN_WIDTH * 0.8
        start_y = SCREEN_HEIGHT * 0.72
        spacing = 150

        for i, texture in enumerate(self.side_maps):
            # Texte "Niveau X"
            arcade.draw_text(
                f"Niveau {i + 1} :",
                start_x - mini_width / 2 - 20,
                start_y - i * spacing,
                arcade.color.WHITE,
                16,
                anchor_x="right",
                anchor_y="center"
            )

            # Mini carte
            arcade.draw_texture_rectangle(
                start_x,
                start_y - i * spacing,
                mini_width,
                mini_height,
                texture
            )

        # =====================
        # TEXTE BAS
        # =====================
        arcade.draw_text(
            "Appuie sur ESPACE pour entrer dans le monde",
            SCREEN_WIDTH / 2,
            40,
            arcade.color.WHITE,
            16,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.window.show_view(Level1())




# ---------------- CLASSE DE BASE POUR LES NIVEAUX ----------------
class BaseLevel(arcade.View):
    def __init__(self):
        super().__init__()

        # Vie
        # ---------------- VIE PERSISTANTE ----------------
        if not hasattr(self.window, "current_health"):
            self.window.max_health = 10
            self.window.current_health = 10

        self.max_health = self.window.max_health
        self.current_health = self.window.current_health

        self.heart_texture = arcade.load_texture("Images/heart.png")

        # Caméra
        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera.move_to((0, 0))

        # Game over
        self.game_over = False

        # Sprites
        self.player = None
        self.ground_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()  # défini ici pour tous les niveaux

        # Fond
        self.background = None
        self.background_scale = 1
        self.backgrounds = []

        # Enemis
        self.crayfish_list = arcade.SpriteList()  # ecrevisse
        self.heron_list = arcade.SpriteList()  # heron

        # Proies
        self.prey_list = arcade.SpriteList()

        # Values (parchemins)
        self.value_list = arcade.SpriteList()
        self.active_value = None

        # Sons
        self.sound_prey = arcade.load_sound("Sons/prey.mp3")
        self.sound_value = arcade.load_sound("Sons/value.mp3")
        self.sound_game_over = arcade.load_sound("Sons/GO.mp3")
        self.game_over_played = False  # pour éviter que le son se répète
        self.sound_walk_grass = arcade.load_sound("Sons/walk_grass.mp3")

        # Filtre atmosphérique (paramétrable par niveau)
        self.filter_color = None  # (R, G, B)
        self.filter_alpha = 0

    def on_hide_view(self):
        if self.walk_sound_player:
            arcade.stop_sound(self.walk_sound_player)
            self.walk_sound_player = None


    # Filtre coloré
    def draw_color_filter(self):
        if not self.filter_color or self.filter_alpha <= 0:
            return

        arcade.draw_rectangle_filled(
            self.camera.position[0] + SCREEN_WIDTH / 2,
            self.camera.position[1] + SCREEN_HEIGHT / 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (*self.filter_color, self.filter_alpha)
        )

    # ---------------- FOND ----------------
    def draw_background(self):
        if not self.backgrounds:
            return
        for i, tex in enumerate(self.backgrounds):
            draw_width = tex.width * self.background_scale
            draw_height = tex.height * self.background_scale
            arcade.draw_lrwh_rectangle_textured(
                i * draw_width,
                0,
                draw_width,
                draw_height,
                tex
            )

    # ---------------- VIE ----------------
    def draw_health_bar(self):
        heart_x = self.camera.position[0] + 20
        heart_y = self.camera.position[1] + SCREEN_HEIGHT - 40
        arcade.draw_lrwh_rectangle_textured(heart_x, heart_y, 32, 32, self.heart_texture)

        jauge_width = 150
        jauge_height = 20
        jauge_x = heart_x + 40
        jauge_y = heart_y + 6

        arcade.draw_rectangle_filled(
            jauge_x + jauge_width / 2,
            jauge_y + jauge_height / 2,
            jauge_width, jauge_height,
            arcade.color.DARK_GRAY
        )
        arcade.draw_rectangle_filled(
            jauge_x + (jauge_width * self.current_health / self.max_health) / 2,
            jauge_y + jauge_height / 2,
            jauge_width * self.current_health / self.max_health,
            jauge_height,
            arcade.color.RED
        )

    # ---------------- ITEMS / SOINS ----------------
    def handle_item_collision(self, heal_amount=2):
        items_hit = arcade.check_for_collision_with_list(self.player, self.prey_list)
        for item in items_hit:
            arcade.play_sound(self.sound_prey)

            self.current_health += heal_amount
            self.current_health = min(self.current_health, self.max_health)
            item.remove_from_sprite_lists()

    # ---------------- CAMERA ----------------
    def scroll_to_player(self):
        if not self.player:
            return

        # Limites du monde
        max_x = max(0, self.world_width - SCREEN_WIDTH)
        max_y = max(0, self.world_height - SCREEN_HEIGHT)

        target_x = self.player.center_x - 200
        target_y = self.player.center_y - SCREEN_HEIGHT / 2

        target_x = max(0, min(target_x, max_x))
        target_y = max(0, min(target_y, max_y))

        # Lissage vertical léger
        smooth_y = self.camera.position[1] + (target_y - self.camera.position[1]) * 0.05

        self.camera.move_to((target_x, smooth_y))

    # Collisions avec enemy

    def handle_enemy_collision(self, enemy_list, knockback=20):
        hits = arcade.check_for_collision_with_list(self.player, enemy_list)
        for _ in hits:
            self.current_health -= 1
            self.current_health = max(self.current_health, 0)
            self.window.current_health = self.current_health

            self.player.center_x -= knockback

            if self.current_health == 0:
                self.game_over = True
                if not self.game_over_played:
                    arcade.play_sound(self.sound_game_over)
                    self.game_over_played = True

    # Setup player

    def setup_player(self, start_x, start_y):
        self.player = arcade.AnimatedWalkingSprite(scale=3)
        self.player.animation_speed = 0.05

        # Textures DROITE
        idle_right = arcade.load_texture("Images/crapaud1.png")
        walk1_right = arcade.load_texture("Images/crapaud22.png")
        walk2_right = arcade.load_texture("Images/crapaud3.png")

        # Textures GAUCHE (mirrored)
        idle_left = arcade.load_texture("Images/crapaud1.png", mirrored=True)
        walk1_left = arcade.load_texture("Images/crapaud22.png", mirrored=True)
        walk2_left = arcade.load_texture("Images/crapaud3.png", mirrored=True)

        # Saut/Chute
        self.jump_texture = arcade.load_texture("Images/Jumping_Toad.png")
        self.fall_texture = arcade.load_texture("Images/Falling_Toad.png")
        self.jump_texture_left = arcade.load_texture("Images/Jumping_Toad.png", mirrored=True)
        self.fall_texture_left = arcade.load_texture("Images/Falling_Toad.png", mirrored=True)

        # Assignation
        self.player.stand_right_textures = [idle_right]
        self.player.stand_left_textures = [idle_left]
        self.player.walk_right_textures = [walk1_right, walk2_right]
        self.player.walk_left_textures = [walk1_left, walk2_left]

        self.player.texture = idle_right
        self.player.set_hit_box(self.player.texture.hit_box_points)
        self.player.center_x = start_x
        self.player.center_y = start_y
        self.player.facing_right = True

    # Setup physics

    def setup_physics(self):
        ground = arcade.SpriteSolidColor(10000, 20, (0, 0, 0, 0))
        self.ground_list.append(ground)

        self.physics = arcade.PhysicsEnginePlatformer(
            self.player,
            self.ground_list,
            gravity_constant=0.8
        )

    # Animation player

    def update_player_animation(self, delta_time):
        # Saut
        if self.player.change_y > 0:
            self.player.texture = (
                self.jump_texture if self.player.facing_right else self.jump_texture_left
            )
            return

        # Chute
        elif self.player.change_y < 0:
            self.player.texture = (
                self.fall_texture if self.player.facing_right else self.fall_texture_left
            )
            return

        # AU SOL : laisser Arcade gérer idle/marche automatiquement
        if self.physics.can_jump():
            self.player.update_animation(delta_time)

    # Key clavier

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.player.change_x = 8
            self.player.facing_right = True
        elif key == arcade.key.LEFT:
            self.player.change_x = -8
            self.player.facing_right = False
        elif key == arcade.key.UP:
            self.physics.jump(15)

        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.RIGHT, arcade.key.LEFT):
            self.player.change_x = 0

    # VALUES

    def update_values_floating(self):
        for value in self.value_list:
            if value.active:
                if value.base_y is None:
                    value.base_y = value.center_y

                value.float_angle += 0.05
                value.center_y = value.base_y + math.sin(value.float_angle) * 6

    def handle_value_collision(self, delta_time):
        if not self.active_value:
            hits = arcade.check_for_collision_with_list(self.player, self.value_list)
            for value in hits:
                if value.active:
                    arcade.play_sound(self.sound_value)

                    value.active = False
                    self.active_value = value
                    value.collected_time = 0

        if self.active_value:
            self.active_value.collected_time += delta_time
            if self.active_value.collected_time > 3:
                self.active_value = None

    def draw_values(self):
        for value in self.value_list:
            if value.active:
                value.draw()

    def draw_values_ui(self):
        icon_x = self.camera.position[0] + 70
        icon_y = self.camera.position[1] + SCREEN_HEIGHT - 70

        for value in self.value_list:
            if not value.active:
                arcade.draw_texture_rectangle(
                    icon_x, icon_y,
                    80, 60,
                    value.opened_texture
                )
                arcade.draw_text(
                    value.info_text,
                    icon_x,
                    icon_y - 5,
                    arcade.color.BLACK,
                    font_size=5,
                    anchor_x="center",
                    anchor_y="center",
                    width=50,
                    multiline=True
                )
                icon_x += 90

        if self.active_value:
            x = self.camera.position[0] + SCREEN_WIDTH // 2
            y = self.camera.position[1] + SCREEN_HEIGHT // 2

            arcade.draw_texture_rectangle(
                x, y,
                350, 250,
                self.active_value.opened_texture
            )

            arcade.draw_text(
                self.active_value.info_text,
                x, y - 10,
                arcade.color.BLACK,
                font_size=20,
                anchor_x="center",
                anchor_y="center",
                width=150,
                multiline=True
            )


# ---------------- NIVEAU 1 ----------------

class Level1(BaseLevel):
    PLATFORM_IMAGES = {
        "A": "Images/squelette/A.png",
        "B": "Images/squelette/B.png",
        "H": "Images/squelette/H.png",
        "I": "Images/squelette/I.png",
        "L": "Images/squelette/L.png",
        "i": "Images/squelette/w.png",
        "O": "Images/squelette/O.png",
        "P": "Images/squelette/P.png",
        "p": "Images/squelette/m.png",
        "Z": "Images/squelette/Z.png",
        "S": "Images/squelette/S.png",
        "R": "Images/squelette/R.png",
        "E": "Images/squelette/E.png",
        "T": "Images/decor/terre.png",
        "G": "Images/decor/terre_gauche.png",
        "D": "Images/decor/terre_droit.png",
        "H": "Images/decor/terre_haut.png",
        "J": "Images/squelette/T.png"
    }
    DECOR_IMAGES = {
        "C": "Images/decor/Curved_tree3.png",
        "I": "Images/decor/Living gazebo1.png",
        "L": "Images/decor/Luminous_tree1.png",
        "G": "Images/decor/terre_gauche.png",
        "D": "Images/decor/terre_droit.png",
        "H": "Images/decor/terre_haut.png",
        "T": "Images/decor/terre.png",
        "W": "Images/decor/White_tree1.png"
    }

    BACK_DECOR_IMAGES = {
        "C": "Images/decor/Curved_tree3.png",
        "I": "Images/decor/Living gazebo1.png",
        "L": "Images/decor/Luminous_tree1.png",
        "G": "Images/decor/terre_gauche.png",
        "D": "Images/decor/terre_droit.png",
        "H": "Images/decor/terre_haut.png",
        "T": "Images/decor/terre.png",
        "M": "Images/decor/moon.png",
        "S": "Images/decor/stars.png",
        "N": "Images/decor/smoke1.png",
        "U": "Images/decor/smoke2.png",
        "W": "Images/decor/White_tree1.png"
    }

    def load_level_from_file(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

        rows = len(lines)
        cols = max(len(line.strip()) for line in lines)

        self.world_width = cols * TILE_SIZE
        self.world_height = rows * TILE_SIZE

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.PLATFORM_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    platform = arcade.Sprite(
                        self.PLATFORM_IMAGES[char],
                        scale=1.2
                    )
                    platform.center_x = x + TILE_SIZE // 2
                    platform.center_y = y + TILE_SIZE // 2
                    self.ground_list.append(platform)
                    print("WORLD SIZE:", self.world_width, self.world_height)

    def load_decor_from_file(self, filename, sprite_list=None):
        if sprite_list is None:
            sprite_list = self.decor_list  # par défaut
        TILE_SIZE = 64
        with open(filename, "r") as file:
            lines = file.readlines()

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.DECOR_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    decor = arcade.Sprite(
                        self.DECOR_IMAGES[char],
                        scale=2
                    )
                    decor.center_x = x + TILE_SIZE // 2
                    decor.center_y = y + TILE_SIZE // 2

                    sprite_list.append(decor)

    def load_back_decor_from_file(self, filename):
        TILE_SIZE = 64
        with open(filename, "r") as file:
            lines = file.readlines()

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.BACK_DECOR_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    # Choix du scale selon le type de décor
                    if char == "M":  # Lune
                        scale = 4
                    elif char in ("N", "U"):  # petites décorations
                        scale = 0.8
                    else:  # décor normal
                        scale = 2

                    decor = arcade.Sprite(
                        self.BACK_DECOR_IMAGES[char],
                        scale=scale
                    )
                    decor.center_x = x + TILE_SIZE // 2
                    decor.center_y = y + TILE_SIZE // 2

                    self.back_decor_list.append(decor)

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)


        # Musique
        # Arrêter la musique main theme
        if self.window.main_theme_player:
            arcade.stop_sound(self.window.main_theme_player)
            self.window.main_theme_player = None
        self.niv1_sound = arcade.load_sound("Sons/Niv3.mp3")
        self.niv1_player = arcade.play_sound(self.niv1_sound, looping=True)
        # Sons
        self.sound_door = arcade.load_sound("Sons/door.mp3")

        # Fond
        #n = 3
        #self.background = arcade.load_texture("Images/origbig.png")
        #self.background_scale = 0.5
        #self.backgrounds = [self.background] * n

        # Player
        self.setup_player(190, 150)
        self.setup_physics()

        # Plateformes
        self.load_level_from_file("levels/level1.txt")

        # Décor
        self.decor_list = arcade.SpriteList()
        self.load_decor_from_file("levels/level1_decor.txt")

        # Filtre semi-transparent devant (pour effet de profondeur)
        self.front_filter = arcade.create_rectangle_filled(
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            (0, 0, 0, 50)  # noir transparent (0=opaque, 255=complet)
        )

        # Décor de fond (arrière-plan supplémentaire)
        self.back_decor_list = arcade.SpriteList()
        self.load_back_decor_from_file("levels/level1_back_decor.txt")


        # Ennemis
        #for i in range(3):
        #    enemy = arcade.Sprite("Images/raven.png", scale=0.2)
        #    enemy.center_x = 500 + i * 800
        #    enemy.center_y = 200
        #    enemy.speed = 2
        #    self.enemy_list.append(enemy)

        # Heron
        self.heron = arcade.Sprite(scale=2)
        self.heron_texture_stand = arcade.load_texture("Images/Heron_cendre_Standing.png")
        self.heron_texture_crouch = arcade.load_texture("Images/Heron_cendre_Flexing.png")
        self.heron.texture = self.heron_texture_stand
        self.heron.set_hit_box(self.heron.texture.hit_box_points)
        self.heron.center_x = 800
        self.heron.center_y = 305
        self.heron_list.append(self.heron)
        self.heron_crouch_timer = 0

        # Proies
        self.prey_list = arcade.SpriteList()

        prey1 = Prey("Images/Lombric.png", scale=2)
        prey1.center_x = 270
        prey1.center_y = 200
        self.prey_list.append(prey1)

        prey2 = Prey("Images/Scarabe.png", scale=2)
        prey2.center_x = 1100
        prey2.center_y = 200
        self.prey_list.append(prey2)

        prey3 = Prey("Images/Larve_Coleo.png", scale=2)
        prey3.center_x = 1720
        prey3.center_y = 300
        self.prey_list.append(prey3)

        # Door
        door = arcade.Sprite("Images/door1.png", scale=1)
        door.center_x = 2400
        door.center_y = 320
        self.door_list.append(door)

        # Values
        value1 = Value(
            "Images/03_scroll.png",
            "Images/01_papers.png",
            "Les hérons sont des prédateurs immobiles !",
            scale=0.4
        )
        value1.center_x = 500
        value1.center_y = 400
        self.value_list.append(value1)


    def on_hide_view(self):
        # Arrêter la pluie quand on quitte le niveau
        if hasattr(self, 'niv1_player') and self.niv1_player:
            arcade.stop_sound(self.niv1_player)

    def on_draw(self):
        self.clear()

        # =====================
        # MONDE (avec caméra)
        # =====================
        self.camera.use()

        self.draw_background()

        self.back_decor_list.draw()  # arrière-plan
        self.decor_list.draw()  # décor normal
        self.ground_list.draw()  # plateformes
        self.enemy_list.draw()
        self.item_list.draw()
        self.prey_list.draw()
        self.heron_list.draw()
        self.door_list.draw()
        self.player.draw()

        self.draw_health_bar()
        self.draw_values()
        self.draw_values_ui()

        # --- Icônes / parchemins collectés ---
        icon_x = 70
        icon_y = SCREEN_HEIGHT - 70

        for value in self.value_list:
            if not value.active:
                arcade.draw_texture_rectangle(
                    icon_x,
                    icon_y,
                    80, 60,
                    value.opened_texture
                )
                arcade.draw_text(
                    value.info_text,
                    icon_x,
                    icon_y - 5,
                    arcade.color.BLACK,
                    font_size=5,
                    anchor_x="center",
                    anchor_y="center",
                    width=50,
                    multiline=True
                )
                icon_x += 90

        # =====================
        # GAME OVER
        # =====================
        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.BLACK,
                50,
                anchor_x="center",
                anchor_y="center"
            )

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.physics.update()

        # --- Corbeaux ---
        for enemy in self.enemy_list:
            enemy.center_x += enemy.speed
            if enemy.center_x > 1400 or enemy.center_x < 400:
                enemy.speed *= -1

        self.handle_enemy_collision(self.enemy_list, knockback=20)

        # --- Écrevisses ---
        for crayfish in self.crayfish_list:
            crayfish.center_x += crayfish.change_x
            if crayfish.center_x > crayfish.right_limit or crayfish.center_x < crayfish.left_limit:
                crayfish.change_x *= -1
            crayfish.update_animation(delta_time)

        self.handle_enemy_collision(self.crayfish_list, knockback=30)

        # --- HÉRON ---
        heron_hit = arcade.check_for_collision_with_list(self.player, self.heron_list)

        for heron in self.heron_list:
            if heron in heron_hit:
                heron.texture = self.heron_texture_crouch
                self.heron_crouch_timer = 15  # reste baissé 15 frames (~0.25s)
            elif self.heron_crouch_timer > 0:
                self.heron_crouch_timer -= 1
            else:
                heron.texture = self.heron_texture_stand

        self.handle_enemy_collision(self.heron_list)

        # --- Items --- Proies
        self.handle_item_collision(heal_amount=2)

        for prey in self.prey_list:
            prey.update_float()

        # --- Gestion textures saut / chute ---
        self.update_player_animation(delta_time)


        # --- VALUES ---
        self.update_values_floating()
        self.handle_value_collision(delta_time)

        # Son herbe
        if self.player.change_x != 0:
            if not self.window.walk_sound_player:
                self.window.walk_sound_player = arcade.play_sound(
                    self.sound_walk_grass,
                    volume=0.6,
                    looping=True
                )
        else:
            if self.window.walk_sound_player:
                arcade.stop_sound(self.window.walk_sound_player)
                self.window.walk_sound_player = None

        # --- Transition vers le niveau 2 ---
        if arcade.check_for_collision_with_list(self.player, self.door_list):
            # jouer le son de la porte
            arcade.play_sound(self.sound_door, volume=1)

            # passer au niveau suivant
            self.window.show_view(Level2())
            return

        self.scroll_to_player()

    # Key

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)

        if key == arcade.key.SPACE and self.active_value:
            self.active_value = None


# ---------------- NIVEAU 2 ----------------
class Level2(BaseLevel):
    PLATFORM_IMAGES = {
        "A": "Images/squelette/A.png",
        "B": "Images/squelette/B.png",
        "H": "Images/squelette/H.png",
        "I": "Images/squelette/I.png",
        "L": "Images/squelette/L.png",
        "i": "Images/squelette/w.png",
        "O": "Images/squelette/O.png",
        "P": "Images/squelette/P.png",
        "p": "Images/squelette/m.png",
        "Z": "Images/squelette/Z.png",
        "S": "Images/squelette/S.png",
        "R": "Images/squelette/R.png",
        "E": "Images/squelette/E.png",
        "T": "Images/squelette/T.png"
    }
    DECOR_IMAGES = {
        "C": "Images/decor/Curved_tree3.png",
        "G": "Images/decor/Living gazebo1.png",
        "L": "Images/decor/Luminous_tree1.png",
        "W": "Images/decor/White_tree1.png"
    }

    BACK_DECOR_IMAGES = {
        "C": "Images/decor/Curved_tree3.png",
        "I": "Images/decor/Living gazebo1.png",
        "L": "Images/decor/Luminous_tree1.png",
        "G": "Images/decor/terre_gauche.png",
        "D": "Images/decor/terre_droit.png",
        "H": "Images/decor/terre_haut.png",
        "T": "Images/decor/terre.png",
        "M": "Images/decor/moon.png",
        "S": "Images/decor/stars.png",
        "N": "Images/decor/smoke1.png",
        "U": "Images/decor/smoke2.png",
        "W": "Images/decor/White_tree1.png"
    }


    def load_level_from_file(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

        rows = len(lines)
        cols = max(len(line.strip()) for line in lines)

        self.world_width = cols * TILE_SIZE
        self.world_height = rows * TILE_SIZE

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.PLATFORM_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    platform = arcade.Sprite(
                        self.PLATFORM_IMAGES[char],
                        scale=1.2
                    )
                    platform.center_x = x + TILE_SIZE // 2
                    platform.center_y = y + TILE_SIZE // 2
                    self.ground_list.append(platform)

    def load_decor_from_file(self, filename):
        TILE_SIZE = 64
        with open(filename, "r") as file:
            lines = file.readlines()

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.DECOR_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    decor = arcade.Sprite(
                        self.DECOR_IMAGES[char],
                        scale=2
                    )
                    decor.center_x = x + TILE_SIZE // 2
                    decor.center_y = y + TILE_SIZE // 2

                    self.decor_list.append(decor)

    def load_back_decor_from_file(self, filename):
        TILE_SIZE = 64
        with open(filename, "r") as file:
            lines = file.readlines()

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.BACK_DECOR_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    # Choix du scale selon le type de décor
                    if char == "M":  # Lune
                        scale = 4
                    elif char in ("N", "U"):  # petites décorations
                        scale = 0.8
                    else:  # décor normal
                        scale = 2

                    decor = arcade.Sprite(
                        self.BACK_DECOR_IMAGES[char],
                        scale=scale
                    )
                    decor.center_x = x + TILE_SIZE // 2
                    decor.center_y = y + TILE_SIZE // 2

                    self.back_decor_list.append(decor)



    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

        # Fond Niveau 2
        #n = 3
        #self.background = arcade.load_texture("Images/city_night.png")
        #self.background_scale = 2.5
        #self.backgrounds = [self.background] * n

        ## PLAYER
        self.setup_player(130, 150)  # ou autre position
        self.setup_physics()

        # Plateformes
        self.load_level_from_file("levels/level2.txt")

        # Décor
        self.decor_list = arcade.SpriteList()
        self.load_decor_from_file("levels/level2_decor.txt")

        # Décor de fond (arrière-plan supplémentaire)
        self.back_decor_list = arcade.SpriteList()
        self.load_back_decor_from_file("levels/level1_back_decor.txt")

        # Musique
        self.niv2_sound = arcade.load_sound("Sons/Niv2.mp3")
        self.niv2_player = arcade.play_sound(self.niv2_sound, looping=True)
        # Sons
        self.sound_door = arcade.load_sound("Sons/door.mp3")

        # --- PARCHEMIN (Value) ---
        value1 = Value(
            "Images/03_scroll.png",
            "Images/01_papers.png",
            "Un chat est embusqué là haut!",
            scale=0.4
        )

        value1.center_x = 200
        value1.center_y = 320

        self.value_list.append(value1)

        # Ennemis
        # --- CORBEAUX ---
        self.raven_list = arcade.SpriteList()

        for i in range(2):
            raven = arcade.AnimatedTimeBasedSprite(scale=0.25)

            # textures droite
            raven.walk_right_frames = [
                arcade.AnimationKeyframe(0, 150, arcade.load_texture("Images/raven.png")),
                arcade.AnimationKeyframe(1, 150, arcade.load_texture("Images/raven2.png")),
                arcade.AnimationKeyframe(2, 150, arcade.load_texture("Images/raven3.png")),
            ]

            # textures gauche (miroir)
            raven.walk_left_frames = [
                arcade.AnimationKeyframe(0, 150, arcade.load_texture("Images/raven.png", mirrored=True)),
                arcade.AnimationKeyframe(1, 150, arcade.load_texture("Images/raven2.png", mirrored=True)),
                arcade.AnimationKeyframe(2, 150, arcade.load_texture("Images/raven3.png", mirrored=True)),
            ]

            # animation initiale
            raven.frames = raven.walk_right_frames

            # position
            raven.center_x = 600 + i * 400
            raven.center_y = 800

            # déplacement horizontal
            raven.change_x = 2
            raven.left_limit = 500 + i * 400
            raven.right_limit = 700 + i * 400

            self.raven_list.append(raven)

        # --- CHAT ENNEMI ---
        self.cat_list = arcade.SpriteList()

        cat = arcade.AnimatedTimeBasedSprite(scale=4)

        cat.walk_right_frames = [
            arcade.AnimationKeyframe(0, 120, arcade.load_texture("Images/catwalk1.png")),
            arcade.AnimationKeyframe(1, 120, arcade.load_texture("Images/catwalk2.png")),
            arcade.AnimationKeyframe(2, 120, arcade.load_texture("Images/catwalk3.png")),
            arcade.AnimationKeyframe(3, 120, arcade.load_texture("Images/catwalk4.png")),
            arcade.AnimationKeyframe(4, 120, arcade.load_texture("Images/catwalk5.png")),
            arcade.AnimationKeyframe(5, 120, arcade.load_texture("Images/catwalk6.png")),
        ]

        cat.walk_left_frames = [
            arcade.AnimationKeyframe(0, 120, arcade.load_texture("Images/catwalk1.png", mirrored=True)),
            arcade.AnimationKeyframe(1, 120, arcade.load_texture("Images/catwalk2.png", mirrored=True)),
            arcade.AnimationKeyframe(2, 120, arcade.load_texture("Images/catwalk3.png", mirrored=True)),
            arcade.AnimationKeyframe(3, 120, arcade.load_texture("Images/catwalk4.png", mirrored=True)),
            arcade.AnimationKeyframe(4, 120, arcade.load_texture("Images/catwalk5.png", mirrored=True)),
            arcade.AnimationKeyframe(5, 120, arcade.load_texture("Images/catwalk6.png", mirrored=True)),
        ]

        # animation initiale
        cat.frames = cat.walk_right_frames

        # position
        cat.center_x = 1000
        cat.center_y = 500

        # déplacement
        cat.change_x = 2
        cat.left_limit = 900
        cat.right_limit = 1100

        self.cat_list.append(cat)

        # Item
        #item = arcade.Sprite("Images/Larve_coleo.png", scale=0.5)
        #item.center_x = 700
        #item.center_y = 400
        #self.item_list.append(item)

        # Porte vers le Niveau 3
        door = arcade.Sprite("Images/door1.png", scale=1)
        door.center_x = 1850
        door.center_y = 520
        self.door_list.append(door)

    def on_hide_view(self):
        if hasattr(self, 'niv2_player') and self.niv2_player:
            arcade.stop_sound(self.niv2_player)


    def on_draw(self):
        self.clear()

        # =====================
        # MONDE (avec caméra)
        # =====================
        self.camera.use()

        self.draw_background()

        self.back_decor_list.draw()
        self.decor_list.draw()  # décor derrière
        self.ground_list.draw()  # plateformes
        self.enemy_list.draw()
        self.raven_list.draw()

        self.cat_list.draw()
        self.item_list.draw()
        self.prey_list.draw()
        self.heron_list.draw()
        self.door_list.draw()
        self.player.draw()

        self.draw_health_bar()
        self.draw_values()
        self.draw_values_ui()

        # --- Icônes / parchemins collectés ---
        icon_x = 70
        icon_y = SCREEN_HEIGHT - 70

        for value in self.value_list:
            if not value.active:
                arcade.draw_texture_rectangle(
                    icon_x,
                    icon_y,
                    80, 60,
                    value.opened_texture
                )
                arcade.draw_text(
                    value.info_text,
                    icon_x,
                    icon_y - 5,
                    arcade.color.BLACK,
                    font_size=5,
                    anchor_x="center",
                    anchor_y="center",
                    width=50,
                    multiline=True
                )
                icon_x += 90

        # =====================
        # GAME OVER
        # =====================
        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.BLACK,
                50,
                anchor_x="center",
                anchor_y="center"
            )

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.physics.update()

        # Ennemis
        for raven in self.raven_list:
            # déplacement
            raven.center_x += raven.change_x

            # inversion aux limites
            if raven.center_x > raven.right_limit:
                raven.change_x *= -1
                raven.frames = raven.walk_left_frames
            elif raven.center_x < raven.left_limit:
                raven.change_x *= -1
                raven.frames = raven.walk_right_frames

            # animation
            raven.update_animation(delta_time)

        # collisions avec le joueur
        raven_hit = arcade.check_for_collision_with_list(self.player, self.raven_list)
        for raven in raven_hit:
            self.current_health -= 1
            self.current_health = max(self.current_health, 0)
            self.player.center_x -= 30
            if self.current_health == 0:
                self.game_over = True

        # --- UPDATE CHAT ---
        for cat in self.cat_list:
            cat.center_x += cat.change_x

            if cat.center_x > cat.right_limit:
                cat.change_x *= -1
                cat.frames = cat.walk_left_frames

            elif cat.center_x < cat.left_limit:
                cat.change_x *= -1
                cat.frames = cat.walk_right_frames

            cat.update_animation(delta_time)

        cat_hit = arcade.check_for_collision_with_list(self.player, self.cat_list)
        for cat in cat_hit:
            self.current_health -= 1
            self.current_health = max(self.current_health, 0)
            self.player.center_x -= 25

            if self.current_health == 0:
                self.game_over = True

        # Items
        self.handle_item_collision()

        # --- Gestion textures saut / chute ---
        self.update_player_animation(delta_time)

        # --- VALUES ---
        self.update_values_floating()
        self.handle_value_collision(delta_time)

        # --- Son herbe ---
        if self.player.change_x != 0:
            if not self.window.walk_sound_player:
                self.window.walk_sound_player = arcade.play_sound(
                    self.sound_walk_grass,
                    volume=0.6,
                    looping=True
                )
        else:
            if self.window.walk_sound_player:
                arcade.stop_sound(self.window.walk_sound_player)
                self.window.walk_sound_player = None

        #--- Transition vers le niveau 3 ---
        if arcade.check_for_collision_with_list(self.player, self.door_list):
            # jouer le son de la porte
            arcade.play_sound(self.sound_door, volume=1)

            # passer au niveau suivant
            self.window.show_view(Level3())
            return

        self.scroll_to_player()




# ---------------- NIVEAU 3 ----------------
class Level3(BaseLevel):
    PLATFORM_IMAGES = {
        "A": "Images/squelette/A.png",
        "B": "Images/squelette/B.png",
        "H": "Images/squelette/H.png",
        "I": "Images/squelette/I.png",
        "L": "Images/squelette/L.png",
        "i": "Images/squelette/w.png",
        "O": "Images/squelette/O.png",
        "P": "Images/squelette/P.png",
        "p": "Images/squelette/m.png",
        "Z": "Images/squelette/Z.png",
        "S": "Images/squelette/S.png",
        "R": "Images/squelette/R.png",
        "E": "Images/squelette/E.png",
        "T": "Images/squelette/T.png"
    }
    DECOR_IMAGES = {
        "C": "Images/decor/Curved_tree3.png",
        "G": "Images/decor/Living gazebo1.png",
        "L": "Images/decor/Luminous_tree1.png",
        "W": "Images/decor/White_tree1.png"
    }

    BACK_DECOR_IMAGES = {
        "C": "Images/decor/Curved_tree3.png",
        "I": "Images/decor/Living gazebo1.png",
        "L": "Images/decor/Luminous_tree1.png",
        "G": "Images/decor/terre_gauche.png",
        "D": "Images/decor/terre_droit.png",
        "H": "Images/decor/terre_haut.png",
        "T": "Images/decor/terre.png",
        "M": "Images/decor/moon.png",
        "S": "Images/decor/stars.png",
        "N": "Images/decor/smoke1.png",
        "U": "Images/decor/smoke2.png",
        "W": "Images/decor/White_tree1.png"
    }

    def load_level_from_file(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

        rows = len(lines)
        cols = max(len(line.strip()) for line in lines)

        self.world_width = cols * TILE_SIZE
        self.world_height = rows * TILE_SIZE

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.PLATFORM_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    platform = arcade.Sprite(
                        self.PLATFORM_IMAGES[char],
                        scale=1.2
                    )
                    platform.center_x = x + TILE_SIZE // 2
                    platform.center_y = y + TILE_SIZE // 2
                    self.ground_list.append(platform)

    def load_decor_from_file(self, filename):
        TILE_SIZE = 64
        with open(filename, "r") as file:
            lines = file.readlines()

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.DECOR_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    decor = arcade.Sprite(
                        self.DECOR_IMAGES[char],
                        scale=2
                    )
                    decor.center_x = x + TILE_SIZE // 2
                    decor.center_y = y + TILE_SIZE // 2

                    self.decor_list.append(decor)

    def load_back_decor_from_file(self, filename):
        TILE_SIZE = 64
        with open(filename, "r") as file:
            lines = file.readlines()

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.BACK_DECOR_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    # Choix du scale selon le type de décor
                    if char == "M":  # Lune
                        scale = 4
                    elif char in ("N", "U"):  # petites décorations
                        scale = 0.8
                    else:  # décor normal
                        scale = 2

                    decor = arcade.Sprite(
                        self.BACK_DECOR_IMAGES[char],
                        scale=scale
                    )
                    decor.center_x = x + TILE_SIZE // 2
                    decor.center_y = y + TILE_SIZE // 2

                    self.back_decor_list.append(decor)

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Fond Niveau 3
        #n = 3
        #self.background = arcade.load_texture("Images/city_night.png")
        #self.background_scale = 2.5
        #self.backgrounds = [self.background] * n

        # Plateformes
        self.load_level_from_file("levels/level3.txt")

        # Musique
        self.niv3_sound = arcade.load_sound("Sons/Niv3.mp3")
        self.niv3_player = arcade.play_sound(self.niv3_sound, looping=True)
        # Sons
        self.sound_door = arcade.load_sound("Sons/door.mp3")

        # Décor
        self.decor_list = arcade.SpriteList()
        self.load_decor_from_file("levels/level3_decor.txt")

        # Décor de fond (arrière-plan supplémentaire)
        self.back_decor_list = arcade.SpriteList()
        self.load_back_decor_from_file("levels/level1_back_decor.txt")

        # Chouette
        self.owl_list = arcade.SpriteList()

        # --- CHOUETTE ---
        owl = arcade.AnimatedTimeBasedSprite(scale=3)

        # Frames GAUCHE (image originale)
        owl.fly_left_frames = [
            arcade.AnimationKeyframe(0, 200, arcade.load_texture("Images/chouette1.png")),
            arcade.AnimationKeyframe(1, 200, arcade.load_texture("Images/chouette2.png")),
        ]

        # Frames DROITE (miroir)
        owl.fly_right_frames = [
            arcade.AnimationKeyframe(0, 200, arcade.load_texture("Images/chouette1.png", mirrored=True)),
            arcade.AnimationKeyframe(1, 200, arcade.load_texture("Images/chouette2.png", mirrored=True)),
        ]

        # Animation initiale
        owl.frames = owl.fly_right_frames
        owl.texture = owl.frames[0].texture

        # Position
        owl.center_x = 500
        owl.center_y = 500

        # Mouvement
        owl.change_x = 2
        owl.left_limit = 400
        owl.right_limit = 950

        self.owl_list.append(owl)

        ## PLAYER
        self.setup_player(130, 700)  # ou autre position
        self.setup_physics()

        # --- PARCHEMIN (Value) ---
        value1 = Value(
            "Images/03_scroll.png",
            "Images/01_papers.png",
            "La chouette effraie est un prédateur redoutable..",
            scale=0.4
        )

        value1.center_x = 200
        value1.center_y = 320

        self.value_list.append(value1)

        # Proie
        prey = arcade.Sprite("Images/Larve_coleo.png", scale=2)
        prey.center_x = 1000
        prey.center_y = 600
        self.prey_list.append(prey)

        # Porte vers le Niveau 4
        door = arcade.Sprite("Images/door1.png", scale=1)
        door.center_x = 1700
        door.center_y = 650
        self.door_list.append(door)

    def on_hide_view(self):
        if hasattr(self, 'niv3_player') and self.niv3_player:
            arcade.stop_sound(self.niv3_player)


    def on_draw(self):
        self.clear()

        # =====================
        # MONDE (avec caméra)
        # =====================
        self.camera.use()

        self.draw_background()
        self.back_decor_list.draw()
        self.decor_list.draw()  # décor derrière
        self.ground_list.draw()  # plateformes
        self.enemy_list.draw()
        self.crayfish_list.draw()
        self.owl_list.draw()
        self.item_list.draw()
        self.prey_list.draw()
        self.heron_list.draw()
        self.door_list.draw()
        self.player.draw()

        self.draw_health_bar()
        self.draw_values()
        self.draw_values_ui()

        # --- Icônes / parchemins collectés ---
        icon_x = 70
        icon_y = SCREEN_HEIGHT - 70

        for value in self.value_list:
            if not value.active:
                arcade.draw_texture_rectangle(
                    icon_x,
                    icon_y,
                    80, 60,
                    value.opened_texture
                )
                arcade.draw_text(
                    value.info_text,
                    icon_x,
                    icon_y - 5,
                    arcade.color.BLACK,
                    font_size=5,
                    anchor_x="center",
                    anchor_y="center",
                    width=50,
                    multiline=True
                )
                icon_x += 90

        # =====================
        # GAME OVER
        # =====================
        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.BLACK,
                50,
                anchor_x="center",
                anchor_y="center"
            )

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.physics.update()

        # --- CHOUETTE ---
        for owl in self.owl_list:
            owl.center_x += owl.change_x

            if owl.center_x > owl.right_limit:
                owl.change_x *= -1
                owl.frames = owl.fly_left_frames

            elif owl.center_x < owl.left_limit:
                owl.change_x *= -1
                owl.frames = owl.fly_right_frames

            owl.update_animation(delta_time)

        # Collision chouette ↔ joueur
        owl_hit = arcade.check_for_collision_with_list(self.player, self.owl_list)
        for owl in owl_hit:
            self.current_health -= 1
            self.current_health = max(self.current_health, 0)
            self.player.center_x -= 30  # ou autre réaction
            if self.current_health == 0:
                self.game_over = True

        # Saut / chute
        self.update_player_animation(delta_time)

        # --- VALUES ---
        self.update_values_floating()
        self.handle_value_collision(delta_time)

        # Item/proie
        self.handle_item_collision()

        # --- Son herbe ---
        if self.player.change_x != 0:
            if not self.window.walk_sound_player:
                self.window.walk_sound_player = arcade.play_sound(
                    self.sound_walk_grass,
                    volume=0.6,
                    looping=True
                )
        else:
            if self.window.walk_sound_player:
                arcade.stop_sound(self.window.walk_sound_player)
                self.window.walk_sound_player = None

        # --- Transition vers le niveau 4 ---
        if arcade.check_for_collision_with_list(self.player, self.door_list):
            # jouer le son de la porte
            arcade.play_sound(self.sound_door, volume=1)

            # passer au niveau suivant
            self.window.show_view(Level4())
            return

        self.scroll_to_player()



# ---------------- NIVEAU 4 ----------------
class Level4(BaseLevel):
    PLATFORM_IMAGES = {
        "A": "Images/squelette/Mossy1.png",
        "B": "Images/squelette/Mossy2.png",
        "C": "Images/squelette/Mossy3.png",
        "D": "Images/squelette/Mossy4.png",
        "E": "Images/squelette/Mossy5.png",
    }
    DECOR_IMAGES = {
        "A": "Images/decor/MossyD1.png",
        "B": "Images/decor/MossyRoc1.png",
        "C": "Images/decor/MossyRoc2.png",
        "P": "Images/decor/mossyplant1.png",
        "D": "Images/decor/Mossy - Hanging Plants1.png"
    }

    BACK_DECOR_IMAGES = {
        "C": "Images/decor/Curved_tree3.png",
        "I": "Images/decor/Living gazebo1.png",
        "L": "Images/decor/Luminous_tree1.png",
        "G": "Images/decor/terre_gauche.png",
        "D": "Images/decor/terre_droit.png",
        "H": "Images/decor/terre_haut.png",
        "T": "Images/decor/terre.png",
        "M": "Images/decor/moon.png",
        "S": "Images/decor/stars.png",
        "N": "Images/decor/smoke1.png",
        "U": "Images/decor/smoke2.png",
        "W": "Images/decor/White_tree1.png"
    }

    def load_level_from_file(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

        rows = len(lines)
        cols = max(len(line.strip()) for line in lines)

        self.world_width = cols * TILE_SIZE
        self.world_height = rows * TILE_SIZE

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.PLATFORM_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    platform = arcade.Sprite(
                        self.PLATFORM_IMAGES[char],
                        scale=0.2
                    )
                    platform.center_x = x + TILE_SIZE // 2
                    platform.center_y = y + TILE_SIZE // 2
                    self.ground_list.append(platform)

    def load_decor_from_file(self, filename):
        TILE_SIZE = 64
        with open(filename, "r") as file:
            lines = file.readlines()

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.DECOR_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    decor = arcade.Sprite(
                        self.DECOR_IMAGES[char],
                        scale=0.2
                    )
                    decor.center_x = x + TILE_SIZE // 2
                    decor.center_y = y + TILE_SIZE // 2

                    self.decor_list.append(decor)

    def load_back_decor_from_file(self, filename):
        TILE_SIZE = 64
        with open(filename, "r") as file:
            lines = file.readlines()

        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line.strip()):
                if char in self.BACK_DECOR_IMAGES:
                    x = col_index * TILE_SIZE
                    y = (len(lines) - row_index - 1) * TILE_SIZE

                    # Choix du scale selon le type de décor
                    if char == "M":  # Lune
                        scale = 4
                    elif char in ("N", "U"):  # petites décorations
                        scale = 0.8
                    else:  # décor normal
                        scale = 2

                    decor = arcade.Sprite(
                        self.BACK_DECOR_IMAGES[char],
                        scale=scale
                    )
                    decor.center_x = x + TILE_SIZE // 2
                    decor.center_y = y + TILE_SIZE // 2

                    self.back_decor_list.append(decor)

    def __init__(self):
        super().__init__()

        # === FEMELLE PNJ ===
        self.female = arcade.AnimatedWalkingSprite(scale=3)

        # Textures DROITE
        fwalk1_right = arcade.load_texture("Images/Fwalk1.png")
        fwalk2_right = arcade.load_texture("Images/Fwalk2.png")
        f3_right = arcade.load_texture("Images/F3.png")

        # Textures GAUCHE (mirrored)
        fwalk1_left = arcade.load_texture("Images/Fwalk1.png", mirrored=True)
        fwalk2_left = arcade.load_texture("Images/Fwalk2.png", mirrored=True)
        f3_left = arcade.load_texture("Images/F3.png", mirrored=True)

        # Assignation (comme pour le joueur)
        self.female.stand_right_textures = [fwalk1_right]
        self.female.stand_left_textures = [fwalk1_left]
        self.female.walk_right_textures = [fwalk1_right, fwalk2_right, f3_right]
        self.female.walk_left_textures = [fwalk1_left, fwalk2_left, f3_left]

        self.female.texture = fwalk1_right
        self.female.center_x = 1800
        self.female.center_y = 500
        self.female.change_x = 0  # immobile au début
        self.female_active = False
        self.female_speed = 2

        self.female_list = arcade.SpriteList()
        self.female_list.append(self.female)

        self.game_won = False

        # Sons
        # Son victoire
        self.win_sound = arcade.load_sound("Sons/win.mp3")
        # Musique
        self.niv4_sound = arcade.load_sound("Sons/Main_theme.mp3")
        self.niv4_player = arcade.play_sound(self.niv4_sound, looping=True)

        # Eau
        # Zone d'eau (tout ce qui est EN DESSOUS de ce y est sous l'eau)
        self.water_level_y = 500
        self.underwater_alpha = 0
        self.float_offset = 0

        # Fond Niveau 4
        n = 3
        self.background = None
        self.background_scale = []
        arcade.set_background_color(arcade.color.DARK_BLUE)

        # Filtre
        self.filter_color = (64, 224, 208)
        self.filter_alpha = 70

        ## PLAYER
        self.setup_player(130, 700)  # ou autre position
        self.setup_physics()

        # Ennemi
        # --- ECREVISSE ANIMÉE ---
        self.crayfish_list = arcade.SpriteList()

        crayfish = arcade.AnimatedTimeBasedSprite(scale=2)

        # Textures droite
        crayfish.walk_right_frames = [
            arcade.AnimationKeyframe(
                0, 200, arcade.load_texture("Images/Ecrevisse_Walk1.png")
            ),
            arcade.AnimationKeyframe(
                1, 200, arcade.load_texture("Images/Ecrevisse_Walk2.png")
            ),
        ]

        # Textures gauche (miroir)
        crayfish.walk_left_frames = [
            arcade.AnimationKeyframe(
                0, 200, arcade.load_texture("Images/Ecrevisse_Walk1.png", mirrored=True)
            ),
            arcade.AnimationKeyframe(
                1, 200, arcade.load_texture("Images/Ecrevisse_Walk2.png", mirrored=True)
            ),
        ]

        # Animation initiale
        crayfish.frames = crayfish.walk_right_frames
        # Position
        crayfish.center_x = 300
        crayfish.center_y = 200
        # Mouvement
        crayfish.change_x = 2
        crayfish.left_limit = 200
        crayfish.right_limit = 400

        self.crayfish_list.append(crayfish)

        # --- PARCHEMIN (Value) ---
        value1 = Value(
            "Images/03_scroll.png",
            "Images/01_papers.png",
            "Eloigne toi de cette ecrevisse mangeuse d'eufs",
            scale=0.4
        )

        value1.center_x = 300
        value1.center_y = 650

        self.value_list.append(value1)

        value2 = Value(
            "Images/03_scroll.png",
            "Images/01_papers.png",
            "Press A pour appeler la femelle",
            scale=0.4
        )

        value2.center_x = 950
        value2.center_y = 590

        self.value_list.append(value2)

        # Plateformes
        self.load_level_from_file("levels/level4.txt")

        # Décor
        self.decor_list = arcade.SpriteList()
        self.load_decor_from_file("levels/level4_decor.txt")

        # Décor de fond (arrière-plan supplémentaire)
        self.back_decor_list = arcade.SpriteList()
        self.load_back_decor_from_file("levels/level1_back_decor.txt")

        # Porte pour futur Level5
        door = arcade.Sprite("Images/door1.png", scale=1)
        door.center_x = 1600
        door.center_y = 200
        self.door_list.append(door)

    def is_player_underwater(self):
        return self.player.center_y < self.water_level_y

    def draw_underwater_filter(self):
        if self.underwater_alpha <= 1:
            return

        screen_bottom = self.camera.position[1]
        screen_top = screen_bottom + SCREEN_HEIGHT

        # si la surface est hors écran
        if self.water_level_y > screen_top:
            return

        # hauteur immergée visible
        water_height = max(0, screen_bottom + SCREEN_HEIGHT - self.water_level_y)

        if water_height <= 0:
            return

        arcade.draw_rectangle_filled(
            self.camera.position[0] + SCREEN_WIDTH / 2,
            self.water_level_y - water_height / 2,
            SCREEN_WIDTH,
            water_height,
            (*self.filter_color, int(self.underwater_alpha))
        )

    def on_hide_view(self):
        if hasattr(self, 'niv4_player') and self.niv4_player:
            arcade.stop_sound(self.niv4_player)

    def on_draw(self):
        self.clear()

        # =====================
        # MONDE (avec caméra)
        # =====================
        self.camera.use()

        self.draw_background()


        # Surface de l'eau
        arcade.draw_rectangle_filled(
            self.camera.position[0] + SCREEN_WIDTH / 2,
            self.water_level_y,
            SCREEN_WIDTH * 4,
            6,
            arcade.color.DARK_TURQUOISE
        )

        self.draw_underwater_filter()

        self.back_decor_list.draw()
        self.decor_list.draw()  # décor derrière
        self.ground_list.draw()  # plateformes
        self.enemy_list.draw()
        self.crayfish_list.draw()
        self.item_list.draw()
        self.prey_list.draw()
        self.heron_list.draw()
        self.female_list.draw()
        original_y = self.player.center_y
        self.player.center_y += self.float_offset
        self.player.draw()
        self.player.center_y = original_y

        self.draw_health_bar()
        self.draw_values()
        self.draw_values_ui()

        # --- Icônes / parchemins collectés ---
        icon_x = 70
        icon_y = SCREEN_HEIGHT - 70

        for value in self.value_list:
            if not value.active:
                arcade.draw_texture_rectangle(
                    icon_x,
                    icon_y,
                    80, 60,
                    value.opened_texture
                )
                arcade.draw_text(
                    value.info_text,
                    icon_x,
                    icon_y - 5,
                    arcade.color.BLACK,
                    font_size=5,
                    anchor_x="center",
                    anchor_y="center",
                    width=50,
                    multiline=True
                )
                icon_x += 90

        # =====================
        # GAME OVER
        # =====================
        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.BLACK,
                50,
                anchor_x="center",
                anchor_y="center"
            )

        # =====================
        # YOU WIN
        # =====================
        if hasattr(self, "game_won") and self.game_won:
            arcade.draw_text(
                "YOU WIN",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.GOLD,
                50,
                anchor_x="center",
                anchor_y="center"
            )

    def on_update(self, delta_time):
        # Tout bloque si game over ou game won
        if self.game_over or getattr(self, "game_won", False):
            return

        self.physics.update()

        # --- Ecrevisse ---
        for crayfish in self.crayfish_list:
            crayfish.center_x += crayfish.change_x
            if crayfish.center_x > crayfish.right_limit:
                crayfish.change_x *= -1
                crayfish.frames = crayfish.walk_right_frames
            elif crayfish.center_x < crayfish.left_limit:
                crayfish.change_x *= -1
                crayfish.frames = crayfish.walk_left_frames
            crayfish.update_animation(delta_time)

        crayfish_hit = arcade.check_for_collision_with_list(self.player, self.crayfish_list)
        for crayfish in crayfish_hit:
            self.current_health -= 1
            self.current_health = max(self.current_health, 0)
            self.player.center_x -= 30
            if self.current_health == 0:
                self.game_over = True

        # --- Player ---
        self.update_player_animation(delta_time)
        self.update_values_floating()
        self.handle_value_collision(delta_time)

        # Son herbe
        # --- Son herbe ---
        if self.player.change_x != 0:
            if not self.window.walk_sound_player:
                self.window.walk_sound_player = arcade.play_sound(
                    self.sound_walk_grass,
                    volume=0.6,
                    looping=True
                )
        else:
            if self.window.walk_sound_player:
                arcade.stop_sound(self.window.walk_sound_player)
                self.window.walk_sound_player = None

        # --- Femelle ---
        if self.female_active:
            distance = self.player.center_x - self.female.center_x
            self.female.change_x = self.female_speed if distance > 0 else -self.female_speed if distance < 0 else 0

            self.female.center_x += self.female.change_x
            self.female.update_animation(delta_time)

            # Collision victoire
            if arcade.check_for_collision(self.female, self.player) and not getattr(self, "game_won", False):
                self.game_won = True
                arcade.play_sound(self.win_sound)
                print("Collision femelle → YOU WIN !")

        # Dans l'eau
        if self.is_player_underwater():
            self.float_offset = math.sin(time.time() * 2) * 6
        else:
            self.float_offset = 0

        target_alpha = self.filter_alpha if self.is_player_underwater() else 0
        self.underwater_alpha += (target_alpha - self.underwater_alpha) * 0.1

        self.scroll_to_player()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)  # flèches/saut

        if key == arcade.key.A:
            self.female_active = True
            print("A pressé - femelle active")  # debug


# ---------------- LANCEMENT ----------------
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

# Musique principale (pages de présentation)
window.main_theme = arcade.load_sound("Sons/Main_theme.mp3")
window.main_theme_player = None
window.walk_sound_player = None


# On commence par la page d'accueil
home = HomeView()
window.show_view(home)

arcade.run()
