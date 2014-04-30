from optparse import OptionParser

parser = OptionParser()
parser.add_option("-l", "--level", dest="level", default="level1", help="level to load")

options, args = parser.parse_args()
def get(name_or_number):
    if type(name_or_number) == int:
        return args[name_or_number]
    return getattr(options, name_or_number)

if __name__=="__main__":
    print options
    print args
