import pygame
import random
import time
pygame.font.init()

#Créé les dimensions de la fenètres
WIDTH, HEIGHT = 1000, 800 #Largeur/Hauteur
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge") #Nomme la fenètre

BG = pygame.transform.scale(pygame.image.load("bg.webp"),(WIDTH, HEIGHT)) #séléctionne l'image de background et modifie la scale de l'image pour remplir la fénètre

#définit les caractéristiques des projectiles
STAR_WIDTH = 10 #Largeur du projectile
STAR_HEIGHT = 8 #Hauteur du projectile
STAR_VEL= 3 #Vitesse du projectile

#Définit les dimensions du joueur
PLAYER_WIDTH = 40 #Largeur
PLAYER_HEIGHT = 40 #Hauteur
PLAYER_VEL = 5 #Vitesse

FONT = pygame.font.SysFont("comiscsans", 30)
def draw(player, elapsed_time,stars,level): # définit le fond écran/joeur
    WIN.blit(BG, (0, 0)) #Appel la valeur BG et définit le pixel de départ du BG full écran = 0,0
    
    pygame.draw.rect(WIN, "red", player) #Affiche le joueur
    
    time_text=FONT.render (f"Time : {round(elapsed_time)}s",1,"white") #Définit le texte du temps
    WIN.blit(time_text, (10, 30)) # Affiche le texte au coordonnées  10, 30 -> horizontal, vertical
    
    current_level=FONT.render (f"Level : " + str(level), 1, "white" ) #Définit le texte du niveau
    WIN.blit(current_level, (10,10)) # Affiche le texte du niveau  10, 10 -> horizontal, vertical
    
    for star in stars:
        pygame.draw.rect(WIN, "white", star) #Affiche les étoiles
    
    
    pygame.display.update() #mets à jour les éléments affichés


    
"""
def paused():
    pause_text = FONT.render("Game Paused", 1, "Green")
    WIN.blit (pause_text, (WIDTH/2-pause_text.get_width()/2, HEIGHT/2 - pause_text.get_height()/2))
    pygame.display.update()
    print("Entrée en Pause")
    pygame.time.delay(4000)
"""
  


def main():#fonction qui va faire tourner le jeu sinon la fenètre se ferme
    run = True # Lance le jeu
    
    player = pygame.Rect(500, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) #Créé le joueur est définit son emplacement
    
    clock = pygame.time.Clock() # Définit l'horloge
    
    start_time = time.time()  # Définit la fonction pour lancer l'horloge
    elapsed_time=0 # temps écoulé
    level = 0 # niveau de départ
    star_add_increment = 2000 # temps avant les nouveaux projectiles
    star_count = 0 # Compte les étoiles
    
    stars = [] #Liste des étoiles
    hit = False # définit quand le joueur est touché pour déclencher le "if hit :"

    nb_star = 2 # Nombre d'étoile a générer
    
    #is_paused = False
    
    while run :
        star_count += clock.tick (60) 
        elapsed_time = time.time() - start_time #Temps écoulé depuis le début de la partie
        
        if star_count > star_add_increment :
            for _ in range(nb_star) : #Pour _ jusqu'au nombre d'étoile définit dans la valeur de nb_star
                star_x = random.randint(0, WIDTH - STAR_WIDTH) # Génère chaque étoile à une valeur aléatoire en 0 et Width - Starwidth pour faire en sorte que le projectile ne se génère pas en dehors de la fénètre de jeu
                star= pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)  # Définit le corps du projectile
                stars.append(star) # ???
                
            star_add_increment = max(200, star_add_increment - 50) #Définit le temps de spawn des projectiles
            star_count=0
        
        for event in pygame.event.get(): # Programme qui va fermer la fenètre quand on clique sur la croix rouge -> Pas présent de base
            if event.type == pygame.QUIT: # Si on quitte sur la croix
                run = False # Run passe a false se qui termine le programme
                break

        #Définit les touches
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >=0: # Si la touche flèche de gauche est préssée
            player.x -= PLAYER_VEL # Déplace vers la gauche le joueur de la valeur de PLAYER_VEL
            
        elif keys [pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH: # Si la touche de droite est préssée
            player.x += PLAYER_VEL # Déplace vers la droite le joueur de la valeur de PLAYER_VEL
        """   
        if keys [pygame.K_UP] :
            is_paused = not is_paused
        """
        """ 
       if is_paused == True :
            paused()
        """
            
        for star in stars[:]: # Fait les intéractions avec les projectiles
            star.y += STAR_VEL # fait descendres les projectiles de la valeur de STAR_VEL
            if star.y > HEIGHT : # Si la valeur du projectile est supérieure à celle de la fenètre
                stars.remove(star) # Fait disparaitre le projectile
            elif star.y + star.height >= player.y and star.colliderect(player): # Si le projectile rentre en contact avec le joueur
                stars.remove(star) # Enlève le projectile
                hit = True # Fait passer la valeur de hit a true pour lancer la condition "hit"
                break
                     
        if hit : # Si le joueur est touché par un projectile
            lost_text = FONT.render("You Lost!", 1, "Green") # affecte a lost_text le texte a afficher
            lost_text2 = FONT.render("You survived : "+str(int(elapsed_time))+" seconds", 1, "Green") # affecte a lost_text2 le texte a afficher
            WIN.blit (lost_text, (WIDTH/2-lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2)) #Affiche le texte de lost_text au milieu
            WIN.blit (lost_text2, (WIDTH/2-lost_text2.get_width()/2, HEIGHT/1.75 - lost_text2.get_height()/2)) #Affiche le texte de lost_text au milieu mais en dessous de lost_text
            pygame.display.update() #update les éléments a l'écran pour faire apparaitre les textes
            pygame.time.delay(4000) # Attend 4 secondes
            break # Ferme la fenètre
               
        if int(elapsed_time) % 10 == 0 : # Toutes les 10 secondes
            nb_star += 1 # Ajoute un projectile
            level += 1 # Ajoute 1 au compteur de niveau
            new_level = FONT.render("New Level", 1, "Green") # Affecte la valeur "New Level" à la variable "new_level"
            WIN.blit (new_level, (WIDTH/2-new_level.get_width()/2, HEIGHT/2 - new_level.get_height()/2)) # Affiche la variable new_level au milieu de la fenètre
            pygame.display.update() # update les éléments pour afficher le texte
            pygame.time.delay(1000) # pause le jeu pendant 1 secondes
             
        draw(player, elapsed_time,stars,level) # Dessine les différents éléments
                 
    pygame.quit() # Quitte le jeu

if __name__ == "__main__": #fais en sorte de lancer le jeu uniquement si celui ci est éxécuter depuis ce main.py
    main()
