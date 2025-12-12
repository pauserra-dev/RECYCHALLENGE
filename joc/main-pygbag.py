# TDR RECYCHALLENGE
import asyncio
import pygame
import os
import random
import sys

# Inicialitzar Pygame
pygame.init()

# --- SO ---
try:
    pygame.mixer.init()
    if os.path.exists("musica.ogg"):
        pygame.mixer.music.load("musica.ogg")
        pygame.mixer.music.play(-1)
except Exception as e:
    print(f"Avís so: {e}")

# --- PANTALLA ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RECYCHALLENGE")

# --- CÀRREGA D'IMATGES ---
try:
    background = pygame.transform.scale(pygame.image.load("background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    pantalla_inici = pygame.transform.scale(pygame.image.load("pantalla_inici.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    instruccions_img = pygame.transform.scale(pygame.image.load("instruccions.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    informacio_img = pygame.transform.scale(pygame.image.load("informació.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
except Exception as e:
    print(f"Error carregant fons: {e}")
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((200, 240, 255))
    pantalla_inici = background
    instruccions_img = background
    informacio_img = background

# --- CONTENIDORS ---
scale_w = SCREEN_WIDTH / 1920
scale_h = SCREEN_HEIGHT / 1080
container_width = int(280 * scale_w)
container_height = int(280 * scale_h)

def load_container(name):
    try:
        return pygame.transform.scale(pygame.image.load(name), (container_width, container_height))
    except:
        s = pygame.Surface((container_width, container_height))
        s.fill((100,100,100))
        return s

contenidor_blau = load_container("contenidor_blau.png")
contenidor_verd = load_container("contenidor_verd.png")
contenidor_groc = load_container("contenidor_groc.png")
contenidor_marro = load_container("contenidor_marro.png")
contenidor_gris = load_container("contenidor_gris.png")

try:
    deixalleria = pygame.transform.scale(pygame.image.load("deixalleria.png"), (int(350 * scale_w), int(350 * scale_h)))
except:
    deixalleria = pygame.Surface((int(350 * scale_w), int(350 * scale_h)))
    deixalleria.fill((50,50,50))

contenidors = [contenidor_blau, contenidor_verd, contenidor_groc, contenidor_marro, contenidor_gris, deixalleria]

spacing = 10
x_offset = (SCREEN_WIDTH - (len(contenidors) * (container_width + spacing))) // 2 
if x_offset < 0: x_offset = 10

contenidor_positions = [(x_offset + i * (container_width + spacing), SCREEN_HEIGHT - container_height - 20) for i in range(len(contenidors) - 1)] + [(SCREEN_WIDTH - int(350 * scale_w) - 20, (SCREEN_HEIGHT - int(350 * scale_h)) // 2)]

# --- OBJECTES ---
objectes = {
    "1_diari.png": "blau", "2_ampolla_plastic.png": "groc", "3_ampolla_vidre.png": "verd",
    "4_tovalloletes_humides.png": "gris", "5_cadira_trencada.png": "deixalleria",
    "6_bossa_paper.png": "blau", "7_bric_suc_taronja.png": "groc", "8_closques_fruits_secs.png": "marro",
    "9_ampolla_vi.png": "verd", "10_raspall_dents.png": "gris", "11_bossa_plastic.png": "groc",
    "12_llapis.png": "gris", "13_teclat.png": "deixalleria", "14_capsa_sabates.png": "blau",
    "15_paper_alumini.png": "groc", "16_iogurt_vidre.png": "verd", "17_capsa_galetes.png": "blau",
    "18_restes_menjar.png": "marro", "19_llit_vell.png": "deixalleria", "20_llauna.png": "groc",
    "21_sobre.png": "blau", "22_taps_botella.png": "groc", "23_closca_ou.png": "marro",
    "24_bombeta.png": "gris", "25_armari_fusta.png": "deixalleria", "26_escuradents.png": "marro",
    "27_bossa_patates.png": "groc", "28_maquineta.png": "gris", "29_televisio.png": "deixalleria",
    "30_mascareta.png": "gris",
}

objecte_images = {}
for name in objectes:
    img_loaded = None
    try:
        img_loaded = pygame.image.load(name)
    except:
        try:
            img_loaded = pygame.image.load("objectes/" + name)
        except:
            pass
            
    if img_loaded:
        try:
            img_scaled = pygame.transform.scale(img_loaded, (int(200 * scale_w), int(200 * scale_h)))
            objecte_images[name] = img_scaled
        except:
            pass

# Variables joc
current_object_name = random.choice(list(objectes.keys())) if objecte_images else None
current_object = objecte_images.get(current_object_name)
object_x, object_y = 100, 100
object_dragging = False
correct_classifications = 0

# --- FONTS ---
try:
    button_font = pygame.font.Font("Roboto.ttf", 70)
    font = pygame.font.Font("Roboto.ttf", 50)
    # NOVA FONT PETITA PER ALS BOTONS DE TORNAR
    small_font = pygame.font.Font("Roboto.ttf", 30)
except:
    button_font = pygame.font.Font(None, 70)
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 30)

button_color = (173, 216, 230)
button_hover_color = (135, 206, 235)
button_padding = 20

# --- FUNCIONS ---

def show_message(message, color, x, y):
    text = font.render(message, True, color)
    screen.blit(text, (x, y))

# Ara accepta una font opcional
def draw_button(text, x, y, font_to_use=button_font, color=(173, 216, 230), border_radius=20):
    button_text = font_to_use.render(text, True, (0, 0, 0))
    width = button_text.get_width() + button_padding * 2
    height = button_text.get_height() + button_padding * 2
    mouse_pos = pygame.mouse.get_pos()
    
    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        color = button_hover_color
    
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=20)
    screen.blit(button_text, (x + button_padding, y + button_padding))
    return rect

def button_clicked(rect, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if rect.collidepoint(event.pos):
            return True
    return False

# --- PANTALLES ---

async def pantalla_instruccions():
    waiting = True
    while waiting:
        screen.blit(instruccions_img, (0, 0))
        
        # BOTÓ PETIT A DALT A LA DRETA
        text_boto = "TORNAR"
        width_boto = small_font.size(text_boto)[0] + button_padding * 2
        tornar_button = draw_button(text_boto, SCREEN_WIDTH - width_boto - 20, 20, font_to_use=small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if button_clicked(tornar_button, event):
                waiting = False
        
        pygame.display.flip()
        await asyncio.sleep(0)

async def pantalla_informacio():
    waiting = True
    while waiting:
        screen.blit(informacio_img, (0, 0))
        
        # BOTÓ PETIT A DALT A LA DRETA
        text_boto = "TORNAR"
        width_boto = small_font.size(text_boto)[0] + button_padding * 2
        tornar_button = draw_button(text_boto, SCREEN_WIDTH - width_boto - 20, 20, font_to_use=small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if button_clicked(tornar_button, event):
                waiting = False
        
        pygame.display.flip()
        await asyncio.sleep(0)

async def pantalla_inici_func():
    inici = True
    while inici:
        screen.fill((255, 255, 255))
        screen.blit(pantalla_inici, (0, 0))
        
        # Botó Sortir (X)
        sortir_button = draw_button("X", SCREEN_WIDTH - 80, 20, font_to_use=small_font, color=(255, 0, 0), border_radius=50)

        # TEXTOS DELS BOTONS
        txt_jugar = "JUGAR"
        txt_inst = "INSTRUCCIONS"
        txt_info = "INFORMACIÓ ÚTIL"

        # CÀLCUL DE L'AMPLADA TOTAL DEL BOTÓ (Text + Padding) PER CENTRAR
        w_jugar = button_font.size(txt_jugar)[0] + button_padding * 2
        w_inst = button_font.size(txt_inst)[0] + button_padding * 2
        w_info = button_font.size(txt_info)[0] + button_padding * 2

        # POSICIONS X CENTRADES PERFECTAMENT
        x_jugar = (SCREEN_WIDTH - w_jugar) // 2
        x_inst = (SCREEN_WIDTH - w_inst) // 2
        x_info = (SCREEN_WIDTH - w_info) // 2

        # DIBUIXAR BOTONS
        jugar_button = draw_button(txt_jugar, x_jugar, SCREEN_HEIGHT // 2 - 80)
        instruccions_button = draw_button(txt_inst, x_inst, SCREEN_HEIGHT // 2 + 60)
        informacio_button = draw_button(txt_info, x_info, SCREEN_HEIGHT // 2 + 200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if button_clicked(sortir_button, event):
                pygame.quit(); sys.exit()
            if button_clicked(jugar_button, event):
                return
            if button_clicked(instruccions_button, event):
                await pantalla_instruccions()
            if button_clicked(informacio_button, event):
                await pantalla_informacio()

        pygame.display.flip()
        await asyncio.sleep(0)

# --- BUCLE PRINCIPAL ---

async def main():
    global object_x, object_y, object_dragging, correct_classifications, current_object_name, current_object
    
    await pantalla_inici_func()

    running = True
    offset_x = 0
    offset_y = 0

    while running:
        screen.blit(background, (0, 0))

        for i, contenidor in enumerate(contenidors):
            if i < len(contenidor_positions):
                screen.blit(contenidor, contenidor_positions[i])

        show_message(f"Punts: {correct_classifications}", (255, 255, 255), 20, 20)
        
        # BOTÓ TORNAR (PETIT I A DALT A LA DRETA)
        text_boto = "TORNAR"
        width_boto = small_font.size(text_boto)[0] + button_padding * 2
        tornar_button = draw_button(text_boto, SCREEN_WIDTH - width_boto - 20, 20, font_to_use=small_font)

        if current_object:
            screen.blit(current_object, (object_x, object_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if button_clicked(tornar_button, event):
                correct_classifications = 0
                await pantalla_inici_func()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if current_object and object_x < event.pos[0] < object_x + current_object.get_width() and object_y < event.pos[1] < object_y + current_object.get_height():
                        object_dragging = True
                        offset_x = object_x - event.pos[0]
                        offset_y = object_y - event.pos[1]
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    object_dragging = False
                    dropped = False
                    
                    for i, (container_x, container_y) in enumerate(contenidor_positions):
                        if i >= len(contenidors): break
                        
                        if container_x < event.pos[0] < container_x + container_width and container_y < event.pos[1] < container_y + container_height:
                            container_name = ["blau", "verd", "groc", "marro", "gris", "deixalleria"][i]
                            
                            if container_name == objectes.get(current_object_name):
                                show_message("CORRECTE", (0, 255, 0), SCREEN_WIDTH // 2 - 100, 50)
                                
                                # FRASES EDUCATIVES
                                frases = {
                                    "1_diari.png": "Sabies que un diari reciclat pot ser transformat en paper higiènic o nou paper per escriure?",
                                    "2_ampolla_plastic.png": "Amb 22 ampolles de plàstic reciclades es pot fabricar una samarreta.",
                                    "3_ampolla_vidre.png": "El vidre es pot reciclar infinitament sense perdre la seva qualitat.",
                                    "4_tovalloletes_humides.png": "Les tovalloletes humides no es poden llençar al WC ni reciclar; sempre han d'anar al contenidor gris.",
                                    "5_cadira_trencada.png": "Les cadires de fusta o plàstic trencades s'han de portar a la deixalleria per poder reciclar els materials.",
                                    "6_bossa_paper.png": "Reciclant paper s'evita la tala d'arbres i es redueixen les emissions de CO2.",
                                    "7_bric_suc_taronja.png": "Els envasos de bric tenen una combinació de paper, alumini i plàstic que es poden reciclar si es separen correctament.",
                                    "8_closques_fruits_secs.png": "Les closques de fruits secs es poden convertir en compost per nodrir les plantes.",
                                    "9_ampolla_vi.png": "Sabies que el vidre d'una ampolla de vi pot ser reutilitzat per fer una altra ampolla en menys de 30 dies?",
                                    "10_raspall_dents.png": "Els raspalls de dents contenen plàstic i altres materials que no es poden reciclar, per això van al contenidor gris.",
                                    "11_bossa_plastic.png": "Les bosses de plàstic es poden reciclar per fabricar mobles o altres objectes de plàstic reutilitzat.",
                                    "12_llapis.png": "Quan els llapis estan gastats ja no es poden reutilitzar ni reciclar, per tant, han d'anar al contenidor gris.",
                                    "13_teclat.png": "Els teclats contenen components electrònics que s'han de portar a la deixalleria per ser reciclats de manera segura.",
                                    "14_capsa_sabates.png": "Reciclant una capsa de sabates ajudes a estalviar energia i reduir la contaminació de l'aigua.",
                                    "15_paper_alumini.png": "L'alumini es pot reciclar completament sense perdre qualitat, fent-lo ideal per a la reutilització.",
                                    "16_iogurt_vidre.png": "Els pots de vidre de iogurt es poden reutilitzar o reciclar infinitament sense perdre qualitat.",
                                    "17_capsa_galetes.png": "La majoria de les capses de galetes estan fetes de cartró i poden ser reciclades per fer nous productes de paper.",
                                    "18_restes_menjar.png": "Les restes de menjar es poden transformar en compost, que és un excel·lent fertilitzant natural.",
                                    "19_llit_vell.png": "Els llits vells contenen diferents materials que necessiten ser separats i reciclats a la deixalleria.",
                                    "20_llauna.png": "Les llaunes d'alumini es poden reciclar infinitament i poden convertir-se en noves llaunes en tan sols 60 dies.",
                                    "21_sobre.png": "Els sobres de paper es poden reciclar i convertir en nou paper, ajudant a reduir la tala d'arbres.",
                                    "22_taps_botella.png": "Els taps de plàstic es poden reutilitzar per fer joguines, mobiliari urbà o fins i tot nous envasos.",
                                    "23_closca_ou.png": "Les closques d'ou es poden utilitzar per enriquir el compost i aportar calci al sòl.",
                                    "24_bombeta.png": "No totes les bombetes es poden reciclar; per això s'han de dipositar en punts especials o al contenidor gris.",
                                    "25_armari_fusta.png": "Els mobles grans com els armaris han de portar-se a la deixalleria per facilitar-ne el reciclatge.",
                                    "26_escuradents.png": "Els escuradents es poden compostar ja que són de fusta, que és biodegradable.",
                                    "27_bossa_patates.png": "Les bosses de patates solen estar fetes de materials plàstics que es poden reciclar en el contenidor groc.",
                                    "28_maquineta.png": "Les maquinetes per afilar llapis tenen metall i plàstic, per la qual cosa s'han de llençar al contenidor gris.",
                                    "29_televisio.png": "Les televisions contenen components tòxics i han de ser reciclades a la deixalleria per evitar la contaminació.",
                                    "30_mascareta.png": "Les mascaretes contenen materials que no es poden reciclar i han de ser llençades al contenidor gris per seguretat."
                                }
                                
                                frase = frases.get(current_object_name, "")
                                
                                # Dibuixar frase centrada
                                if font.size(frase)[0] > SCREEN_WIDTH - 40:
                                    words = frase.split()
                                    line1, line2 = "", ""
                                    for word in words:
                                        if font.size(line1 + word)[0] < SCREEN_WIDTH - 40:
                                            line1 += word + " "
                                        else:
                                            line2 += word + " "
                                    show_message(line1.strip(), (0, 0, 0), 20, 150)
                                    show_message(line2.strip(), (0, 0, 0), 20, 200)
                                else:
                                    show_message(frase, (0, 0, 0), 20, 150)
                                
                                pygame.display.flip()
                                await asyncio.sleep(4) 
                                
                                correct_classifications += 1
                                current_object_name = random.choice(list(objectes.keys()))
                                current_object = objecte_images[current_object_name]
                                object_x, object_y = 100, 100
                            else:
                                show_message("INCORRECTE", (255, 0, 0), SCREEN_WIDTH // 2 - 100, 50)
                                pygame.display.flip()
                                await asyncio.sleep(1)
                                object_x, object_y = 100, 100
                            
                            dropped = True
                            break
                    
                    if not dropped:
                        object_x, object_y = 100, 100

            elif event.type == pygame.MOUSEMOTION:
                if object_dragging:
                    object_x = event.pos[0] + offset_x
                    object_y = event.pos[1] + offset_y

        pygame.display.flip()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())