# ESP32 Pong Game (ESP-NOW Multiplayer)

This project is a multiplayer Pong game running on two ESP32 microcontrollers. They communicate with each other using the **ESP-NOW** protocol (a low-power, Wi-Fi independent protocol from Espressif). One ESP32 acts as the **Master** (computes game physics) and the other as the **Slave** (displays game state and sends input).

## 🛠 Hardware Required

You need two identical setups (one for Player 1, one for Player 2):

-   **2x** ESP32 Development Boards (e.g., ESP32 DevKit V1)
-   **2x** OLED SSD1306 Displays (128x64 resolution, I2C interface)
-   **2x** Push Buttons
-   Breadboard and Jumper Wires

## 🔌 Wiring / Pinout

<img width="748" height="376" alt="image" src="https://github.com/user-attachments/assets/f379f9af-b625-4a51-84af-d841239587a1" />


> **Note**: The code enables the internal `PULL_UP` resistor for the buttons. This means you should connect the button between the GPIO pin and **GND**. No external resistors are needed.

## 🚀 Installation & Configuration

### Step 1: Install MicroPython
1.  Download and install **Thonny IDE**.
2.  Connect your ESP32 to the PC.
3.  In Thonny, go to **Run -> Configure Interpreter**.
4.  Select `MicroPython (ESP32)` and your COM Port.
5.  Click **Install or Update MicroPython**.
6.  Repeat for the second ESP32.

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
2.  Find the line: `peer = b'\x30\xc6\xf7\x21\xed\x7c'` (approx line 49).
3.  Replace the hex codes with the MAC address of **Player 2**.
    *   *Example*: If P2 MAC is `30:c9:22:11:00:ff`, write `b'\x30\xc9\x22\x11\x00\xff'`.
4.  (Optional) Update `mi_mac` check on line 43 if you want to enforce identity.

**For Player 2 (Slave):**
1.  Open `Pong_Slave_P2.py`.
2.  Find the line `peer = b'\x68\xfe\x71\x80\x74\x44'` (approx line 39).
3.  Replace with the MAC address of **Player 1** using the same hex format.

### Step 4: Uploading Files
**Do NOT rename the `.py` files on your computer.** Keep them organized.

**On ESP32 #1 (Master):**
1.  Open the `ssd1306.py` file in Thonny and save it to the device as `ssd1306.py`.
2.  Open your configured `Pong_Master_P1.py`.
3.  Go to **File -> Save As... -> MicroPython device**.
4.  **Save it as `main.py`**. (This runs it automatically on boot).

**On ESP32 #2 (Slave):**
1.  Open the `ssd1306.py` file in Thonny and save it to the device as `ssd1306.py`.
2.  Open your configured `Pong_Slave_P2.py`.
3.  Go to **File -> Save As... -> MicroPython device**.
4.  **Save it as `main.py`**.

## 🎮 How to Play
1.  Power up both ESP32s (USB or Battery).
2.  The screens should initialize.
3.  **Player 1** starts the game.
4.  Press the button to move your paddle (Single button control: Press to go UP/DOWN checks or holding logic depending on code implementation).

