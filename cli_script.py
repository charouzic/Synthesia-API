import argparse

# Initiate the parser
parser = argparse.ArgumentParser()

# mandatory argument
parser.add_argument("-s", "--script", help="script containing the video message", required=True)
# optional argument
parser.add_argument("-b", "--background", help="background of the video", required=True)
# optional argument
parser.add_argument("-d", "--data", help="path to csv file with data", required=True)
# mandatory argument
parser.add_argument("-o", "--output", help="output path for saving the video", required=True)

# Read arguments from the command line
args = parser.parse_args()

# check for script
print("%s" % args.script)
print("%s" % args.background)
print("%s" % args.output)

"""
1. create function calling the HTTP POST request based on the arguments from the cl
2. inject the token safely from different location
3. create function checking the background list
4. create a function checking the path of imported data
5. create a function calling the HTTP GET request to downloand the video
"""
