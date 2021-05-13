import os, sys, platform
from UPT import Context
from UPT import CorrectText
import argparse



def main():
    words = ["hello","world","my","name","is","hans","theere"]
    print(CorrectText.check_replace.spell_check_driver(words))

if __name__ == '__main__':
    main()