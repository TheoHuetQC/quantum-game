import pygame
import time

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Musée Quantique")

# Couleurs
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (220, 220, 220)
PURPLE = (128, 0, 128)

# État du jeu
state = "start"

# Définition des portes
entrance_door = pygame.Rect(250, HEIGHT - 50, 300, 40)  # Porte d'entrée en bas
exit_door = pygame.Rect(350, 20, 100, 40)  # Porte de sortie en haut

# Définition de l'inventaire
inventory_slots = [pygame.Rect(WIDTH - 260 + i * 50, HEIGHT - 60, 40, 40) for i in range(5)]
inventory = [None] * 5  # Liste des objets dans l'inventaire
selected_slot = None  # Indice de la case sélectionnée
main = None  # Objet actuellement sélectionné

# Définition du caillou quantique
quantum_stone_positions = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2, exit_door.bottom + 20)]
quantum_stone_radius = 25
quantum_measured = False

# Police
font = pygame.font.Font(None, 50)
dialogue_font = pygame.font.Font(None, 30)

# État de la porte de sortie
door_locked = True  # La porte est verrouillée par défaut

# Dialogue du narrateur
dialogues = [
    "Bienvenue au Musée de la Quantique !",
    "Ici, les scientifiques ont réussi à donner des propriétés quantiques\nà des objets macroscopiques.",
    "Dans cette première salle, nous avons un caillou quantique...",
    "Il peut être à plusieurs endroits à la fois !",
    "Mais... Oh non ! Il bloque l'accès à la salle suivante !",
    "En physique quantique, mesurer un objet réduit sa superposition\net le fixe à un seul état.",
    "Tiens, prends cet appareil, il te sera utile !",
    "Essaye donc ici de le mesurer en sélectionnant le positiomètre."
]

# Ajout d'un message après la mesure
measured_message = "Bravo ! Tu as fixé le caillou, tu peux passer à la salle suivante !"
dialogue_index = 0
showing_dialogue = True
show_measured_message = False
positiometer_given = False
animating_item = False
item_pos = None
animation_steps = 50  # Nombre d'étapes pour ralentir l'animation
step_counter = 0
wait_for_click = False  # Variable pour attendre le clic avant de commencer l'animation

# Boucle de jeu
running = True
while running:
    WINDOW.fill(WHITE)  # Fond blanc
    
    if state == "start":
        start_text = font.render("Musée de la Quantique - Entrer", True, BLACK)
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WINDOW.blit(start_text, start_rect)
    
    elif state == "game":
        # Dessiner les portes
        pygame.draw.rect(WINDOW, BROWN, entrance_door)
        pygame.draw.rect(WINDOW, BROWN, exit_door)
        
        # Dessiner l'inventaire
        for i, slot in enumerate(inventory_slots):
            color = LIGHT_GRAY if i == selected_slot else GRAY
            pygame.draw.rect(WINDOW, color, slot)
            if inventory[i] == "positiometre":
                pygame.draw.rect(WINDOW, DARK_GRAY, slot)
        
        # Dessiner le caillou quantique
        if not quantum_measured:
            for pos in quantum_stone_positions:
                pygame.draw.circle(WINDOW, PURPLE, pos, quantum_stone_radius)
        else:
            pygame.draw.circle(WINDOW, PURPLE, quantum_stone_positions[0], quantum_stone_radius)
        
        # Afficher le dialogue
        if showing_dialogue and dialogue_index < len(dialogues):
            lines = dialogues[dialogue_index].split("\n")
            for i, line in enumerate(lines):
                dialogue_text = dialogue_font.render(line, True, BLACK)
                dialogue_rect = dialogue_text.get_rect(center=(WIDTH // 2, HEIGHT - 100 + i * 30))
                WINDOW.blit(dialogue_text, dialogue_rect)
            
            # Ajouter le positimètre au bon moment avec animation
            if dialogue_index == 6 and not positiometer_given:
                item_pos = [WIDTH // 2 - 40, HEIGHT // 2 - 40]  # Appareil plus grand au centre
                animating_item = True
                positiometer_given = True
                step_counter = 0
                wait_for_click = True  # Attendre le clic avant de commencer l'animation
        
        elif show_measured_message:
            measured_text = dialogue_font.render(measured_message, True, BLACK)
            measured_rect = measured_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            WINDOW.blit(measured_text, measured_rect)
        
        # Afficher l'appareil au centre du dialogue
        if animating_item and item_pos and wait_for_click:
            pygame.draw.rect(WINDOW, DARK_GRAY, (item_pos[0], item_pos[1], 80, 80))
        
        # L'animation ne commence qu'après le clic
        if animating_item and not wait_for_click:
            # Déplacer l'appareil vers la première case de l'inventaire
            pygame.draw.rect(WINDOW, DARK_GRAY, (item_pos[0], item_pos[1], 40, 40))
            target_x, target_y = inventory_slots[0].x, inventory_slots[0].y
            item_pos[0] += (target_x - item_pos[0]) / (animation_steps - step_counter)
            item_pos[1] += (target_y - item_pos[1]) / (animation_steps - step_counter)
            step_counter += 1
            if step_counter >= animation_steps:
                inventory[0] = "positiometre"
                animating_item = False
    
    elif state == "end":
        end_text = font.render("Passer à la salle 2", True, BLACK)
        end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WINDOW.blit(end_text, end_rect)
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "start":
                state = "game"
            elif state == "game":
                if showing_dialogue:
                    dialogue_index += 1
                    if dialogue_index >= len(dialogues):
                        showing_dialogue = False
                else:
                    for i, slot in enumerate(inventory_slots):
                        if slot.collidepoint(event.pos):
                            selected_slot = i if inventory[i] is not None else None
                            main = inventory[i]
                    
                    for pos in quantum_stone_positions:
                        distance = ((event.pos[0] - pos[0])**2 + (event.pos[1] - pos[1])**2) ** 0.5
                        if distance <= quantum_stone_radius and main == "positiometre":
                            quantum_measured = True
                            door_locked = False
                            show_measured_message = True
                            break
                    
                    if exit_door.collidepoint(event.pos) and not door_locked:
                        state = "end"
            
            # Lorsque le joueur clique, démarrer l'animation du positimètre
            if wait_for_click:
                wait_for_click = False  # L'animation commence après le clic
    
    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()
