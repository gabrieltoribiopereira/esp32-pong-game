# ESP32 Pong Game (ESP-NOW Multiplayer)

This project is a multiplayer Pong game running on two ESP32 microcontrollers. They communicate with each other using the **ESP-NOW** protocol. One ESP32 acts as the **Master** (computes game physics) and the other as the **Slave** (displays game state and sends input).

## Hardware Required

You need two identical setups (one for Player 1, one for Player 2):

-   **2x** ESP32 Development Boards
-   **2x** OLED SSD1306 Displays 
-   **2x** Push Buttons
-   Breadboard and Jumper Wires

## Wiring / Pinout

<img width="748" height="376" alt="Captura desde 2026-01-27 10-00-29" src="https://github.com/user-attachments/assets/fb908a69-9171-4af0-899f-05be110b250d" />


you do the same wairing in both esp32 and in the code change de pins where you had put the pins. 


## Installation & Configuration

### Step 1: Install MicroPython
1.  Download and install **Thonny IDE**.
2.  Connect your ESP32 to the PC.
3.  In Thonny, go to **Run -> Configure Interpreter**.
   
<img width="505" height="560" alt="Captura desde 2026-01-27 15-39-02" src="https://github.com/user-attachments/assets/d3866b53-19bc-4142-98b6-cc02a6f9f8a2" />

4.  Select `MicroPython (ESP32)` and your COM Port.
 
<img width="676" height="556" alt="Captura desde 2026-01-27 15-39-27" src="https://github.com/user-attachments/assets/23c1f105-1e2a-4d51-a192-06a5c24538f6" />

5.  Click **Install or Update MicroPython**.

<img width="676" height="556" alt="Captura desde 2026-01-27 15-39-52" src="https://github.com/user-attachments/assets/81a2bbc9-4c38-42ab-9439-e890fc8b60e2" />

6.  Select the options and click install:
   
<img width="676" height="556" alt="Captura desde 2026-01-27 15-40-34" src="https://github.com/user-attachments/assets/efbbe17e-9e26-4caa-ba76-49a14154c33e" />


### Step 2: Get MAC Addresses
ESP-NOW requires knowing the exact MAC address of the *other* device to send data.

1.  Open `get_mac.py` in Thonny.
2.  Run it on **ESP32 #1**. Write down its MAC address (e.g., `68:fe:71:80:74:44`).
3.  Run it on **ESP32 #2**. Write down its MAC address.

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
   
   1.1.
      <img width="417" height="346" alt="Captura desde 2026-01-27 15-44-00" src="https://github.com/user-attachments/assets/eae31770-f1ea-48cd-b44c-1763d4e7aea0" />

   1.2.
      <img width="529" height="538" alt="Captura desde 2026-01-27 15-47-45" src="https://github.com/user-attachments/assets/fa5a0678-7da8-4990-85c4-9c76b79d1ce6" />

   1.3.
      <img width="589" height="439" alt="Captura desde 2026-01-27 15-48-10" src="https://github.com/user-attachments/assets/5de0a31c-6722-40f7-9e4f-ded1dcf3ae10" />

   1.4.
      <img width="219" height="127" alt="Captura desde 2026-01-27 15-48-26" src="https://github.com/user-attachments/assets/58a81e4b-f231-417f-85c4-dfe0c1ba49ed" />


2.  Open your configured `Pong_Master_P1.py`.
3.  Go to **File -> Save As... -> MicroPython device**.
4.  **Save it as `main.py`**.
(It's the same proces as the last one but with the actual code)

**On ESP32 #2 (Slave):**
reapet the exact same proces with the pong_slave_p2.py file

## 🎮 How to Play
1.  Power up both ESP32s (USB or Battery).
2.  The screens should initialize.
4.  Press the button to move UP your paddle. 







