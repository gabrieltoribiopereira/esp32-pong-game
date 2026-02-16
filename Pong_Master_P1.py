import espnow
import network
from machine import Pin, I2C, freq
import ssd1306
import utime
import ustruct

# --- TRUCO POWER BANK ---
# Aumentar frecuencia para evitar que la batería se apague por bajo consumo
freq(240000000)

print("\n" + "=" * 50)
print("PONG - JUGADOR 1 (MASTER)")
print("=" * 50)

# Configuración WiFi y ESP-NOW
sta = network.WLAN(network.STA_IF)
sta.active(False)
utime.sleep_ms(100)
sta.active(True)
utime.sleep_ms(100)
sta.disconnect()
utime.sleep_ms(200)

# Configurar canal WiFi
canal_actual = 1
for canal in [1, 6, 11]:
    try:
        sta.config(channel=canal)
        canal_actual = sta.config('channel')
        print("Canal configurado:", canal_actual)
        break
    except:
        pass

esp = espnow.ESPNow()
esp.active(True)

# Verificación de MAC
mi_mac = sta.config('mac')
print("Mi MAC:", ":".join(["%02x" % b for b in mi_mac]))

if mi_mac != b'\x68\xfe\x71\x80\x74\x44':
    print("ERROR: Este codigo es para P1 (68:fe:71:80:74:44)")
    while True:
        utime.sleep(1)

# MAC del Jugador 2 (SLAVE)
peer = b'\x30\xc6\xf7\x21\xed\x7c'
try:
    for p in esp.get_peers():
        esp.del_peer(p[0])
except:
    pass

try:
    esp.add_peer(peer)
    print("Peer añadido OK")
except:
    print("Peer ya existe")

# Configuración Hardware
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=1000000) 
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.fill(0)
display.text("SISTEMA INICIADO", 0, 20, 1)
display.show()
utime.sleep(2)

boton1 = Pin(15, Pin.IN, Pin.PULL_UP)

# Configuración del juego
largo = 15
ancho = 4
boton2_remoto = 1

utime.sleep(3)
print("JUEGO INICIADO!\n")

while True:
    # Reiniciar partida
    y1, y2 = 25.0, 25.0
    bx, by = 64.0, 32.0
    dx, dy = 3.0, 3.0
    ganador = ""
    status = 0 # 0=jugando, 1=gana P1, 2=gana P2

    while True:
        start_time = utime.ticks_ms()

        # Recibir input del Slave
        while True:
            host, msg = esp.recv(0)
            if msg:
                boton2_remoto = 0 if msg == b'1' else 1
            else:
                break

        # Lógica de paletas
        if boton1.value() == 0: y1 -= 3
        else: y1 += 2
            
        if boton2_remoto == 0: y2 -= 3
        else: y2 += 2

        y1 = max(0, min(64 - largo, y1))
        y2 = max(0, min(64 - largo, y2))

        # Física de la pelota
        bx += dx
        by += dy
        
        if by <= 0 or by >= 63:
            dy = -dy
            by = max(0, min(63, by))
            
        if bx <= ancho and y1 <= by <= y1 + largo:
            dx = abs(dx)
            bx = ancho + 1
            
        if bx >= 127 - ancho and y2 <= by <= y2 + largo:
            dx = -abs(dx)
            bx = 127 - ancho - 1
            
        if bx < 0:
            ganador, status = "Player 2", 2
        elif bx > 128:
            ganador, status = "Player 1", 1

        # Enviar estado al Slave
        packet = ustruct.pack('BBBBB', int(bx), int(by), int(y1), int(y2), status)
        esp.send(peer, packet)

        # Dibujar
        display.fill(0)
        display.fill_rect(0, int(y1), ancho, largo, 1)
        display.fill_rect(128 - ancho, int(y2), ancho, largo, 1)
        display.fill_rect(int(bx), int(by), 2, 2, 1)
        display.show()

        if status != 0: break

        # Control de FPS 
        elapsed = utime.ticks_diff(utime.ticks_ms(), start_time)
        if elapsed < 18: utime.sleep_ms(18 - elapsed)

    # Game Over
    display.fill(0)
    display.text("GAME OVER", 30, 20, 1)
    display.text("GANA: " + ganador, 15, 35, 1)
    display.text("PULSA BOTON", 20, 50, 1)
    display.show()
    
    esperando_reinicio = True
    while esperando_reinicio:
        esp.send(peer, packet) # Seguir enviando status de Game Over
        if boton1.value() == 0: esperando_reinicio = False
        host, msg = esp.recv(0)
        if msg == b'1': esperando_reinicio = False
        utime.sleep_ms(50)
    
    utime.sleep_ms(500)
