#ifndef STRINGEXT_H
#define STRINGEXT_H

#include <string>
#include <vector>

/// String handling utility functions package in a namespace.
/// Implementation of a utility "class" (without a class).
namespace utils
{
void removeLeadingSpacesTabs(std::string& line);
void removeTrailingSpacesTabs(std::string& line);
void removeLeadingTrailingSpacesTabs(std::string& line);
void replaceCommasBySpaces(std::string& line);
void removeReturns(std::string& line);
void tokenize(const std::string& str,
              std::vector<std::string>& tokens,
              const std::string& delimiters = " ");
void capitalize(std::string& str);
void decapitalize(std::string& str);
}

#endif
