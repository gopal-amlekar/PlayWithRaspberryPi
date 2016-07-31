
/* This code demonstrates basic usage of wiringPi library */
/* It is the most basic LED blinking code (0.5 sec duty cycle) */
/* An LED is connected to pin 11 (GPIO 17) and ground */

/* To compile -  gcc -Wall -o ledBlink1 ledBlink-1.c -lwiringPi */
/* Needs sudo to run. So use sudo ./ledBlink1 */

#include <wiringPi.h>

int main(void)
{
    wiringPiSetup();		/* Initialize  the library */

    pinMode(17, OUTPUT);	/* Set GPIO17 as output */

    while (1)
    {
    	digitalWrite(0, HIGH);	/* Switch on the LED */
	delay (500);

	digitalWrite(0, LOW);  /* Switch off the LED */
	delay (500);
    }

    return 0;
}
