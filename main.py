import pygame

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Musée de la Quantique - Entrée")

# Couleurs
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
PURPLE = (75, 0, 130)
LIGHT_PURPLE = (138, 43, 226)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
SELECTED_COLOR = (255, 255, 255)

# Variables du jeu
enter_museum = False
superposition = True  # Le caillou est en deux endroits
next_room = False
text_index = 0
selected_inventory = None

# Définition de l'inventaire
inventory = [None] * 5  # 5 emplacements d'inventaire
inventory[0] = "appareil de mesure"  # Premier objet

# Positions des éléments
door_top = pygame.Rect(WIDTH // 2 - 50, 20, 100, 20)
door_bottom = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 40, 100, 20)
stone_center = (WIDTH // 2, HEIGHT // 2)
stone_blocking = (WIDTH // 2, 60)

# Positions de l'inventaire
inventory_slots = [pygame.Rect(WIDTH - 150 + i * 30, HEIGHT - 50, 25, 25) for i in range(5)]

dialogues = [
    "Bienvenue au Musée de la Quantique !",
    "Ici, les scientifiques ont réussi à donner des propriétés quantiques\nà des objets macroscopiques.",
    "Dans cette première salle, nous avons un caillou quantique...",
    "Il peut être à plusieurs endroits à la fois !",
    "Mais... Oh non ! Il bloque l'accès à la salle suivante !",
    "En physique quantique, mesurer un objet réduit sa superposition\net le fixe à un seul état.",
    "Cliquez sur l'un des cailloux pour effectuer une mesure et libérer l'accès."
]

def show_entry_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Cliquez pour entrer dans le musée", True, BLACK)
    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2))
    pygame.display.flip()

def draw_dialogue(text):
    font = pygame.font.Font(None, 24)
    dialogue_box = pygame.Rect(20, HEIGHT - 60, WIDTH - 40, 40)
    pygame.draw.rect(screen, BLACK, dialogue_box)
    pygame.draw.rect(screen, WHITE, dialogue_box.inflate(-4, -4))
    lines = text.split("\n")
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (30, HEIGHT - 50 + i * 20))

def draw_inventory():
    for i, slot in enumerate(inventory_slots):
        color = SELECTED_COLOR if selected_inventory == i else GRAY
        pygame.draw.rect(screen, color, slot)
        pygame.draw.rect(screen, BLACK, slot, 2)
        if inventory[i] == "appareil de mesure":
            pygame.draw.rect(screen, BLACK, slot.inflate(-5, -5))

# Boucle pour l'écran d'entrée
running = True
while running and not enter_museum:
    show_entry_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            enter_museum = True

# Mise à jour du titre pour indiquer le niveau 1
pygame.display.set_caption("Musée de la Quantique - Niveau 1")

dialogue_active = True

# Boucle du jeu
while running:
    screen.fill(WHITE)
    
    if next_room:
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Vous entrez dans la salle 2", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
    else:
        # Dessiner les portes
        pygame.draw.rect(screen, BROWN, door_top)
        pygame.draw.rect(screen, BROWN, door_bottom)
        
        # Dessiner le caillou en superposition
        if superposition:
            pygame.draw.circle(screen, LIGHT_PURPLE, stone_blocking, 20)  # Devant la porte
        pygame.draw.circle(screen, PURPLE, stone_center, 20)  # Au centre de la salle
        
        # Afficher le dialogue
        if dialogue_active:
            draw_dialogue(dialogues[text_index])
        
        # Dessiner l'inventaire
        draw_inventory()
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if dialogue_active:
                if text_index < len(dialogues) - 1:
                    text_index += 1
                else:
                    dialogue_active = False
            elif not next_room:
                for i, slot in enumerate(inventory_slots):
                    if slot.collidepoint(event.pos):
                        selected_inventory = i
    
    pygame.display.flip()

pygame.quit()
