import numpy as np
import tensorflow as tf
import pandas as pd
import collections
import fluidsynth
import glob
import pretty_midi as pm
from IPython import display
from typing import Dict, List, Optional, Sequence, Tuple

# Load a MIDI file
midi_data = pm.PrettyMIDI('example.mid')

def display_audio(midi_data, seconds=30):
    # Generate waveform using FluidSynth
    waveform = midi_data.fluidsynth(fs=44100)
    # Take a sample of the generated waveform for display
    waveform_short = waveform[:seconds*44100]
    return display.Audio(waveform_short, rate=44100)


def midi_to_notes(midi_file):
      pm = pretty_midi.PrettyMIDI(midi_file)
      instrument = pm.instruments[0]
      notes = collections.defaultdict(list)
      sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
      prev_start = sorted_notes[0].start

      for note in sorted_notes:
            start = note.start
            end = note.end
            notes["pitch"].append(note.pitch)
            notes["start"].append(start)
            notes["end"].append(end)
            notes["step"].append(start - prev_start)
            notes["duration"].append(end - start)
            prev_start = start
      return pd.DataFrame({name: np.array(value) for name, value in notes.items()})


raw_notes = midi_to_notes(sample_file)
note_names = np.vectorize(pretty_midi.note_number_to_name)
sample_note_names = note_names(raw_notes["pitch"])
