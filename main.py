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

# Définition des portes
entrance_door = pygame.Rect(250, HEIGHT - 50, 300, 40)  # Porte d'entrée en bas
exit_door = pygame.Rect(350, 20, 100, 40)  # Porte de sortie en haut

# Définition de l'inventaire
inventory_slots = [pygame.Rect(WIDTH - 260 + i * 50, HEIGHT - 60, 40, 40) for i in range(5)]
inventory = [None] * 5  # Liste des objets dans l'inventaire
selected_slot = None  # Indice de la case sélectionnée
main = None  # Objet actuellement sélectionné

# Police
font = pygame.font.Font(None, 50)

# État de la porte de sortie
door_locked = True  # La porte est verrouillée par défaut

# Écran d'accueil
def show_start_screen():
    WINDOW.fill(WHITE)
    title_text = font.render("Musée de la quantique", True, BLACK)
    enter_text = font.render("Entrer", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    enter_rect = enter_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    WINDOW.blit(title_text, title_rect)
    WINDOW.blit(enter_text, enter_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Écran de fin de niveau
def show_end_screen():
    WINDOW.fill(WHITE)
    end_text = font.render("Passer à la salle 2", True, BLACK)
    end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    WINDOW.blit(end_text, end_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                exit()

# Affichage de l'écran d'accueil
show_start_screen()

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
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si un slot de l'inventaire est cliqué
            for i, slot in enumerate(inventory_slots):
                if slot.collidepoint(event.pos):
                    selected_slot = i if inventory[i] is not None else None
                    main = inventory[i]  # Met à jour l'objet sélectionné
            
            # Vérifier si la porte de sortie est cliquée
            if exit_door.collidepoint(event.pos) and not door_locked:
                show_end_screen()
    
    pygame.display.flip()

pygame.quit()
