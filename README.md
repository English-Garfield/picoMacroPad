# Pico RGB Keypad Macropad

A ready-to-use soft-touch macropad built with the Pimoroni Pico RGB Keypad Base. The Raspberry Pi Pico plugs directly into the base - no wiring or soldering is required

## Specs

- 16-key layout (4x4 grid)
- Per-key RGB lighting with individually addressable APA102 LEDs
- Pico connects directly to base
- USB micro connectivity to Raspberry Pi Pico
- MicroPython firmware with CircuitPython libraries


## Hardware Connections

The Pimoroni Pico RGB Keypad Base handles all connections internally when you plug in the Pico:

**Internal connections (handled automatically):**
- Power: 3.3V and GND from Pico
- Key matrix: Connected to GPIO pins 0-3 and 4-7
- APA102 LEDs: Data and clock lines connected to SPI pins
- All pull-up resistors included on-board

**GPIO Usage:**
```
Pico Pin → Function
GP0-GP3  → Key matrix rows
GP4-GP7  → Key matrix columns  
GP17     → Chip Select (CS)
GP18     → APA102 Data (SPI0 TX)
GP19     → APA102 Clock (SPI0 SCK)
GP5      → I2C SCL
GP4      → I2C SDA
```


### Install MicroPython

This project uses CircuitPython with the following libraries:
- adafruit_bus_device
- adafruit_dotstar
- adafruit_hid
- digitalio


## Assembly Instructions

**It's incredibly simple**

1.**Connect to base**:
   - Simply plug the Pico directly into the keypad base
   - The USB-C port should face outward for easy access
   - Ensure all pins are properly seated

2.**Flash firmware**:
   - Connect USB-C cable to Pico
   - Install CircuitPython
   - Copy code and libraries

3.**Test**:
   - All 16 keys should light up and respond
   - Each key press should register properly

4.**Optional customizations**:
   - Add rubber feet to bottom for stability
   - Create custom key labels
   - Design and print a case if desired

## Default Key Layout

```
┌─────┬─────┬─────┬─────┐
│  0  │  1  │  2  │  3  │
├─────┼─────┼─────┼─────┤
│  4  │  5  │  6  │  7  │
├─────┼─────┼─────┼─────┤
│  8  │  9  │ 10  │ 11  │
├─────┼─────┼─────┼─────┤
│ 12  │ 13  │ 14  │ 15  │
└─────┴─────┴─────┴─────┘
```

### Layer Selection
- **Keys 0-3**: Used to switch between the four different function sets/layers
- Each layer is indicated by pink color on the corresponding key (0-3)

### Layer 0 (Show Software)
- **Key 4**: Ctrl+Shift+S (Open ATEM + OBS) - Purple
- **Key 8**: Ctrl+Shift+A (Open ATEM) - Red
- **Key 12**: Ctrl+Shift+O (Open OBS) - Blue
- **Key 13**: Shift+Command+R (Start recording) - Green
- **Key 14**: Alt+Shift+R (Stop recording) - Red

### Layer 1 (Daily Applications)
- **Key 4**: Shift+Command+F (Open Firefox) - Purple
- **Key 12**: Shift+Command+P (Open PyCharm) - Yellow
- **Key 13**: Shift+Command+T (Open Thonny) - Blue
- **Key 14**: Shift+Command+M (Open Mu editor) - Orange

### Layer 2 (Music Control)
- **Key 4**: Ctrl+Shift+M (Open music) - Purple
- **Key 6**: Ctrl+Shift+F (Next song) - Blue
- **Key 7**: Ctrl+Shift+V (Play music) - Green
- **Key 8**: Alt+Shift+I - Pink
- **Key 9**: Ctrl+Shift+B - Green
- **Key 10**: Alt+Shift+F (Previous song) - Blue
- **Key 11**: Ctrl+Shift+W (Pause music) - Red
- **Key 12**: Ctrl+Shift+Tab - Blue
- **Key 14**: Command+Up Arrow (Volume up) - Red
- **Key 15**: Command+Down Arrow (Volume down) - Green

### Layer 3 (Unassigned)
- Currently unassigned in the code

### RGB Lighting
- Top row keys (0-3) light up pink when selected
- Function keys light up with specific colors based on their function
- Base color for defined keys: Orange (255, 103, 0)
- Keys toggle their LED state when pressed (if configured to latch)

## Customization

The code includes a button_set dictionary that can be modified to customize key functions:
- Each key can send keycodes or text
- Keys can be configured to latch or not
- Custom colors can be assigned to each key
- Random text messages can be configured for meeting endings