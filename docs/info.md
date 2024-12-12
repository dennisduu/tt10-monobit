<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The monobit test in this setup checks if a stream of 128 bits (1s and 0s) is "random" by comparing the counts of 1s and 0s. A bit is fed into the design one at a time (serially) through an input signal (ui_in). The design keeps track of how many 1s and 0s it has seen so far and calculates the absolute difference between the two counts. If the difference is less than or equal to 29, the output is_random is set to 1 (indicating randomness); otherwise, it is set to 0 (not random). This test ensures the design behaves correctly by generating various 128-bit patterns, running them through the design, and verifying that the output matches the expected result.

## How to test

Input 128 binary bitstream and this device will output the result. 

## External hardware

na
