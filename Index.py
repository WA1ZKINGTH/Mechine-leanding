#include <Wire.h>
#ifdef ESP32
#pragma message(THIS EXAMPLE IS FOR ESP8266 ONLY!)
#error Select ESP8266 board.
#endif
#include <Adafruit_GFX.h>
#define i2c_Address 0x3c
#include <SPI.h>
#include <Adafruit_SH110X.h>
#include <ESP8266WiFiMulti.h>
#include <time.h>
#include <Adafruit_INA219.h>
// #include <Adafruit_MLX90614.h>
// #include "Adafruit_SHT31.h"
#include <ArtronShop_SHT45.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <BH1750FVI.h>
#include <Nextion.h>
#include <SoftwareSerial.h>
#include <WiFiManager.h>
#include <Adafruit_ADS1X15.h>
#include "Adafruit_CCS811.h"
/* Uncomment the initialize the I2C address , uncomment only one,
If you get a totally blank screen try the other*/
 
#define i2c_Address 0x3c //initialize with the I2C addr 0x3C Typically eBay OLED's
//#define i2c_Address 0x3d //initialize with the I2C addr 0x3D Typically Adafruit OLED's
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
#define OLED_RESET -1   //  QT-PY / XIAO
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
// Adafruit_MLX90614 mlx = Adafruit_MLX90614(0x6A);
Adafruit_INA219 ina219;
Adafruit_ADS1115 ads;
ArtronShop_SHT45 sht45(&Wire, 0x44);
Adafruit_CCS811 ccs;
// 'image_2022-06-19_112935674', 128x64px
// Can change Image by go to this link https://javl.github.io/image2cpp/
// '284789214_152828010611484_6182985402915567467_n', 128x64px
const unsigned char epd_bitmap_284789214_152828010611484_6182985402915567467_n [] PROGMEM = {
  0x00, 0x00, 0xff, 0xff, 0xff, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x01, 0xff, 0xff, 0xff, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x03, 0xff, 0xff, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x03, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x07, 0xff, 0xff, 0xff, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x07, 0xff, 0xff, 0xff, 0xff, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x0f, 0xff, 0xff, 0xff, 0xff, 0x9d, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xcc, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xc6, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xe3, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x07, 0xff, 0x7e, 0xff, 0xff, 0xe1, 0x82, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x07, 0xff, 0x9f, 0x3f, 0xff, 0xf0, 0x83, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x03, 0xff, 0x47, 0x07, 0x7f, 0xf0, 0x41, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x07, 0xff, 0x80, 0x00, 0x1f, 0xf0, 0x41, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x07, 0xff, 0xf8, 0x00, 0x0f, 0xf8, 0x61, 0x80, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x02, 0xfe, 0xfc, 0x00, 0x0f, 0xf8, 0x20, 0x80, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x03, 0xfe, 0xfc, 0x00, 0x1f, 0xfc, 0x00, 0x80, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x03, 0xff, 0xfc, 0x00, 0x1f, 0xfe, 0x00, 0xc0, 0xff, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x03, 0xff, 0x98, 0x00, 0x1f, 0xbf, 0xff, 0xcf, 0xff, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x01, 0xff, 0xc0, 0x00, 0x00, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xf1, 0xff, 0x80, 0x00, 0x00, 
  0x00, 0x01, 0xff, 0xc0, 0x00, 0x00, 0x1f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xe0, 0xe0, 0x00, 0x00, 
  0x00, 0x01, 0xff, 0xf0, 0x00, 0x00, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x30, 0x00, 0x00, 
  0x00, 0x01, 0xff, 0xf8, 0x00, 0x00, 0x33, 0xf3, 0xff, 0xff, 0xff, 0xff, 0xde, 0x18, 0x00, 0x00, 
  0x00, 0x00, 0xff, 0xff, 0x3c, 0x00, 0x19, 0xb8, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xf8, 0x00, 0x00, 
  0x00, 0x00, 0xff, 0xff, 0xfe, 0x00, 0x08, 0xe6, 0x1f, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 
  0x00, 0x00, 0xef, 0xff, 0xfc, 0x00, 0x00, 0x61, 0x8f, 0x8f, 0xff, 0xff, 0xdf, 0xff, 0xe0, 0x00, 
  0x00, 0x00, 0x67, 0xff, 0xfc, 0x00, 0x00, 0x18, 0x0f, 0xfc, 0x00, 0xff, 0xc0, 0xff, 0x00, 0x00, 
  0x00, 0x00, 0x52, 0x7f, 0xf8, 0x00, 0x00, 0x0c, 0x04, 0x00, 0x00, 0x5f, 0xf0, 0x3f, 0x80, 0x00, 
  0x00, 0x00, 0x09, 0x1f, 0xfe, 0x00, 0x00, 0x03, 0x07, 0x80, 0x00, 0xff, 0xfc, 0x1d, 0xc0, 0x00, 
  0x00, 0x00, 0x08, 0x8f, 0xff, 0xc0, 0x00, 0x01, 0x87, 0xc0, 0x03, 0xe0, 0x7e, 0x0c, 0xe0, 0x00, 
  0x00, 0x00, 0x04, 0x43, 0xff, 0xe0, 0x00, 0x00, 0x67, 0xd8, 0x0e, 0x00, 0x1f, 0x0c, 0x70, 0x00, 
  0x00, 0x00, 0x02, 0x37, 0xff, 0xf0, 0x00, 0x00, 0x0f, 0xdc, 0x70, 0x00, 0x1f, 0x1a, 0x38, 0x00, 
  0x00, 0x00, 0x11, 0x0e, 0x1f, 0xfe, 0x00, 0x01, 0x07, 0xff, 0x80, 0x00, 0x07, 0x92, 0x1c, 0x00, 
  0x00, 0x00, 0x08, 0x80, 0x07, 0xf8, 0x00, 0x01, 0x87, 0xbf, 0x00, 0x00, 0x03, 0xa0, 0x1e, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x07, 0xfc, 0x20, 0x00, 0xc7, 0x7f, 0x80, 0x00, 0x03, 0xe0, 0x0f, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x03, 0xfc, 0x18, 0x00, 0xc6, 0x7f, 0xc0, 0x00, 0x01, 0xc0, 0x0f, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x01, 0xfc, 0x0c, 0x00, 0x66, 0xfc, 0x00, 0x00, 0x01, 0xc0, 0x0f, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0xfe, 0x07, 0x00, 0x04, 0xf0, 0x00, 0x00, 0x01, 0x80, 0x07, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0xfe, 0x03, 0x80, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x80, 0x06, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0xfe, 0x01, 0x80, 0x00, 0x80, 0x00, 0x00, 0x00, 0x80, 0x06, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x04, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x80, 0x00, 0x00, 0x00, 0x0f, 0xf8, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0x80, 0x00, 0x00, 0x00, 0xff, 0xfc, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0xfd, 0xc0, 0x00, 0x00, 0x13, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x01, 0xfc, 0xe0, 0x00, 0x00, 0x1f, 0xff, 0xff, 0xc0, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x01, 0xfc, 0x70, 0x00, 0x00, 0x1f, 0xff, 0xff, 0xf8, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x02, 0xf8, 0x1f, 0xfc, 0x00, 0x1f, 0xff, 0xff, 0xf8, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x01, 0xfe, 0x7f, 0xff, 0x00, 0x1f, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x01, 0xff, 0xfe, 0x7f, 0xc0, 0x1f, 0xff, 0xff, 0xff, 0xf0, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x01, 0xff, 0xfb, 0xff, 0xe0, 0x0f, 0xff, 0xff, 0xff, 0xfe, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0xf3, 0xcf, 0xff, 0xf0, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x03, 0xf1, 0x3f, 0xff, 0xf0, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xc0, 
  0x00, 0x00, 0x00, 0x00, 0x07, 0xf8, 0x7f, 0xff, 0xf8, 0x1f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xe0, 
  0x00, 0x00, 0x00, 0x00, 0x07, 0xf8, 0x3f, 0xff, 0xfc, 0x7f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 
  0x00, 0x00, 0x00, 0x00, 0x0f, 0xf8, 0x3f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 
  0x00, 0x00, 0x00, 0x00, 0x0f, 0xfc, 0x1f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 
  0x00, 0x00, 0x00, 0x00, 0x1f, 0xff, 0x0f, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xf0, 
  0x00, 0x00, 0x00, 0x00, 0x1f, 0xde, 0x07, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xe0, 
  0x00, 0x00, 0x00, 0x00, 0x3f, 0xf7, 0x03, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x83, 
  0x00, 0x00, 0x00, 0x00, 0x7f, 0xc1, 0x83, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfe, 0x01, 
  0x00, 0x00, 0x00, 0x00, 0xff, 0xc0, 0x01, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xfc, 0x01
};
// 'image_2022-08-07_222028191', 128x64px
const unsigned char epd_bitmap_image_2022_08_07_222028191 [] PROGMEM = {
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x03, 0xc0, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x7f, 0xff, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x03, 0xff, 0xff, 0xc0, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x0f, 0xf0, 0x0f, 0xf0, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x03, 0x00, 0x1f, 0x80, 0x00, 0xfc, 0xe0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x01, 0x8e, 0x3c, 0x00, 0x00, 0x1e, 0x70, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x01, 0xce, 0x38, 0x00, 0x00, 0x0e, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xff, 0x00, 0x00, 0x00, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x79, 0x00, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x30, 0x00, 0x00, 0x00, 0x00, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x08, 0x00, 0x03, 0xe0, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x0e, 0x00, 0x1f, 0xf8, 0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x1c, 0x00, 0x3f, 0x7e, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x38, 0x00, 0x78, 0x0f, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x38, 0x00, 0xe0, 0x03, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x70, 0x00, 0xc0, 0x01, 0x80, 0x0e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x70, 0x01, 0xc0, 0x01, 0x80, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x70, 0x01, 0x87, 0xf0, 0xc0, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xe0, 0x01, 0x87, 0xf0, 0xc0, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xe0, 0x01, 0x87, 0x70, 0xc0, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xe0, 0x01, 0x86, 0x30, 0xc0, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xe0, 0x01, 0x82, 0x60, 0xc0, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xc0, 0x01, 0xc3, 0x61, 0xc0, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xc0, 0x00, 0xc3, 0x61, 0x80, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xc0, 0x00, 0xe0, 0x03, 0x80, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xc0, 0x00, 0x70, 0x07, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xc0, 0x00, 0x30, 0x0e, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xc0, 0x00, 0x18, 0x0e, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xc0, 0x00, 0x18, 0x0c, 0x00, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xe0, 0x00, 0x0c, 0x1c, 0x00, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xe0, 0x00, 0x0c, 0x18, 0x00, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0xe0, 0x00, 0x0c, 0x18, 0x00, 0x03, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x60, 0x00, 0x1e, 0x38, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x70, 0x00, 0x0f, 0xf8, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x70, 0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x38, 0x00, 0x0f, 0xf8, 0x00, 0x0e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x1c, 0x00, 0x07, 0xf8, 0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x1c, 0x00, 0x00, 0x00, 0x00, 0x3c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x0c, 0x00, 0x0f, 0xf0, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x0f, 0xf8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x07, 0x00, 0x00, 0x00, 0x00, 0xcf, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x0e, 0x20, 0x00, 0x00, 0x04, 0x7f, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x0e, 0x78, 0x00, 0x00, 0x0e, 0x39, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x07, 0x3e, 0x00, 0x00, 0x3e, 0x30, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x03, 0x9f, 0x80, 0x01, 0xfc, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x07, 0x07, 0xfc, 0x1f, 0xf0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x0f, 0x01, 0xff, 0xff, 0xc0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x1c, 0x00, 0x3f, 0xfe, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x38, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};
// ----------------------------------------BLYNK CODE for WIfi-------------------------------------------------//
#define BLYNK_PRINT Serial
/* Fill-in your Template ID (only if using Blynk.Cloud) */
#define BLYNK_TEMPLATE_ID "TMPLupX37pt2"
#define BLYNK_DEVICE_NAME "Quickstart Template"
#define BLYNK_AUTH_TOKEN "gB7TZoc-D-ceRgqqudVdN5aBK-1S9URQ"
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
// You should get Auth Token in the Blynk App.
// Go to the Project Settings (nut icon).
char auth[] = "gB7TZoc-D-ceRgqqudVdN5aBK-1S9URQ";
// Your WiFi credentials.
// Set password to "" for open networks.
// char ssid[] = "pu_kgs";
// char pass[] = "0960698678";
int p1 = 0;
int threeshore;
int lightLIM;
int lightState;
#define relay1 D0
#define relay2 D8
#define relay3 D5
#define relay4 D6
#define relay5 D7
int relayinteger1 = 0;
int StateFan;
int auto_state;
int resetRelay;
BLYNK_WRITE(V1){  
    if (param.asInt())
    { 
        digitalWrite(relay4, HIGH); 
    } 
    else 
    {
        digitalWrite(relay4, LOW);  
    }
}
BLYNK_WRITE(V5)
{
  int val = param.asInt();
  p1++;
}
BLYNK_WRITE(V6){  
  if (param.asInt())
    { 
        digitalWrite(relay2, HIGH); 
        lightState++;
    } 
    else 
    {
        digitalWrite(relay2, LOW);  
        lightState = 0;
    }
}

BLYNK_WRITE(V13){ 
  if (param.asInt())
    { 
        digitalWrite(relay3, HIGH); 
    } 
    else 
    {
        digitalWrite(relay3, LOW);  
    }
    // for external relay
    // if (param.asInt())
    // { 
    //     digitalWrite(relay1, HIGH); 
    // } 
    // else 
    // {
    //     digitalWrite(relay1, LOW);  
    // }
}
BLYNK_WRITE(V17){  
  if (param.asInt())
    { 
        digitalWrite(relay5, HIGH);
        StateFan++;
    } 
    else 
    {
        StateFan = 0;
        digitalWrite(relay5, LOW);  
    }
}
BLYNK_WRITE(V20){
  threeshore = param.asInt();
}
BLYNK_WRITE(V21){
  lightLIM = param.asInt();
}
BLYNK_WRITE(V22){
      if (param.asInt() == 1)
    { 
        auto_state = 1;
    } 
      if (param.asInt() == 0)
    {
        auto_state = 0;
 
    }
}
BLYNK_WRITE(V24){
  if(param.asInt()){
     resetRelay = 1;
  }
  else
  {
    resetRelay = 0;
  }
    
}
//--------------------------------voltage and Ampair watt--------------------------------------------//
int value1;
int value2;
int value3;
const int SWITCH_ON = 1;
const int SWITCH_OFF = 0;
byte received_data[4];
int  switch_pos;
float shuntvoltage = 0;
float busvoltage = 0;
float current_mA = 0;
float power_mW = 0;
float loadvoltage = 0;
// int sensitive = 100; // สำหรับ 20A
int sensitive = 66; // สำหรับ 30A
// int sensitive = 185; // สำหรับ 5A
int offset = 3810; // ค่าเริ่มต้น 2500 ปรับค่าตรงนี้เพื่อให้ค่ายังไม่มีโหลดเป็น 0.00
 
//Muli WIFI 
ESP8266WiFiMulti wifiMulti;
// #define YOUR_SSID "pu_kgs"
// #define YOUR_PASS "0960698678"

// Config time
int timezone = 7;       // Zone +7 for Thailand
char ntp_server1[20] = "ntp.ku.ac.th";
char ntp_server2[20] = "fw.eng.ku.ac.th";
char ntp_server3[20] = "time.uni.net.th";
int dst = 0;
int  Sec = 0;
String tmpNow = tmpNow;

String NowString() {
  time_t now = time(nullptr);
  struct tm* newtime = localtime(&now);

  String tmpNow = "";
  tmpNow += String(newtime->tm_year + 1900);
  tmpNow += "-";
  tmpNow += String(newtime->tm_mon + 1);
  tmpNow += "-";
  tmpNow += String(newtime->tm_mday);
  tmpNow += " ";
  tmpNow += String(newtime->tm_hour);
  tmpNow += ":";
  tmpNow += String(newtime->tm_min);
  tmpNow += ":";
  tmpNow += String(newtime->tm_sec);
  Sec = newtime->tm_sec;
  return tmpNow;

}
/////// HTTP code /////////
WiFiClient wifiClient;
HTTPClient http;
int val = 0;
int analogPin = A0;
BH1750FVI LightSensor(BH1750FVI::k_DevModeContLowRes);

SoftwareSerial nextion(1, 3);// Nextion TX to pin 2 and RX to pin 3 of Arduino
Nextion myNextion(nextion, 9600); //create a Nextion object named myNextion using the nextion serial port @ 9600bps
/////////////////////////////////////


void displayTIME()
{
  display.invertDisplay(false);
  display.clearDisplay();
  delay(400);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(4, 21);
  display.setTextSize(2);
  display.print("Time in TH");
  display.setTextSize(1);
  display.setCursor(4, 41);
  display.print(NowString());
  display.display();
  
}
void displayVoltage(){
  shuntvoltage = ina219.getShuntVoltage_mV();
  busvoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getPower_mW();
  loadvoltage = busvoltage + (shuntvoltage / 1000);
  if(current_mA < 0){
    current_mA = 0;
  }
  if(busvoltage < 1){
    busvoltage = 0;
  }
  display.clearDisplay();
  display.drawBitmap(0, 0, epd_bitmap_image_2022_08_07_222028191, 128, 64, SH110X_WHITE);
  display.setTextColor(SH110X_WHITE);
  display.setCursor(66, 20);
  display.print(loadvoltage);
  display.print(" V");
  display.setCursor(66, 30);
  display.print(current_mA);
  display.print(" mA");
  display.setCursor(66, 40);
  int powerOled = power_mW/1000;
  display.print(powerOled);
  display.print(" W");
  display.display();
}
///// ตั้งค่า IFTTT
String event = "TGorgeorius"; // ชื่อ event
String key = "R3A6wHgSp7McWiqkKUQIk"; // Key
String sheets = "Urloopter";

String server = "http://maker.ifttt.com";
String eventName = "TGorgeorius";
String IFTTT_Key = "R3A6wHgSp7McWiqkKUQIk";
String IFTTTUrl="http://maker.ifttt.com/trigger/temp_data/with/key/R3A6wHgSp7McWiqkKUQIk";
void setup()
{
  ads.begin(0x48);
  sht45.begin();
  myNextion.init();
  LightSensor.begin();
  ccs.begin(0x5A);
  WiFiManager wifiManager;
  wifiManager.autoConnect ("Esp8266");
  Serial.begin(9600);
  // mlx.begin();
  ina219.begin();
  display.begin(i2c_Address, true);
  display.display();
  // pinMode(D2, INPUT_PULLUP);
  pinMode(relay1, OUTPUT); 
  pinMode(relay2 , OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);
  pinMode(relay5, OUTPUT); 
  Blynk.config(auth);
  display.display();
  delay(1500);

    // The ADC input range (or gain) can be changed via the following
  // functions, but be careful never to exceed VDD +0.3V max, or to
  // exceed the upper and lower limits if you adjust the input range!
  // Setting these values incorrectly may destroy your ADC!
  //                                                                ADS1015  ADS1115
  //                                                                -------  -------
  //  ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
  ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV

  // Clear the buffer.
  display.clearDisplay();
  wifiMulti.addAP("Year2020", "1235th");
  wifiMulti.addAP("AndroidAP", "ifmd0883");
  // wifiMulti.addAP(YOUR_SSID, YOUR_PASS);
  Serial.begin(9600);
  Serial.println();
  String thisBoard= ARDUINO_BOARD;
  Serial.println(thisBoard);
  display.drawBitmap(0, 0, epd_bitmap_284789214_152828010611484_6182985402915567467_n, 128, 64, SH110X_WHITE);
  display.display();
  delay(3000);
  // Autodetect is not working reliable, don't use the following line
  // dht.setup(17);
  // use this instead: 
  configTime(timezone * 3600, dst, ntp_server1, ntp_server2, ntp_server3);
  while (!time(nullptr)) {
    Serial.print(".");
  }
  sheets = "http://maker.ifttt.com/trigger/MetaGenius/with/key/R3A6wHgSp7McWiqkKUQIk";
}
 

void loop()
{
  String url = server + "/trigger/" + eventName + "/with/key/" + IFTTT_Key + "?value1=" + String((int)value1) + "&value2="+String((int)value2) +"&value3=" + String((int)value3);
  display.clearDisplay();
  display.invertDisplay(true);
  delay(2000);
  display.invertDisplay(false);
  delay(1000);
 for (int i = 0; i <= 100; i++){ 
    display.clearDisplay();
    display.drawRoundRect(12, 30, 104, 8, 10 , SH110X_WHITE);
    display.fillRoundRect(14, 32, i, 4,10, SH110X_WHITE);
    display.setTextSize(1);
    display.setTextColor(SH110X_WHITE);
    display.setCursor(30, 50);
    display.print("Loading ");
    display.print(i);
    display.print("%");
    //Un-comment below line for invert the display.
    //display.invertDisplay(true);
    delay(100);
    display.display();
 while(i == 100){
    String url = server + "/trigger/" + eventName + "/with/key/" + IFTTT_Key + "?value1=" + String((int)value1) + "&value2="+String((int)value2) +"&value3=" + String((int)value3);
    Blynk.run();
    delay(600);
    sht45.measure();
     ccs.available();
    ccs.readData();
    shuntvoltage = ina219.getShuntVoltage_mV();
    busvoltage = ina219.getBusVoltage_V();
    current_mA = ina219.getCurrent_mA();
    power_mW = ina219.getPower_mW();
    value1 = sht45.humidity();
    value2 = sht45.temperature();
    value3 = map(val, 1024, 0, 0, 100);
    int CO2_ppm = ccs.geteCO2();
     float sensorValueVoltage_CH0 = (float)ads.readADC_SingleEnded(0)*5000/32768;
     float sensorValueVoltage_CH2 = (float)ads.readADC_SingleEnded(2)*5000/32768;
     float sensorValueVoltage_CH3 = (float)ads.readADC_SingleEnded(3)*5000/32768;
      // อ่านค่าอนาล๊อคจากANALOG_PIN และแปลงค่าที่อ่านได้เป็นแรงดันไฟฟ้า
      int highV = 3090;
      int LowV = 2090;
      float moisturelevel2 = map(sensorValueVoltage_CH0, highV, LowV, 0 ,100);
      float moisturelevel3 = map(sensorValueVoltage_CH2, highV, LowV, 0 ,100);
      float moisturelevel4 = map(sensorValueVoltage_CH3, highV, LowV, 0 ,100);
      
     int16_t adc0, adc1, adc2, adc3;
    adc0 = ads.readADC_SingleEnded(0);
    adc1 = ads.readADC_SingleEnded(1);
    int moisST =  map(adc1, 32768, 0, 0, 100); 
    loadvoltage = busvoltage + (shuntvoltage / 1000);
    int power2 = power_mW/1000;
    int Amp = power_mW/current_mA;
    Blynk.virtualWrite(V7, loadvoltage);
    Blynk.virtualWrite(V8, current_mA);
    Blynk.virtualWrite(V9, power2);
    Blynk.virtualWrite(V10, current_mA);
    // Blynk.virtualWrite(V11, ambTemp);
    // Blynk.virtualWrite(V12, ObjTemp);
    Blynk.virtualWrite(V18, moisturelevel3);
    Blynk.virtualWrite(V19, moisturelevel4);

    if (auto_state == 1){
       
      if(StateFan != 1){
          if (sht45.temperature() > threeshore){
              digitalWrite(relay5,1);
               } 
          if(sht45.temperature() <= threeshore){
              digitalWrite(relay5,0);
               }
      }
      if(lightState != 1){
          if (LightSensor.GetLightIntensity() > lightLIM){
              digitalWrite(relay2,0);
              } 
          if(LightSensor.GetLightIntensity() <= lightLIM){
              digitalWrite(relay2,1);
              }
      }
    }
    if (auto_state == 0){
        if (resetRelay == 1){
           reset_Relay();
        }
    }

    
    ////////// Trans. data to nextion
    
    ////// time
    Serial.print("t1.txt=");
    Serial.print("\"");
    Serial.print(NowString());
    Serial.print("\"");
    Serial.write(0xff);
    Serial.write(0xff);
    Serial.write(0xff);

    ///////Temperature
  int T = sht45.temperature();
  int G1 = map(T, 0, 100, 0,200 ); 
  Serial.print("n0.val=");
  Serial.print(T);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);

  Serial.print("z0.val=");
  Serial.print(G1);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
  ////////HUMID
  int H = sht45.humidity();
  int G2 = map(H, 0, 100, 0,200 ); 
  Serial.print("n1.val=");
  Serial.print(H);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);

  Serial.print("z1.val=");
  Serial.print(G2);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
 ////////LIGHT INTENSITY
  uint16_t lux = LightSensor.GetLightIntensity();
  int Light = lux;
  int Light1 = map(Light,0,32767,0,200);
  Serial.print("n4.val=");
  Serial.print(Light);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);

  Serial.print("z4.val=");
  Serial.print(Light1);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
//////////// Soil Moisure
  val = analogRead(analogPin); 
  int percen = map(val, 1024, 0, 0, 100); 
  float AVRsoilarea = (moisturelevel2 + moisturelevel3 + moisturelevel4 + moisST + percen)/5;
  Serial.print("n3.val=");
  Serial.print(AVRsoilarea);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);


  int percen1 = map(AVRsoilarea,0,100,0,200);
  Serial.print("z3.val=");
  Serial.print(percen1);
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);

///////HTTP to google data sheets
  http.begin(wifiClient,url); //กำหนด url เพื่อเซฟข้อมูลลง google sheets
  int httpCode = http.GET();
  if (httpCode > 0) { //ถ้าส่งสำเร็จ

      String payload = http.getString();// อ่านค่าผลลัพธ์
      
    }
    http.end(); //ปิดการเชื่อมต่อ
    Blynk.virtualWrite(V0, T);
    Blynk.virtualWrite(V2, H);
    Blynk.virtualWrite(V3, percen);
    Blynk.virtualWrite(V4, lux);
    Blynk.virtualWrite(V15, moisturelevel2);
    Blynk.virtualWrite(V16, moisST);
    Blynk.virtualWrite(V14, CO2_ppm);
    Blynk.virtualWrite(V23, AVRsoilarea);
    if(loadvoltage > 16){
      Blynk.logEvent("high_volt");
    }
    if(p1 > 1){
      p1 = 0;
    }
    if(p1 == 1){
      displayVoltage();
    }
    else{
      displayTIME();
    }
    while (Serial.available() > 0) {
      switch_control();
  }
   } 
    }
}
void switch_control() {
    int size = Serial.readBytesUntil('\n', received_data, 4);
    // First Byte has the switch position data 
    switch_pos = received_data[0];
    if (switch_pos == SWITCH_ON) {
      digitalWrite(relay4, HIGH);
    } else if (switch_pos == SWITCH_OFF) {
      digitalWrite(relay4, LOW);
    }
}
void reset_Relay(){
  digitalWrite(relay2,LOW);
  digitalWrite(relay3,LOW);
  digitalWrite(relay4,LOW);
  digitalWrite(relay5,LOW);
}
