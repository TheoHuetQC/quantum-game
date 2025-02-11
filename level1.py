import pygame

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Musée Quantique - Niveau 1")

# Couleurs
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
PURPLE = (128, 0, 128)

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
    "Essaye donc ici de le mesurer."
]

# Ajout d'un message après la mesure
measured_message = "Bravo ! Tu as fixé le caillou, tu peux passer à la salle suivante !"
dialogue_index = 0
showing_dialogue = True
show_measured_message = False

# Boucle de jeu
running = True
while running:
    WINDOW.fill(WHITE)  # Fond blanc
    
    # Dessiner les portes
    pygame.draw.rect(WINDOW, BROWN, entrance_door)
    pygame.draw.rect(WINDOW, BROWN, exit_door)
    
    # Dessiner l'inventaire
    for i, slot in enumerate(inventory_slots):
        color = LIGHT_GRAY if i == selected_slot else GRAY
        pygame.draw.rect(WINDOW, color, slot)
    
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
    elif show_measured_message:
        measured_text = dialogue_font.render(measured_message, True, BLACK)
        measured_rect = measured_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        WINDOW.blit(measured_text, measured_rect)
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if showing_dialogue:
                dialogue_index += 1
                if dialogue_index >= len(dialogues):
                    showing_dialogue = False
            else:
                # Vérifier si on clique sur un des cailloux quantiques
                for pos in quantum_stone_positions:
                    distance = ((event.pos[0] - pos[0])**2 + (event.pos[1] - pos[1])**2) ** 0.5
                    if distance <= quantum_stone_radius:
                        quantum_measured = True
                        door_locked = False
                        show_measured_message = True
                        break
                
                # Vérifier si une case de l'inventaire est cliquée
                for i, slot in enumerate(inventory_slots):
                    if slot.collidepoint(event.pos):
                        selected_slot = i if inventory[i] is not None else None
                        main = inventory[i]  # Met à jour l'objet sélectionné
                
                # Vérifier si la porte de sortie est cliquée
                if exit_door.collidepoint(event.pos) and not door_locked:
                    running = False  # Terminer le niveau
    
    pygame.display.flip()

pygame.quit()
