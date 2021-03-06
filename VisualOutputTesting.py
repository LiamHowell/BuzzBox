from MidiParser import MidiParser
from MidiData import MidiData
from Util import Util
from MidiEventDecoder import MidiEventDecoder
import math

midi_file = "Midis/League of Legends - Warriors.mid"
print(midi_file)


def midicsv_note_freq(note_num):  # Where mid C is 60
    off_st = -20
    freq = math.pow(2, ((note_num - 49 + off_st)) / 12) * 440
    return freq


def printHex(_bytes):
    temp = ""
    for i in range(len(_bytes)):
        temp = temp + " " + str(hex(_bytes[i]))
    print(temp)


def printRawFile():
    print("-----------------raw file-----------------------")
    with open(midi_file, 'rb') as file:
        printHex(file.read())
    file.close()
    print()
    print()


def testMidiParser():
    midiParser = MidiParser(midi_file)
    print("---------------Testing MidiParser--------------")
    print("Header def and size: " + str(midiParser.readNextData()))
    headerBody = midiParser.readNextData()
    print("Body of header chunk: " + str(headerBody) + " number of tracks: " +
          str(int.from_bytes(headerBody[2:4], "big")))
    while midiParser.hasMoreData():
        trackDef = midiParser.readNextData()
        print("Track def and size: " + str(trackDef) + " track size: "
              + str(int.from_bytes(trackDef[4:8], "big")))
        while midiParser.bytesLeftInChunk > 0:
            print(str(midiParser.readNextData()) + " size left: " +
                  str(midiParser.bytesLeftInChunk))
        print()
    midiParser.close()


def testEventDecoder():
    print("-----Testing MidiEventDecoder---------")
    # testing MidiEventDecoder
    eventDecoder = MidiEventDecoder(midi_file)  # testMidiFile.mid
    print(eventDecoder.headerData())
    # eventData = eventDecoder.nextEvent().midiData
    # print(int.from_bytes(eventData[0:1],"big"))
    # print(Util.msbIsOne(eventData))
    # print(type(eventData))
    while eventDecoder.hasMoreEvents():
        event = eventDecoder.nextEvent()
        print(event)
    eventDecoder.close()
    print()


def testMidiData():
    print("-----Testing MidiData---------")
    midiData = MidiData(midi_file)
    for i in range(midiData.getNumTracks()):
        track = midiData.getTrack(i)
        print(track.name)
        for note in track.notes:
            print(note)
            print(note.pitch)
            print(midicsv_note_freq(note.pitch))
            print(note.startTime)
            print(note.endTime)
        print()
    print()
    print("Note F4 329.04s to 339.32s Channel: 11 <-- expected last note (TestMidiFile2.mid)")
    # print("Note A4 12.50s to 13.00s Channel: 1 <-- expected last note (testingrunningstatus.mid)")


# printRawFile()
# testMidiParser()
# testEventDecoder()
testMidiData()