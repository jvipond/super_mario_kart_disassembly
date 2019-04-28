# super_mario_kart_disassembly
Python script to produce a disassembly of **Super Mario Kart (USA).sfc** from dynamically traced instructions using a modified version of snes9x https://github.com/snes9xgit/snes9x which assembles under `asar` https://github.com/RPGHacker/asar and produces a fully clean ROM.

To reproduce:
1. Clone snes9x https://github.com/snes9xgit/snes9x and apply instruction_trace_snex9x_patch.diff e.g. `git apply instruction_trace_snex9x_patch.diff`. This will apply a small modification to allow snes9x to generate an instruction trace which is used by the disassembler. Build snes9x and play Super Mario Kart. As you are playing the traced instructions will be written to `instruction_trace.txt`.
2. Copy this file to the `super_mario_kart_disassembly` directory and place a copy of the rom (Super Mario Kart (USA).sfc) in the same directory.
3. Run `python main.py` which will generate the disassembly files `bank00.asm, bank01.asm ... bank bank07.asm`.
4. These files can then be assembled with `asar super_mario_kart.asm smk.sfc`.


