# ESP32 Pong Game (ESP-NOW Multiplayer)

This project is a multiplayer Pong game running on two ESP32 microcontrollers. They communicate with each other using the **ESP-NOW** protocol (a low-power, Wi-Fi independent protocol from Espressif). One ESP32 acts as the **Master** (computes game physics) and the other as the **Slave** (displays game state and sends input).

## Hardware Required

You need two identical setups (one for Player 1, one for Player 2):

-   **2x** ESP32 Development Boards (e.g., ESP32 DevKit V1)
-   **2x** OLED SSD1306 Displays (128x64 resolution, I2C interface)
-   **2x** Push Buttons
-   Breadboard and Jumper Wires

## Wiring / Pinout

![alt text](image.png)

you do the same wairing in both esp32 and in the code change de pins where you had put the pins. 


## Installation & Configuration

### Step 1: Install MicroPython
1.  Download and install **Thonny IDE**.
2.  Connect your ESP32 to the PC.
3.  In Thonny, go to **Run -> Configure Interpreter**.
![alt text](image-1.png)
4.  Select `MicroPython (ESP32)` and your COM Port.
![alt text](image-2.png)
5.  Click **Install or Update MicroPython**.
![alt text](image-3.png)
6.  Select the options and click install:
![alt text](image-4.png)

### Step 2: Get MAC Addresses (Crucial!)
ESP-NOW requires knowing the exact MAC address of the *other* device to send data.

1.  Open `get_mac.py` in Thonny.
2.  Run it on **ESP32 #1**. Write down its MAC address (e.g., `68:fe:71:80:74:44`).
3.  Run it on **ESP32 #2**. Write down its MAC address.
4.  Mark which board will be **Player 1 (Master)** and which is **Player 2 (Slave)**.

### Step 3: Configure the Code
You must edit the scripts before uploading them.

**For Player 1 (Master):**
1.  Open `Pong_Master_P1.py`.
2.  Find the line: `peer = b'\x30\xc6\xf7\x21\xed\x7c'` 
3.  Replace the hex codes with the MAC address of **Player 2**.
    *   *Example*: If P2 MAC is `30:c9:22:11:00:ff`, write `b'\x30\xc9\x22\x11\x00\xff'`.

**For Player 2 (Slave):**
1.  Open `Pong_Slave_P2.py`.
2.  Find the line `peer = b'\x68\xfe\x71\x80\x74\x44'` 
3.  Replace with the MAC address of **Player 1** using the same hex format.

### Step 4: Uploading Files

**On ESP32 #1 (Master):**
1.  Open the `ssd1306.py` file in Thonny and save it to the device as `ssd1306.py`.
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)
![alt text](image-8.png)
2.  Open your configured `Pong_Master_P1.py`.
3.  Go to **File -> Save As... -> MicroPython device**.
4.  **Save it as `main.py`**.

**On ESP32 #2 (Slave):**
reapet the exact same proces with the pong_slave_p2.py file

## 🎮 How to Play
1.  Power up both ESP32s (USB or Battery).
2.  The screens should initialize.
4.  Press the button to move UP your paddle. 

#creando el esquema parael desto

I've been doing the readme now it's in a good version but I think I will improve it in the future. Right now the game is functional but before ship it I will improve the game making a counter for the pointa and I'll make a way that the game starts slow and gain speed over time.