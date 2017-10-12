What the heck does this do?
	This is a question I often ask myself of programs I have downloaded in a
	frenzy and forgotten about.  And one that the Help, annoyingly, never answers.
	
	Jagent is a suite of tools for working with Creatures Series files.
	If you don't know what Creatures 3 or Docking Station are, then these
	tools will be of no use to you whatsoever.
	
	+ Edos is an Editor of Sprites.
		+ It works mostly like the old SpriteBuilder
	
	+ Monk deals with PRAY files.
		+ Choose the output format with the radio buttons, then drop an input file on it





Jagent is created by RProgrammer (rprogrammer@gmail.com)
Icons and other graphics are painted by Embri (embritheunisus@hotmail.com)
Edos "About" page is written by Shane Kelly, aka Skelly (blameshane@gmail.com)
Malkin (malkin86@gmail.com) assisted with beta testing and promotion.


Jagent is distributed under a BSD License:

Copyright (c) 2013, RProgrammer (rprogrammer@gmail.com)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    * Neither the name of the copyright holder, nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



















Release notes:
---2.0.1---
b	+ Fixed a PRAY bug that caused multiple agents in a PRAY file to overwrite each other on decompile
		+ Credit for discovery goes to Malkin
	
f	+ Made PRAY decompilation of a single script for an agent not end in "_1".

b	+ Linux Drag 'n Drop of multiple files works now
		+ Credit: Papriko

f	+ Added support for quoted C2P command arguments (eg, you can put spaces in your agent's name now; just put "" around it)

f	+ Sanitized the CAOS2PRAY subsystem

b	+ Edos menu sometimes disappeared in Mac OS X, 64 bit Leopard
		+ Credit: Malkin

b	+ rscr scanning in CAOS2PRAY didn't work at all

--2.0.2--
b	+ Fixed a PRAY bug that caused slightly-malformed PRAY files to be catostrophically unreadable
		+ Note: It seems that some of the CL Breed egg files have this glitch.
		+ Credit: Papriko

--2.0.3--
b	+ Fixed a bug that prevented Monk from decompiling when used on the command-line

b	+ Jagent now handles the possibility of the PRAY entries used for filenames containing characters that are illegal in a file name (eg, '/' unix, '\' ':' windows, ':' classic macos, etc.)
		+ The behavior on decompile is to replace the illegal characters as best it can
		+ The behavior on compile is to not allow characters that would pose a problem for other platforms; PRAY files should be platform-independent

f	+ I added my CAOS lexer I made while learning JFlex for no particular reason (note that CAOS2PRAY uses a different, more primitive lexer)

--2.0.4--
f	+ Added support for arbitrary PRAY block ids in CAOS2PRAY to support Amaikokonut's Garden Box (DSGB) agent injection system

f	+ Added fast-fail feature to C16, S16, BLK reading libraries to fail immediately attempting to read the wrong format (can't distinguish between S16 and BLK currently, though)

f	+ Added support (enabled by default) for reading colors as transparent in S16's

f	+ Added primitive command line interface to Edos (EdosTool.jar)

b	+ Files weren't closed if an error was thrown during reading (including format mismatch / parse error) leading to program crash or inability to open new files once too many open files had accumulated

--2.0.5--
f	+ Added option for disabling or enabling (default) the merge-scripts feature on PRAY compilation at Papriko's request and for The Norn Garden (historically, Jagent has always merged all the scripts into one "Script 1" for compatibility reasons, which can break upon injection if files other than the last contain an "rscr")

f	+ Made sprite writing more robust; now checks to insure written images are not larger than maximum dimensions

f	+ Added GUI support for controlling the Jagent transparency-emulation option in writing C16's to emulate the engine in considering black as transparent; note: only works on images without actual alpha channels and only pure/exactly black (#000000) is considered transparent

b	+ Fixed two horrible bugs involving the CAOS2PRAY C3-Name directive

b	+ Changed the Jagent build system to use an intelligent dependency scanner instead of manual includes; the .jar files will have slightly different contents now

f	+ Added support for decompiling Garden Box agents!

b	+ Fixed command-line Monk to actually output the .txt pray template file (heh sry!)
