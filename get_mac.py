import network
import utime

sta = network.WLAN(network.STA_IF)
sta.active(True)
mac = sta.config('mac')
print("\n" + "="*30)
print("TU DIRECCION MAC ES:")
print(":".join(["%02x" % b for b in mac]))
print("="*30 + "\n")

# Mantener activo para que se pueda leer en Thonny
while True:
    utime.sleep(1)
