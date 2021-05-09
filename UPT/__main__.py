import os, sys, platform
import Context
import CorrectText
import argparse



def main():
    words = load_words()
    CorrectText.CheckReplace.spell_check_driver()

if __name__ == '__main__':
    main()