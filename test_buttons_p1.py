import espnow
import network 
from machine import Pin, I2C
import ssd1306
import utime

print("\n" + "=" * 50)
print("TEST BOTONES - JUGADOR 1 (MASTER)")
print("=" * 50)

# Configuración WiFi
sta = network.WLAN(network.STA_IF)
sta.active(False)
utime.sleep_ms(100)
sta.active(True)
utime.sleep_ms(100)
sta.disconnect()
utime.sleep_ms(200)

# Configurar canal robusto
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

# MACs
mi_mac = sta.config('mac')
peer = b'\x68\xfe\x71\x80\x74\x44' # MAC de P2

print("Mi MAC:", ":".join(["%02x" % b for b in mi_mac]))
print("Enviando a P2:", ":".join(["%02x" % b for b in peer]))

# Añadir peer
try:
    esp.add_peer(peer)
    print("Peer P2 añadido OK")
except:
    print("Peer P2 ya existe")

# Configuración Hardware
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
boton_local = Pin(15, Pin.IN, Pin.PULL_UP)

estado_remoto = "SUELTO"
ultimo_envio = 0
paquetes_recibidos = 0

while True:
    current_time = utime.ticks_ms()
    
    # Leer botón local
    es_presionado = boton_local.value() == 0
    estado_local = "PRESIONADO" if es_presionado else "SUELTO"
    
    # Enviar mi estado cada 50ms
    if utime.ticks_diff(current_time, ultimo_envio) > 50:
        msg = b'1' if es_presionado else b'0'
        try:
            if esp.send(peer, msg):
                pass
            else:
                print("Error enviando a P2")
        except Exception as e:
            print("Error ESP-NOW:", e)
        ultimo_envio = current_time

    # Recibir estado remoto
    while True:
        host, msg = esp.recv(0)
        if msg:
            paquetes_recibidos += 1
            if msg == b'1':
                estado_remoto = "PRESIONADO"
            elif msg == b'0':
                estado_remoto = "SUELTO"
        else:
            break

    # Actualizar pantalla
    display.fill(0)
    display.text("TEST BOTONES P1", 5, 0, 1)
    display.text("Canal: " + str(canal_actual), 5, 10, 1)
    display.text("L: " + estado_local, 5, 25, 1)
    display.text("R: " + estado_remoto, 5, 40, 1)
    display.text("PKTS RCV: " + str(paquetes_recibidos), 5, 55, 1)
    
    # Cuadrado Local
    if es_presionado:
        for i in range(15):
            for j in range(15):
                display.pixel(105 + i, 22 + j, 1)
    
    # Cuadrado Remoto
    if estado_remoto == "PRESIONADO":
        for i in range(15):
            for j in range(15):
                display.pixel(105 + i, 37 + j, 1)
        
    display.show()
    utime.sleep_ms(20)
