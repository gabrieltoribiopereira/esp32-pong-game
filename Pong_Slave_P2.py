import espnow
import network 
from machine import Pin, I2C
import ssd1306
import utime
import ustruct

print("\n" + "=" * 50)
print("PONG - JUGADOR 2 (SLAVE)")
print("=" * 50)
print("IMPORTANTE: Asegúrate de configurar las MACs correctas")
print("=" * 50)

# Configuración WiFi
sta = network.WLAN(network.STA_IF)
sta.active(False)
utime.sleep_ms(100)
sta.active(True)
utime.sleep_ms(100)

sta.disconnect()
utime.sleep_ms(200)

# Configurar canal
canal_actual = 1
for canal in [1, 6, 11]:
    try:
        sta.config(channel=canal)
        canal_actual = sta.config('channel')
        print("Canal configurado:", canal_actual)
        break
    except:
        pass

# Inicializar ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Verificar que soy P2
mi_mac = sta.config('mac')
print("Mi MAC:", ":".join(["%02x" % b for b in mi_mac]))

if mi_mac != b'\x68\xfe\x71\x80\x74\x44':
    print("ERROR: Este codigo es para P2 (68:fe:71:80:74:44)")
    print("Tu MAC es:", ":".join(["%02x" % b for b in mi_mac]))
    print("Debes usar el codigo de P1 (MASTER)")
    while True:
        utime.sleep(1)

# MAC del Jugador 1 (MASTER) - ¡ACTUALIZAR ESTO!
peer = b'\x30\xc6\xf7\x21\xed\x7c'
print("Esperando a P1:", ":".join(["%02x" % b for b in peer]))

# Limpiar y añadir peer
try:
    for p in esp.get_peers():
        esp.del_peer(p[0])
except:
    pass

try:
    esp.add_peer(peer)
    print("Peer anadido OK")
except:
    print("Peer ya existe")

# Configuración Hardware
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
boton2 = Pin(18, Pin.IN, Pin.PULL_UP)

# Variables
largo = 15
ancho = 4
y1 = 25 
y2 = 25 
bx = 64
by = 32
status = 0
ganador = ""
ultimo_envio = 0
ultimo_paquete = utime.ticks_ms()

print("=" * 50)
print("LISTO - Esperando datos de P1...\n")

while True:
    while True:
        current_time = utime.ticks_ms()
        
        # Enviar mi input
        if utime.ticks_diff(current_time, ultimo_envio) > 20:
            mi_estado = b'1' if boton2.value() == 0 else b'0'
            esp.send(peer, mi_estado)
            ultimo_envio = current_time

        # Recibir estado del Master
        nuevo_frame = False
        while True:
            host, msg = esp.recv(0)
            if msg and len(msg) == 5:
                try:
                    bx, by, y1, y2, status = ustruct.unpack('BBBBB', msg)
                    nuevo_frame = True
                    ultimo_paquete = current_time
                except:
                    pass
            else:
                break
        
        # Verificar conexión
        if utime.ticks_diff(current_time, ultimo_paquete) > 2000:
            display.fill(0)
            display.text("BUSCANDO P1...", 10, 10, 1)
            display.text("Canal:" + str(canal_actual), 10, 25, 1)
            mac_corta = ":".join(["%02x" % b for b in mi_mac[3:]])
            display.text("Mi MAC: " + mac_corta, 10, 40, 1)
            display.show()
            utime.sleep_ms(100)
            continue

        # Detectar fin
        if status == 1:
            ganador = "Player 1"
            break
        elif status == 2:
            ganador = "Player 2"
            break

        # Dibujar
        if nuevo_frame:
            display.fill(0)
            for y in range(int(y1), int(y1 + largo)):
                for x in range(0, ancho):
                    display.pixel(x, y, 1)
            for y in range(int(y2), int(y2 + largo)):
                for x in range(128 - ancho, 128):
                    display.pixel(x, y, 1)
            for px in range(2):
                for py in range(2):
                    display.pixel(int(bx) + px, int(by) + py, 1)
            display.show()

    # Game Over
    print("GAME OVER - Gana:", ganador)
    display.fill(0)
    display.text("GAME OVER", 30, 20, 1)
    display.text("GANA: " + ganador, 15, 35, 1)
    display.text("PULSA BOTON", 20, 50, 1)
    display.show()
    
    esperando = True
    while esperando:
        if boton2.value() == 0:
            esp.send(peer, b'1')
        
        host, msg = esp.recv(0)
        if msg and len(msg) == 5:
            try:
                _, _, _, _, new_status = ustruct.unpack('BBBBB', msg)
                if new_status == 0:
                    ultimo_paquete = utime.ticks_ms()
                    esperando = False
            except:
                pass
            
        utime.sleep_ms(50)
    
    print("Reiniciando partida...\n")
    utime.sleep_ms(200)