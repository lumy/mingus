#!/usr/bin/env python
"""

*** Description ***

	Converts a progression to chords and plays them using fluidsynth.

	Make sure you have a fluidsynth server listening at port 9800
	for this example to work.


"""

from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.extra import fluidsynth
import time, sys
from random import random


progression = ["I", "vi", "ii", "iii7",
	       "I7", "viidom7", "iii7", "V7"]
key = 'C'

chords = progressions.to_chords(progression, key)

if not fluidsynth.init_fluidsynth():
	print "Couldn't connect to FluidSynth server at port 9800."
	sys.exit(1)

while 1:
	i = 0 
	for chord in chords:
		c = NoteContainer(chords[i])
		l = Note(c[0].name)
		p = c[1]
		l.octave_down()
		print ch.determine(chords[i])[0]

		# Play chord and lowered first note
		fluidsynth.play_NoteContainer(c)
		fluidsynth.play_Note(l)
		time.sleep(1.0)

		# Play highest note in chord
		fluidsynth.play_Note(c[-1])

		# 50% chance on a bass note
		if random() > 0.5:
			p = Note(c[1].name)
			p.octave_down()
			fluidsynth.play_Note(p)
		time.sleep(0.50)
		
		# 50% chance 
		if random() > 0.5:
			l = Note(intervals.second(c[0].name, key))
			l.octave_up()
			fluidsynth.play_Note(l)
		time.sleep(0.25)

		# 50% chance on the second highest note
		if random() > 0.5:
			fluidsynth.play_Note(c[-2])
		time.sleep(0.25)

		fluidsynth.stop_NoteContainer(c)
		fluidsynth.stop_Note(l)
		fluidsynth.stop_Note(p)
		i += 1
	print "-" * 20
