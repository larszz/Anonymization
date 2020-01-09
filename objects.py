import helper as h
import names as n
import exceptions as ex

INITIAL_VALUE = -1

class Configuration:
    file_directories = INITIAL_VALUE
    output_directory = INITIAL_VALUE
    tablenames = INITIAL_VALUE
    plainrows = INITIAL_VALUE
    anonymrows = INITIAL_VALUE
    pseudonymrows = INITIAL_VALUE


    # sets a configuration
    # ignores, if a configuration value is already set
    # returns 1 if setting worked
    #
    # EXCEPTIONS:
    #   NoneTypeError: value is NoneType
    #   TypeError: value is not a list
    def setConfigurationValue(self, key, value):

        # check if value is in valid format
        if(value is None):
            raise ex.NoneTypeError(str(key))

        if(not isinstance(value, list)):
            raise TypeError

        # set configuration

        # filedirectory
        if key == n.conf.DIRECTORY:
            self.file_directories = value

        # output directory
        if key == n.conf.OUTPUTDIRECTORY:
            self.output_directory = value[0]

        # tablename
        elif key == n.conf.TABLE:
            self.tablenames = value

        # plainrows
        elif key == n.conf.PLAIN:
            self.plainrows = value

        # anonym
        elif key == n.conf.ANONYM:
            self.anonymrows = value

        # pseudonym
        elif key == n.conf.PSEUDONYM:
            self.pseudonymrows = value


        return 1




    def __init__(self):
        pass


    def to_string(self):
        newline = '\n'

        output = newline

        output += "CONFIGURATION" + newline

        output += h.listToString(self.file_directories, n.conf.DIRECTORY, headlineseperator=':\t') + newline
        output += n.conf.OUTPUTDIRECTORY + ":\t" + self.output_directory + newline
        output += h.listToString(self.tablenames, n.conf.TABLE, headlineseperator=':\t') + newline
        output += h.listToString(self.plainrows, n.conf.PLAIN, headlineseperator=':\t') + newline
        output += h.listToString(self.anonymrows, n.conf.ANONYM, headlineseperator=':\t') + newline
        output += h.listToString(self.pseudonymrows, n.conf.PSEUDONYM, headlineseperator=':\t') + newline

        output += 3*newline

        return output





