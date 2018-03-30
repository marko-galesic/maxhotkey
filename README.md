# maxhotkey
Indefinitely: If you can get this to run, you get:

Generate macro scripts + macro -> hotkey binding file - all based off a config (config.json), generate keyboard image with the macros shown on the appropriate keys

You will probably need to change a few of the constants I've defined in the program, unless your Windows user directory is also called 'CONRAD II'.

If you use a key that's not used, yet, and you want to have your macro appear on the keyboard-layout.png, you'll need to add that key to the [locations] section in keys.cfg. You'll likely need to experiment with placement. Those locations are the initial starting point. Spacing is based off the size of the font (no clever coding, just a magic/constant number I've put into the code).

My workflow is:
1. Figure out what I want in a macro script (look at the Maxscript listener, for example)
2. Take whatever lines of Maxscript are doing the thing I want
3. Create a new file in the "macros" directory
4. Run the program
5. Profit! (and reload hotkeys/bindings)
