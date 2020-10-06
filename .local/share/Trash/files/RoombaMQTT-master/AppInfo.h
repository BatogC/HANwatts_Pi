#ifndef APPINFO_H
#define APPINFO_H

/**
 * MAJOR_VERSION    =  0 -> The project is still under construction
 *                  =  1 -> The first program with all of primary functions
 *                  >= 2 -> Add new functions to the project
 * MINOR_VERSION    =  Number of times that the current major version has been modified
 * REVISION_VERSION =  1 -> Nhat is the last person who modified the program
 *                  =  2 -> Bas is the last person who modified the program
 */

#define APPNAME "Roomba"

#define MAJOR_VERSION "0"
#define MINOR_VERSION "3"
#define REVISION_VERSION "1"
#define VERSION MAJOR_VERSION "." MINOR_VERSION "." REVISION_VERSION
#define APPNAME_VERSION APPNAME " v" VERSION

#endif